#!/usr/bin/env python3
"""
generate_paper_textbook.py

Generates a print-friendly, standard academic textbook PDF for a GATE paper set:
- Optimized for black-and-white / grayscale printing (zero ink waste).
- Side-by-side design: Question + options with checkboxes on the left,
  clean vertical divider, Answer + Topic + Explanation on the right.
- Cover-and-practice layout: users can cover the right side with paper/ruler
  and tick choices on the left.
- Full LaTeX math and code rendering.
- Produces:
    dataset/papers/<paper_id>/<paper_id>_textbook.pdf
    pdf_books/<paper_id>.pdf
"""

import os
import sys
import json
import re
import shutil
import subprocess

def escape_latex_outside_math(text):
    if not text:
        return ""
        
    # Split text into math parts and non-math parts
    # Tokens can be $...$, $$...$$, \begin{...}...\end{...}, or regular text
    math_pattern = r'(\$\$.*?\$\$|\$.*?\$|\\begin\{[a-zA-Z*]+\}.*?\\end\{[a-zA-Z*]+\})'
    parts = re.split(math_pattern, text, flags=re.DOTALL)

    escaped_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            # Inside math / environment - preserve as is
            escaped_parts.append(part)
        else:
            # Outside math - escape special LaTeX characters
            p = part
            # Escape & (if not already escaped)
            p = re.sub(r'(?<!\\)&', r'\&', p)
            # Escape % (if not already escaped)
            p = re.sub(r'(?<!\\)%', r'\%', p)
            # Escape # (if not already escaped)
            p = re.sub(r'(?<!\\)#', r'\#', p)
            # Escape _ (if not already escaped)
            p = re.sub(r'(?<!\\)_', r'\_', p)
            escaped_parts.append(p)

    return "".join(escaped_parts)

def convert_markdown_tables_to_latex(text):
    # Detect markdown tables: lines starting with |
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
                # Process collected table lines
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
            # Alignment row
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
    
    # Header row
    header_cells = rows[0]
    out.append(" & ".join(header_cells) + " \\\\")
    out.append("\\midrule")

    # Data rows
    for r in rows[1:]:
        out.append(" & ".join(r) + " \\\\")

    out.append("\\bottomrule")
    out.append("\\end{tabular}\\end{center}")
    return "\n".join(out)

def convert_code_blocks_to_latex(text):
    # Replace ```c ... ``` with lstlisting
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
    # Prefer question_text_latex if available
    text = q.get("question_text_latex") or q.get("question_text", "")
    
    # Clean PDF artifacts
    text = re.sub(r'Organising Institute:.*', '', text)
    text = re.sub(r'Organizing Institute:.*', '', text)
    
    # Format code blocks first (verbatim)
    # Split code blocks so we don't escape inside them
    code_parts = re.split(r'(```(?:c|C|cpp)?\s*\n.*?\n```)', text, flags=re.DOTALL)
    processed_parts = []
    for idx, cp in enumerate(code_parts):
        if idx % 2 == 1:
            # Code block
            processed_parts.append(convert_code_blocks_to_latex(cp))
        else:
            # Normal text: tables and escaping
            t = convert_markdown_tables_to_latex(cp)
            t = escape_latex_outside_math(t)
            # Normalize double newlines to paragraph breaks
            t = t.replace("\n\n", "\n\\par\\medskip\n")
            processed_parts.append(t)

    return "".join(processed_parts)

def format_options(q):
    options = q.get("options_latex") or q.get("options")
    if not options or not isinstance(options, dict):
        # NAT Question
        return "\\par\\vspace{6pt}\\noindent\\textbf{Your Answer:} \\fbox{\\rule{0pt}{1.3ex}\\hspace{3cm}}"

    clean_opts = {}
    for opt_key in ["A", "B", "C", "D"]:
        if opt_key in options:
            val = options[opt_key]
            # Clean footers
            val = re.sub(r'Organising Institute:.*', '', str(val)).strip()
            val = re.sub(r'Organizing Institute:.*', '', val).strip()
            val = escape_latex_outside_math(val)
            val = val.replace("\n", r" \newline ")
            clean_opts[opt_key] = val

    if not clean_opts:
        return ""

    # Determine if 2-column tabular is suitable:
    # All 4 options exist, none has newlines or is too long (> 30 chars)
    is_short_2col = (
        len(clean_opts) == 4
        and all(len(v) < 32 for v in clean_opts.values())
        and all(r"\newline" not in v for v in clean_opts.values())
    )

    if is_short_2col:
        # Laser-straight 2-column alignment
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
        # Laser-straight 1-column stacked alignment
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

def generate_latex_document(paper_data, abs_logo_path):
    paper_id = paper_data.get("paper_id", "GATE")
    year = paper_data.get("year", 2025)
    session = paper_data.get("session", "CS2")
    subject = paper_data.get("subject", "Computer Science and Information Technology")
    questions = paper_data.get("questions", [])

    # Escape logo path for LaTeX (convert backslashes to forward slashes)
    logo_path_latex = abs_logo_path.replace("\\", "/")

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

% Persistent Unremovable Canvas Watermark on Every Page (Shared XObject)
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
\fancyhead[L]{\small\scshape GATE """ + f"{year} {subject} ({session})" + r"""}
\fancyhead[R]{\small\scshape Practice Compendium \& Solutions}
\fancyfoot[L]{\scriptsize\textsc{Copyright \copyright\ 2026 Rupam Ghosh \& Studiva}}
\fancyfoot[C]{\small Page \thepage\ of \pageref{LastPage}}
\fancyfoot[R]{\scriptsize\texttt{www.studiva.co.in}}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}

% Code Listing Style (Monochrome, clean)
\lstset{
    basicstyle=\footnotesize\ttfamily,
    numbers=none,
    frame=none,
    tabsize=2,
    breaklines=true,
    showstringspaces=false
}

\begin{document}

% ==================== PAGE 1: DEDICATED IMPRINT & COPYRIGHT PAGE ====================
\thispagestyle{empty}
\vspace*{0.5cm}
\begin{center}
    \includegraphics[width=2.5cm]{""" + logo_path_latex + r"""}\\[0.6em]
    {\LARGE \textbf{GATE COMPUTER SCIENCE \& IT}}\\[0.3em]
    {\Large \textbf{PREVIOUS YEAR QUESTIONS COMPENDIUM}}\\[0.2em]
    {\normalsize \textsc{Session """ + str(session) + r""" $\cdot$ Examination Year """ + str(year) + r"""}}\\[1.2em]
    \rule{0.6\textwidth}{0.6pt}
\end{center}

\vspace{1em}
\noindent\begin{tabular}{ll}
\textbf{Author / Compiler:} & Rupam Ghosh \\
\textbf{Publisher \& Platform:} & Studiva (\texttt{www.studiva.co.in}) \\
\textbf{Official Inquiries:} & \texttt{contact@studiva.co.in} \\
\textbf{Edition:} & First Standard Edition (2026) \\
\textbf{Syllabus Reference:} & Official GATE 2026 Syllabus (Organizing Institute: IIT Guwahati) \\
\end{tabular}

\vspace{1.5em}
\begin{tcolorbox}[enhanced, standard jigsaw, opacityback=0, colframe=black!40, arc=1mm, boxrule=0.5pt, left=10pt, right=10pt, top=8pt, bottom=8pt]
\textbf{\large COPYRIGHT \& INTELLECTUAL PROPERTY NOTICE}\\[0.6em]
Copyright \copyright\ 2026 Rupam Ghosh \& Studiva. All Rights Reserved.\\[0.5em]
This educational compilation, problem organization, taxonomy classification, LaTeX typesetting, hints, and explanatory solutions are the proprietary intellectual property of \textbf{Rupam Ghosh} and \textbf{Studiva}.\\[0.6em]
\textbf{Terms of Use \& Attribution Rules:}
\begin{itemize}[leftmargin=*, nosep]
    \item \textbf{Personal Educational Use:} Permitted freely for individual students and educators preparing for competitive examinations.
    \item \textbf{Mandatory Attribution:} Any reproduction, republication, hosting, or sharing (digital or physical) must prominently credit \textbf{Rupam Ghosh \& Studiva} and include an active, direct link to \texttt{https://www.studiva.co.in}.
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
% ==================== PAGE 2 ONWARDS: QUESTION COMPENDIUM ====================
"""
    ]

    current_section = None
    for q in questions:
        sec = q.get("section", "Computer Science and Information Technology")
        if sec != current_section:
            current_section = sec
            tex.append(f"\\vspace{{6pt}}\n\\subsection*{{{sec}}}\n\\vspace{{-4pt}}")

        q_num = q.get("question_number", 0)
        q_type = q.get("question_type", "MCQ")
        marks = q.get("marks", 1.0)
        neg = q.get("negative_marks", 0.0)
        qid = q.get("id", "")

        q_body = format_question_body(q)
        q_options = format_options(q)
        sol_panel = format_solution_panel(q)

        neg_text = f"Neg: {neg:.2f}" if neg > 0 else "No Neg"
        clean_qid = qid.replace("_", r"\_")

        box_header = (
            "\\textbf{Q.%d} \\quad {\\footnotesize\\textsc{[%s $\\cdot$ %.0f Mark(s) $\\cdot$ %s]}} \\hfill {\\tiny\\texttt{%s}}"
            % (q_num, q_type, marks, neg_text, clean_qid)
        )

        box_tex = "\n".join([
            r"\noindent",
            r"\begin{tcolorbox}[",
            r"    blanker,",
            r"    sidebyside,",
            r"    sidebyside align=top,",
            r"    lefthand width=0.55\textwidth,",
            r"    segmentation style={draw=black!40, line width=0.4pt, dashed},",
            r"    top=4pt, bottom=4pt, left=0pt, right=0pt,",
            r"    middle=12pt",
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

def compile_latex_to_pdf(tex_content, output_dir, file_basename):
    tex_path = os.path.join(output_dir, f"{file_basename}.tex")
    pdf_path = os.path.join(output_dir, f"{file_basename}.pdf")

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex_content)

    print(f"Compiling {tex_path} with xelatex...")
    
    # Run xelatex twice to resolve page counts / LastPage
    cmd = ["xelatex", "-interaction=nonstopmode", f"{file_basename}.tex"]
    res1 = subprocess.run(cmd, cwd=output_dir, capture_output=True, text=True)
    if res1.returncode != 0:
        print("First xelatex pass finished with warnings/errors. Running second pass...")
        
    res2 = subprocess.run(cmd, cwd=output_dir, capture_output=True, text=True)
    
    if os.path.exists(pdf_path):
        print(f"Successfully generated PDF: {pdf_path}")
        # Clean aux files
        for ext in [".aux", ".log", ".out"]:
            aux_file = os.path.join(output_dir, f"{file_basename}{ext}")
            if os.path.exists(aux_file):
                try:
                    os.remove(aux_file)
                except Exception:
                    pass
        return pdf_path
    else:
        print(f"Error: PDF was not generated. Compilation log tail:")
        print(res2.stdout[-1500:])
        return None

def main():
    paper_id = sys.argv[1] if len(sys.argv) > 1 else "2025_CS2"
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    paper_dir = os.path.join(root_dir, "dataset", "papers", paper_id)
    pdf_books_dir = os.path.join(root_dir, "pdf_books")
    os.makedirs(pdf_books_dir, exist_ok=True)

    full_paper_path = os.path.join(paper_dir, "full_paper.json")
    if not os.path.exists(full_paper_path):
        print(f"full_paper.json not found in {paper_dir}. Running generate_full_paper_json.py...")
        subprocess.run([sys.executable, os.path.join(root_dir, "scripts", "generate_full_paper_json.py"), paper_id], check=True)

    # Ensure PNG logo exists from webp
    assets_dir = os.path.join(root_dir, "assets")
    png_logo_path = os.path.join(assets_dir, "studiva_butterfly_icon_transparent.png")
    webp_logo_path = os.path.join(assets_dir, "studiva_butterfly_icon_transparent.webp")
    if not os.path.exists(png_logo_path) and os.path.exists(webp_logo_path):
        try:
            from PIL import Image
            im = Image.open(webp_logo_path)
            im.save(png_logo_path)
            print(f"Converted {webp_logo_path} to {png_logo_path}")
        except Exception as e:
            print(f"Notice: Pillow conversion warning: {e}")

    with open(full_paper_path, "r", encoding="utf-8") as f:
        paper_data = json.load(f)

    print(f"Generating LaTeX source for {paper_id} ({len(paper_data.get('questions', []))} questions)...")
    tex_content = generate_latex_document(paper_data, png_logo_path)

    file_basename = f"{paper_id}_textbook"
    pdf_path = compile_latex_to_pdf(tex_content, paper_dir, file_basename)

    if pdf_path and os.path.exists(pdf_path):
        # Also copy to centralized pdf_books/
        dest_copy = os.path.join(pdf_books_dir, f"{paper_id}.pdf")
        shutil.copy2(pdf_path, dest_copy)
        print(f"Copied centralized PDF to: {dest_copy}")
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"Done! PDF size: {size_kb:.1f} KB")

if __name__ == "__main__":
    main()
