"""Global JSON Schema and Data Models for GATE CS PYQ Database.

Defines the structure for questions and exam papers, ensuring 100% schema consistency
across all years and sessions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class GateQuestion(BaseModel):
    """Schema for an individual extracted GATE question."""

    id: str = Field(
        ...,
        description="Unique identifier for the question (e.g., '2024_CS1_Q01' or '2018_CS_GA_Q01')",
    )
    question_number: int = Field(
        ...,
        description="Question number as printed in the exam paper",
        ge=1,
        le=100,
    )
    section: str = Field(
        ...,
        description="Section name (e.g. 'General Aptitude' or 'Computer Science and Information Technology')",
    )
    section_code: Literal["GA", "CS"] = Field(
        ...,
        description="Standard 2-letter section code: GA (General Aptitude) or CS (Computer Science)",
    )
    question_type: Literal["MCQ", "MSQ", "NAT"] = Field(
        ...,
        description="Question type: Multiple Choice (MCQ), Multiple Select (MSQ), or Numerical Answer Type (NAT)",
    )
    marks: float = Field(
        ...,
        description="Marks allocated for correct answer (typically 1.0 or 2.0)",
        gt=0.0,
    )
    negative_marks: float = Field(
        default=0.0,
        description="Deduction for wrong answer (typically 0.33, 0.66, or 0.0)",
        ge=0.0,
    )
    question_text: str = Field(
        ...,
        description="Clean text, markdown, or LaTeX representation of the question stem",
    )
    options: Optional[Dict[str, str]] = Field(
        default=None,
        description="Options dictionary mapping 'A', 'B', 'C', 'D' to their text. Null/None for NAT questions.",
    )
    has_images: Literal[False] = Field(
        default=False,
        description="Whether question contains images. Must be false for all extracted questions as questions containing images are omitted.",
    )
    page_start: int = Field(
        ...,
        description="Starting page number of the question in the PDF (1-indexed)",
        ge=1,
    )
    page_end: int = Field(
        ...,
        description="Ending page number of the question in the PDF (1-indexed)",
        ge=1,
    )


class GatePaper(BaseModel):
    """Schema for a parsed GATE exam paper."""

    paper_id: str = Field(
        ...,
        description="Identifier of the paper matching filename (e.g., '2026_CS1', '2018_CS')",
    )
    year: int = Field(
        ...,
        description="Examination year (e.g., 2024)",
        ge=1990,
        le=2050,
    )
    subject: str = Field(
        default="Computer Science and Information Technology",
        description="Full subject title",
    )
    subject_code: str = Field(
        default="CS",
        description="Subject paper code",
    )
    session: Optional[str] = Field(
        default=None,
        description="Session or set designator (e.g., 'Set 1', 'CS1', 'CS2', or None)",
    )
    total_questions_in_paper: int = Field(
        ...,
        description="Total questions identified in the source paper (typically 65)",
        ge=0,
    )
    extracted_questions_count: int = Field(
        ...,
        description="Count of questions extracted (text-only, images omitted)",
        ge=0,
    )
    omitted_questions_count: int = Field(
        ...,
        description="Count of questions omitted due to containing images, diagrams, or scanned format",
        ge=0,
    )
    questions: List[GateQuestion] = Field(
        ...,
        description="List of text-only questions parsed from this paper",
    )


def export_json_schema(output_path: str = "schema/gate_paper_schema.json") -> str:
    """Exports the Pydantic model to a standard JSON Schema file."""
    schema_dict = GatePaper.model_json_schema()
    schema_dict["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(schema_dict, f, indent=2, ensure_ascii=False)
    return str(path)


if __name__ == "__main__":
    schema_file = export_json_schema()
    print(f"Exported JSON schema to: {schema_file}")
