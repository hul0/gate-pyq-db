"""OCR-based parser for old image-clicked and scanned GATE CS question papers (2007-2011).

Uses multi-threaded Tesseract OCR (--psm 4) to extract text questions.
Detects and omits any questions containing images, figures, circuit diagrams, state graphs,
or visual option choices.
Outputs data adhering strictly to the global GatePaper and GateQuestion schema.
"""

from __future__ import annotations

import concurrent.futures
import io
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from PIL import Image
import pymupdf
import pytesseract

from src.schema import GatePaper, GateQuestion
from src.text_cleaner import (
    clean_markdown_formatting,
    clean_math_notation,
    decode_symbols,
    parse_options,
    strip_boilerplate,
)

# Phrases that indicate a question relies on an image, diagram, circuit, or graph
DIAGRAM_KEYWORDS = [
    "shown below",
    "shown in the figure",
    "shown in figure",
    "following figure",
    "given in the figure",
    "in the given circuit",
    "the circuit shown",
    "state diagram",
    "transition diagram",
    "timing diagram",
    "following graph",
    "truth table shown",
    "karnaugh map",
    "k-map",
    "flow chart",
    "flowchart",
    "following tree",
    "block diagram",
    "as shown in the network",
    "shown in the diagram",
    "given diagram",
    "network shown",
    "in the diagram",
    "given in table",
    "shown in table",
    "the table below",
]


class GateOCRParser:
    """Extracts text questions from old scanned GATE question papers via Tesseract OCR."""

    def __init__(self, dpi: int = 150, max_workers: int = 6):
        self.dpi = dpi
        self.max_workers = max_workers

    def _ocr_single_page(self, page_data: Tuple[int, bytes]) -> Tuple[int, str]:
        """OCRs a single rendered page pixmap bytes."""
        p_num, img_bytes = page_data
        img = Image.open(io.BytesIO(img_bytes))
        try:
            txt = pytesseract.image_to_string(img, config="--psm 4")
        except Exception:
            txt = pytesseract.image_to_string(img)
        return p_num, txt

    def parse_image_paper(
        self,
        doc: pymupdf.Document,
        paper_id: str,
        year: int,
        session: Optional[str],
    ) -> GatePaper:
        """Runs parallel OCR across pages and segments questions, omitting any with images."""
        total_pages = len(doc)

        # 1. Render all pages to PNG bytes
        render_tasks: List[Tuple[int, bytes]] = []
        for p_idx in range(total_pages):
            page = doc[p_idx]
            pix = page.get_pixmap(dpi=self.dpi)
            render_tasks.append((p_idx + 1, pix.tobytes("png")))

        # 2. Run OCR in parallel using ThreadPoolExecutor
        page_texts_dict: Dict[int, str] = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_page = {
                executor.submit(self._ocr_single_page, task): task[0]
                for task in render_tasks
            }
            for future in concurrent.futures.as_completed(future_to_page):
                p_num, txt = future.result()
                page_texts_dict[p_num] = txt

        # Sort pages in reading order
        page_texts = [(p, page_texts_dict[p]) for p in sorted(page_texts_dict.keys())]

        # 3. Segment questions
        raw_candidates = []
        cur_q = None

        current_sec_name = "Computer Science and Information Technology"
        current_sec_code = "CS"
        current_marks = 1.0

        for p_num, p_txt in page_texts:
            lines = p_txt.split("\n")
            for l in lines:
                l_s = l.strip()
                if not l_s:
                    continue

                if "general aptitude" in l_s.lower():
                    current_sec_name = "General Aptitude"
                    current_sec_code = "GA"
                elif "computer science" in l_s.lower() or "cs :" in l_s.lower():
                    current_sec_name = "Computer Science and Information Technology"
                    current_sec_code = "CS"

                # Check range header
                if re.search(r"Q\s*[\.\s]*\d+\s*[–\-]\s*Q\s*[\.\s]*\d+\s*(?:carry|Carry)", l_s, re.IGNORECASE):
                    if "two" in l_s.lower() or " 2 " in l_s:
                        current_marks = 2.0
                    else:
                        current_marks = 1.0
                    continue

                # Question heading match
                q_match = re.match(
                    r"^(?:Question\s*Number\s*:\s*|Q\s*[\.\s]*(?:No\s*[\.\s]*)?)(\d+|[lI])(?:[\.:\s]+(.*))?$",
                    l_s,
                    re.IGNORECASE,
                )

                if q_match and not re.search(r"[–\-]\s*Q", l_s) and "carry" not in l_s.lower() and "mark" not in l_s.lower():
                    if cur_q:
                        raw_candidates.append(cur_q)

                    raw_num_str = q_match.group(1)
                    q_num = 1 if raw_num_str in ("l", "I", "i") else int(raw_num_str)

                    sec_name, sec_code, q_marks = self._determine_section_and_marks(
                        year, q_num, current_sec_name, current_sec_code, current_marks
                    )

                    rest_text = q_match.group(2) or ""

                    cur_q = {
                        "num": q_num,
                        "text": rest_text,
                        "section": sec_name,
                        "section_code": sec_code,
                        "marks": q_marks,
                        "page_start": p_num,
                        "page_end": p_num,
                    }
                elif cur_q:
                    cur_q["text"] += "\n" + l_s
                    cur_q["page_end"] = p_num

        if cur_q:
            raw_candidates.append(cur_q)

        # 4. Filter questions with diagrams and extract clean questions
        extracted_questions: List[GateQuestion] = []
        omitted_count = 0
        seen_ids: Set[str] = set()

        for cand in raw_candidates:
            raw_text = cand["text"]

            if self._contains_diagram(raw_text):
                omitted_count += 1
                continue

            cleaned = strip_boilerplate(decode_symbols(raw_text))
            cleaned = clean_math_notation(cleaned)
            stem, options = parse_options(cleaned)

            if len(stem.strip()) < 15:
                omitted_count += 1
                continue

            if options:
                if any(len(v.strip()) == 0 or "figure" in v.lower() or "fig." in v.lower() for v in options.values()):
                    omitted_count += 1
                    continue
                q_type = "MCQ"
                neg_marks = 0.25 if year == 2007 else (0.33 if cand["marks"] == 1.0 else 0.66)
            else:
                q_type = "NAT"
                neg_marks = 0.0

            base_id = f"{paper_id}_{cand['section_code']}_Q{cand['num']:02d}"
            q_id = base_id
            counter = 2
            while q_id in seen_ids:
                q_id = f"{base_id}_v{counter}"
                counter += 1
            seen_ids.add(q_id)

            question = GateQuestion(
                id=q_id,
                question_number=cand["num"],
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

        expected_total = 85 if year == 2007 else 65
        total_questions = max(expected_total, len(extracted_questions) + omitted_count)
        adjusted_omitted = total_questions - len(extracted_questions)

        return GatePaper(
            paper_id=paper_id,
            year=year,
            subject="Computer Science and Information Technology",
            subject_code="CS",
            session=session,
            total_questions_in_paper=total_questions,
            extracted_questions_count=len(extracted_questions),
            omitted_questions_count=adjusted_omitted,
            questions=extracted_questions,
        )

    def _contains_diagram(self, text: str) -> bool:
        """Checks if question text references diagrams, figures, or visual charts."""
        text_lower = text.lower()
        for kw in DIAGRAM_KEYWORDS:
            if kw in text_lower:
                return True
        return False

    def _determine_section_and_marks(
        self,
        year: int,
        q_num: int,
        detected_sec_name: str,
        detected_sec_code: str,
        current_marks: float,
    ) -> Tuple[str, str, float]:
        """Maps question number to section and mark allocation."""
        if year == 2007:
            marks = 1.0 if q_num <= 20 else 2.0
            return "Computer Science and Information Technology", "CS", marks
        elif year <= 2011:
            marks = 1.0 if q_num <= 25 else 2.0
            return "Computer Science and Information Technology", "CS", marks
        return detected_sec_name, detected_sec_code, current_marks
