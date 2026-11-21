#!/usr/bin/env python3
"""
test_gemini_flash_lite_ocr.py

Tests Google AI Studio's Gemini 3.1 Flash Lite model on a single exam page
to benchmark OCR accuracy, LaTeX transcription, latency, and token consumption
without exhausting rate limits (15 RPM / 250K TPM / 500 RPD).
"""

import os
import base64
import json
import time
import requests
from dotenv import load_dotenv

def test_page_ocr(image_path: str, model: str = "gemini-3.1-flash-lite"):
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set in environment or .env file.")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")

    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    prompt = (
        "You are an expert OCR and academic examination transcription system.\n"
        "Carefully OCR this exam page from GATE Computer Science.\n"
        "Extract all questions printed on the page accurately:\n"
        "- Convert all math expressions, formulas, and matrices to clean LaTeX ($...$ or $$...$$).\n"
        "- Convert tables into Markdown table format.\n"
        "- Extract question numbers and all options (A, B, C, D).\n\n"
        "Return ONLY a valid JSON list of question objects:\n"
        "[\n"
        "  {\n"
        '    "question_number": int,\n'
        '    "question_text": "...",\n'
        '    "options": {\n'
        '      "A": "...",\n'
        '      "B": "...",\n'
        '      "C": "...",\n'
        '      "D": "..."\n'
        "    }\n"
        "  }\n"
        "]"
    )

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

    print(f"Sending request to {model}...")
    t0 = time.time()
    resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    elapsed = time.time() - t0

    if resp.status_code != 200:
        print(f"Request failed with status {resp.status_code}: {resp.text}")
        return None

    res_json = resp.json()
    usage = res_json.get("usageMetadata", {})
    candidate = res_json.get("candidates", [{}])[0]
    content_text = candidate.get("content", {}).get("parts", [{}])[0].get("text", "")

    print(f"Success! Status: {resp.status_code} in {elapsed:.2f}s")
    print(f"Token Usage:")
    print(f"  - Prompt Tokens: {usage.get('promptTokenCount')} (Image: {usage.get('promptTokensDetails', [{}])[0].get('tokenCount')})")
    print(f"  - Output Tokens: {usage.get('candidatesTokenCount')}")
    print(f"  - Total Tokens:  {usage.get('totalTokenCount')}")

    parsed = json.loads(content_text)
    print(f"Successfully extracted {len(parsed)} questions.")
    return {
        "model": model,
        "elapsed_seconds": round(elapsed, 2),
        "usage": usage,
        "questions": parsed
    }

if __name__ == "__main__":
    test_page_ocr("temp/page_3_200dpi-03.png")
