"""Command-line runner to parse GATE CS exam papers into standardized JSON files."""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import time
from pathlib import Path
from typing import List

from src.pdf_parser import GatePDFParser
from src.schema import export_json_schema


def run_parser(
    pdf_dir: str = "CS",
    output_dir: str = "output",
    specific_file: str | None = None,
) -> None:
    """Parses all PDFs in `pdf_dir` or a specific PDF and saves JSON files."""
    start_time = time.time()
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # 1. Ensure global JSON schema is exported
    schema_file = export_json_schema("schema/gate_paper_schema.json")
    print(f"[Schema] Exported global JSON schema to: {schema_file}\n")

    parser = GatePDFParser()

    if specific_file:
        pdf_files = [specific_file]
    else:
        pdf_files = sorted(glob.glob(os.path.join(pdf_dir, "*.pdf")))

    if not pdf_files:
        print(f"Error: No PDF files found in '{pdf_dir}'.")
        sys.exit(1)

    print(f"Starting batch parsing for {len(pdf_files)} GATE CS question paper(s)...\n")
    print(f"{'Paper ID':<15} | {'Total Qs':<10} | {'Extracted (Text)':<18} | {'Omitted (Images)':<18} | {'Status'}")
    print("-" * 75)

    summary_records = []
    total_extracted_all = 0
    total_omitted_all = 0

    for pdf_path in pdf_files:
        try:
            t0 = time.time()
            paper = parser.parse_pdf(pdf_path)
            json_file = parser.save_paper(paper, output_dir)
            elapsed = time.time() - t0

            total_extracted_all += paper.extracted_questions_count
            total_omitted_all += paper.omitted_questions_count

            summary_records.append({
                "paper_id": paper.paper_id,
                "year": paper.year,
                "session": paper.session,
                "total_questions": paper.total_questions_in_paper,
                "extracted_questions": paper.extracted_questions_count,
                "omitted_questions": paper.omitted_questions_count,
                "json_file": str(json_file),
                "elapsed_seconds": round(elapsed, 2),
            })

            status_str = f"Done ({elapsed:.1f}s)"
            print(
                f"{paper.paper_id:<15} | {paper.total_questions_in_paper:<10} | "
                f"{paper.extracted_questions_count:<18} | {paper.omitted_questions_count:<18} | {status_str}"
            )
        except Exception as e:
            print(f"{Path(pdf_path).stem:<15} | ERROR: {str(e)}")

    total_time = time.time() - start_time
    print("-" * 75)
    print(f"Total Papers Processed: {len(pdf_files)}")
    print(f"Total Questions Extracted (Text/Markdown/LaTeX): {total_extracted_all}")
    print(f"Total Questions Omitted (Containing Images/Scanned): {total_omitted_all}")
    print(f"Total Processing Time: {total_time:.2f} seconds")

    # Save summary report
    summary_path = out_path / "summary_report.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "total_papers": len(pdf_files),
                "total_extracted": total_extracted_all,
                "total_omitted": total_omitted_all,
                "papers": summary_records,
            },
            f,
            indent=2,
        )
    print(f"\n[Summary] Report saved to: {summary_path}")


def main():
    arg_parser = argparse.ArgumentParser(
        description="GATE CS Previous Year Questions (PYQ) PDF to JSON Parser"
    )
    arg_parser.add_argument(
        "--input-dir",
        default="CS",
        help="Directory containing GATE PDF files (default: CS)",
    )
    arg_parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to store extracted JSON files (default: output)",
    )
    arg_parser.add_argument(
        "--file",
        default=None,
        help="Specific PDF file to parse instead of entire directory",
    )

    args = arg_parser.parse_args()
    run_parser(
        pdf_dir=args.input_dir,
        output_dir=args.output_dir,
        specific_file=args.file,
    )


if __name__ == "__main__":
    main()
