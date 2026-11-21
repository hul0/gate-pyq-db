#!/usr/bin/env python3
"""
build_latex_comparison_csv.py

Extracts all question texts and options containing LaTeX from full_paper_manual.json
and api_full_paper.json, builds a side-by-side CSV comparison, and computes
detailed LaTeX scoring benchmarks.
"""

import os
import json
import csv
import re

def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    manual_path = os.path.join(root, "full_paper_manual.json")
    api_path = os.path.join(root, "api_full_paper.json")
    
    with open(manual_path, "r", encoding="utf-8") as f:
        manual_data = json.load(f)
    with open(api_path, "r", encoding="utf-8") as f:
        api_data = json.load(f)

    man_map = {q["question_number"]: q for q in manual_data["questions"]}
    api_map = {q["question_number"]: q for q in api_data["questions"]}

    csv_rows = []
    
    # Tracking metrics for scoring
    total_entries = 0
    exact_matches = 0
    math_mode_enclosure_manual_better = 0
    math_mode_enclosure_api_better = 0
    markdown_formatting_api_better = 0
    variable_coverage_api_better = 0
    variable_coverage_manual_better = 0

    all_qnums = sorted(set(man_map.keys()).union(api_map.keys()))

    for qnum in all_qnums:
        mq = man_map.get(qnum)
        aq = api_map.get(qnum)
        qid = (mq or aq).get("id", f"Q{qnum}")

        fields_to_check = [
            ("question_text", mq.get("question_text", "") if mq else "", aq.get("question_text", "") if aq else "")
        ]
        
        m_opts = mq.get("options") or {} if mq else {}
        a_opts = aq.get("options") or {} if aq else {}
        for opt in ["A", "B", "C", "D"]:
            fields_to_check.append((f"option_{opt}", str(m_opts.get(opt, "")), str(a_opts.get(opt, ""))))

        for field_name, m_val, a_val in fields_to_check:
            # Check if either entry contains LaTeX indicators
            has_latex = any(k in m_val or k in a_val for k in ["$", "\\", "^", "_", "{", "}"])
            if not has_latex:
                continue

            total_entries += 1
            m_clean = m_val.strip()
            a_clean = a_val.strip()

            if m_clean == a_clean:
                status = "EXACT_MATCH"
                analysis = "100% identical transcription and LaTeX syntax."
                exact_matches += 1
            else:
                notes = []
                # Check $ delimiters
                m_has_delim = m_clean.startswith("$") and m_clean.endswith("$")
                a_has_delim = a_clean.startswith("$") and a_clean.endswith("$")
                if m_has_delim and not a_has_delim:
                    if "\\begin{" in a_clean or any(sym in a_clean for sym in ["\\Theta", "\\Omega", "O("]):
                        notes.append("Manual includes proper $ math delimiters (needed for KaTeX/LaTeX matrix).")
                        math_mode_enclosure_manual_better += 1
                elif a_has_delim and not m_has_delim:
                    notes.append("API wraps math expression in $ delimiters.")
                    math_mode_enclosure_api_better += 1

                # Check bold emphasis (**NOT**, **TRUE**)
                if "**" in a_clean and "**" not in m_clean:
                    notes.append("API adds Markdown bold emphasis matching printed exam typography.")
                    markdown_formatting_api_better += 1

                # Variable wrapping
                m_dollars = m_clean.count("$")
                a_dollars = a_clean.count("$")
                if a_dollars > m_dollars:
                    notes.append(f"API has denser LaTeX variable wrapping ({a_dollars//2} vs {m_dollars//2} math spans).")
                    variable_coverage_api_better += 1
                elif m_dollars > a_dollars:
                    notes.append(f"Manual has denser LaTeX variable wrapping ({m_dollars//2} vs {a_dollars//2} math spans).")
                    variable_coverage_manual_better += 1

                if not notes:
                    notes.append("Minor whitespace, punctuation, or equivalent LaTeX notation variation.")
                
                status = "VARIATION"
                analysis = " | ".join(notes)

            csv_rows.append({
                "question_number": qnum,
                "question_id": qid,
                "field": field_name,
                "manual": m_clean,
                "api": a_clean,
                "match_status": status,
                "analysis": analysis
            })

    out_csv_paths = [
        os.path.join(root, "latex_comparison.csv"),
        os.path.join(root, "output", "latex_comparison.csv")
    ]

    for p in out_csv_paths:
        os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
        with open(p, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "question_number", "question_id", "field", "manual", "api", "match_status", "analysis"
            ])
            writer.writeheader()
            writer.writerows(csv_rows)
        print(f"Saved LaTeX comparison CSV: {p}")

    print("\n--- Summary Benchmark Metrics ---")
    print(f"Total LaTeX Fields Checked: {total_entries}")
    print(f"Exact Matches:              {exact_matches} ({exact_matches/total_entries*100:.1f}%)")
    print(f"Variations:                 {total_entries - exact_matches} ({(total_entries - exact_matches)/total_entries*100:.1f}%)")
    print(f"Manual Superior Enclosure:  {math_mode_enclosure_manual_better}")
    print(f"API Superior Enclosure:     {math_mode_enclosure_api_better}")
    print(f"API Markdown Typography:    {markdown_formatting_api_better}")
    print(f"API Denser Math Coverage:   {variable_coverage_api_better}")
    print(f"Manual Denser Math Coverage:{variable_coverage_manual_better}")

if __name__ == "__main__":
    main()
