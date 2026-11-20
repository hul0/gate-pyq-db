# GATE CS PYQ Database: Architecture & Technical Specifications

> **Status:** Approved Standard  
> **Target Dataset Scope:** GATE CSE Question Papers (2011 – 2025)  
> **Last Updated:** 2026-11-20  

---

## 1. System Overview & Scope

The purpose of this repository is to build and maintain a complete, verified, standardized, and machine-readable database of GATE Computer Science and Information Technology (CS/IT) Previous Year Questions (PYQs) from **2011 to 2025**.

The platform is designed to support:
1. Programmatic access for web applications, mock test engines, and databases.
2. Fast querying and faceting across multiple dimensions (marks, topics, question types, sections).
3. Downstream AI enrichment (automated tagging, short solution hints, and LaTeX formula conversion).
4. Automated generation of high-quality, print-ready, monochrome academic textbook compendiums.

Papers before 2011 are explicitly excluded from this standard.

---

## 2. Directory Hierarchy Standard

The directory structure is strictly maintained as follows:

```text
GATE_CS_PYQ_DB/
├── answer_keys/                          # Official answer key PDFs and raw scraped key sets
├── digitized_answer_keys/                # Standardized JSON representations of official keys
├── combined_qa/                          # Merged questions and verified answers (paper-level)
├── syllabus/
│   └── cs_2026_syllabus.json             # Canonical syllabus reference (CS & IT + General Aptitude)
├── dataset/                              # Primary structured database
│   ├── manifest.json                     # Master catalog, summary statistics, and query lookup index
│   ├── papers/                           # Partitioned per paper set
│   │   └── <paper_id>/                   # e.g., 2025_CS2, 2024_CS1, 2023_CS
│   │       ├── ga_1_mark.json            # General Aptitude 1-mark questions
│   │       ├── ga_2_mark.json            # General Aptitude 2-mark questions
│   │       ├── cs_1_mark.json            # Computer Science 1-mark questions
│   │       ├── cs_2_mark.json            # Computer Science 2-mark questions
│   │       ├── full_paper.json           # Monolithic paper JSON (Q1 to Q65 in official sequence)
│   │       ├── <paper_id>_textbook.tex   # Generated LaTeX source for the compendium
│   │       └── <paper_id>_textbook.pdf   # Compiled print-ready academic textbook PDF
│   ├── views/                            # Global faceted slices across all papers
│   │   ├── by_marks/                     # 1_mark.json, 2_mark.json
│   │   ├── by_type/                      # mcq.json, msq.json, nat.json
│   │   └── by_section/                   # general_aptitude.json, computer_science.json
│   └── categorized/                      # Multi-year combined categorized datasets (2018-2025)
│       ├── subject_wise/                 # 12 core subjects + 7 modular subtopics JSONs
│       ├── question_type_wise/           # mcq.json, msq.json, nat.json
│       ├── difficulty_wise/              # easy.json, medium.json, hard.json
│       └── marks_wise/                   # 1_mark.json, 2_marks.json
├── pdf_books/                            # Centralized repository of all compiled textbook PDFs
│   ├── <paper_id>.pdf                    # Individual exam papers (e.g. 2025_CS2.pdf)
│   ├── subject_wise/                     # Subject-wise compiled textbooks (12 Core + 7 Modules)
│   ├── question_type_wise/               # MCQ, MSQ, NAT compiled textbooks
│   ├── difficulty_wise/                  # Easy, Medium, Hard compiled textbooks
│   └── marks_wise/                       # 1-Mark, 2-Mark compiled textbooks
└── scripts/                              # Production pipeline scripts
    ├── download_answer_keys.py
    ├── digitize_and_merge_keys.py
    ├── build_categorized_dataset.py
    ├── sync_dataset.py
    ├── generate_categorized_textbooks.py
    ├── generate_full_paper_json.py
    └── generate_paper_textbook.py
    ├── enrich_2025_cs2.py
    ├── generate_full_paper_json.py
    └── generate_paper_textbook.py
```

---

## 3. Data Schemas & Invariant Fields

### 3.1 Question Object Schema

Each question object in any category slice, monolithic paper file, or faceted view adheres to the following specification:

| Field Name | Type | Description | Invariants / Constraints |
| :--- | :--- | :--- | :--- |
| `id` | string | Unique question identifier | Format: `<paper_id>_<section_code>_Q<num>` (e.g. `2025_CS2_CS_Q11`) |
| `question_number` | integer | Official question number | Sequential within paper ($1 \le n \le 65$) |
| `category` | string | Section and mark category | Lowercase snake_case: `ga_1_mark`, `ga_2_mark`, `cs_1_mark`, `cs_2_mark` |
| `marks` | float | Assigned positive marks | `1.0` or `2.0` |
| `negative_marks` | float | Penalty for incorrect answer | `0.33` for 1-mark MCQ, `0.66` for 2-mark MCQ; strictly `0.0` for MSQ and NAT |
| `section` | string | Official section name | `"General Aptitude"` or `"Computer Science and Information Technology"` |
| `section_code` | string | Short section code | `"GA"` or `"CS"` |
| `paper_id` | string | Paper set identifier | e.g. `"2025_CS2"`, `"2024_CS1"` |
| `year` | integer | Examination year | $2011 \le \text{year} \le 2025$ |
| `session` | string | Session name | e.g. `"CS1"`, `"CS2"`, `"CS"` |
| `question_type` | string | Question format type | `"MCQ"` (Single choice), `"MSQ"` (Multiple select), `"NAT"` (Numerical) |
| `is_multiple_choice`| boolean | Multiple choice indicator | `true` for MCQ and MSQ; `false` for NAT |
| `has_images` | boolean | Diagram dependency flag | `true` if question relies on image rendering |
| `page_start` | integer | PDF start page | Source PDF page number |
| `page_end` | integer | PDF end page | Source PDF page number |
| `question_text` | string | Raw extracted question text | Original OCR/PDF text baseline |
| `options` | object / null | Raw options dictionary | `{"A": ..., "B": ..., "C": ..., "D": ...}` for MCQ/MSQ; `null` for NAT |
| `answer` | string | Official answer key string | e.g. `"A"`, `"B; C"`, `"13 to 13"` |
| `correct_options` | array / null | Parsed list of correct options| e.g. `["B", "C"]` for MSQ; `null` for NAT |
| `numerical_answer_range` | object / null | Range for numerical answers | `{"min": float, "max": float}` for NAT; `null` for MCQ/MSQ |
| `topic` | string | High-level syllabus module | Aligned to `syllabus/cs_2026_syllabus.json` (e.g. `"Linear Algebra"`) |
| `subtopic` | string | Granular syllabus concept | e.g. `"Matrices and matrix powers"` |
| `difficulty_level` | string | 3-tier difficulty taxonomy | `"Easy"`, `"Medium"`, or `"Hard"` |
| `explaination` | string | Solution guidance / hint | 2–3 sentences with embedded LaTeX math ($...$); formula/principle focus |
| `question_text_latex`| string | LaTeX formatted question | Original text preserved with proper inline LaTeX math ($...$) |
| `options_latex` | object / null | LaTeX formatted options | Options with clean LaTeX formatting and stripped PDF artifacts |
| `tags` | array[string]| Fast filter tags | Facets: year, session, category, type, image status, negative marking |

---

## 4. Architectural Decisions Record (ADR)

### ADR-01: Scope Restriction (2011–2025)
* **Decision:** Exclude papers prior to 2011. Focus exclusively on 2011–2025.
* **Rationale:** GATE format changed substantially prior to 2011 (General Aptitude was introduced in 2010/2011; marking scheme, NAT questions, and computer-based tests standardized from 2014 onwards). Earlier papers have lower structural alignment with current syllabi.

### ADR-02: Partitioning by Section + Marks
* **Decision:** Partition each paper into four canonical files: `ga_1_mark.json`, `ga_2_mark.json`, `cs_1_mark.json`, and `cs_2_mark.json`.
* **Rationale:** GATE questions follow a rigid mark and section structure (5 GA 1-mark, 5 GA 2-mark, 25 CS 1-mark, 30 CS 2-mark). Splitting by Section + Marks provides optimal modularity for targeted study sets and mock generation without over-fragmenting by question type.

### ADR-03: Non-Destructive Dual-Field Architecture for Text
* **Decision:** Retain raw extracted `question_text` and `options` untouched, while introducing `question_text_latex` and `options_latex` for rendered views.
* **Rationale:** Prevents irreversible data corruption or unintended regex errors during automated text transformations. Raw parser output remains intact as a verifiable ground truth.

### ADR-04: Master Manifest and Global Faceted Views
* **Decision:** Maintain synchronized global views (`dataset/views/`) and a lightweight query index inside `dataset/manifest.json`.
* **Rationale:** Enables sub-millisecond multi-paper filtering (e.g., retrieving all MSQs across all years, or all 2-mark Discrete Mathematics questions) without traversing the filesystem or parsing hundreds of individual JSON files.

### ADR-05: Print-Friendly Textbook Format (Cover-and-Practice)
* **Decision:** Format textbook compendiums using a horizontal split on Portrait A4 ($55\%$ left for question and options, $45\%$ right for official key and explanation).
* **Rationale:** 
  1. Allows students to physically cover the right half with a piece of paper or ruler during mock practice.
  2. Embeds checkboxes ($\square$) next to options for direct ticking.
  3. Ensures zero leakage of answers or hints onto the left-hand question panel.

### ADR-06: Zero Color / Monochrome Printing Optimization
* **Decision:** Use 100% monochrome styling (clean white backgrounds, sharp hairline borders at $0.4\,\text{pt}$, zero solid gray or color fills).
* **Rationale:** Maximizes toner and ink efficiency for high-volume student printing, ensuring high contrast on both standard home printers and industrial copy machines.

### ADR-07: Typeface Standard — Variation A (Times Roman / Liberation Serif)
* **Decision:** Standardize on **Times Roman / Liberation Serif** (`\usepackage{fontspec}`, `\setmainfont{Liberation Serif}`) via XeLaTeX.
* **Rationale:** Selected after evaluating 5 textbook variations. Times Roman is the universally recognized standard for academic exam papers and STEM university textbooks (Pearson, McGraw-Hill, Springer), offering maximum readability, compact line length, and sharp mathematical typesetting.

### ADR-08: Copyright, Imprint Page, and Anti-Tampering Watermark Policy
* **Decision:**
  1. **Intellectual Property Ownership:** All software, taxonomy, categorized datasets, LaTeX formatting, hints, and PDF compendiums are the proprietary copyright of **Rupam Ghosh** and **Studiva** ([www.studiva.co.in](https://www.studiva.co.in)), licensed under a Proprietary Educational License.
  2. **Dedicated Imprint Page (Page 1):** Every generated textbook PDF must begin with a dedicated Imprint & Copyright Page setting out title details, author/publisher identity (Rupam Ghosh & Studiva, `contact@studiva.co.in`), terms of use, mandatory attribution requirements, commercial use prohibition, and fair use disclaimer. Problem content starts strictly on Page 2.
  3. **Unremovable Background Watermark:** Every single page must feature the transparent Studiva butterfly icon (`assets/studiva_butterfly_icon_transparent.png`, width $8\,\text{cm}$, opacity $12\%$) with `www.studiva.co.in` underneath, embedded directly into the page content stream using `\AddToShipoutPictureBG` and `tikz`. The watermark must be integrated into the page graphics stream rather than an optional PDF layer/OCG to prevent programmatic layer stripping.
  4. **Running Footer Attribution:** Every page must include running footer attribution: `Copyright © 2026 Studiva™` on the left and Studiva logo + `www.studiva.co.in` on the right.
* **Rationale:** Protects author and organizational intellectual property across public distributions and prints while maintaining student educational access and preventing uncredited scraping.

---

## 5. Tooling & Automation Pipeline

The repository provides automated scripts under `scripts/`:

| Script | Purpose |
| :--- | :--- |
| [scripts/download_answer_keys.py](file:///home/johan/GATE/GATE_CS_PYQ_DB/scripts/download_answer_keys.py) | Downloads official GATE answer key PDFs and HTML tables (2011–2025). |
| [scripts/digitize_and_merge_keys.py](file:///home/johan/GATE/GATE_CS_PYQ_DB/scripts/digitize_and_merge_keys.py) | Digitizes answer keys into JSON and merges them with extracted questions in `combined_qa/`. |
| [scripts/build_categorized_dataset.py](file:///home/johan/GATE/GATE_CS_PYQ_DB/scripts/build_categorized_dataset.py) | Builds `dataset/papers/` and `dataset/views/` from `combined_qa/`. |
| [scripts/enrich_2025_cs2.py](file:///home/johan/GATE/GATE_CS_PYQ_DB/scripts/enrich_2025_cs2.py) | Populates syllabus topics, difficulty levels, LaTeX hints, and formatted text for 2025 CS2. |
| [scripts/sync_dataset.py](file:///home/johan/GATE/GATE_CS_PYQ_DB/scripts/sync_dataset.py) | Synchronizes `dataset/views/` and `dataset/manifest.json` from the paper files. |
| [scripts/generate_full_paper_json.py](file:///home/johan/GATE/GATE_CS_PYQ_DB/scripts/generate_full_paper_json.py) | Combines category files into sequential monolithic `full_paper.json`. |
| [scripts/generate_paper_textbook.py](file:///home/johan/GATE/GATE_CS_PYQ_DB/scripts/generate_paper_textbook.py) | Compiles print-optimized side-by-side textbook PDFs via XeLaTeX. |

---

## 6. Protocols for Future Modifications

To maintain dataset integrity, any future changes must adhere to these rules:
1. **Never alter schema field names** without updating this specification and all parsing/sync scripts.
2. **Never overwrite raw text:** Always store edited/LaTeX representations in `_latex` fields.
3. **Keep `manifest.json` in sync:** Run `scripts/sync_dataset.py` whenever paper question JSONs are edited or enriched.
4. **Preserve print standards:** Textbook PDF generation must remain strictly monochrome, maintaining the side-by-side cover-and-practice layout and Variation A font.

