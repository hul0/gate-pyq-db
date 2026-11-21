"""
manifest.py - Updates data/dataset/manifest.json when a new paper is processed.
"""

import os
import json
from typing import Dict, Any

def update_dataset_manifest(
    manifest_path: str,
    paper_data: Dict[str, Any]
) -> None:
    """
    Registers or updates the paper entry in data/dataset/manifest.json.
    """
    if not os.path.exists(manifest_path):
        print(f"Manifest file not found at {manifest_path}; skipping manifest sync.")
        return

    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"Failed to read manifest {manifest_path}: {e}")
        return

    paper_id = paper_data.get("paper_id")
    year = paper_data.get("year")
    session = paper_data.get("session", "CS")
    questions = paper_data.get("questions", [])

    # Count categories
    cat_counts = {
        "cs_1_mark": 0,
        "cs_2_mark": 0,
        "ga_1_mark": 0,
        "ga_2_mark": 0
    }
    for q in questions:
        cat = q.get("category")
        if cat in cat_counts:
            cat_counts[cat] += 1

    paper_entry = {
        "paper_id": paper_id,
        "year": year,
        "session": session,
        "total_questions": len(questions),
        "categories": {
            k: {
                "file": f"papers/{paper_id}/{k}.json",
                "count": cat_counts[k]
            } for k in cat_counts
        }
    }

    papers_list = manifest.get("papers", [])
    updated = False
    for i, p in enumerate(papers_list):
        if p.get("paper_id") == paper_id:
            papers_list[i] = paper_entry
            updated = True
            break
    if not updated:
        papers_list.append(paper_entry)

    # Re-sort papers by year ascending
    papers_list.sort(key=lambda x: (x.get("year", 0), x.get("paper_id", "")))
    manifest["papers"] = papers_list
    manifest["total_papers"] = len(papers_list)
    manifest["total_questions"] = sum(p.get("total_questions", 0) for p in papers_list)

    try:
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        print(f"Successfully synced {paper_id} to {manifest_path} (Total questions: {len(questions)})")
    except Exception as e:
        print(f"Failed to write updated manifest: {e}")
