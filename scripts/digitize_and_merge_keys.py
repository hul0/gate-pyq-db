#!/usr/bin/env python3
"""
digitize_and_merge_keys.py

1. Digitizes official GATE CSE answer keys (2011 - 2025) into digitized_answer_keys/
   - Each key entry contains:
     * paper_question_number: continuous index in paper (1 to 65)
     * printed_question_number: exact number printed in the PDF table column Q. No. (e.g. 1..10 in GA, 1..55 in CS)
     * section_code: "GA" or "CS"
     * question_type: "MCQ", "MSQ", "NAT"
     * key: official key string (e.g. "B; C; D", "5040 to 5040")
     * correct_options: explicit array (e.g. ["B", "C", "D"])
     * marks: float
   - Provides lookup maps:
     * keys_by_paper_number: continuous 1..65 -> key
     * keys_by_section_and_number: e.g. "CS_11" -> key, "GA_1" -> key
     * correct_options_by_section_and_number: e.g. "CS_11" -> ["B", "C"]
2. Combines extracted questions with answer keys into combined_qa/
"""

import os
import json
import glob
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
import pdfplumber

DIGITIZED_DIR = Path("digitized_answer_keys")
COMBINED_DIR = Path("combined_qa")
OUTPUT_DIR = Path("output")
ANSWER_KEYS_DIR = Path("answer_keys")


def clean_cell(c: Any) -> str:
    if c is None:
        return ""
    return str(c).strip().replace("\n", " ")


def extract_correct_options(key_str: Optional[str], q_type: str) -> Optional[List[str]]:
    """Extract individual option letters for MCQ/MSQ, or null for NAT."""
    if not key_str or q_type == "NAT":
        return None
    key_upper = str(key_str).strip().upper()
    if key_upper in ["MTA", "MARKS TO ALL"]:
        return ["A", "B", "C", "D"]

    # Match option letters separated by ;, ,, or 'OR'
    parts = re.split(r"[;,]|\bOR\b", key_upper)
    opts = [p.strip() for p in parts if p.strip() in ["A", "B", "C", "D"]]
    if opts:
        return sorted(list(dict.fromkeys(opts)))
    return None


def parse_pdf_table(pdf_path: Path) -> List[Dict[str, Any]]:
    with pdfplumber.open(pdf_path) as pdf:
        all_rows = []
        for p in pdf.pages:
            tables = p.extract_tables()
            for t in tables:
                all_rows.extend(t)

    cleaned = [[clean_cell(c) for c in r] for r in all_rows if any(r)]
    fname = pdf_path.name

    records = []

    # 2011, 2012
    if "2011_CS" in fname or "2012_CS" in fname:
        for r in cleaned:
            if len(r) >= 3 and r[1].isdigit():
                qno = int(r[1])
                sec = "GA" if (56 <= qno <= 65) else "CS"
                q_type = "MCQ"
                key_val = r[2]
                records.append({
                    "question_number": qno,
                    "paper_question_number": qno,
                    "printed_question_number": qno,
                    "section_code": sec,
                    "section": "General Aptitude" if sec == "GA" else "Computer Science and Information Technology",
                    "question_type": q_type,
                    "key": key_val,  # Code A
                    "code_a": r[2],
                    "code_b": r[3] if len(r) > 3 else "",
                    "code_c": r[4] if len(r) > 4 else "",
                    "code_d": r[5] if len(r) > 5 else "",
                    "correct_options": extract_correct_options(key_val, q_type),
                    "marks": 1.0 if (1 <= qno <= 25 or 56 <= qno <= 60) else 2.0
                })
        return records

    # 2013
    if "2013_CS" in fname:
        for r in cleaned:
            if len(r) >= 3 and r[1].isdigit():
                qno = int(r[1])
                sec = "GA" if (56 <= qno <= 65) else "CS"
                q_type = "MCQ"
                key_val = r[2]
                records.append({
                    "question_number": qno,
                    "paper_question_number": qno,
                    "printed_question_number": qno,
                    "section_code": sec,
                    "section": "General Aptitude" if sec == "GA" else "Computer Science and Information Technology",
                    "question_type": q_type,
                    "key": key_val,  # Code A
                    "code_a": r[2],
                    "code_b": r[3] if len(r) > 3 else "",
                    "code_c": r[4] if len(r) > 4 else "",
                    "code_d": r[5] if len(r) > 5 else "",
                    "correct_options": extract_correct_options(key_val, q_type),
                    "marks": 1.0 if (1 <= qno <= 25 or 56 <= qno <= 60) else 2.0
                })
        return records

    # 2014
    if "2014_CS" in fname:
        for r in cleaned:
            if len(r) >= 3 and r[1].isdigit() and r[0] in ["GA", "CS"]:
                raw_q = int(r[1])
                sec = r[0]
                qno = raw_q if sec == "GA" else raw_q + 10
                q_type = "NAT" if ("." in r[2] or "to" in r[2]) else "MCQ"
                key_val = r[2]
                records.append({
                    "question_number": qno,
                    "paper_question_number": qno,
                    "printed_question_number": raw_q,
                    "raw_question_number": raw_q,
                    "section_code": sec,
                    "section": "General Aptitude" if sec == "GA" else "Computer Science and Information Technology",
                    "question_type": q_type,
                    "key": key_val,
                    "correct_options": extract_correct_options(key_val, q_type),
                    "marks": float(r[3]) if len(r) > 3 and r[3].replace(".", "", 1).isdigit() else 1.0
                })
        return records

    # 2016, 2017
    if "2016_CS" in fname or "2017_CS" in fname:
        for r in cleaned:
            if len(r) >= 4 and r[0].isdigit():
                raw_q = int(r[0])
                sec = r[2]
                sec_code = "GA" if "GA" in sec else "CS"
                qno = raw_q if (sec_code == "GA" or "2017" in fname) else raw_q + 10
                q_type = r[1]
                key_val = r[3]
                records.append({
                    "question_number": qno,
                    "paper_question_number": qno,
                    "printed_question_number": raw_q,
                    "raw_question_number": raw_q,
                    "section_code": sec_code,
                    "section": sec,
                    "question_type": q_type,
                    "key": key_val,
                    "correct_options": extract_correct_options(key_val, q_type),
                    "marks": float(r[4]) if len(r) > 4 and r[4].replace(".", "", 1).isdigit() else 1.0
                })
        return records

    # 2018, 2019
    if "2018_CS" in fname or "2019_CS" in fname:
        for r in cleaned:
            if len(r) >= 4 and r[0].isdigit():
                raw_q = int(r[0])
                sec = r[2]
                sec_code = "GA" if "GA" in sec else "CS"
                qno = raw_q if sec_code == "GA" else raw_q + 10
                q_type = r[1]
                key_val = r[3]
                records.append({
                    "question_number": qno,
                    "paper_question_number": qno,
                    "printed_question_number": raw_q,
                    "raw_question_number": raw_q,
                    "section_code": sec_code,
                    "section": sec,
                    "question_type": q_type,
                    "key": key_val,
                    "correct_options": extract_correct_options(key_val, q_type),
                    "marks": float(r[4]) if len(r) > 4 and r[4].replace(".", "", 1).isdigit() else 1.0
                })
        return records

    # 2020, 2021
    if "2020_CS" in fname or "2021_CS" in fname:
        for r in cleaned:
            if len(r) >= 5 and r[0].isdigit():
                raw_q = int(r[0])
                sec = r[3]
                sec_code = "GA" if "GA" in sec else "CS"
                qno = raw_q if sec_code == "GA" else raw_q + 10
                q_type = r[2]
                key_val = r[4]
                records.append({
                    "question_number": qno,
                    "paper_question_number": qno,
                    "printed_question_number": raw_q,
                    "raw_question_number": raw_q,
                    "section_code": sec_code,
                    "section": sec,
                    "question_type": q_type,
                    "key": key_val,
                    "correct_options": extract_correct_options(key_val, q_type),
                    "marks": float(r[5]) if len(r) > 5 and r[5].replace(".", "", 1).isdigit() else 1.0
                })
        return records

    # 2022, 2023, 2024, 2025 (Continuous Q1 to Q65)
    for r in cleaned:
        if len(r) >= 5 and r[0].isdigit():
            qno = int(r[0])
            sec = r[3]
            sec_code = "GA" if "GA" in sec else "CS"
            q_type = r[2]
            key_val = r[4]
            records.append({
                "question_number": qno,
                "paper_question_number": qno,
                "printed_question_number": qno,
                "raw_question_number": qno,
                "section_code": sec_code,
                "section": sec,
                "question_type": q_type,
                "key": key_val,
                "correct_options": extract_correct_options(key_val, q_type),
                "marks": float(r[5]) if len(r) > 5 and r[5].replace(".", "", 1).isdigit() else 1.0
            })

    return records


def parse_2015_json(json_path: Path) -> List[Dict[str, Any]]:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    records = []
    for item in data:
        qn_str = item.get("Qn. No.", "").strip()
        if not qn_str or qn_str.lower() == "total":
            continue
        key_val = item.get("Official GATE Key", "").strip().upper()

        if qn_str.startswith("GA"):
            raw_q = int(qn_str[2:])
            sec_code = "GA"
            qno = raw_q
        else:
            digits = "".join([c for c in qn_str if c.isdigit()])
            raw_q = int(digits) if digits else len(records) + 1
            sec_code = "CS"
            qno = raw_q + 10

        q_type = "MCQ" if len(key_val) == 1 and key_val.isalpha() else "NAT"

        records.append({
            "question_number": qno,
            "paper_question_number": qno,
            "printed_question_number": raw_q,
            "raw_question_number": raw_q,
            "section_code": sec_code,
            "section": "General Aptitude" if sec_code == "GA" else "Computer Science and Information Technology",
            "question_type": q_type,
            "key": key_val,
            "correct_options": extract_correct_options(key_val, q_type),
            "marks": 1.0 if (qno <= 5 or (11 <= qno <= 35)) else 2.0
        })

    return records


def digitize_all_keys() -> Dict[str, List[Dict[str, Any]]]:
    DIGITIZED_DIR.mkdir(parents=True, exist_ok=True)
    all_digitized = {}

    # 1. Parse PDFs in answer_keys/
    pdf_files = sorted(ANSWER_KEYS_DIR.glob("*.pdf"))
    for pdf_file in pdf_files:
        name = pdf_file.stem  # e.g. '2024_CS1_key'
        paper_id = name.replace("_key", "")
        year = int(paper_id.split("_")[0])
        records = parse_pdf_table(pdf_file)

        doc = {
            "paper_id": paper_id,
            "year": year,
            "total_keys": len(records),
            "keys": records,
            "keys_by_number": {str(r["question_number"]): r["key"] for r in records},
            "correct_options_by_number": {str(r["question_number"]): r["correct_options"] for r in records},
            "keys_by_section_and_number": {
                f"{r['section_code']}_{r['printed_question_number']}": r["key"] for r in records
            },
            "correct_options_by_section_and_number": {
                f"{r['section_code']}_{r['printed_question_number']}": r["correct_options"] for r in records
            }
        }

        out_path = DIGITIZED_DIR / f"{paper_id}_key.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2)

        all_digitized[paper_id] = records
        print(f"Digitized {paper_id}: {len(records)} keys -> {out_path}")

    # 2. Parse 2015 JSON files
    for s in [1, 2, 3]:
        p15_path = ANSWER_KEYS_DIR / f"2015_CS{s}_key.json"
        if p15_path.exists():
            records = parse_2015_json(p15_path)
            paper_id = f"2015_CS{s}"
            doc = {
                "paper_id": paper_id,
                "year": 2015,
                "session": f"CS{s}",
                "total_keys": len(records),
                "keys": records,
                "keys_by_number": {str(r["question_number"]): r["key"] for r in records},
                "correct_options_by_number": {str(r["question_number"]): r["correct_options"] for r in records},
                "keys_by_section_and_number": {
                    f"{r['section_code']}_{r['printed_question_number']}": r["key"] for r in records
                },
                "correct_options_by_section_and_number": {
                    f"{r['section_code']}_{r['printed_question_number']}": r["correct_options"] for r in records
                }
            }
            out_path = DIGITIZED_DIR / f"{paper_id}_key.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(doc, f, indent=2)
            all_digitized[paper_id] = records
            print(f"Digitized {paper_id}: {len(records)} keys -> {out_path}")

    return all_digitized


def merge_answers_into_questions(all_keys: Dict[str, List[Dict[str, Any]]]):
    COMBINED_DIR.mkdir(parents=True, exist_ok=True)

    paper_files = sorted(OUTPUT_DIR.glob("20*.json"))
    paper_files = [f for f in paper_files if not f.name.startswith("summary")]

    print("\n--- Merging Questions + Answers into combined_qa/ ---")

    for p_file in paper_files:
        with open(p_file, encoding="utf-8") as f:
            data = json.load(f)

        paper_id = data.get("paper_id", p_file.stem)
        year = data.get("year", int(paper_id.split("_")[0]))
        if year < 2011 or year > 2025:
            continue

        questions = data.get("questions", [])
        updated_questions = []

        # Find matching key map
        for q in questions:
            q_copy = dict(q)
            q_num = q.get("question_number", 0)
            page = q.get("page_start", 1)

            answer = None
            official_q_type = None

            # Special case: 2013 has 4 booklet codes in 1 paper
            if paper_id == "2013_CS":
                records = all_keys.get("2013_CS", [])
                recs_by_num = {r["question_number"]: r for r in records}
                r = recs_by_num.get(q_num)
                if r:
                    official_q_type = r.get("question_type", "MCQ")
                    if page <= 15:
                        answer = r.get("code_a")
                    elif page <= 30:
                        answer = r.get("code_b")
                    elif page <= 45:
                        answer = r.get("code_c")
                    else:
                        answer = r.get("code_d")

            # Special case: 2014 has 3 sessions in 1 paper
            elif paper_id == "2014_CS":
                if page <= 22:
                    target_key_id = "2014_CS1"
                    is_ga = (page <= 7)
                elif page <= 45:
                    target_key_id = "2014_CS2"
                    is_ga = (page <= 30)
                else:
                    target_key_id = "2014_CS3"
                    is_ga = (page <= 53)

                mapped_qno = q_num if is_ga else q_num + 10
                records = all_keys.get(target_key_id, [])
                recs_by_num = {r["question_number"]: r for r in records}
                r = recs_by_num.get(mapped_qno)
                if r:
                    answer = r.get("key")
                    official_q_type = r.get("question_type")

            # Special case: 2016 has 2 sessions in 1 paper
            elif paper_id == "2016_CS":
                if page <= 22:
                    target_key_id = "2016_CS1"
                    is_ga = (page <= 3)
                else:
                    target_key_id = "2016_CS2"
                    is_ga = (page <= 25)

                mapped_qno = q_num if is_ga else q_num + 10
                records = all_keys.get(target_key_id, [])
                recs_by_num = {r["question_number"]: r for r in records}
                r = recs_by_num.get(mapped_qno)
                if r:
                    answer = r.get("key")
                    official_q_type = r.get("question_type")

            # Special case: 2018 (GA Q1-10 on p1-3, CS Q1-55 on p4+)
            elif paper_id == "2018_CS":
                is_ga = (page <= 3)
                mapped_qno = q_num if is_ga else q_num + 10
                records = all_keys.get("2018_CS", [])
                recs_by_num = {r["question_number"]: r for r in records}
                r = recs_by_num.get(mapped_qno)
                if r:
                    answer = r.get("key")
                    official_q_type = r.get("question_type")

            # Special case: 2023 CS - fix footer-based off-by-one shift for CS questions
            elif paper_id == "2023_CS":
                if page >= 8:
                    real_qno = q_num + 1
                else:
                    real_qno = q_num

                q_copy["question_number"] = real_qno
                q_copy["id"] = f"2023_CS_{'GA' if real_qno <= 10 else 'CS'}_Q{real_qno:02d}"

                records = all_keys.get("2023_CS", [])
                recs_by_num = {r["question_number"]: r for r in records}
                r = recs_by_num.get(real_qno)
                if r:
                    answer = r.get("key")
                    official_q_type = r.get("question_type")

            # Standard 1-to-1 matching (2011, 2012, 2022, 2024, 2025)
            else:
                records = all_keys.get(paper_id, [])
                recs_by_num = {r["question_number"]: r for r in records}
                r = recs_by_num.get(q_num)
                if r:
                    answer = r.get("key")
                    official_q_type = r.get("question_type")

            # Determine final question_type and negative_marks
            final_type = official_q_type if official_q_type else q.get("question_type", "MCQ")
            if answer and (";" in str(answer) or "," in str(answer)):
                final_type = "MSQ"

            q_copy["question_type"] = final_type

            # Correct negative marks: MSQ and NAT have 0.0 negative marks in GATE
            if final_type in ["MSQ", "NAT"]:
                q_copy["negative_marks"] = 0.0

            q_copy["answer"] = answer
            q_copy["correct_options"] = extract_correct_options(answer, final_type)
            q_copy["explaination"] = ""

            updated_questions.append(q_copy)

        combined_data = dict(data)
        combined_data["questions"] = updated_questions

        out_file = COMBINED_DIR / f"{paper_id}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(combined_data, f, indent=2)

        msq_count = sum(1 for q in updated_questions if q.get("question_type") == "MSQ")
        multi_count = sum(1 for q in updated_questions if q.get("correct_options") and len(q["correct_options"]) > 1)
        print(f"Saved {out_file.name}: {len(updated_questions)} questions ({msq_count} MSQs, {multi_count} multi-option answers)")


def main():
    print("=== Step 1: Digitize Official Answer Keys with Dual Section/Paper Lookups ===")
    all_keys = digitize_all_keys()

    print("\n=== Step 2: Combine Questions + Answers with Full MSQ Support ===")
    merge_answers_into_questions(all_keys)

    print("\nDigitization and merge complete.")


if __name__ == "__main__":
    main()
