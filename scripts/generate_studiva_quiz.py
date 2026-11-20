#!/usr/bin/env python3
"""
generate_studiva_quiz.py

Converts GATE question paper datasets into Studiva QUIZ JSON format.
Follows the Studiva schema specification (sample_format.json / Quiz.fromJson in Flutter):
- Top-level: negative_marking, negative_marking_factor, questions
- MCQ: id, type ('mcq'), points, question, options (list of strings), answer (matching option string), explanation
- Numerical / NAT: id, type ('fill_number'), points, question, answer (single number string, midpoint if range), explanation
- MSQ: omitted when unavailable in Studiva, per specification

Usage:
    python3 scripts/generate_studiva_quiz.py --paper 2025_CS2
    python3 scripts/generate_studiva_quiz.py --all
    python3 scripts/generate_studiva_quiz.py --input path/to/full_paper.json --output path/to/output.json
"""

import os
import sys
import json
import re
import argparse
from typing import Dict, Any, List, Optional


def sanitize_text(text: Optional[str]) -> str:
    """Strip leading/trailing whitespace and normalize line breaks."""
    if not text:
        return ""
    text = text.strip()
    # Remove common trailing PDF/OCR artifacts
    text = re.sub(r'\n+Organising Institute:.*$', '', text, flags=re.IGNORECASE | re.DOTALL)
    return text.strip()


def parse_numerical_answer(answer_str: Optional[str], num_range: Optional[Dict[str, Any]]) -> str:
    """
    Extract a single numerical answer string for Studiva.
    Studiva fill_number performs exact text comparison against answer,
    so range strings ('13 to 13' or '0.70 to 0.80') are converted to a single
    representative number (the exact value or range midpoint).
    """
    ans_val: Optional[float] = None

    # Check numerical_answer_range first
    if num_range and isinstance(num_range, dict):
        min_v = num_range.get("min")
        max_v = num_range.get("max")
        if min_v is not None and max_v is not None:
            try:
                min_f = float(min_v)
                max_f = float(max_v)
                ans_val = (min_f + max_f) / 2.0
            except (ValueError, TypeError):
                pass

    # Fallback to parsing answer string
    if ans_val is None and answer_str:
        cleaned_str = str(answer_str).strip()
        # Pattern like '260.20 to 261.20'
        range_match = re.match(
            r'^\s*([+-]?\d+(?:\.\d+)?)\s+to\s+([+-]?\d+(?:\.\d+)?)\s*$',
            cleaned_str,
            re.IGNORECASE
        )
        if range_match:
            try:
                min_f = float(range_match.group(1))
                max_f = float(range_match.group(2))
                ans_val = (min_f + max_f) / 2.0
            except (ValueError, TypeError):
                pass
        else:
            try:
                ans_val = float(cleaned_str)
            except ValueError:
                pass

    if ans_val is not None:
        # Check if float is effectively an integer
        if abs(ans_val - round(ans_val)) < 1e-9:
            return str(int(round(ans_val)))
        # Format decimal cleanly without trailing zeros
        return f"{ans_val:.4f}".rstrip("0").rstrip(".")

    # Final fallback if parsing completely fails
    return str(answer_str or "").strip()


def convert_paper_to_studiva_quiz(
    paper_data: Dict[str, Any],
    msq_action: str = "skip",
    negative_marking: bool = True,
    negative_marking_factor: float = 0.33
) -> Dict[str, Any]:
    """
    Converts full_paper.json dict structure into Studiva Quiz JSON structure.
    """
    raw_questions = paper_data.get("questions", [])
    studiva_questions: List[Dict[str, Any]] = []

    stats = {
        "total_source": len(raw_questions),
        "mcq": 0,
        "nat": 0,
        "msq_skipped": 0,
        "other_skipped": 0,
        "total_converted": 0
    }

    for q in raw_questions:
        qtype = (q.get("question_type") or "").upper()
        qid = q.get("id") or f"q_{q.get('question_number', len(studiva_questions) + 1)}"
        points = float(q.get("marks", 1.0))

        # Use LaTeX formatted text if available, fallback to raw text
        q_text = sanitize_text(q.get("question_text_latex") or q.get("question_text"))
        explanation = sanitize_text(q.get("explaination") or q.get("explanation"))

        if qtype == "MCQ":
            # Prefer options_latex for clean mathematical formatting and no OCR artifacts
            opts_dict = q.get("options_latex") or q.get("options") or {}
            
            # Preserve standard A, B, C, D order
            keys = [k for k in ["A", "B", "C", "D"] if k in opts_dict] or sorted(opts_dict.keys())
            options_list = [sanitize_text(opts_dict[k]) for k in keys]

            # Resolve answer key
            ans_key = q.get("answer")
            if not ans_key and q.get("correct_options"):
                ans_key = q["correct_options"][0]
            ans_key = str(ans_key).strip().upper() if ans_key else ""

            # Studiva MCQ answer must be the exact option string text
            ans_text = sanitize_text(opts_dict.get(ans_key))
            if not ans_text and options_list:
                ans_text = options_list[0]

            item = {
                "id": qid,
                "type": "mcq",
                "points": points,
                "question": q_text,
                "options": options_list,
                "answer": ans_text,
                "explanation": explanation
            }
            studiva_questions.append(item)
            stats["mcq"] += 1

        elif qtype == "NAT":
            num_ans = parse_numerical_answer(q.get("answer"), q.get("numerical_answer_range"))

            item = {
                "id": qid,
                "type": "fill_number",
                "points": points,
                "question": q_text,
                "answer": num_ans,
                "explanation": explanation
            }
            studiva_questions.append(item)
            stats["nat"] += 1

        elif qtype == "MSQ":
            if msq_action == "skip":
                stats["msq_skipped"] += 1
                continue
            elif msq_action == "include_as_mcq":
                opts_dict = q.get("options_latex") or q.get("options") or {}
                keys = [k for k in ["A", "B", "C", "D"] if k in opts_dict] or sorted(opts_dict.keys())
                options_list = [sanitize_text(opts_dict[k]) for k in keys]
                
                correct_keys = q.get("correct_options") or []
                if not correct_keys and q.get("answer"):
                    correct_keys = [k.strip().upper() for k in re.split(r'[,;]+', str(q.get("answer")))]
                
                ans_text = sanitize_text(opts_dict.get(correct_keys[0])) if correct_keys else (options_list[0] if options_list else "")
                
                item = {
                    "id": qid,
                    "type": "mcq",
                    "points": points,
                    "question": q_text,
                    "options": options_list,
                    "answer": ans_text,
                    "explanation": explanation
                }
                studiva_questions.append(item)
                stats["mcq"] += 1
            else:
                stats["msq_skipped"] += 1
                continue
        else:
            stats["other_skipped"] += 1

    stats["total_converted"] = len(studiva_questions)

    quiz_payload = {
        "negative_marking": negative_marking,
        "negative_marking_factor": negative_marking_factor,
        "questions": studiva_questions
    }

    return quiz_payload, stats


def process_paper(
    paper_id: str,
    root_dir: str,
    output_dir: str,
    msq_action: str = "skip",
    negative_marking_factor: float = 0.33
) -> str:
    """Process a single paper ID and save to output directory."""
    input_path = os.path.join(root_dir, "dataset", "papers", paper_id, "full_paper.json")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        paper_data = json.load(f)

    quiz_json, stats = convert_paper_to_studiva_quiz(
        paper_data=paper_data,
        msq_action=msq_action,
        negative_marking=True,
        negative_marking_factor=negative_marking_factor
    )

    os.makedirs(output_dir, exist_ok=True)
    out_filename = f"{paper_id.lower()}.json"
    out_path = os.path.join(output_dir, out_filename)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(quiz_json, f, indent=2, ensure_ascii=False)

    print(f"[{paper_id}] Generated: {out_path}")
    print(f"   Converted: {stats['total_converted']}/{stats['total_source']} "
          f"(MCQ: {stats['mcq']}, NAT: {stats['nat']}, Skipped MSQ: {stats['msq_skipped']})")

    return out_path


def main():
    parser = argparse.ArgumentParser(
        description="Convert GATE question papers to Studiva QUIZ JSON format"
    )
    parser.add_argument(
        "--paper", "-p",
        type=str,
        default="2025_CS2",
        help="Paper ID to convert (e.g. 2025_CS2). Default: 2025_CS2"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Convert all available papers in dataset/papers/"
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        help="Explicit input full_paper.json file path"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Explicit output JSON file path"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="studiva_quiz_json",
        help="Directory to save generated JSON files. Default: studiva_quiz_json"
    )
    parser.add_argument(
        "--msq",
        choices=["skip", "include_as_mcq"],
        default="skip",
        help="How to handle MSQ questions (skip or include_as_mcq). Default: skip"
    )
    parser.add_argument(
        "--negative-marking-factor",
        type=float,
        default=0.33,
        help="Negative marking penalty factor. Default: 0.33"
    )

    args = parser.parse_args()

    # Determine workspace root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, ".."))
    out_dir = os.path.abspath(os.path.join(root_dir, args.output_dir))

    if args.input and args.output:
        with open(args.input, "r", encoding="utf-8") as f:
            paper_data = json.load(f)
        quiz_json, stats = convert_paper_to_studiva_quiz(
            paper_data=paper_data,
            msq_action=args.msq,
            negative_marking=True,
            negative_marking_factor=args.negative_marking_factor
        )
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(quiz_json, f, indent=2, ensure_ascii=False)
        print(f"Generated custom output: {args.output}")
        print(f"Converted: {stats['total_converted']}/{stats['total_source']} "
              f"(MCQ: {stats['mcq']}, NAT: {stats['nat']}, Skipped MSQ: {stats['msq_skipped']})")
        return

    if args.all:
        papers_dir = os.path.join(root_dir, "dataset", "papers")
        paper_ids = sorted([
            d for d in os.listdir(papers_dir)
            if os.path.isdir(os.path.join(papers_dir, d)) and
            os.path.exists(os.path.join(papers_dir, d, "full_paper.json"))
        ])
        print(f"Converting {len(paper_ids)} papers to Studiva QUIZ format...")
        for pid in paper_ids:
            process_paper(
                paper_id=pid,
                root_dir=root_dir,
                output_dir=out_dir,
                msq_action=args.msq,
                negative_marking_factor=args.negative_marking_factor
            )
        print("All papers converted successfully.")
    else:
        process_paper(
            paper_id=args.paper,
            root_dir=root_dir,
            output_dir=out_dir,
            msq_action=args.msq,
            negative_marking_factor=args.negative_marking_factor
        )


if __name__ == "__main__":
    main()

