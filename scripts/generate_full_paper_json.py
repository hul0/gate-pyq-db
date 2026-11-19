#!/usr/bin/env python3
"""
generate_full_paper_json.py

Combines all category JSON files (ga_1_mark, ga_2_mark, cs_1_mark, cs_2_mark)
for a given paper set into a single monolithic JSON:
dataset/papers/<paper_id>/full_paper.json
"""

import os
import json
import glob
import sys

def build_full_paper(paper_id="2025_CS2"):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    paper_dir = os.path.join(root_dir, "dataset", "papers", paper_id)

    if not os.path.exists(paper_dir):
        print(f"Error: {paper_dir} does not exist.")
        return None

    category_files = [
        "ga_1_mark.json",
        "ga_2_mark.json",
        "cs_1_mark.json",
        "cs_2_mark.json"
    ]

    all_questions = []
    paper_metadata = {}

    for cfile in category_files:
        path = os.path.join(paper_dir, cfile)
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not paper_metadata:
                paper_metadata["paper_id"] = data.get("paper_id", paper_id)
                paper_metadata["year"] = data.get("year")
                paper_metadata["session"] = data.get("session")
            all_questions.extend(data.get("questions", []))

    # Sort questions by question_number
    all_questions.sort(key=lambda q: q.get("question_number", 0))

    ga_questions = [q for q in all_questions if q.get("section_code") == "GA"]
    cs_questions = [q for q in all_questions if q.get("section_code") == "CS"]

    monolithic_payload = {
        "paper_id": paper_metadata.get("paper_id", paper_id),
        "year": paper_metadata.get("year", 2025),
        "session": paper_metadata.get("session", "CS2"),
        "subject": "Computer Science and Information Technology",
        "total_questions": len(all_questions),
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

    out_path = os.path.join(paper_dir, "full_paper.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(monolithic_payload, f, indent=2, ensure_ascii=False)

    print(f"Created monolithic JSON: {out_path} ({len(all_questions)} questions)")
    return out_path

if __name__ == "__main__":
    pid = sys.argv[1] if len(sys.argv) > 1 else "2025_CS2"
    build_full_paper(pid)

