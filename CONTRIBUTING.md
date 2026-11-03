# Contributing to GATE CS PYQ Database

Thank you for your interest in contributing to `gate-pyq-db`. This document provides guidelines for reporting issues, contributing code, and improving the question dataset.

---

## Code of Conduct and Principles

- Maintain respect, professionalism, and clarity in all discussions.
- Avoid introducing proprietary third-party text or closed-source assets.
- Never include images, diagrams, or copyright-sensitive figure extracts in the dataset files. All extracted questions must strictly omit questions requiring visual figures or diagrams (`has_images: false`).

---

## Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/hul0/gate-pyq-db.git
   cd gate-pyq-db
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install system dependencies (for OCR parsing):
   - Linux (Ubuntu/Debian):
     ```bash
     sudo apt-get install tesseract-ocr
     ```
   - macOS:
     ```bash
     brew install tesseract
     ```

---

## Running Tests

All test cases are defined in `tests/`. Verify that tests pass before submitting changes:

```bash
pytest -v
```

To run unit tests quickly without requiring sample PDF files:
```bash
pytest -v -k "not test_parser_sample_paper and not test_ocr_parser_image_paper"
```

---

## Schema Consistency Guidelines

All question papers in `output/` must strictly validate against `schema/gate_paper_schema.json`.

Key schema constraints:
- `has_images` must always be `false`. Questions with diagrams or visual options must be omitted and counted under `omitted_questions_count`.
- `question_type` must be one of `MCQ`, `MSQ`, or `NAT`.
- `marks` must be either `1.0` or `2.0`.
- All text should be cleaned of exam boilerplate, watermarks, and raw Symbol font artifacts.

---

## Submitting Pull Requests

1. Create a descriptive feature branch:
   ```bash
   git checkout -b feature/improved-cleaner
   ```
2. Commit your changes with clear, concise commit messages.
3. Push your branch to GitHub and open a Pull Request against `main`.
4. Provide a detailed description of what your PR changes and why.

