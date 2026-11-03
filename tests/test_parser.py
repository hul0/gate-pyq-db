"""Unit and integration tests for GATE CS PDF to JSON parser."""

import json
from pathlib import Path
import pytest
from src.schema import GatePaper, GateQuestion, export_json_schema
from src.text_cleaner import (
    decode_symbols,
    strip_boilerplate,
    clean_math_notation,
    parse_options,
    clean_markdown_formatting,
)
from src.pdf_parser import GatePDFParser


def test_schema_export():
    """Verify that JSON Schema exports correctly and contains required definitions."""
    schema_path = export_json_schema("schema/gate_paper_schema.json")
    assert Path(schema_path).exists()

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    assert schema["title"] == "GatePaper"
    assert "required" in schema
    assert "questions" in schema["required"]
    assert "$defs" in schema
    assert "GateQuestion" in schema["$defs"]


def test_text_cleaner_symbols():
    """Verify Symbol font PUA codes are translated to standard math characters."""
    raw = "x \uf02d y = 10 \uf0b4 2 \uf0b9 5"
    cleaned = decode_symbols(raw)
    assert "−" in cleaned
    assert "×" in cleaned
    assert "≠" in cleaned


def test_text_cleaner_math():
    """Verify math formatting like exponents and inequalities."""
    text = "Let x ^ 2 + y ^ 3 <= 10 and a != b"
    formatted = clean_math_notation(text)
    assert "x^{2}" in formatted
    assert "y^{3}" in formatted
    assert "≤" in formatted
    assert "≠" in formatted


def test_boilerplate_removal():
    """Verify institute headers and page numbers are removed."""
    raw = "Organizing Institute: IIT Guwahati\nPage 1 of 46\nWhat is the output?"
    cleaned = strip_boilerplate(raw)
    assert "Organizing Institute" not in cleaned
    assert "Page 1 of 46" not in cleaned
    assert "What is the output?" in cleaned


def test_parse_options_mcq():
    """Verify MCQ options parsing."""
    block = """Which algorithm has O(n log n) average time?
(A) Quick sort
(B) Bubble sort
(C) Selection sort
(D) Insertion sort"""
    stem, options = parse_options(block)
    assert "Which algorithm has" in stem
    assert options is not None
    assert options["A"] == "Quick sort"
    assert options["B"] == "Bubble sort"
    assert options["C"] == "Selection sort"
    assert options["D"] == "Insertion sort"


def test_parse_options_nat():
    """Verify NAT question (no options) returns None."""
    block = "The number of vertices in a complete bipartite graph K_{3,4} is ________."
    stem, options = parse_options(block)
    assert "complete bipartite graph" in stem
    assert options is None


def test_gate_question_model_validation():
    """Verify that a valid GateQuestion adheres to the Pydantic schema."""
    q = GateQuestion(
        id="2026_CS1_GA_Q01",
        question_number=1,
        section="General Aptitude",
        section_code="GA",
        question_type="MCQ",
        marks=1.0,
        negative_marks=0.33,
        question_text="The antonym of protagonist is ________.",
        options={"A": "agnostic", "B": "antagonist", "C": "arsonist", "D": "anarchist"},
        has_images=False,
        page_start=1,
        page_end=1,
    )
    assert q.has_images is False
    assert q.negative_marks == 0.33

    # Ensure has_images cannot be True
    with pytest.raises(Exception):
        GateQuestion(
            id="2026_CS1_GA_Q02",
            question_number=2,
            section="General Aptitude",
            section_code="GA",
            question_type="MCQ",
            marks=1.0,
            negative_marks=0.33,
            question_text="Question with image",
            options=None,
            has_images=True,  # Should fail validation!
            page_start=2,
            page_end=2,
        )


def test_parser_sample_paper():
    """Verify parsing a real GATE paper (2026_CS1.pdf) produces compliant output."""
    pdf_path = Path("CS/2026_CS1.pdf")
    if not pdf_path.exists():
        pytest.skip("CS/2026_CS1.pdf not found")

    parser = GatePDFParser()
    paper = parser.parse_pdf(pdf_path)

    assert paper.paper_id == "2026_CS1"
    assert paper.year == 2026
    assert paper.total_questions_in_paper == 65
    assert paper.extracted_questions_count > 50
    assert paper.omitted_questions_count > 0
    # Every extracted question must have has_images == False
    for q in paper.questions:
        assert q.has_images is False
        assert q.marks in (1.0, 2.0)
        assert q.question_type in ("MCQ", "MSQ", "NAT")
        assert len(q.question_text.strip()) > 0


def test_ocr_parser_image_paper():
    """Verify OCR parsing on image-clicked paper (2009_CS.pdf)."""
    pdf_path = Path("CS/2009_CS.pdf")
    if not pdf_path.exists():
        pytest.skip("CS/2009_CS.pdf not found")

    parser = GatePDFParser()
    paper = parser.parse_pdf(pdf_path)

    assert paper.paper_id == "2009_CS"
    assert paper.year == 2009
    assert paper.extracted_questions_count > 30
    for q in paper.questions:
        assert q.has_images is False
        assert len(q.question_text.strip()) > 0
