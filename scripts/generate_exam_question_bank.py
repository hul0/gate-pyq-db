#!/usr/bin/env python3
"""
generate_exam_question_bank.py

Compiles an authentic EXAM-STYLE academic Question Bank for GATE CSE (2011 - 2025):
- Format: EXAM Style, Black and White, publishable book typography.
- Typography: Clear Sans Serif fonts only (Liberation Sans).
- Layout: Questions in two columns across both sides of the page.
- Bold Questions: Question text is bold, while options are in regular/normal font.
- Section Marks: Mark divisions specified before each question block; individual questions feature a clean type badge.
- Solution Placement: Full Official Answer Key at the end of each Year & Shift.
- Brand & Company: Studiva, www.studiva.co.in, contact@studiva.co.in.
- Icon: JPEG icon for optimized document size.

Produces:
- Master Book: pdf_books/GATE_CS_2011_2025_PYQ_Question_Bank.pdf
- Individual Paper Sets: pdf_books/<paper_id>_exam.pdf
"""

import os
import sys
import json
import re
import math
import shutil
import argparse
import subprocess
from pathlib import Path

# Special character and symbol replacements
UNICODE_LATEX_MAP = {
    "≤": r"$\le$",
    "≥": r"$\ge$",
    "≠": r"$\ne$",
    "±": r"$\pm$",
    "×": r"$\times$",
    "÷": r"$\div$",
    "∈": r"$\in$",
    "∉": r"$\notin$",
    "⊆": r"$\subseteq$",
    "⊂": r"$\subset$",
    "∪": r"$\cup$",
    "∩": r"$\cap$",
    "→": r"$\to$",
    "⇒": r"$\implies$",
    "↔": r"$\leftrightarrow$",
    "⇔": r"$\iff$",
    "∞": r"$\infty$",
    "√": r"$\sqrt{\vphantom{x}}$",
    "∑": r"$\sum$",
    "Σ": r"$\Sigma$",
    "Π": r"$\Pi$",
    "α": r"$\alpha$",
    "β": r"$\beta$",
    "γ": r"$\gamma$",
    "δ": r"$\delta$",
    "ε": r"$\epsilon$",
    "λ": r"$\lambda$",
    "μ": r"$\mu$",
    "π": r"$\pi$",
    "σ": r"$\sigma$",
    "θ": r"$\theta$",
    "ω": r"$\omega$",
    "Ω": r"$\Omega$",
    "⊕": r"$\oplus$",
    "≈": r"$\approx$",
    "≡": r"$\equiv$",
    "⁰": r"$^0$",
    "¹": r"$^1$",
    "²": r"$^2$",
    "³": r"$^3$",
    "⁴": r"$^4$",
    "⁵": r"$^5$",
    "⁶": r"$^6$",
    "⁷": r"$^7$",
    "⁸": r"$^8$",
    "⁹": r"$^9$",
    "ⁿ": r"$^n$",
    "ⁱ": r"$^i$",
    "ଶ": r"$^2$",
    "₀": r"$_0$",
    "₁": r"$_1$",
    "₂": r"$_2$",
    "₃": r"$_3$",
    "₄": r"$_4$",
    "₅": r"$_5$",
    "₆": r"$_6$",
    "₇": r"$_7$",
    "₈": r"$_8$",
    "₉": r"$_9$",
    "ᵢ": r"$_i$",
    "ⱼ": r"$_j$",
    "𝑥": r"$x$",
    "𝑦": r"$y$",
    "𝑧": r"$z$",
    "𝑟": r"$r$",
    "𝑛": r"$n$",
    "𝑘": r"$k$",
    "𝑖": r"$i$",
    "𝑗": r"$j$",
    "—": "---",
    "–": "--",
    "“": "``",
    "”": "''",
    "‘": "`",
    "’": "'",
}

def clean_unicode_math_symbols(text):
    r"""
    Cleans Unicode mathematical symbols:
    - Inside math mode: converts to bare LaTeX math commands (e.g. \le, \ge, ^2) without nested $.
    - Outside math mode: converts to LaTeX math enclosed in $...$.
    """
    if not text:
        return ""

    math_pattern = r'(\$\$.*?\$\$|\$.*?\$|\\begin\{[a-zA-Z*]+\}.*?\\end\{[a-zA-Z*]+\})'
    parts = re.split(math_pattern, text, flags=re.DOTALL)
    res = []

    inside_math_replacements = {
        "≤": r"\le ", "≥": r"\ge ", "≠": r"\ne ", "±": r"\pm ", "×": r"\times ", "÷": r"\div ",
        "∈": r"\in ", "∉": r"\notin ", "⊆": r"\subseteq ", "⊂": r"\subset ", "∪": r"\cup ", "∩": r"\cap ",
        "→": r"\to ", "⇒": r"\implies ", "↔": r"\leftrightarrow ", "⇔": r"\iff ", "∞": r"\infty ",
        "∑": r"\sum ", "Σ": r"\Sigma ", "Π": r"\Pi ", "α": r"\alpha ", "β": r"\beta ", "γ": r"\gamma ",
        "δ": r"\delta ", "ε": r"\epsilon ", "λ": r"\lambda ", "μ": r"\mu ", "π": r"\pi ", "σ": r"\sigma ",
        "θ": r"\theta ", "ω": r"\omega ", "Ω": r"\Omega ", "⊕": r"\oplus ", "≈": r"\approx ", "≡": r"\equiv ",
        "⁰": "^0", "¹": "^1", "²": "^2", "³": "^3", "⁴": "^4", "⁵": "^5", "⁶": "^6", "⁷": "^7", "⁸": "^8", "⁹": "^9", "ⁿ": "^n", "ⁱ": "^i", "ଶ": "^2",
        "₀": "_0", "₁": "_1", "₂": "_2", "₃": "_3", "₄": "_4", "₅": "_5", "₆": "_6", "₇": "_7", "₈": "_8", "₉": "_9", "ᵢ": "_i", "ⱼ": "_j",
        "−": "-", "–": "-", "—": "-"
    }

    for i, part in enumerate(parts):
        if i % 2 == 1:
            p = part
            for k, v in inside_math_replacements.items():
                p = p.replace(k, v)
            res.append(p)
        else:
            p = part
            for u_char, tex_equiv in UNICODE_LATEX_MAP.items():
                p = p.replace(u_char, tex_equiv)
            res.append(p)

    return "".join(res)

def escape_latex_outside_math(text, is_preformatted_latex=False):
    """
    Escapes special LaTeX characters outside math environments.
    """
    if not text:
        return ""

    # Replace special Unicode characters
    text = clean_unicode_math_symbols(text)

    # Clean PDF artifacts
    text = re.sub(r'Organising Institute:[^\n]*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Organizing Institute:[^\n]*', '', text, flags=re.IGNORECASE)

    # Split text into math segments ($...$, $$...$$, \begin{...}...\end{...})
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

            if not is_preformatted_latex:
                p = re.sub(r'(?<!\\)\{', r'\{', p)
                p = re.sub(r'(?<!\\)\}', r'\}', p)
                p = re.sub(r'\^', r'\^{}', p)
                p = re.sub(r'~', r'\~{}', p)

            escaped_parts.append(p)

    return "".join(escaped_parts)

def convert_markdown_tables_to_latex(text):
    """
    Detects markdown tables in text and formats them as LaTeX tabular.
    """
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

    col_spec = "|" + "|".join(alignments) + "|"
    out = [
        r"\begin{center}\footnotesize",
        r"\resizebox{\columnwidth}{!}{%",
        f"\\begin{{tabular}}{{{col_spec}}}",
        r"\hline"
    ]

    header_cells = rows[0]
    escaped_headers = [escape_latex_outside_math(c) for c in header_cells]
    out.append(" & ".join([f"\\textbf{{{c}}}" for c in escaped_headers]) + r" \\ \hline\hline")

    for r in rows[1:]:
        while len(r) < num_cols:
            r.append("")
        escaped_row = [escape_latex_outside_math(c) for c in r]
        out.append(" & ".join(escaped_row) + r" \\ \hline")

    out.append(r"\end{tabular}%")
    out.append(r"}\end{center}")
    return "\n".join(out)

def convert_code_blocks_to_latex(text):
    """
    Converts markdown code blocks (```c ... ```) to lstlisting.
    """
    code_pattern = r'```(?:c|C|cpp)?\s*\n(.*?)\n```'
    def replacer(m):
        code_content = m.group(1)
        return (
            "\\begin{lstlisting}[language=C, basicstyle=\\scriptsize\\ttfamily, "
            "frame=single, rulecolor=\\color{black!40}, tabsize=2, breaklines=true, "
            "aboveskip=4pt, belowskip=4pt]\n"
            + code_content + "\n\\end{lstlisting}"
        )
    return re.sub(code_pattern, replacer, text, flags=re.DOTALL)

def format_question_text(q):
    """
    Formats the question body into clean, bold, printable LaTeX.
    Question text is wrapped in \textbf so that question statements stand out prominently,
    while math formulas and code listings maintain their respective clean typography.
    """
    raw_latex = q.get("question_text_latex")
    if raw_latex:
        text = raw_latex
        is_preformatted = True
    else:
        text = q.get("question_text", "")
        is_preformatted = False

    text = re.sub(r'Organising Institute:[^\n]*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Organizing Institute:[^\n]*', '', text, flags=re.IGNORECASE)

    code_parts = re.split(r'(```(?:c|C|cpp)?\s*\n.*?\n```)', text, flags=re.DOTALL)
    processed_parts = []
    for idx, cp in enumerate(code_parts):
        if idx % 2 == 1:
            processed_parts.append(convert_code_blocks_to_latex(cp))
        else:
            t = convert_markdown_tables_to_latex(cp)
            t = escape_latex_outside_math(t, is_preformatted_latex=is_preformatted)
            t = t.replace("\n\n", "\n\\par\\smallskip\n")
            # Apply bold typography to the question narrative text
            processed_parts.append(f"{{\\bfseries {t} \\par}}")

    return "".join(processed_parts)

def format_options(q):
    """
    Formats MCQ/MSQ options or NAT answer space.
    Options are formatted in normal/regular font weight, with bold (A), (B), (C), (D) labels.
    """
    raw_opts_latex = q.get("options_latex")
    if raw_opts_latex and isinstance(raw_opts_latex, dict):
        options = raw_opts_latex
        is_preformatted = True
    else:
        options = q.get("options")
        is_preformatted = False

    if not options or not isinstance(options, dict):
        return r"\par\vspace{3pt}\noindent\textbf{Answer:} \rule{3.2cm}{0.4pt}"

    clean_opts = {}
    for k in ["A", "B", "C", "D"]:
        if k in options:
            val = str(options[k]).strip()
            val = re.sub(r'Organising Institute:[^\n]*', '', val, flags=re.IGNORECASE).strip()
            val = re.sub(r'Organizing Institute:[^\n]*', '', val, flags=re.IGNORECASE).strip()
            val = escape_latex_outside_math(val, is_preformatted_latex=is_preformatted)
            val = val.replace("\n", r" \newline ")
            clean_opts[k] = val

    if not clean_opts:
        return r"\par\vspace{3pt}\noindent\textbf{Answer:} \rule{3.2cm}{0.4pt}"

    is_short_2col = (
        len(clean_opts) == 4
        and all(len(v) < 22 for v in clean_opts.values())
        and all(r"\newline" not in v for v in clean_opts.values())
    )

    if is_short_2col:
        a, b = clean_opts["A"], clean_opts["B"]
        c, d = clean_opts["C"], clean_opts["D"]
        return (
            "\\par\\vspace{2pt}\\noindent\n"
            "\\begin{tabular*}{\\columnwidth}{@{\\extracolsep{\\fill}}p{0.46\\columnwidth}p{0.46\\columnwidth}@{}}\n"
            f"\\textbf{{(A)}}~{a} & \\textbf{{(B)}}~{b} \\\\\n"
            f"\\addlinespace[2pt]\n"
            f"\\textbf{{(C)}}~{c} & \\textbf{{(D)}}~{d}\n"
            "\\end{tabular*}"
        )
    else:
        rows = []
        for k in ["A", "B", "C", "D"]:
            if k in clean_opts:
                rows.append(f"\\textbf{{({k})}}~{clean_opts[k]}")
        joined = "\\par\\vspace{2pt}\\noindent\n".join(rows)
        return f"\\par\\vspace{{2pt}}\\noindent\n{joined}"

def build_answer_key_table(questions, year, session):
    """
    Generates a compact, exam-style answer key grid (4 balanced columns)
    for the end of the year & shift.
    """
    if not questions:
        return ""

    num_q = len(questions)
    num_cols = 4
    num_rows = math.ceil(num_q / num_cols)

    table_lines = [
        r"\begin{center}",
        r"\small",
        r"\resizebox{\linewidth}{!}{%",
        r"\begin{tabular}{|c|c|l||c|c|l||c|c|l||c|c|l|}",
        r"\hline",
        r"\textbf{Q} & \textbf{Type} & \textbf{Key} & "
        r"\textbf{Q} & \textbf{Type} & \textbf{Key} & "
        r"\textbf{Q} & \textbf{Type} & \textbf{Key} & "
        r"\textbf{Q} & \textbf{Type} & \textbf{Key} \\",
        r"\hline\hline"
    ]

    for r in range(num_rows):
        row_entries = []
        for c in range(num_cols):
            idx = r + c * num_rows
            if idx < num_q:
                q = questions[idx]
                qnum = q.get("question_number", idx + 1)
                qtype = q.get("question_type", "MCQ")
                ans = str(q.get("answer", "")).strip()

                if ans.lower() in ["marks to all", "mta"]:
                    disp_ans = "MTA"
                elif " to " in ans:
                    parts = ans.split(" to ")
                    if len(parts) == 2 and parts[0].strip() == parts[1].strip():
                        disp_ans = parts[0].strip()
                    else:
                        disp_ans = ans
                else:
                    disp_ans = ans

                disp_ans = escape_latex_outside_math(disp_ans)
                row_entries.append(f"{qnum} & {qtype} & {disp_ans}")
            else:
                row_entries.append(" & & ")
        table_lines.append(" & ".join(row_entries) + r" \\ \hline")

    table_lines.append(r"\end{tabular}%")
    table_lines.append(r"}")
    table_lines.append(r"\end{center}")
    return "\n".join(table_lines)

def generate_paper_latex(paper_data):
    """
    Generates LaTeX for a single paper (Year & Shift).
    Includes section banners with mark divisions and clean question headers.
    """
    year = paper_data.get("year", 2025)
    session = paper_data.get("session", "CS")
    subject = paper_data.get("subject", "Computer Science and IT")
    paper_id = paper_data.get("paper_id", f"{year}_{session}")
    raw_questions = paper_data.get("questions", [])

    if paper_id in ["2013_CS", "2014_CS", "2016_CS"]:
        questions = [q for q in raw_questions if len(q.get("id", "").split("_")) <= 4]
    else:
        questions = raw_questions

    questions.sort(key=lambda x: x.get("question_number", 0))

    tex = []
    # Title Banner (single column span)
    tex.append(f"% ==================== PAPER: {paper_id} ====================")
    tex.append(r"\begin{center}")
    tex.append(f"{{\\Large\\textbf{{GATE {year} EXAMINATION}}}}\\\\[3pt]")
    tex.append(f"{{\\normalsize\\textbf{{{subject.upper()}}}}}\\\\[2pt]")
    tex.append(f"{{\\small\\textbf{{Session / Shift: {session}}}}}\\\\[5pt]")
    tex.append(r"\rule{\linewidth}{0.8pt}\vspace{-4pt}")
    tex.append(f"{{\\footnotesize\\textbf{{Duration: 180 Minutes}} \\hfill \\textbf{{Total Marks: 100}} \\hfill \\textbf{{Questions: {len(questions)}}}}}\\\\")
    tex.append(r"\vspace{-4pt}\rule{\linewidth}{0.4pt}")
    tex.append(r"\end{center}")
    tex.append(r"\vspace{4pt}")

    # Exam Instructions Box (Single column)
    tex.append(r"\noindent\fbox{\parbox{\dimexpr\linewidth-2\fboxsep-2\fboxrule}{%")
    tex.append(r"\footnotesize\textbf{Examination Instructions:}\\[1pt]")
    tex.append(r"1. Question Types: Multiple Choice Questions (MCQ), Multiple Select Questions (MSQ), and Numerical Answer Type (NAT).\\")
    tex.append(r"2. Negative Marking Scheme: For 1-mark MCQ, $1/3$ mark is deducted; for 2-mark MCQ, $2/3$ mark is deducted. There is no negative marking for MSQ and NAT questions.\\")
    tex.append(r"3. Mark Division: Questions are grouped by mark allocation within each section as specified below. Full official answer key is provided at the end of this paper.")
    tex.append(r"}}")
    tex.append(r"\vspace{10pt}")

    # Begin Two Columns for Questions
    tex.append(r"\begin{multicols}{2}")

    current_section = None
    current_marks = None

    for q in questions:
        sec = q.get("section", "Computer Science and Information Technology")
        marks = float(q.get("marks", 1.0))
        q_num = q.get("question_number", 0)
        q_type = q.get("question_type", "MCQ")

        # Determine section and mark banner changes
        sec_changed = (sec != current_section)
        marks_changed = (marks != current_marks)

        if sec_changed:
            current_section = sec
            current_marks = marks
            m_label = f"{marks:.0f}-mark" if marks.is_integer() else f"{marks}-mark"
            tex.append(
                f"\n\\vspace{{8pt}}\n"
                f"\\noindent\\textbf{{\\large\\underline{{{sec.upper()}}}}}\\\\[2pt]\n"
                f"\\noindent{{\\footnotesize\\textit{{[Section Block: {m_label} questions]}}}}\n"
                f"\\vspace{{4pt}}\n"
            )
        elif marks_changed:
            current_marks = marks
            m_label = f"{marks:.0f}-mark" if marks.is_integer() else f"{marks}-mark"
            tex.append(
                f"\n\\vspace{{6pt}}\n"
                f"\\noindent{{\\footnotesize\\textit{{[Section Block: {m_label} questions]}}}}\n"
                f"\\vspace{{3pt}}\n"
            )

        q_body = format_question_text(q)
        q_opts = format_options(q)

        # Question header with clean type badge (without distracting mark numbers)
        box_header = f"\\noindent\\textbf{{Q.{q_num}}} \\hfill {{\\footnotesize\\textsf{{[{q_type}]}}}}"

        tex.append(box_header)
        tex.append(r"\par\vspace{2pt}")
        tex.append(q_body)
        tex.append(q_opts)
        tex.append(r"\par\vspace{6pt}\hrule height 0.25pt\vspace{6pt}")

    tex.append(r"\end{multicols}")

    # End of paper divider
    tex.append(r"\vspace{8pt}")
    tex.append(r"\begin{center}")
    tex.append(r"\rule{0.35\linewidth}{0.5pt}\\[2pt]")
    tex.append(r"\textbf{\small --- END OF QUESTION PAPER ---}\\[-8pt]")
    tex.append(r"\rule{0.35\linewidth}{0.5pt}")
    tex.append(r"\end{center}")
    tex.append(r"\vspace{10pt}")

    # Full Answer Key at the end of the year & shift
    tex.append(f"\\subsection*{{OFFICIAL ANSWER KEY --- GATE {year} ({session})}}")
    tex.append(r"\vspace{-4pt}")
    tex.append(r"\noindent{\footnotesize\textit{Official final answer keys published by the GATE Organising Institute. For NAT questions, allowable numerical ranges are displayed where applicable. MTA = Marks To All.}}")
    tex.append(r"\vspace{4pt}")
    ans_table = build_answer_key_table(questions, year, session)
    tex.append(ans_table)

    return "\n".join(tex), len(questions)

def generate_master_book_latex(papers_data, abs_logo_path):
    """
    Generates the complete master LaTeX document for all 2011-2025 papers.
    """
    logo_path_latex = abs_logo_path.replace("\\", "/")

    tex = [
        r"""\documentclass[a4paper,10pt,twoside]{article}
\usepackage{fontspec}
\setmainfont{Liberation Sans}
\setsansfont{Liberation Sans}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{amsmath,amssymb}
\usepackage{geometry}
\usepackage{multicol}
\usepackage{graphicx}
\usepackage{fancyhdr}
\usepackage{lastpage}
\usepackage{booktabs}
\usepackage{listings}
\usepackage{eso-pic}
\usepackage{tikz}
\usepackage{array}
\usepackage{tabularx}
\usepackage{enumitem}
\usepackage{microtype}

\geometry{
    a4paper,
    top=1.8cm,
    bottom=1.8cm,
    left=1.2cm,
    right=1.2cm,
    headsep=14pt,
    footskip=20pt
}

\setlength{\columnsep}{16pt}
\setlength{\columnseprule}{0.35pt}

% Persistent Subtle Watermark on Every Page
\newsavebox{\watermarkbox}
\sbox{\watermarkbox}{%
    \begin{tabular}{c}
        \includegraphics[width=6.0cm]{""" + logo_path_latex + r"""} \\[-0.2em]
        {\fontsize{14}{17}\selectfont\bfseries Studiva}
    \end{tabular}%
}
\AddToShipoutPictureBG{%
    \begin{tikzpicture}[remember picture, overlay]
        \node[opacity=0.035] at (current page.center) {\usebox{\watermarkbox}};
    \end{tikzpicture}%
}

% Running Headers & Footers
\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{\small\textbf{Studiva GATE Question Bank}}
\fancyhead[LE]{\small\textit{Computer Science \& IT (2011--2025)}}
\fancyhead[RO]{\small\textit{Studiva}}
\fancyfoot[LE,RO]{\scriptsize\textbf{Studiva} $\cdot$ \texttt{www.studiva.co.in}}
\fancyfoot[C]{\small\textbf{Page \thepage\ of \pageref{LastPage}}}
\fancyfoot[RE,LO]{\scriptsize\texttt{contact@studiva.co.in}}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}

% Listings Style (Clean, professional)
\lstset{
    basicstyle=\scriptsize\ttfamily,
    numbers=none,
    frame=single,
    rulecolor=\color{black!30},
    tabsize=2,
    breaklines=true,
    showstringspaces=false
}

\begin{document}

% ==================== PAGE 1: FORMAL TITLE & COVER PAGE ====================
\thispagestyle{empty}
\vspace*{1.5cm}
\begin{center}
    \includegraphics[width=2.5cm]{""" + logo_path_latex + r"""}\\[1.5em]
    {\fontsize{24}{28}\selectfont\textbf{GATE COMPUTER SCIENCE \& IT}}\\[0.5em]
    {\fontsize{16}{20}\selectfont\textbf{PREVIOUS YEARS QUESTION BANK (2011 -- 2025)}}\\[0.6em]
    {\normalsize Detailed Examination Papers with Complete Official Answer Keys}\\[2.0em]
    \rule{0.65\textwidth}{0.8pt}\\[2.0em]
    {\large\textbf{Studiva GATE Examination Series}}\\[0.4em]
    {\small Comprehensive Authentic Question Bank for GATE Computer Science \& Information Technology}\\[2.8cm]

    \begin{tabular}{|ll|}
        \hline
        \textbf{Subject:} & Computer Science and Information Technology (CS/IT) \\
        \textbf{Period Covered:} & 2011 to 2025 \\
        \textbf{Examination Papers:} & """ + str(len(papers_data)) + r""" Complete Verified Paper Sets \\
        \textbf{Contents:} & Examination Questions \& Official Final Answer Keys \\
        \textbf{Published by:} & Studiva (\texttt{www.studiva.co.in}) \\
        \hline
    \end{tabular}

    \vfill
    {\small\textbf{Studiva $\cdot$ \texttt{www.studiva.co.in} $\cdot$ \texttt{contact@studiva.co.in}}}
\end{center}

\newpage

% ==================== PAGE 2: PUBLICATION IMPRINT & NOTES ====================
\thispagestyle{empty}
\vspace*{0.6cm}
\begin{center}
    {\large\textbf{PUBLICATION INFORMATION \& COPYRIGHT NOTICE}}\\[0.4em]
    \rule{0.6\textwidth}{0.5pt}
\end{center}

\vspace{1.2em}
\noindent\begin{tabular}{ll}
\textbf{Title:} & Studiva GATE Question Bank: Computer Science \& IT (2011--2025) \\
\textbf{Publisher:} & Studiva \\
\textbf{Website:} & \texttt{www.studiva.co.in} \\
\textbf{Official Inquiries:} & \texttt{contact@studiva.co.in} \\
\textbf{Edition:} & First Edition (2026) \\
\textbf{Syllabus Scope:} & Official GATE Syllabus (General Aptitude and CS / IT) \\
\end{tabular}

\vspace{1.8em}
\noindent\fbox{\parbox{\dimexpr\linewidth-2\fboxsep-2\fboxrule}{%
\textbf{COPYRIGHT NOTICE}\\[0.4em]
Copyright \copyright\ 2026 Studiva. All Rights Reserved.\\[0.4em]
No part of this publication may be reproduced, stored in a retrieval system, or transmitted in any form or by any means, electronic, mechanical, photocopying, recording, or otherwise, without prior written permission of Studiva, except for individual academic study.
}}

\vspace{1.5em}
\noindent\fbox{\parbox{\dimexpr\linewidth-2\fboxsep-2\fboxrule}{%
\textbf{PUBLISHER'S NOTE: ARCHIVAL QUESTION FORMAT}\\[0.4em]
This compendium has been meticulously curated and verified against official GATE question papers and final answer keys.
\par\medskip\noindent
\textbf{Notice on Image-Based Questions:}\\
Questions containing diagrams, circuit schematics, graphs, or image-based figures from the original examination papers have been omitted in this text edition due to non-readable format in historical source archives. All text-based conceptual, analytical, mathematical, algorithmic, and numerical questions are fully included with verified official keys.
}}

\vspace{1.5em}
\begin{center}
\textbf{EXAMINATION STRUCTURE \& PRACTICE GUIDELINES}
\end{center}
\begin{enumerate}[leftmargin=*]
    \item \textbf{Sectional Mark Division:} Each paper comprises General Aptitude (GA) and Computer Science (CS). Questions are clearly grouped into 1-mark and 2-mark blocks at the head of each section.
    \item \textbf{Question Types:} Includes Multiple Choice Questions (MCQ), Multiple Select Questions (MSQ), and Numerical Answer Type (NAT).
    \item \textbf{Official Answer Keys:} For self-evaluation without distraction, complete official answer keys are printed at the conclusion of each respective examination paper set.
\end{enumerate}

\newpage

% ==================== PAGE 3: TABLE OF CONTENTS ====================
\begin{center}
    {\Large\textbf{TABLE OF CONTENTS}}\\[0.4em]
    \rule{0.5\textwidth}{0.6pt}
\end{center}
\vspace{1em}

\noindent\begin{tabularx}{\linewidth}{|X|l|c|r|}
\hline
\textbf{Examination Paper} & \textbf{Session / Shift} & \textbf{Total Questions} & \textbf{Content Type} \\
\hline
"""
    ]

    for p in papers_data:
        yr = p.get("year")
        sess = p.get("session")
        tot = len(p.get("questions", []))
        tex.append(f"GATE {yr} Computer Science & Shift {sess} & {tot} & Questions + Answer Key \\\\ \\hline")

    tex.append(r"""\end{tabularx}

\vspace{1.5em}
\noindent{\footnotesize\textit{Note: All questions in this edition have been typeset from verified digital records and cross-referenced with official answer keys released by the organising IIT/IISc institutes.}}

\newpage
""")

    # Append all papers
    for idx, paper in enumerate(papers_data):
        paper_tex, count = generate_paper_latex(paper)
        tex.append(paper_tex)
        if idx < len(papers_data) - 1:
            tex.append(r"\newpage")

    tex.append(r"\end{document}")
    return "\n".join(tex)

def compile_latex(tex_path, output_dir):
    """
    Compiles LaTeX file twice using XeLaTeX to resolve all page numbers.
    """
    base_name = os.path.splitext(os.path.basename(tex_path))[0]
    pdf_path = os.path.join(output_dir, f"{base_name}.pdf")

    cmd = ["xelatex", "-interaction=nonstopmode", os.path.basename(tex_path)]
    print(f"Compiling {base_name} with XeLaTeX (Pass 1)...")
    res1 = subprocess.run(cmd, cwd=output_dir, capture_output=True, text=True)

    print(f"Compiling {base_name} with XeLaTeX (Pass 2 for page references)...")
    res2 = subprocess.run(cmd, cwd=output_dir, capture_output=True, text=True)

    if os.path.exists(pdf_path):
        print(f"Successfully compiled: {pdf_path}")
        for ext in [".aux", ".log", ".out", ".toc"]:
            aux_f = os.path.join(output_dir, f"{base_name}{ext}")
            if os.path.exists(aux_f):
                try:
                    os.remove(aux_f)
                except Exception:
                    pass
        return pdf_path
    else:
        print(f"Compilation failed for {tex_path}. Log tail:")
        print(res2.stdout[-1500:])
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate GATE CS Exam Question Bank PDFs")
    parser.add_argument("--paper", type=str, help="Generate for a specific paper_id (e.g. 2024_CS1)")
    parser.add_argument("--master-only", action="store_true", help="Generate only the Master Question Bank")
    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parent.parent
    dataset_papers_dir = root_dir / "dataset" / "papers"
    pdf_books_dir = root_dir / "pdf_books"
    pdf_books_dir.mkdir(parents=True, exist_ok=True)
    assets_dir = root_dir / "assets"

    # Use JPEG icon to optimize document size as requested
    logo_jpeg = assets_dir / "studiva_butterfly_icon_transparent.jpeg"
    if not logo_jpeg.exists():
        logo_jpeg = assets_dir / "studiva-butterfly-icon.jpg"

    # Chronological paper ordering
    paper_ids = [
        "2011_CS",
        "2012_CS",
        "2013_CS",
        "2014_CS",
        "2016_CS",
        "2018_CS",
        "2022_CS",
        "2023_CS",
        "2024_CS1",
        "2024_CS2",
        "2025_CS1",
        "2025_CS2"
    ]

    if args.paper:
        target_papers = [args.paper]
    else:
        target_papers = paper_ids

    all_papers_data = []
    print(f"Loading paper sets for the Question Bank...")
    for pid in target_papers:
        pfile = dataset_papers_dir / pid / "full_paper.json"
        if not pfile.exists():
            print(f"Warning: {pfile} not found. Running generate_full_paper_json.py...")
            subprocess.run([sys.executable, str(root_dir / "scripts" / "generate_full_paper_json.py"), pid], check=True)

        with open(pfile, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_papers_data.append(data)
            print(f"  Loaded {pid}: {len(data.get('questions', []))} questions")

    # 1. Generate individual paper exam PDFs (unless master-only)
    if not args.master_only:
        print("\n--- Compiling Individual Paper Exam PDFs ---")
        for pdata in all_papers_data:
            pid = pdata.get("paper_id")
            p_dir = dataset_papers_dir / pid

            single_tex = generate_master_book_latex([pdata], str(logo_jpeg))
            single_tex_path = p_dir / f"{pid}_exam.tex"
            with open(single_tex_path, "w", encoding="utf-8") as f:
                f.write(single_tex)

            single_pdf = compile_latex(single_tex_path, str(p_dir))
            if single_pdf and os.path.exists(single_pdf):
                dest_copy = pdf_books_dir / f"{pid}_exam.pdf"
                shutil.copy2(single_pdf, dest_copy)
                print(f"  Saved individual exam PDF to {dest_copy}")

    # 2. Generate Master 2011-2025 Question Bank Book (if multiple papers or master-only)
    if not args.paper or args.master_only:
        print("\n--- Compiling Master 2011-2025 GATE PYQ Question Bank Book ---")
        master_tex = generate_master_book_latex(all_papers_data, str(logo_jpeg))
        master_tex_path = pdf_books_dir / "GATE_CS_2011_2025_PYQ_Question_Bank.tex"
        with open(master_tex_path, "w", encoding="utf-8") as f:
            f.write(master_tex)

        master_pdf = compile_latex(master_tex_path, str(pdf_books_dir))
        if master_pdf and os.path.exists(master_pdf):
            size_mb = os.path.getsize(master_pdf) / (1024 * 1024)
            print(f"\nSUCCESS! Master Question Bank compiled:")
            print(f"Location: {master_pdf}")
            print(f"Size: {size_mb:.2f} MB")

if __name__ == "__main__":
    main()
