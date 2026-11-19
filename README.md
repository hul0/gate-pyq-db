# GATE CS PYQ Database

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![JSON Schema](https://img.shields.io/badge/Schema-Draft--2020--12-green.svg)](schema/gate_paper_schema.json)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](tests/)

A standardized, machine-readable JSON database and automated extraction pipeline for GATE Computer Science & Information Technology (CS/IT) Previous Year Question papers covering 2007 through 2026 (24 exam sessions).

Repository: [https://github.com/hul0/gate-pyq-db](https://github.com/hul0/gate-pyq-db)

Author / Maintainer: Rupam Ghosh

---

## Highlights

- **Standardized Global Schema**: Every question paper produces a validated JSON file strictly conforming to `schema/gate_paper_schema.json`.
- **Pre-computed Database**: The `output/` directory contains fully parsed, validated JSON files for all 24 papers ready for immediate educational and research use.
- **Strict Diagram / Image Omission**: All questions containing circuit diagrams, graphs, flowcharts, or visual options are omitted (`has_images: false`), filtering out ambiguous visual dependencies and watermark artifacts.
- **Markdown & LaTeX Cleansing**: Mathematical notations, exponents, logic operators (and, or, not, implies), and formatting are normalized into clean Markdown/LaTeX representations.
- **Metadata Extraction**: Automatically classifies question type (MCQ, MSQ, NAT), section (General Aptitude, Computer Science), mark weighting (1.0, 2.0), and negative markings.
- **Dual Engine Pipeline**: Employs native PDF parsing for digital papers (2012-2026) and multi-threaded Tesseract OCR (`--psm 4`) for legacy scanned papers (2007-2011).

---

## Repository Structure

```
├── answer_keys/                     # Official answer key PDFs and scraped CSV/JSON keys
├── digitized_answer_keys/           # Standardized JSON representations of official keys
├── combined_qa/                     # Consolidated paper-level questions merged with official keys
├── syllabus/
│   └── cs_2026_syllabus.json        # Canonical GATE 2026 CS/IT & GA syllabus reference
├── dataset/                         # Partitioned dataset, views, and master manifest
│   ├── manifest.json                # Master catalog, summary stats, and lookup index
│   ├── papers/                      # Per-paper directories (ga/cs slices, full_paper.json)
│   └── views/                       # Global faceted views (by_marks, by_type, by_section)
├── pdf_books/                       # Centralized print-ready textbook compendium PDFs
├── docs/
│   └── SPECIFICATIONS_AND_DECISIONS.md  # Comprehensive technical specs & ADRs
├── scripts/                         # Production dataset building, enrichment & PDF scripts
├── output/                          # Ready-to-use parsed JSON papers (2007 - 2026)
│   ├── 2007_CS.json
│   ├── 2008_CS.json
│   ├── ...
│   ├── 2026_CS1.json
│   ├── 2026_CS2.json
│   └── summary_report.json          # Overall extraction report and statistics
├── schema/
│   └── gate_paper_schema.json       # Formal JSON Schema (Draft 2020-12)
├── src/
│   ├── __init__.py
│   ├── schema.py                    # Pydantic models (GatePaper, GateQuestion)
│   ├── pdf_parser.py                # Main parser and pipeline router
│   ├── ocr_parser.py                # Multi-threaded Tesseract OCR engine
│   ├── image_detector.py            # Raster and vector diagram detection
│   └── text_cleaner.py              # Symbol decoding and option extraction
├── tests/
│   └── test_parser.py               # Unit and regression test suite
├── CONTRIBUTING.md                  # Contribution guidelines
├── DISCLAIMER.md                    # Legal disclaimer, fair use and copyright notices
├── LICENSE                          # CC BY 4.0 license text with attribution
├── parse_all.py                     # Batch CLI parser runner
├── pyproject.toml                   # Project packaging configuration
├── pytest.ini                       # Test runner configuration
└── requirements.txt                 # Python dependencies
```

---

## Categorized Dataset, AI Enrichment & Textbook PDFs (2011–2025)

The database includes a multi-dimensional categorized dataset, official syllabus alignment, AI metadata enrichment, and print-ready textbook compendiums:

- **Syllabus Reference**: [syllabus/cs_2026_syllabus.json](syllabus/cs_2026_syllabus.json) contains a hierarchical representation of Sections 1–10 (CS & IT) plus General Aptitude.
- **Categorized Slices**: Each paper under `dataset/papers/<paper_id>/` contains modular category slices (`ga_1_mark.json`, `ga_2_mark.json`, `cs_1_mark.json`, `cs_2_mark.json`) as well as the sequential monolithic `full_paper.json`.
- **Global Faceted Views**: Cross-paper slicing available under `dataset/views/` (by marks, by question type, and by section).
- **Master Query Manifest**: [dataset/manifest.json](dataset/manifest.json) provides fast in-memory indexing of all questions with tags and file pointers.
- **Print-Optimized Textbook Compendiums**: High-resolution monochrome PDFs under `pdf_books/<paper_id>.pdf` designed with a 2-column cover-and-practice layout (left for questions with checkboxes, right for solutions and hints) using standard Times Roman (Liberation Serif).

For the authoritative specification and architecture decisions record, refer to:
- [docs/SPECIFICATIONS_AND_DECISIONS.md](docs/SPECIFICATIONS_AND_DECISIONS.md)

---

## Dataset Schema

Each paper file in `output/<paper_id>.json` conforms to the following structure:

```json
{
  "paper_id": "2026_CS1",
  "year": 2026,
  "subject": "Computer Science and Information Technology",
  "subject_code": "CS",
  "session": "CS1",
  "total_questions_in_paper": 65,
  "extracted_questions_count": 62,
  "omitted_questions_count": 3,
  "questions": [
    {
      "id": "2026_CS1_GA_Q01",
      "question_number": 1,
      "section": "General Aptitude",
      "section_code": "GA",
      "question_type": "MCQ",
      "marks": 1.0,
      "negative_marks": 0.33,
      "question_text": "The antonym of the word protagonist is ________.",
      "options": {
        "A": "agnostic",
        "B": "antagonist",
        "C": "arsonist",
        "D": "anarchist"
      },
      "has_images": false,
      "page_start": 1,
      "page_end": 1
    }
  ]
}
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Tesseract OCR (required only if running OCR extraction on 2007-2011 papers):
  - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
  - macOS: `brew install tesseract`
  - Windows: Install via UB-Mannheim Tesseract installer

### Installation

```bash
# Clone the repository
git clone https://github.com/hul0/gate-pyq-db.git
cd gate-pyq-db

# Set up a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Usage

### 1. Using the Pre-Parsed Dataset

You can directly load and query any JSON paper from `output/` using Python or any programming language:

```python
import json

with open("output/2026_CS1.json", "r", encoding="utf-8") as f:
    paper = json.load(f)

print(f"Paper: {paper['paper_id']}, Questions Extracted: {paper['extracted_questions_count']}")

for q in paper["questions"][:5]:
    print(f"[{q['id']}] ({q['marks']} marks, {q['question_type']}): {q['question_text'][:80]}...")
```

### 2. Running the Parser Pipeline

To run the parser against PDF papers stored in a local directory (e.g., `CS/`):

```bash
# Parse all papers in the CS directory
python3 parse_all.py --dir CS --out output

# Parse a single paper
python3 parse_all.py --file CS/2026_CS1.pdf --out output
```

### 3. Running Tests

```bash
pytest -v
```

---

## License and Attribution

The codebase, JSON schemas, parsing algorithms, and structured dataset formatting in this project are created by **Rupam Ghosh** and licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

Under this license, you are free to share and adapt the material for any purpose, provided appropriate credit is given to Rupam Ghosh. See [LICENSE](LICENSE) for the full license text.

---

## Legal Disclaimer and Fair Use Notice

- **Questions Ownership**: The examination questions, problems, solutions, and official answer keys originate from the Graduate Aptitude Test in Engineering (GATE) examinations, conducted by the Indian Institutes of Technology (IITs) and Indian Institute of Science (IISc) on behalf of the National Coordination Board (NCB) - GATE, Ministry of Education, Government of India.
- **Fair Use / Fair Dealing**: Questions and exam texts are presented for non-commercial educational, academic research, and study purposes under the fair dealing provisions of Section 52 of the Indian Copyright Act, 1957, and applicable international fair use doctrines. No copyright is claimed over the underlying GATE examination questions.
- **Trademarks**: "GATE" and related marks belong to their respective authorities. This project is an independent community initiative and is not endorsed by or affiliated with the GATE organizing institutes or the Government of India.
- For complete details and takedown inquiries, please refer to [DISCLAIMER.md](DISCLAIMER.md).
