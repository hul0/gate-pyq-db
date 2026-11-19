#!/usr/bin/env python3
"""
sync_dataset.py

Synchronizes dataset/views/ and dataset/manifest.json from the current files
in dataset/papers/<paper_id>/*.json.
"""

import os
import json
import glob
from datetime import datetime

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dataset_dir = os.path.join(root_dir, "dataset")
    papers_dir = os.path.join(dataset_dir, "papers")
    views_dir = os.path.join(dataset_dir, "views")
    views_marks_dir = os.path.join(views_dir, "by_marks")
    views_type_dir = os.path.join(views_dir, "by_type")
    views_sec_dir = os.path.join(views_dir, "by_section")

    for d in [views_marks_dir, views_type_dir, views_sec_dir]:
        os.makedirs(d, exist_ok=True)

    paper_dirs = sorted([d for d in glob.glob(os.path.join(papers_dir, "*")) if os.path.isdir(d)])
    
    all_questions = []
    paper_catalog = []
    
    by_marks = {"1_mark": [], "2_mark": []}
    by_type = {"mcq": [], "msq": [], "nat": []}
    by_section = {"general_aptitude": [], "computer_science": []}

    for p_dir in paper_dirs:
        paper_id = os.path.basename(p_dir)
        paper_questions = []
        categories_summary = {}

        json_files = sorted(glob.glob(os.path.join(p_dir, "*.json")))
        for j_file in json_files:
            with open(j_file, "r", encoding="utf-8") as f:
                cat_data = json.load(f)
            
            cat_name = cat_data.get("category")
            q_list = cat_data.get("questions", [])
            categories_summary[cat_name] = {
                "file": f"papers/{paper_id}/{os.path.basename(j_file)}",
                "count": len(q_list)
            }

            for q in q_list:
                paper_questions.append(q)
                all_questions.append(q)

                m_key = "1_mark" if q.get("marks") == 1.0 else "2_mark"
                by_marks[m_key].append(q)

                t_key = q.get("question_type", "MCQ").lower()
                if t_key in by_type:
                    by_type[t_key].append(q)

                s_key = "general_aptitude" if q.get("section_code") == "GA" else "computer_science"
                by_section[s_key].append(q)

        first_q = paper_questions[0] if paper_questions else {}
        paper_catalog.append({
            "paper_id": paper_id,
            "year": first_q.get("year"),
            "session": first_q.get("session"),
            "total_questions": len(paper_questions),
            "categories": categories_summary
        })

    # Write views
    for m_k, q_list in by_marks.items():
        with open(os.path.join(views_marks_dir, f"{m_k}.json"), "w", encoding="utf-8") as f:
            json.dump({
                "view": f"by_marks/{m_k}",
                "total_questions": len(q_list),
                "questions": q_list
            }, f, indent=2, ensure_ascii=False)

    for t_k, q_list in by_type.items():
        with open(os.path.join(views_type_dir, f"{t_k}.json"), "w", encoding="utf-8") as f:
            json.dump({
                "view": f"by_type/{t_k}",
                "total_questions": len(q_list),
                "questions": q_list
            }, f, indent=2, ensure_ascii=False)

    for s_k, q_list in by_section.items():
        with open(os.path.join(views_sec_dir, f"{s_k}.json"), "w", encoding="utf-8") as f:
            json.dump({
                "view": f"by_section/{s_k}",
                "total_questions": len(q_list),
                "questions": q_list
            }, f, indent=2, ensure_ascii=False)

    # Manifest
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
            "topic": q.get("topic", ""),
            "subtopic": q.get("subtopic", ""),
            "difficulty_level": q.get("difficulty_level", ""),
            "tags": q["tags"],
            "file_path": f"papers/{q['paper_id']}/{q['category']}.json"
        })

    manifest = {
        "generated_at": datetime.now().isoformat(),
        "total_papers": len(paper_catalog),
        "total_questions": len(all_questions),
        "breakdown_by_marks": {"1.0": len(by_marks["1_mark"]), "2.0": len(by_marks["2_mark"])},
        "breakdown_by_type": {k.upper(): len(v) for k, v in by_type.items()},
        "breakdown_by_section": {
            "GA": len(by_section["general_aptitude"]),
            "CS": len(by_section["computer_science"])
        },
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

    print("Dataset views and manifest synchronized successfully.")

if __name__ == "__main__":
    main()

