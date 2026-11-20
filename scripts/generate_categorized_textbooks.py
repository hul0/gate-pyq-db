#!/usr/bin/env python3
"""
generate_categorized_textbooks.py

Generates categorized Question Bank with Solutions textbook PDFs and JSON datasets
for GATE CS/IT from combined 2018-2025 examination data:
1. Subject Wise (12 Core Subjects + Modular Subtopics)
2. Question Type Wise (MCQ, MSQ, NAT)
3. Difficulty Wise (Easy, Medium, Hard)
4. Marks Wise (1 Mark, 2 Marks)

Output Directories:
- PDFs:
    pdf_books/subject_wise/
    pdf_books/question_type_wise/
    pdf_books/difficulty_wise/
    pdf_books/marks_wise/
- JSONs:
    dataset/categorized/subject_wise/
    dataset/categorized/question_type_wise/
    dataset/categorized/difficulty_wise/
    dataset/categorized/marks_wise/
"""

import os
import sys
import copy
import json
import re
import shutil
import subprocess
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed

# Standard Subject Order for GATE CS
SUBJECT_ORDER = [
    "General Aptitude",
    "Engineering Mathematics",
    "Discrete Mathematics",
    "Digital Logic",
    "Computer Organization and Architecture",
    "Programming and Data Structures",
    "Algorithms",
    "Theory of Computation",
    "Compiler Design",
    "Operating Systems",
    "Databases",
    "Computer Networks"
]

GA_SUBTOPIC_ORDER = [
    "Quantitative Aptitude",
    "Verbal Aptitude",
    "Analytical Aptitude",
    "Spatial Aptitude"
]

EM_SUBTOPIC_ORDER = [
    "Linear Algebra",
    "Calculus",
    "Probability and Statistics",
    "Engineering Mathematics"
]

def escape_latex_outside_math(text):
    if not text:
        return ""
    math_pattern = r'(\$\$.*?\$\$|\$.*?\$|\\begin\{[a-zA-Z*]+\}.*?\\end\{[a-zA-Z*]+\})'
    parts = re.split(math_pattern, text, flags=re.DOTALL)
    escaped_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            escaped_parts.append(part)
        else:
            p = part
            p = re.sub(r'(?<!\\)&', r'\&', p)
            p = re.sub(r'(?<!\\)%', r'\%', p)
            p = re.sub(r'(?<!\\)#', r'\#', p)
            p = re.sub(r'(?<!\\)_', r'\_', p)
            escaped_parts.append(p)
    return "".join(escaped_parts)

def format_latex_table(table_lines):
    if len(table_lines) < 2:
        return "\n".join(table_lines)
    rows = []
    alignments = []
    for idx, l in enumerate(table_lines):
        cells = [c.strip() for c in l.strip("|").split("|")]
        if idx == 1 and all(set(c).issubset({'-', ':', ' '}) for c in cells):
            for c in cells:
                if c.startswith(":") and c.endswith(":"):
                    alignments.append("c")
                elif c.endswith(":"):
                    alignments.append("r")
                else:
                    alignments.append("l")
            continue
        rows.append(cells)
    if not rows:
        return ""
    num_cols = max(len(r) for r in rows)
    if len(alignments) < num_cols:
        alignments = ["l"] * num_cols
    col_spec = "".join(alignments)
    out = ["\\begin{center}\\small", f"\\begin{{tabular}}{{{col_spec}}}", "\\toprule"]
    header_cells = rows[0]
    out.append(" & ".join(header_cells) + " \\\\")
    out.append("\\midrule")
    for r in rows[1:]:
        out.append(" & ".join(r) + " \\\\")
    out.append("\\bottomrule")
    out.append("\\end{tabular}\\end{center}")
    return "\n".join(out)

def convert_markdown_tables_to_latex(text):
    lines = text.split("\n")
    new_lines = []
    table_lines = []
    in_table = False
    for line in lines:
        sline = line.strip()
        if sline.startswith("|") and sline.endswith("|"):
            in_table = True
            table_lines.append(sline)
        else:
            if in_table:
                table_tex = format_latex_table(table_lines)
                new_lines.append(table_tex)
                table_lines = []
                in_table = False
            new_lines.append(line)
    if in_table and table_lines:
        table_tex = format_latex_table(table_lines)
        new_lines.append(table_tex)
    return "\n".join(new_lines)

def convert_code_blocks_to_latex(text):
    code_pattern = r'```(?:c|C|cpp)?\s*\n(.*?)\n```'
    def replacer(m):
        code_content = m.group(1)
        return (
            "\\begin{lstlisting}[language=C, basicstyle=\\footnotesize\\ttfamily, "
            "frame=single, rulecolor=\\color{black!30}, tabsize=2, breaklines=true]\n"
            + code_content + "\n\\end{lstlisting}"
        )
    return re.sub(code_pattern, replacer, text, flags=re.DOTALL)

def format_question_body(q):
    text = q.get("question_text_latex") or q.get("question_text", "")
    text = re.sub(r'Organising Institute:.*', '', text)
    text = re.sub(r'Organizing Institute:.*', '', text)
    code_parts = re.split(r'(```(?:c|C|cpp)?\s*\n.*?\n```)', text, flags=re.DOTALL)
    processed_parts = []
    for idx, cp in enumerate(code_parts):
        if idx % 2 == 1:
            processed_parts.append(convert_code_blocks_to_latex(cp))
        else:
            t = convert_markdown_tables_to_latex(cp)
            t = escape_latex_outside_math(t)
            t = t.replace("\n\n", "\n\\par\\medskip\n")
            processed_parts.append(t)
    return "".join(processed_parts)

def format_options(q):
    options = q.get("options_latex") or q.get("options")
    if not options or not isinstance(options, dict):
        return "\\par\\vspace{6pt}\\noindent\\textbf{Your Answer:} \\fbox{\\rule{0pt}{1.3ex}\\hspace{3cm}}"

    clean_opts = {}
    for opt_key in ["A", "B", "C", "D"]:
        if opt_key in options:
            val = options[opt_key]
            val = re.sub(r'Organising Institute:.*', '', str(val)).strip()
            val = re.sub(r'Organizing Institute:.*', '', val).strip()
            val = escape_latex_outside_math(val)
            val = val.replace("\n", r" \newline ")
            clean_opts[opt_key] = val

    if not clean_opts:
        return ""

    is_short_2col = (
        len(clean_opts) == 4
        and all(len(v) < 32 for v in clean_opts.values())
        and all(r"\newline" not in v for v in clean_opts.values())
    )

    if is_short_2col:
        a, b = clean_opts["A"], clean_opts["B"]
        c, d = clean_opts["C"], clean_opts["D"]
        return (
            "\\par\\vspace{6pt}\\noindent\n"
            "\\begin{tabular}{@{}p{0.48\\linewidth}@{\\hspace{0.04\\linewidth}}p{0.48\\linewidth}@{}}\n"
            f"$\\square$\\ \\textbf{{(A)}} {a} & $\\square$\\ \\textbf{{(B)}} {b} \\\\\n"
            f"\\addlinespace[3pt]\n"
            f"$\\square$\\ \\textbf{{(C)}} {c} & $\\square$\\ \\textbf{{(D)}} {d}\n"
            "\\end{tabular}"
        )
    else:
        rows = []
        for k in ["A", "B", "C", "D"]:
            if k in clean_opts:
                rows.append(f"$\\square$\\ \\textbf{{({k})}} {clean_opts[k]}")
        rows_tex = " \\\\\n\\addlinespace[3pt]\n".join(rows)
        return (
            "\\par\\vspace{6pt}\\noindent\n"
            "\\begin{tabular}{@{}p{0.98\\linewidth}@{}}\n"
            f"{rows_tex}\n"
            "\\end{tabular}"
        )

def format_solution_panel(q):
    ans = q.get("answer", "").strip()
    topic = q.get("topic") or "General"
    subtopic = q.get("subtopic") or ""
    diff = q.get("difficulty_level") or "Standard"
    expl = q.get("explaination") or ""

    topic = escape_latex_outside_math(topic)
    subtopic = escape_latex_outside_math(subtopic)
    expl = escape_latex_outside_math(expl)
    expl = expl.replace("\n\n", "\n\\par\\smallskip\n")

    lines = [
        f"\\textbf{{Official Key:}} \\textbf{{\\large {ans}}} \\hfill \\textit{{\\small [{diff}]}}",
        "\\vspace{2pt}\\hrule height 0.3pt\\vspace{3pt}",
        f"\\textbf{{Topic:}} {topic} \\\\",
        f"\\textbf{{Subtopic:}} \\textit{{{subtopic}}}" if subtopic else "",
        "\\vspace{2pt}\\hrule height 0.3pt\\vspace{3pt}",
        "\\textbf{Guide / Hint:} \\\\",
        f"{{\\small {expl}}}" if expl else "\\textit{\\footnotesize [Hint to be added]}"
    ]
    return "\n".join([l for l in lines if l])

def generate_book_latex(category_name, subcategory_title, questions, abs_logo_path):
    logo_path_latex = abs_logo_path.replace("\\", "/")
    total_qs = len(questions)

    tex = [
        r"""\documentclass[a4paper,10pt]{article}
\usepackage{amsmath,amssymb}
\usepackage{fontspec}
\setmainfont{Liberation Serif}
\usepackage{graphicx}
\usepackage{eso-pic}
\usepackage{tikz}
\usepackage[most]{tcolorbox}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{lastpage}
\usepackage{booktabs}
\usepackage{listings}
\usepackage{enumitem}
\usepackage{microtype}

\geometry{
    a4paper,
    top=1.5cm,
    bottom=1.8cm,
    left=1.2cm,
    right=1.2cm
}

% Persistent Unremovable Canvas Watermark on Every Page
\newsavebox{\watermarkbox}
\sbox{\watermarkbox}{%
    \begin{tabular}{c}
        \includegraphics[width=8cm]{""" + logo_path_latex + r"""} \\[-0.5em]
        {\fontsize{18}{22}\selectfont\bfseries\scshape www.studiva.co.in}
    \end{tabular}%
}
\AddToShipoutPictureBG{%
    \begin{tikzpicture}[remember picture, overlay]
        \node[opacity=0.12] at (current page.center) {\usebox{\watermarkbox}};
    \end{tikzpicture}%
}

% Header and Footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\scshape GATE 2018--2025 CS/IT $\cdot$ \textbf{""" + escape_latex_outside_math(subcategory_title) + r"""}}
\fancyhead[R]{\small\scshape Practice Question Bank with Solutions}
\fancyfoot[L]{\scriptsize\textsc{Copyright \copyright\ 2026} Studiva\textsuperscript{TM}}
\fancyfoot[C]{\small Page \thepage\ of \pageref{LastPage}}
\fancyfoot[R]{\scriptsize\texttt{www.studiva.co.in}}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}

% Code Listing Style (Monochrome)
\lstset{
    basicstyle=\footnotesize\ttfamily,
    numbers=none,
    frame=none,
    tabsize=2,
    breaklines=true,
    showstringspaces=false
}

\begin{document}

% ==================== PAGE 1: IMPRINT & TITLE PAGE ====================
\thispagestyle{empty}
\vspace*{0.5cm}
\begin{center}
    \includegraphics[width=2.5cm]{""" + logo_path_latex + r"""}\\[0.6em]
    {\LARGE \textbf{GATE 2018--2025 COMPUTER SCIENCE \& IT}}\\[0.3em]
    {\Large \textbf{PREVIOUS YEAR QUESTION BANK WITH SOLUTIONS}}\\[0.4em]
    {\large \textsc{\textbf{""" + escape_latex_outside_math(category_name) + r""": """ + escape_latex_outside_math(subcategory_title) + r"""}}}\\[0.2em]
    {\normalsize \textsc{Combined 2018--2025 Examination Papers $\cdot$ Comprehensive Edition ($\mathbf{""" + str(total_qs) + r"""}$ Questions)}}\\[1.2em]
    \rule{0.6\textwidth}{0.6pt}
\end{center}

\vspace{1em}
\noindent\begin{tabular}{ll}
\textbf{Author / Compiler:} & Rupam Ghosh \\
\textbf{Publisher \& Platform:} & Studiva\textsuperscript{TM} (\texttt{www.studiva.co.in}) \\
\textbf{Official Inquiries:} & \texttt{contact@studiva.co.in} \\
\textbf{Edition:} & First Standard Edition (2026) \\
\textbf{Coverage:} & Complete GATE CS/IT Papers (2018, 2022, 2023, 2024 CS1, 2024 CS2, 2025 CS1, 2025 CS2) \\
\textbf{Syllabus Reference:} & Official GATE 2026 Syllabus (Organizing Institute: IIT Guwahati) \\
\end{tabular}

\vspace{1.5em}
\begin{tcolorbox}[enhanced, standard jigsaw, opacityback=0, colframe=black!40, arc=1mm, boxrule=0.5pt, left=10pt, right=10pt, top=8pt, bottom=8pt]
\textbf{\large COPYRIGHT \& INTELLECTUAL PROPERTY NOTICE}\\[0.6em]
Copyright \copyright\ 2026 Rupam Ghosh \& Studiva\textsuperscript{TM}. All Rights Reserved.\\[0.5em]
This educational compilation, problem organization, taxonomy classification, LaTeX typesetting, hints, and explanatory solutions are the proprietary intellectual property of \textbf{Rupam Ghosh} and \textbf{Studiva\textsuperscript{TM}}.\\[0.6em]
\textbf{Terms of Use \& Attribution Rules:}
\begin{itemize}[leftmargin=*, nosep]
    \item \textbf{Personal Educational Use:} Permitted freely for individual students and educators preparing for competitive examinations.
    \item \textbf{Mandatory Attribution:} Any reproduction, republication, hosting, or sharing (digital or physical) must prominently credit \textbf{Rupam Ghosh \& Studiva\textsuperscript{TM}} and include an active, direct link to \texttt{https://www.studiva.co.in}.
    \item \textbf{Commercial Restrictions:} Commercial resale, sublicensing, course bundling, or inclusion in paid test series without prior written permission is strictly prohibited.
    \item \textbf{Anti-Tampering Notice:} Removing, altering, or obscuring copyright notices, page watermarks, or website links from this document is strictly prohibited.
\end{itemize}
\vspace{0.6em}
\textbf{Fair Use Disclaimer:}\\
The underlying examination questions originate from the Graduate Aptitude Test in Engineering (GATE), conducted by the Indian Institutes of Technology (IITs) and Indian Institute of Science (IISc). Question texts are reproduced for non-commercial educational study under Fair Use doctrines. No copyright is claimed over the original GATE examination question texts.
\end{tcolorbox}

\vspace{1.2em}
\begin{center}
\small\itshape
Practice Recommendation: Use an opaque sheet of paper or ruler to cover the right-hand column during mock attempts. Tick your chosen answers directly in the check boxes on the left, then slide the cover to check the solution and hint.
\end{center}

\newpage
% ==================== PAGE 2 ONWARDS: QUESTION BANK ====================
"""
    ]

    current_group = None
    for idx, q in enumerate(questions, 1):
        group_heading = q.get("_group_heading")
        if group_heading and group_heading != current_group:
            current_group = group_heading
            tex.append(f"\\vspace{{8pt}}\n\\subsection*{{{escape_latex_outside_math(current_group)}}}\n\\vspace{{-4pt}}")

        q_type = q.get("question_type", "MCQ")
        marks = q.get("marks", 1.0)
        neg = q.get("negative_marks", 0.0)
        qid = q.get("id", "")
        paper_id = q.get("paper_id", "")
        clean_paper = paper_id.replace("_", " ")

        q_body = format_question_body(q)
        q_options = format_options(q)
        sol_panel = format_solution_panel(q)

        neg_text = f"Neg: {neg:.2f}" if neg > 0 else "No Neg"
        clean_qid = qid.replace("_", r"\_")

        box_header = (
            "\\textbf{Q.%d} \\quad {\\footnotesize\\textsc{[%s $\\cdot$ %.0f Mark(s) $\\cdot$ %s]}} \\hfill {\\footnotesize\\textbf{GATE %s} \\quad \\tiny\\texttt{%s}}"
            % (idx, q_type, marks, neg_text, clean_paper, clean_qid)
        )

        box_tex = "\n".join([
            r"\noindent",
            r"\begin{tcolorbox}[",
            r"    blanker,",
            r"    sidebyside,",
            r"    sidebyside align=top,",
            r"    lefthand width=0.55\textwidth,",
            r"    top=4pt, bottom=4pt, left=0pt, right=0pt,",
            r"    middle=16pt,",
            r"    underlay={",
            r"        \draw[dashed, black!80, line width=0.8pt, dash pattern=on 4pt off 3pt]",
            r"            ([xshift=0.55\textwidth+8pt]frame.north west) --",
            r"            ([xshift=0.55\textwidth+8pt]frame.south west);",
            r"    }",
            r"]",
            box_header,
            r"\vspace{2pt}\hrule height 0.3pt\vspace{4pt}",
            "",
            q_body,
            "",
            q_options,
            "",
            r"\tcblower",
            "",
            sol_panel,
            "",
            r"\end{tcolorbox}",
            r"\vspace{6pt}\hrule height 0.35pt\vspace{6pt}"
        ])
        tex.append(box_tex)

    tex.append(r"\end{document}")
    return "\n".join(tex)

def compile_pdf(tex_path, output_dir, file_basename):
    pdf_path = os.path.join(output_dir, f"{file_basename}.pdf")
    cmd = ["xelatex", "-interaction=nonstopmode", f"{file_basename}.tex"]
    subprocess.run(cmd, cwd=output_dir, capture_output=True, text=True)
    res2 = subprocess.run(cmd, cwd=output_dir, capture_output=True, text=True)

    if os.path.exists(pdf_path):
        for ext in [".aux", ".log", ".out"]:
            aux_file = os.path.join(output_dir, f"{file_basename}{ext}")
            if os.path.exists(aux_file):
                try:
                    os.remove(aux_file)
                except Exception:
                    pass
        print(f"OK: {pdf_path}")
        return True
    else:
        print(f"FAILED: {pdf_path}")
        print(res2.stdout[-1000:])
        return False

def compile_task(args):
    tex_path, output_dir, file_basename = args
    return compile_pdf(tex_path, output_dir, file_basename)

def load_all_2018_2025_questions(root_dir):
    papers = ["2018_CS", "2022_CS", "2023_CS", "2024_CS1", "2024_CS2", "2025_CS1", "2025_CS2"]
    all_questions = []
    for p in papers:
        fpath = os.path.join(root_dir, "dataset", "papers", p, "full_paper.json")
        if not os.path.exists(fpath):
            raise FileNotFoundError(f"Missing {fpath}")
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            for q in data.get("questions", []):
                q["paper_id"] = p
                all_questions.append(q)
    return all_questions

def get_canonical_subject(topic):
    t = (topic or "").strip()
    if t in ["Verbal Aptitude", "Quantitative Aptitude", "Analytical Aptitude", "Spatial Aptitude"]:
        return "General Aptitude"
    if t in ["Linear Algebra", "Calculus", "Probability and Statistics", "Engineering Mathematics"]:
        return "Engineering Mathematics"
    if t == "Operating System":
        return "Operating Systems"
    return t

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    abs_logo_path = os.path.join(root_dir, "assets", "studiva-butterfly-icon.jpg")
    assert os.path.exists(abs_logo_path), f"Logo not found: {abs_logo_path}"

    raw_questions = load_all_2018_2025_questions(root_dir)
    print(f"Loaded {len(raw_questions)} questions from 2018-2025 papers.")

    # Base directories
    pdf_base = os.path.join(root_dir, "pdf_books")
    json_base = os.path.join(root_dir, "dataset", "categorized")

    categories = {
        "subject_wise": {
            "pdf_dir": os.path.join(pdf_base, "subject_wise"),
            "json_dir": os.path.join(json_base, "subject_wise")
        },
        "question_type_wise": {
            "pdf_dir": os.path.join(pdf_base, "question_type_wise"),
            "json_dir": os.path.join(json_base, "question_type_wise")
        },
        "difficulty_wise": {
            "pdf_dir": os.path.join(pdf_base, "difficulty_wise"),
            "json_dir": os.path.join(json_base, "difficulty_wise")
        },
        "marks_wise": {
            "pdf_dir": os.path.join(pdf_base, "marks_wise"),
            "json_dir": os.path.join(json_base, "marks_wise")
        }
    }

    for cat in categories.values():
        os.makedirs(cat["pdf_dir"], exist_ok=True)
        os.makedirs(cat["json_dir"], exist_ok=True)

    # Setup symlinks for aliases
    for alias in ["type_wise", "question_topic_wise"]:
        alias_path = os.path.join(pdf_base, alias)
        if not os.path.exists(alias_path):
            try:
                os.symlink("question_type_wise", alias_path)
            except Exception:
                pass

    book_configs = []

    # ==================== 1. SUBJECT WISE ====================
    subject_groups = defaultdict(list)
    for q in raw_questions:
        subj = get_canonical_subject(q.get("topic"))
        subject_groups[subj].append(copy.deepcopy(q))

    for subj, qlist in subject_groups.items():
        if subj == "General Aptitude":
            def ga_sort_key(x):
                top = x.get("topic", "")
                top_idx = GA_SUBTOPIC_ORDER.index(top) if top in GA_SUBTOPIC_ORDER else 99
                return (top_idx, x.get("year", 0), x.get("session", ""), x.get("question_number", 0))
            qlist.sort(key=ga_sort_key)
            for q in qlist:
                q["_group_heading"] = q.get("topic")
        elif subj == "Engineering Mathematics":
            def em_sort_key(x):
                top = x.get("topic", "")
                top_idx = EM_SUBTOPIC_ORDER.index(top) if top in EM_SUBTOPIC_ORDER else 99
                return (top_idx, x.get("year", 0), x.get("session", ""), x.get("question_number", 0))
            qlist.sort(key=em_sort_key)
            for q in qlist:
                q["_group_heading"] = q.get("topic")
        else:
            qlist.sort(key=lambda x: (x.get("year", 0), x.get("session", ""), x.get("question_number", 0)))
            for q in qlist:
                q["_group_heading"] = None

        file_slug = subj.lower().replace(" ", "_").replace("&", "and")
        book_configs.append({
            "category": "Subject Wise",
            "title": subj,
            "filename": file_slug,
            "pdf_dir": categories["subject_wise"]["pdf_dir"],
            "json_dir": categories["subject_wise"]["json_dir"],
            "questions": qlist
        })

    # Modular subtopics for GA and Engineering Math
    modular_subtopics = [
        "Quantitative Aptitude",
        "Verbal Aptitude",
        "Spatial Aptitude",
        "Analytical Aptitude",
        "Linear Algebra",
        "Calculus",
        "Probability and Statistics"
    ]
    for m in modular_subtopics:
        m_qs = [copy.deepcopy(q) for q in raw_questions if q.get("topic") == m]
        if m_qs:
            m_qs.sort(key=lambda x: (x.get("year", 0), x.get("session", ""), x.get("question_number", 0)))
            for q in m_qs:
                q["_group_heading"] = None
            file_slug = m.lower().replace(" ", "_").replace("&", "and")
            book_configs.append({
                "category": "Subject Wise (Modular)",
                "title": m,
                "filename": file_slug,
                "pdf_dir": categories["subject_wise"]["pdf_dir"],
                "json_dir": categories["subject_wise"]["json_dir"],
                "questions": m_qs
            })

    # ==================== 2. QUESTION TYPE WISE (MCQ, MSQ, NAT) ====================
    type_groups = {"MCQ": [], "MSQ": [], "NAT": []}
    for q in raw_questions:
        qt = q.get("question_type", "MCQ")
        if qt in type_groups:
            type_groups[qt].append(copy.deepcopy(q))

    type_titles = {
        "MCQ": "Multiple Choice Questions (MCQ)",
        "MSQ": "Multiple Select Questions (MSQ)",
        "NAT": "Numerical Answer Type (NAT)"
    }

    for qt, qlist in type_groups.items():
        def type_sort_key(x):
            subj = get_canonical_subject(x.get("topic"))
            subj_idx = SUBJECT_ORDER.index(subj) if subj in SUBJECT_ORDER else 99
            return (subj_idx, x.get("year", 0), x.get("session", ""), x.get("question_number", 0))

        qlist.sort(key=type_sort_key)
        for q in qlist:
            q["_group_heading"] = get_canonical_subject(q.get("topic"))

        file_slug = qt.lower()
        book_configs.append({
            "category": "Question Type Wise",
            "title": type_titles[qt],
            "filename": file_slug,
            "pdf_dir": categories["question_type_wise"]["pdf_dir"],
            "json_dir": categories["question_type_wise"]["json_dir"],
            "questions": qlist
        })

    # ==================== 3. DIFFICULTY WISE ====================
    diff_groups = {"Easy": [], "Medium": [], "Hard": []}
    for q in raw_questions:
        d = q.get("difficulty_level", "Medium")
        if d in diff_groups:
            diff_groups[d].append(copy.deepcopy(q))
        else:
            diff_groups["Medium"].append(copy.deepcopy(q))

    for diff, qlist in diff_groups.items():
        def diff_sort_key(x):
            subj = get_canonical_subject(x.get("topic"))
            subj_idx = SUBJECT_ORDER.index(subj) if subj in SUBJECT_ORDER else 99
            return (subj_idx, x.get("year", 0), x.get("session", ""), x.get("question_number", 0))

        qlist.sort(key=diff_sort_key)
        for q in qlist:
            q["_group_heading"] = get_canonical_subject(q.get("topic"))

        file_slug = diff.lower()
        book_configs.append({
            "category": "Difficulty Wise",
            "title": f"{diff} Questions",
            "filename": file_slug,
            "pdf_dir": categories["difficulty_wise"]["pdf_dir"],
            "json_dir": categories["difficulty_wise"]["json_dir"],
            "questions": qlist
        })

    # ==================== 4. MARKS WISE ====================
    marks_groups = {
        "1_mark": [copy.deepcopy(q) for q in raw_questions if round(q.get("marks", 1.0)) == 1],
        "2_marks": [copy.deepcopy(q) for q in raw_questions if round(q.get("marks", 2.0)) == 2]
    }
    marks_titles = {
        "1_mark": "1-Mark Questions",
        "2_marks": "2-Mark Questions"
    }

    for mk, qlist in marks_groups.items():
        def marks_sort_key(x):
            subj = get_canonical_subject(x.get("topic"))
            subj_idx = SUBJECT_ORDER.index(subj) if subj in SUBJECT_ORDER else 99
            return (subj_idx, x.get("year", 0), x.get("session", ""), x.get("question_number", 0))

        qlist.sort(key=marks_sort_key)
        for q in qlist:
            q["_group_heading"] = get_canonical_subject(q.get("topic"))

        file_slug = mk
        book_configs.append({
            "category": "Marks Wise",
            "title": marks_titles[mk],
            "filename": file_slug,
            "pdf_dir": categories["marks_wise"]["pdf_dir"],
            "json_dir": categories["marks_wise"]["json_dir"],
            "questions": qlist
        })

    print(f"\nPrepared {len(book_configs)} textbook configurations:")

    # Write JSON files and LaTeX source files
    compile_tasks = []
    for b in book_configs:
        clean_qs = []
        for q in b["questions"]:
            q_copy = dict(q)
            q_copy.pop("_group_heading", None)
            clean_qs.append(q_copy)

        json_path = os.path.join(b["json_dir"], f"{b['filename']}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "category": b["category"],
                "title": b["title"],
                "total_questions": len(clean_qs),
                "years_included": [2018, 2022, 2023, 2024, 2025],
                "questions": clean_qs
            }, f, indent=2)

        tex_content = generate_book_latex(b["category"], b["title"], b["questions"], abs_logo_path)
        tex_path = os.path.join(b["pdf_dir"], f"{b['filename']}.tex")
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(tex_content)

        compile_tasks.append((tex_path, b["pdf_dir"], b["filename"]))

    print(f"Saved {len(book_configs)} JSON datasets and .tex files.")
    print("Beginning parallel PDF compilation...")

    max_workers = min(4, os.cpu_count() or 2)
    successful = 0
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(compile_task, task): task for task in compile_tasks}
        for future in as_completed(futures):
            res = future.result()
            if res:
                successful += 1

    print(f"\nCompilation Complete: {successful}/{len(compile_tasks)} PDFs generated successfully.")

if __name__ == "__main__":
    main()
