"""PDF to JSON parser for GATE CS Previous Year Question papers.

Extracts questions, sections, marks, options, and question types.
Uses native PDF parsing for digital papers and fast multi-threaded Tesseract OCR for old scanned papers (2007-2011).
Omits all questions containing images, figures, or diagrams.
Formats text into clean markdown/LaTeX.
Ensures identical schema across all generated JSON files.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import pymupdf

from src.image_detector import ImageDetector
from src.ocr_parser import GateOCRParser
from src.schema import GatePaper, GateQuestion
from src.text_cleaner import (
    clean_markdown_formatting,
    clean_math_notation,
    decode_symbols,
    parse_options,
    strip_boilerplate,
)


class GatePDFParser:
    """Parser that converts GATE CS examination PDFs to structured JSON."""

    def __init__(self, ocr_dpi: int = 150):
        self.ocr_parser = GateOCRParser(dpi=ocr_dpi, max_workers=6)

    def parse_pdf(self, pdf_path: str | Path) -> GatePaper:
        """Parses a single GATE PDF file and returns a validated GatePaper object."""
        path = Path(pdf_path)
        paper_id = path.stem

        year, session = self._extract_paper_meta(paper_id)
        doc = pymupdf.open(str(path))

        total_text_len = sum(len(page.get_text().strip()) for page in doc)
        avg_chars_per_page = total_text_len / len(doc)

        # 1. Old scanned/clicked papers (2007-2011) -> run OCR
        if avg_chars_per_page < 400 and year <= 2011:
            return self.ocr_parser.parse_image_paper(doc, paper_id, year, session)

        # 2. Non-scanned image-screenshot papers (2015, 2017, 2019, 2020, 2021)
        # Questions in these papers are images, so all questions are omitted without slow full-paper OCR
        if avg_chars_per_page < 400:
            return GatePaper(
                paper_id=paper_id,
                year=year,
                subject="Computer Science and Information Technology",
                subject_code="CS",
                session=session,
                total_questions_in_paper=65,
                extracted_questions_count=0,
                omitted_questions_count=65,
                questions=[],
            )

        # 3. Native digital text papers (2012-2026)
        detector = ImageDetector(doc)
        extracted_questions, omitted_count = self._parse_digital_paper(
            doc, paper_id, year, session, detector
        )

        total_questions = len(extracted_questions) + omitted_count
        if len(extracted_questions) == 0 and total_questions == 0:
            total_questions = 65
            omitted_count = 65

        return GatePaper(
            paper_id=paper_id,
            year=year,
            subject="Computer Science and Information Technology",
            subject_code="CS",
            session=session,
            total_questions_in_paper=total_questions,
            extracted_questions_count=len(extracted_questions),
            omitted_questions_count=omitted_count,
            questions=extracted_questions,
        )

    def _extract_paper_meta(self, paper_id: str) -> Tuple[int, Optional[str]]:
        """Parses year and session/set from paper ID string."""
        m = re.match(r"^(\d{4})_?(.*)$", paper_id)
        if m:
            year = int(m.group(1))
            sess = m.group(2).strip()
            session = sess if sess else None
            return year, session
        return 2000, None

    def _parse_digital_paper(
        self,
        doc: pymupdf.Document,
        paper_id: str,
        year: int,
        session: Optional[str],
        detector: ImageDetector,
    ) -> Tuple[List[GateQuestion], int]:
        """Parses a digital text GATE PDF by segmenting questions and evaluating image presence."""
        raw_candidates = []
        current_candidate = None

        current_section_name = "General Aptitude"
        current_section_code = "GA"
        current_marks = 1.0

        for p_idx in range(len(doc)):
            page = doc[p_idx]
            page_rect = page.rect
            blocks = page.get_text("blocks")

            for b in blocks:
                text = b[4].strip()
                if not text:
                    continue

                if b[3] < 65 and ("GATE" in text or "Organizing" in text or "Page" in text):
                    continue
                if b[1] > (page_rect.height - 45) and ("Organizing" in text or "Page" in text or "Computer Science" in text):
                    continue

                if "general aptitude" in text.lower():
                    current_section_name = "General Aptitude"
                    current_section_code = "GA"
                elif (
                    "computer science" in text.lower()
                    or "computer sc." in text.lower()
                    or "cs :" in text.lower()
                    or "cs -" in text.lower()
                ):
                    current_section_name = "Computer Science and Information Technology"
                    current_section_code = "CS"

                range_match = re.search(
                    r"Q\s*\.?\s*\d+\s*[–\-]\s*Q\s*\.?\s*\d+\s*(?:carry|Carry)\s*(one|two|1|2|ONE|TWO)?\s*mark",
                    text,
                    re.IGNORECASE,
                )
                if range_match:
                    marks_str = (range_match.group(1) or "").lower()
                    if "one" in marks_str or "1" in marks_str:
                        current_marks = 1.0
                    elif "two" in marks_str or "2" in marks_str:
                        current_marks = 2.0
                    continue

                lines = text.split("\n")
                first_line = lines[0].strip()
                q_match = re.match(
                    r"^Q\s*\.\s*(?:No\s*\.\s*)?(\d+)(?:\s+(.*))?$",
                    first_line,
                    re.IGNORECASE,
                )

                if (
                    q_match
                    and not re.search(r"[–\-]\s*Q", first_line)
                    and "carry" not in first_line.lower()
                    and "mark" not in first_line.lower()
                ):
                    if current_candidate:
                        raw_candidates.append(current_candidate)

                    q_num = int(q_match.group(1))

                    sec_name, sec_code, q_marks = self._determine_section_and_marks(
                        year, q_num, current_section_name, current_section_code, current_marks
                    )

                    rest = "\n".join(lines[1:]) if len(lines) > 1 else ""
                    if q_match.group(2):
                        rest = q_match.group(2) + ("\n" + rest if rest else "")

                    current_candidate = {
                        "q_num": q_num,
                        "section": sec_name,
                        "section_code": sec_code,
                        "marks": q_marks,
                        "raw_text": rest,
                        "page_start": p_idx + 1,
                        "page_end": p_idx + 1,
                        "segments": [(p_idx, b[1], b[3])],
                    }
                elif current_candidate:
                    current_candidate["raw_text"] += "\n" + text
                    current_candidate["page_end"] = p_idx + 1
                    current_candidate["segments"].append((p_idx, b[1], b[3]))

        if current_candidate:
            raw_candidates.append(current_candidate)

        extracted_questions: List[GateQuestion] = []
        omitted_count = 0
        seen_ids: Set[str] = set()

        for cand in raw_candidates:
            has_image = False
            for (p_idx, y0, y1) in cand["segments"]:
                if detector.question_has_image(p_idx, y0, y1):
                    has_image = True
                    break

            if has_image:
                omitted_count += 1
                continue

            cleaned_raw = strip_boilerplate(decode_symbols(cand["raw_text"]))
            cleaned_math = clean_math_notation(cleaned_raw)
            stem, options = parse_options(cleaned_math)

            if len(stem.strip()) < 10:
                omitted_count += 1
                continue

            if options and len(options) >= 2:
                q_type = "MCQ"
                neg_marks = 0.33 if cand["marks"] == 1.0 else 0.66
            else:
                q_type = "NAT"
                options = None
                neg_marks = 0.0

            base_id = f"{paper_id}_{cand['section_code']}_Q{cand['q_num']:02d}"
            q_id = base_id
            counter = 2
            while q_id in seen_ids:
                q_id = f"{base_id}_v{counter}"
                counter += 1
            seen_ids.add(q_id)

            question = GateQuestion(
                id=q_id,
                question_number=cand["num"] if "num" in cand else cand["q_num"],
                section=cand["section"],
                section_code=cand["section_code"],
                question_type=q_type,
                marks=cand["marks"],
                negative_marks=neg_marks,
                question_text=stem,
                options=options,
                has_images=False,
                page_start=cand["page_start"],
                page_end=cand["page_end"],
            )
            extracted_questions.append(question)

        return extracted_questions, omitted_count

    def _determine_section_and_marks(
        self,
        year: int,
        q_num: int,
        detected_sec_name: str,
        detected_sec_code: str,
        current_marks: float,
    ) -> Tuple[str, str, float]:
        """Refines section and mark allocations according to official GATE pattern for that era."""
        if year >= 2021:
            if 1 <= q_num <= 5:
                return "General Aptitude", "GA", 1.0
            elif 6 <= q_num <= 10:
                return "General Aptitude", "GA", 2.0
            elif 11 <= q_num <= 35:
                return "Computer Science and Information Technology", "CS", 1.0
            elif 36 <= q_num <= 65:
                return "Computer Science and Information Technology", "CS", 2.0

        if year in (2012, 2013):
            if 1 <= q_num <= 25:
                return "Computer Science and Information Technology", "CS", 1.0
            elif 26 <= q_num <= 55:
                return "Computer Science and Information Technology", "CS", 2.0
            elif 56 <= q_num <= 60:
                return "General Aptitude", "GA", 1.0
            elif 61 <= q_num <= 65:
                return "General Aptitude", "GA", 2.0

        return detected_sec_name, detected_sec_code, current_marks

    def save_paper(self, paper: GatePaper, output_dir: str | Path = "output") -> Path:
        """Serializes the GatePaper object to a JSON file matching the global schema."""
        out_path = Path(output_dir) / f"{paper.paper_id}.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(paper.model_dump_json(indent=2))
        return out_path
