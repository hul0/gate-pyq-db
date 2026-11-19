#!/usr/bin/env python3
"""
build_categorized_dataset.py

Constructs the comprehensive categorized GATE CSE dataset under dataset/:
- dataset/papers/<paper_id>/
    - ga_1_mark.json
    - ga_2_mark.json
    - cs_1_mark.json
    - cs_2_mark.json
- dataset/views/
    - by_marks/ (1_mark.json, 2_mark.json)
    - by_type/ (mcq.json, msq.json, nat.json)
    - by_section/ (general_aptitude.json, computer_science.json)
- dataset/manifest.json
    - Global metadata, facet statistics, paper index, and question lookup index
"""

import os
import re
import json
import glob
from datetime import datetime

def normalize_text_for_number(s):
    if not s:
        return ""
    return s.replace('\u2010', '-').replace('\u2013', '-').replace('\u2212', '-').strip()

def extract_numerical_range(answer_str, question_type):
    if question_type != "NAT" and not (answer_str and any(tok in answer_str for tok in [" to ", ":", "-"])):
        return None
    if not answer_str:
        return None
    cleaned = normalize_text_for_number(answer_str)
    
    # Try pattern like "min to max"
    to_match = re.search(r'([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*(?:to|:)\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', cleaned, re.IGNORECASE)
    if to_match:
        try:
            val1 = float(to_match.group(1))
            val2 = float(to_match.group(2))
            return {"min": min(val1, val2), "max": max(val1, val2)}
        except ValueError:
            pass
            
    # Try pattern with single number
    num_match = re.search(r'^[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?$', cleaned)
    if num_match:
        try:
            val = float(num_match.group(0))
            return {"min": val, "max": val}
        except ValueError:
            pass
            
    return None

def determine_category(section_code, marks):
    sec = (section_code or "").lower()
    m = int(round(marks or 1.0))
    if sec in ["ga", "general aptitude"]:
        return f"ga_{m}_mark"
    else:
        return f"cs_{m}_mark"

def build_tags(q):
    tags = []
    if q.get("year"):
        tags.append(str(q["year"]))
    if q.get("session"):
        tags.append(str(q["session"]).lower())
    if q.get("section_code"):
        tags.append(str(q["section_code"]).lower())
    m = int(round(q.get("marks", 1.0)))
    tags.append(f"{m}_mark")
    category = q.get("category")
    if category:
        tags.append(category)
    q_type = q.get("question_type")
    if q_type:
        tags.append(q_type.lower())
    if q.get("has_images"):
        tags.append("has_images")
    else:
        tags.append("text_only")
    neg = q.get("negative_marks", 0.0)
    if neg and neg > 0:
        tags.append("negative_marking")
    else:
        tags.append("no_negative_marking")
    if q.get("options"):
        tags.append(f"{len(q['options'])}_options")
    return sorted(list(set(tags)))

def process_question(raw_q, paper_info):
    marks = raw_q.get("marks", 1.0)
    if marks is None:
        marks = 1.0
    marks = float(marks)
    
    sec_code = raw_q.get("section_code")
    if not sec_code:
        sec = raw_q.get("section", "")
        if "general aptitude" in sec.lower():
            sec_code = "GA"
        else:
            sec_code = "CS"
            
    category = determine_category(sec_code, marks)
    q_type = raw_q.get("question_type", "MCQ")
    is_mc = q_type in ["MCQ", "MSQ"]
    
    num_range = extract_numerical_range(raw_q.get("answer"), q_type)
    
    processed = {
        "id": raw_q.get("id"),
        "category": category,
        "marks": marks,
        "negative_marks": float(raw_q.get("negative_marks", 0.0)),
        "section": raw_q.get("section", "Computer Science and Information Technology"),
        "section_code": sec_code,
        "paper_id": paper_info.get("paper_id"),
        "year": paper_info.get("year"),
        "session": paper_info.get("session"),
        "question_number": raw_q.get("question_number"),
        "question_type": q_type,
        "is_multiple_choice": is_mc,
        "has_images": bool(raw_q.get("has_images", False)),
        "page_start": raw_q.get("page_start"),
        "page_end": raw_q.get("page_end"),
        "question_text": raw_q.get("question_text", ""),
        "options": raw_q.get("options"),
        "answer": raw_q.get("answer", ""),
        "correct_options": raw_q.get("correct_options"),
        "numerical_answer_range": num_range,
        "topic": "",
        "subtopic": "",
        "difficulty_level": "",
        "explaination": "",
        "tags": []
    }
    processed["tags"] = build_tags(processed)
    return processed

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    combined_dir = os.path.join(root_dir, "combined_qa")
    dataset_dir = os.path.join(root_dir, "dataset")
    papers_dir = os.path.join(dataset_dir, "papers")
    views_dir = os.path.join(dataset_dir, "views")
    views_marks_dir = os.path.join(views_dir, "by_marks")
    views_type_dir = os.path.join(views_dir, "by_type")
    views_sec_dir = os.path.join(views_dir, "by_section")

    for d in [papers_dir, views_marks_dir, views_type_dir, views_sec_dir]:
        os.makedirs(d, exist_ok=True)

    paper_files = sorted(glob.glob(os.path.join(combined_dir, "*.json")))
    print(f"Found {len(paper_files)} combined paper files.")

    all_questions = []
    paper_catalog = []
    
    # Global view accumulators
    by_marks = {"1_mark": [], "2_mark": []}
    by_type = {"mcq": [], "msq": [], "nat": []}
    by_section = {"general_aptitude": [], "computer_science": []}

    for p_file in paper_files:
        with open(p_file, "r", encoding="utf-8") as f:
            p_data = json.load(f)

        paper_id = p_data.get("paper_id")
        year = p_data.get("year")
        session = p_data.get("session")
        
        # We only process 2011 to 2025 papers
        if year and (year < 2011 or year > 2025):
            continue

        raw_questions = p_data.get("questions", [])
        if not raw_questions:
            # Paper has 0 extracted questions (e.g. OCR/extraction pending)
            continue

        paper_target_dir = os.path.join(papers_dir, paper_id)
        os.makedirs(paper_target_dir, exist_ok=True)

        paper_questions = []
        categories_map = {
            "ga_1_mark": [],
            "ga_2_mark": [],
            "cs_1_mark": [],
            "cs_2_mark": []
        }

        for q in raw_questions:
            pq = process_question(q, {"paper_id": paper_id, "year": year, "session": session})
            paper_questions.append(pq)
            all_questions.append(pq)

            cat = pq["category"]
            if cat in categories_map:
                categories_map[cat].append(pq)
            else:
                categories_map.setdefault(cat, []).append(pq)

            # Slices for global views
            m_key = "1_mark" if pq["marks"] == 1.0 else "2_mark"
            by_marks[m_key].append(pq)

            t_key = pq["question_type"].lower()
            if t_key in by_type:
                by_type[t_key].append(pq)

            s_key = "general_aptitude" if pq["section_code"] == "GA" else "computer_science"
            by_section[s_key].append(pq)

        # Write categorized files for this paper
        paper_file_summary = {}
        for cat_name, q_list in categories_map.items():
            out_file_name = f"{cat_name}.json"
            out_path = os.path.join(paper_target_dir, out_file_name)
            cat_payload = {
                "paper_id": paper_id,
                "year": year,
                "session": session,
                "category": cat_name,
                "total_questions": len(q_list),
                "questions": q_list
            }
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(cat_payload, f, indent=2, ensure_ascii=False)
            paper_file_summary[cat_name] = {
                "file": f"papers/{paper_id}/{out_file_name}",
                "count": len(q_list)
            }

        paper_catalog.append({
            "paper_id": paper_id,
            "year": year,
            "session": session,
            "total_questions": len(paper_questions),
            "categories": paper_file_summary
        })

    # Write global views
    # 1. By marks
    for m_k, q_list in by_marks.items():
        v_path = os.path.join(views_marks_dir, f"{m_k}.json")
        with open(v_path, "w", encoding="utf-8") as f:
            json.dump({
                "view": f"by_marks/{m_k}",
                "total_questions": len(q_list),
                "questions": q_list
            }, f, indent=2, ensure_ascii=False)

    # 2. By type
    for t_k, q_list in by_type.items():
        v_path = os.path.join(views_type_dir, f"{t_k}.json")
        with open(v_path, "w", encoding="utf-8") as f:
            json.dump({
                "view": f"by_type/{t_k}",
                "total_questions": len(q_list),
                "questions": q_list
            }, f, indent=2, ensure_ascii=False)

    # 3. By section
    for s_k, q_list in by_section.items():
        v_path = os.path.join(views_sec_dir, f"{s_k}.json")
        with open(v_path, "w", encoding="utf-8") as f:
            json.dump({
                "view": f"by_section/{s_k}",
                "total_questions": len(q_list),
                "questions": q_list
            }, f, indent=2, ensure_ascii=False)

    # Build manifest
    breakdown_marks = {"1.0": len(by_marks["1_mark"]), "2.0": len(by_marks["2_mark"])}
    breakdown_type = {k.upper(): len(v) for k, v in by_type.items()}
    breakdown_sec = {
        "GA": len(by_section["general_aptitude"]),
        "CS": len(by_section["computer_science"])
    }
    breakdown_cat = {
        "ga_1_mark": sum(1 for q in all_questions if q["category"] == "ga_1_mark"),
        "ga_2_mark": sum(1 for q in all_questions if q["category"] == "ga_2_mark"),
        "cs_1_mark": sum(1 for q in all_questions if q["category"] == "cs_1_mark"),
        "cs_2_mark": sum(1 for q in all_questions if q["category"] == "cs_2_mark")
    }

    # Lightweight index for fast querying
    questions_index = []
    for q in all_questions:
        questions_index.append({
            "id": q["id"],
            "paper_id": q["paper_id"],
            "year": q["year"],
            "session": q["session"],
            "category": q["category"],
            "marks": q["marks"],
            "question_type": q["question_type"],
            "has_images": q["has_images"],
            "tags": q["tags"],
            "file_path": f"papers/{q['paper_id']}/{q['category']}.json"
        })

    manifest = {
        "generated_at": datetime.now().isoformat(),
        "total_papers": len(paper_catalog),
        "total_questions": len(all_questions),
        "breakdown_by_marks": breakdown_marks,
        "breakdown_by_type": breakdown_type,
        "breakdown_by_section": breakdown_sec,
        "breakdown_by_category": breakdown_cat,
        "papers": paper_catalog,
        "views": {
            "by_marks": ["views/by_marks/1_mark.json", "views/by_marks/2_mark.json"],
            "by_type": ["views/by_type/mcq.json", "views/by_type/msq.json", "views/by_type/nat.json"],
            "by_section": ["views/by_section/general_aptitude.json", "views/by_section/computer_science.json"]
        },
        "questions_index": questions_index
    }

    manifest_path = os.path.join(dataset_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print("Categorized dataset generated successfully:")
    print(f"- Papers processed: {len(paper_catalog)}")
    print(f"- Total questions: {len(all_questions)}")
    print(f"- Breakdown by Category: {breakdown_cat}")
    print(f"- Breakdown by Type: {breakdown_type}")
    print(f"- Manifest saved to: {manifest_path}")

if __name__ == "__main__":
    main()

