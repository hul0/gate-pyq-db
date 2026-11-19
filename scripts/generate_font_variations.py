#!/usr/bin/env python3
"""
generate_font_variations.py

Generates 5 distinct textbook font variations for 2025 CS2:
- Variation A: Times Roman (Liberation Serif) - Universal academic/exam textbook standard
- Variation B: Bitstream Charter - Clean, high-legibility laser print serif
- Variation C: Bookman (URW Bookman) - Classic school/undergraduate textbook typeface
- Variation D: Noto Serif - Modern balanced editorial serif
- Variation E: DejaVu Serif - Robust technical & mathematical serif

Outputs saved to:
    temp/variation_A_Times.pdf
    temp/variation_B_Charter.pdf
    temp/variation_C_Bookman.pdf
    temp/variation_D_NotoSerif.pdf
    temp/variation_E_DejaVuSerif.pdf
"""

import os
import sys
import json
import subprocess
import shutil

# Import generator functions from generate_paper_textbook
sys.path.insert(0, os.path.dirname(__file__))
from generate_paper_textbook import (
    format_question_body,
    format_options,
    format_solution_panel
)

FONT_VARIATIONS = {
    "A": {
        "name": "Times Roman (Liberation Serif)",
        "file_name": "variation_A_Times",
        "font_decl": r"\usepackage{fontspec}" + "\n" + r"\setmainfont{Liberation Serif}",
        "desc": "Universal standard for engineering exam papers and textbooks (Pearson, McGraw-Hill, Springer)."
    },
    "B": {
        "name": "Bitstream Charter",
        "file_name": "variation_B_Charter",
        "font_decl": r"\usepackage{fontspec}" + "\n" + r"\setmainfont{Bitstream Charter}",
        "desc": "Crisp, robust typeface optimized specifically for high legibility on laser printouts."
    },
    "C": {
        "name": "Bookman (URW Bookman)",
        "file_name": "variation_C_Bookman",
        "font_decl": r"\usepackage{fontspec}" + "\n" + r"\setmainfont{URW Bookman}",
        "desc": "Classic Century/Bookman style widely used in foundational school and university textbooks."
    },
    "D": {
        "name": "Noto Serif",
        "file_name": "variation_D_NotoSerif",
        "font_decl": r"\usepackage{fontspec}" + "\n" + r"\setmainfont{Noto Serif}",
        "desc": "Modern academic serif with clean proportions, clear spacing, and sharp character contours."
    },
    "E": {
        "name": "DejaVu Serif",
        "file_name": "variation_E_DejaVuSerif",
        "font_decl": r"\usepackage{fontspec}" + "\n" + r"\setmainfont{DejaVu Serif}",
        "desc": "Sturdy, open-aperture technical serif with solid character weight and strong contrast."
    }
}

def generate_tex_for_font(paper_data, var_key, var_info):
    year = paper_data.get("year", 2025)
    session = paper_data.get("session", "CS2")
    subject = paper_data.get("subject", "Computer Science and Information Technology")
    questions = paper_data.get("questions", [])

    tex = [
        r"""\documentclass[a4paper,10pt]{article}
\usepackage{amsmath,amssymb}
\usepackage[most]{tcolorbox}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{lastpage}
\usepackage{booktabs}
\usepackage{listings}
\usepackage{microtype}
""" + var_info["font_decl"] + r"""

\geometry{
    a4paper,
    top=1.5cm,
    bottom=1.8cm,
    left=1.2cm,
    right=1.2cm
}

% Header and Footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\scshape GATE """ + f"{year} {subject} ({session})" + r"""}
\fancyhead[R]{\small\scshape Variation """ + var_key + r""" --- """ + var_info["name"] + r"""}
\fancyfoot[C]{\small Page \thepage\ of \pageref{LastPage}}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0.4pt}

\lstset{
    basicstyle=\footnotesize\ttfamily,
    numbers=none,
    frame=none,
    tabsize=2,
    breaklines=true,
    showstringspaces=false
}

\begin{document}

% Title Block
\begin{center}
    {\LARGE \textbf{GATE """ + str(year) + r""": Computer Science \& IT}}\\[0.25em]
    {\large \textbf{Session """ + str(session) + r""" --- Problem Compendium with Side-by-Side Solutions}}\\[0.35em]
    {\footnotesize \textsc{Typography Sample: Option """ + var_key + r""" (""" + var_info["name"] + r""")} \quad$\cdot$\quad \textsc{Reference: GATE 2026 Syllabus}}\\[0.4em]
    \rule{\textwidth}{0.6pt}
    \vspace{2pt}
    {\footnotesize \textit{Practice Note: Cover the right column with a sheet of paper or ruler during mock attempts; tick your answers in the checkboxes on the left.}}
    \vspace{-4pt}
\end{center}
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
            r"    sidebyside,",
            r"    sidebyside align=top,",
            r"    lefthand width=0.55\textwidth,",
            r"    colback=white,",
            r"    colframe=black!40,",
            r"    colbacklower=white,",
            r"    arc=0.8mm,",
            r"    boxrule=0.4pt,",
            r"    top=4pt, bottom=4pt, left=5pt, right=5pt,",
            r"    middle=5pt",
            r"]",
            box_header,
            r"\vspace{1pt}\hrule height 0.3pt\vspace{3pt}",
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
            r"\vspace{-4pt}"
        ])
        tex.append(box_tex)

    tex.append(r"\end{document}")
    return "\n".join(tex)

def compile_pdf(tex_str, out_dir, base_name):
    tex_path = os.path.join(out_dir, f"{base_name}.tex")
    pdf_path = os.path.join(out_dir, f"{base_name}.pdf")

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex_str)

    cmd = ["xelatex", "-interaction=nonstopmode", f"{base_name}.tex"]
    subprocess.run(cmd, cwd=out_dir, capture_output=True, text=True)
    subprocess.run(cmd, cwd=out_dir, capture_output=True, text=True)

    if os.path.exists(pdf_path):
        for ext in [".aux", ".log", ".out", ".tex"]:
            aux = os.path.join(out_dir, f"{base_name}{ext}")
            if os.path.exists(aux):
                try:
                    os.remove(aux)
                except Exception:
                    pass
        return pdf_path
    return None

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    temp_dir = os.path.join(root_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    paper_path = os.path.join(root_dir, "dataset", "papers", "2025_CS2", "full_paper.json")
    with open(paper_path, "r", encoding="utf-8") as f:
        paper_data = json.load(f)

    print("Generating 5 font variations in temp/ ...")
    generated = {}
    for code, info in sorted(FONT_VARIATIONS.items()):
        print(f"Generating Variation {code} ({info['name']})...")
        tex_code = generate_tex_for_font(paper_data, code, info)
        pdf = compile_pdf(tex_code, temp_dir, info["file_name"])
        if pdf and os.path.exists(pdf):
            size_kb = os.path.getsize(pdf) / 1024
            generated[code] = {
                "name": info["name"],
                "file": pdf,
                "size_kb": size_kb,
                "desc": info["desc"]
            }
            print(f"-> Generated {pdf} ({size_kb:.1f} KB)")
        else:
            print(f"-> Failed to generate {info['file_name']}.pdf")

    print("\nSummary of Generated Variations:")
    for code, d in generated.items():
        print(f"[{code}] {d['name']}: {d['file']} ({d['size_kb']:.1f} KB)")

if __name__ == "__main__":
    main()

