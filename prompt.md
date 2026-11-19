# Agent Prompt & Instruction Guide for Generating Paper Sets

Use this prompt to process and generate any subsequent GATE CSE paper set (e.g., `2025_CS1`, `2024_CS1`, `2024_CS2`, etc.).

---

## 1. Copyable Task Prompt

```text
Process and generate the complete dataset, AI enrichment, monolithic JSON, and textbook PDF for the paper set: <PAPER_ID> (e.g., 2025_CS1).

Adhere strictly to the architecture and standards defined in docs/SPECIFICATIONS_AND_DECISIONS.md:

1. REFERENCE SYLLABUS:
   Use syllabus/cs_2026_syllabus.json as the authoritative reference for all topics and subtopics.

2. AI METADATA ENRICHMENT:
   For every question in dataset/papers/<PAPER_ID>/ (ga_1_mark.json, ga_2_mark.json, cs_1_mark.json, cs_2_mark.json), populate:
   - "topic": Canonical syllabus module from Section 1-10 or GA (e.g., "Linear Algebra", "Computer Networks", "Operating System", "Verbal Aptitude").
   - "subtopic": Granular concept from the syllabus (e.g., "Matrices and determinants", "CPU and I/O scheduling: SRTF").
   - "difficulty_level": Calibrated on a 3-tier scale: "Easy" | "Medium" | "Hard".
   - "explaination": Concise 2-3 sentence hint with embedded LaTeX formulas ($...$), focusing on core formulas, theorems, and solution guidance.
   - "question_text_latex": Non-destructive LaTeX formatted version of question_text ($...$ for variables, formulas, and code).
   - "options_latex": Non-destructive LaTeX formatted options dictionary with PDF footers stripped.

3. DATASET SYNCHRONIZATION:
   Run `python3 scripts/sync_dataset.py` to synchronize dataset/views/ and dataset/manifest.json with the enriched fields.

4. MONOLITHIC JSON GENERATION:
   Run `python3 scripts/generate_full_paper_json.py <PAPER_ID>` to generate dataset/papers/<PAPER_ID>/full_paper.json containing all questions ordered sequentially (Q1 to Q65).

5. TEXTBOOK PDF GENERATION:
   Run `python3 scripts/generate_paper_textbook.py <PAPER_ID>` to compile the print-ready textbook compendium:
   - Typeface: Variation A (Times Roman / Liberation Serif via fontspec).
   - Layout: Frameless side-by-side design (55% question on left, 45% solution on right) separated by an explicit TikZ underlay dashed vertical divider (black!80, 0.8pt, dash pattern=on 4pt off 3pt).
   - Alignment: Laser-aligned checkboxes using fixed-width tabular grids.
   - Page 1 Imprint: Dedicated book copyright page with Studiva logo, Rupam Ghosh & Studiva metadata, terms of use, and fair use disclaimer.
   - Watermark: Persistent unremovable canvas background watermark (Studiva butterfly logo + www.studiva.co.in at 12% opacity) on every page.
   - Output locations: dataset/papers/<PAPER_ID>/<PAPER_ID>_textbook.pdf and pdf_books/<PAPER_ID>.pdf.

6. VERIFICATION & COMMIT:
   - Verify that all questions are processed without syntax or LaTeX errors.
   - Verify that the PDF compiles cleanly with XeLaTeX.
   - Commit changes with conventional commit: "feat: add AI enrichment, monolithic JSON, and textbook PDF for <PAPER_ID>".
```

---

## 2. Pipeline Execution Sequence

Execute the following commands in order for `<PAPER_ID>`:

```bash
# Step 1: Run the AI enrichment script for the paper
python3 scripts/enrich_<PAPER_ID>.py

# Step 2: Synchronize manifest.json and global views
python3 scripts/sync_dataset.py

# Step 3: Build the sequential monolithic JSON
python3 scripts/generate_full_paper_json.py <PAPER_ID>

# Step 4: Compile the print-ready textbook PDF
python3 scripts/generate_paper_textbook.py <PAPER_ID>

# Step 5: Verify the compiled PDF
pdfinfo dataset/papers/<PAPER_ID>/<PAPER_ID>_textbook.pdf
pdftotext -f 1 -l 2 dataset/papers/<PAPER_ID>/<PAPER_ID>_textbook.pdf - | head -n 45
```

---

## 3. Invariants & Rules Checklist

Before committing any paper set, verify the following contracts:
- [ ] **Dual-Field Architecture:** Never overwrite raw `question_text` or `options`. Only write LaTeX representations to `question_text_latex` and `options_latex`.
- [ ] **Negative Marking Invariant:** `negative_marks` must strictly be `0.0` for all MSQ and NAT questions (`0.33` for 1-mark MCQ, `0.66` for 2-mark MCQ).
- [ ] **Dashed Vertical Divider:** The vertical divider between questions and solutions must be explicitly drawn via `underlay` with `black!80`, `0.8pt`, and `dash pattern=on 4pt off 3pt` (do not rely on `segmentation style` with `blanker`).
- [ ] **Transparent Background:** Boxes must retain `blanker` and `opacityback=0` so the watermark remains visible through every question.
- [ ] **Option Checkbox Alignment:** Checkboxes must strictly use fixed-width `tabular` columns (`p{0.48\linewidth}` or `p{0.98\linewidth}`) to guarantee straight alignment.
- [ ] **Page 1 Imprint:** Every PDF must feature the standalone copyright imprint on Page 1 before questions begin on Page 2.
- [ ] **No Emojis:** Never use emojis in code, LaTeX source, commit messages, or documentation.

