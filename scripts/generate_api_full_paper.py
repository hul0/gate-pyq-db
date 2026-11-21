#!/usr/bin/env python3
"""
generate_api_full_paper.py

Generates api_full_paper.json for GATE 2013 CS (Booklet Code A, Q1-Q65)
using Google AI Studio's Gemini 3.1 Flash Lite model across 13 pages.
Uses thread-safe rate limiting (max 12-13 RPM to strictly respect the 15 RPM cap).
Includes robust JSON sanitization to handle unescaped LaTeX backslashes.
"""

import os
import sys
import json
import base64
import time
import re
import threading
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

# Page to question ranges for GATE 2013 CS Booklet Code A
PAGE_CONFIG = {
    3: (1, 7),
    4: (8, 13),
    5: (14, 18),
    6: (19, 25),
    7: (26, 30),
    8: (31, 34),
    9: (35, 38),
    10: (39, 41),
    11: (42, 47),
    12: (48, 51),
    13: (52, 55),
    14: (56, 62),
    15: (63, 65)
}

class GlobalRateLimiter:
    """Thread-safe rate limiter ensuring at least min_interval seconds between consecutive API calls."""
    def __init__(self, min_interval=4.5):
        self.min_interval = min_interval
        self.last_call = 0.0
        self.lock = threading.Lock()

    def wait(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_call
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self.last_call = time.time()

rate_limiter = GlobalRateLimiter(min_interval=4.5)

def robust_json_load(s: str):
    """Parses JSON even if the model generated unescaped LaTeX backslashes inside string literals."""
    try:
        return json.loads(s, strict=False)
    except Exception:
        pass

    # Re-tokenize / fix unescaped backslashes inside string literals
    res = []
    in_string = False
    escape = False
    for i, c in enumerate(s):
        if not in_string:
            if c == '"':
                in_string = True
            res.append(c)
        else:
            if escape:
                res.append(c)
                escape = False
            else:
                if c == '\\':
                    next_c = s[i+1] if i+1 < len(s) else ''
                    if next_c not in ('"', '\\'):
                        # Double the backslash so LaTeX commands like \sigma, \frac, \alpha don't crash JSON parser
                        res.append('\\')
                    res.append(c)
                    escape = True
                elif c == '"':
                    in_string = False
                    res.append(c)
                else:
                    res.append(c)
    fixed = ''.join(res)
    return json.loads(fixed, strict=False)

def load_keys():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    key_path = os.path.join(root, "data", "digitized_answer_keys", "2013_CS_key.json")
    with open(key_path) as f:
        data = json.load(f)
    keys_dict = {}
    for k in data["keys"]:
        keys_dict[k["question_number"]] = {
            "key": k["key"],
            "correct_options": k["correct_options"],
            "marks": k["marks"],
            "section_code": k["section_code"],
            "section": k["section"],
            "question_type": k["question_type"]
        }
    return keys_dict

def process_page(page_num, start_q, end_q, keys_dict, api_key, model="gemini-3.1-flash-lite"):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cache_dir = os.path.join(root, "temp", "api_pages")
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"page_{page_num:02d}.json")

    # If already cached and valid, reuse
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cached_qs = json.load(f)
            if len(cached_qs) == (end_q - start_q + 1):
                print(f"[Page {page_num:02d}] Loaded from cache ({len(cached_qs)} Qs).")
                return page_num, cached_qs
        except Exception:
            pass

    img_path = os.path.join(root, "temp", "pages", f"page-{page_num:02d}.png")
    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    page_keys = {q: keys_dict[q] for q in range(start_q, end_q + 1) if q in keys_dict}
    keys_summary = "\n".join([
        f"- Q.{q}: Section {info['section_code']}, Marks {info['marks']}, Official Answer: {info['key']} (Options: {info['correct_options']})"
        for q, info in page_keys.items()
    ])

    prompt = f"""You are an expert OCR and GATE computer science exam transcription system.
Carefully OCR page {page_num} of GATE 2013 Computer Science (Booklet Code A).
This page contains questions Q.{start_q} to Q.{end_q}.

Here are the official verified answer keys and section metadata for these questions:
{keys_summary}

CRITICAL FORMATTING INSTRUCTIONS:
1. LaTeX for ALL Math: You MUST use LaTeX notation ($...$ inline or $$...$$ display) for ANY AND ALL mathematical expressions, variables, formulas, bounds, logic symbols, constants, and function names (e.g. $x$, $y$, $n$, $\\oplus$, $\\Theta(n^2)$, $\\Sigma^*$, $\\in$, $\\exists$, $\\le$, etc.). Every variable or mathematical entity must be in LaTeX.
2. IMPORTANT JSON ESCAPING: In the JSON output, all LaTeX backslashes MUST be escaped as double backslashes `\\\\` (e.g. `\\\\oplus`, `\\\\Theta`, `\\\\begin{{vmatrix}}`, `\\\\sigma`).
3. Tables & Markdown: Use clean Markdown tables for truth tables or numerical data tables. Use fenced code blocks with language identifiers (e.g. ```c, ```sql, ```text) for source code.
4. Diagrams & Images:
   - If a question contains a diagram, circuit, state machine graph, flowchart, network topology, or access graph, set "has_images": true and "media": {{}} (empty object).
   - For questions WITHOUT any diagram or figure, set "has_images": false and "media": null.
5. Schema Requirements:
   For each question on this page (from Q.{start_q} to Q.{end_q}), extract:
   - "id": "2013_CS_CS_Q01" (if CS) or "2013_CS_GA_Q56" (if GA)
   - "category": "cs_1_mark", "cs_2_mark", "ga_1_mark", or "ga_2_mark"
   - "marks": 1.0 or 2.0
   - "negative_marks": 0.33 for 1-mark MCQ, 0.66 for 2-mark MCQ, 0.0 for Marks to All
   - "section": "Computer Science and Information Technology" or "General Aptitude"
   - "section_code": "CS" or "GA"
   - "paper_id": "2013_CS"
   - "year": 2013
   - "session": "CS"
   - "question_number": int
   - "question_type": "MCQ"
   - "is_multiple_choice": true
   - "has_images": bool
   - "media": {{}} if has_images else null
   - "page_start": {page_num}
   - "page_end": {page_num}
   - "question_text": string with clean LaTeX math and Markdown
   - "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}} (with LaTeX for math options)
   - "answer": official answer string
   - "correct_options": list of correct option letters
   - "numerical_answer_range": null
   - "topic": canonical subject name
   - "subtopic": specific topic area
   - "difficulty_level": "Easy", "Medium", or "Hard"
   - "explaination": technically rigorous step-by-step explanation using the official answer provided above
   - "tags": list of string tags

Return ONLY a valid JSON list of question objects.
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": img_b64
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "response_mime_type": "application/json"
        }
    }

    max_retries = 6
    for attempt in range(max_retries):
        # Respect global rate limit
        rate_limiter.wait()
        t0 = time.time()
        try:
            resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=90)
            elapsed = time.time() - t0
            if resp.status_code == 200:
                res_data = resp.json()
                usage = res_data.get("usageMetadata", {})
                content = res_data["candidates"][0]["content"]["parts"][0]["text"]
                questions = robust_json_load(content)
                print(f"[Page {page_num:02d}] Success: {len(questions)} Qs in {elapsed:.2f}s ({usage.get('totalTokenCount', 0)} tokens)")
                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(questions, f, indent=2, ensure_ascii=False)
                return page_num, questions
            elif resp.status_code == 429:
                wait_time = (attempt + 1) * 8
                print(f"[Page {page_num:02d}] Rate limit 429. Backing off for {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"[Page {page_num:02d}] HTTP {resp.status_code}: {resp.text[:150]}")
                time.sleep(5)
        except Exception as e:
            print(f"[Page {page_num:02d}] Error: {e}. Retrying in 5s...")
            time.sleep(5)

    raise RuntimeError(f"Failed to process page {page_num} after {max_retries} attempts.")

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not set.")
        sys.exit(1)

    keys_dict = load_keys()
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    print("Starting rate-controlled OCR generation with max 3 concurrent threads...")
    all_questions = []
    start_time = time.time()

    # Using 3 threads with global 4.5s rate limiter ensures <= 13.3 RPM
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(process_page, p, q_range[0], q_range[1], keys_dict, api_key): p
            for p, q_range in PAGE_CONFIG.items()
        }
        for future in as_completed(futures):
            p = futures[future]
            try:
                page_num, questions = future.result()
                all_questions.extend(questions)
            except Exception as e:
                print(f"Error processing page {p}: {e}")

    total_time = time.time() - start_time
    print(f"\nAll pages completed in {total_time:.2f}s! Total questions collected: {len(all_questions)}")

    # Sort questions by section (GA first, then CS) and question_number
    all_questions.sort(key=lambda q: (0 if q.get("section_code") == "GA" else 1, q.get("question_number", 0)))

    ga_questions = [q for q in all_questions if q.get("section_code") == "GA"]
    cs_questions = [q for q in all_questions if q.get("section_code") == "CS"]

    monolithic_payload = {
        "paper_id": "2013_CS",
        "year": 2013,
        "session": "CS",
        "subject": "Computer Science and Information Technology",
        "total_questions": len(all_questions),
        "total_questions_in_paper": len(all_questions),
        "extracted_questions_count": len(all_questions),
        "omitted_questions_count": 0,
        "sections": [
            {
                "section_name": "General Aptitude",
                "section_code": "GA",
                "total_questions": len(ga_questions)
            },
            {
                "section_name": "Computer Science and Information Technology",
                "section_code": "CS",
                "total_questions": len(cs_questions)
            }
        ],
        "questions": all_questions
    }

    out_paths = [
        os.path.join(root, "api_full_paper.json"),
        os.path.join(root, "data", "dataset", "papers", "2013_CS", "api_full_paper.json")
    ]

    for p in out_paths:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(monolithic_payload, f, indent=2, ensure_ascii=False)
        print(f"Saved: {p}")

if __name__ == "__main__":
    main()
