#!/usr/bin/env python3
"""
generate_paper_pdf.py

Advanced academic PDF generator for GATE exam papers.
Design Philosophy:
- Typography: Pure modern Sans-Serif (DejaVu Sans) for all body text, headings, options, and explanations.
- Mathematics: High-fidelity TeX math cursive/italic for formulas and variables.
- Robust Markdown & LaTeX Engine:
  * Automatic detection and wrapping of bare LaTeX math commands outside math mode.
  * Prevention of math-mode leaks (auto-balancing unclosed delimiters).
  * Native translation of Markdown bold, italic, code blocks, lists, and tables.
  * Clean stripping of redundant option labels (e.g. '(A) (A)') and blockquotes.
  * Embedded high-contrast 1-bit monochrome diagrams.
"""

import os
import sys
import json
import re
import base64
import argparse
import subprocess
import tempfile
import shutil

# Common LaTeX math macros that must always be inside math mode ($...$)
MATH_MACROS = [
    r'\\frac\{[^{}]*\}\{[^{}]*\}',
    r'\\sqrt\{[^{}]*\}',
    r'\\sum(?:_[^{}\s]+)?(?:\^[^{}\s]+)?',
    r'\\prod(?:_[^{}\s]+)?(?:\^[^{}\s]+)?',
    r'\\int(?:_[^{}\s]+)?(?:\^[^{}\s]+)?',
    r'\\lim(?:_[^{}\s]+)?',
    r'\\left[()\[\]|.\\]',
    r'\\right[()\[\]|.\\]',
    r'\\to\b', r'\\gets\b', r'\\implies\b', r'\\iff\b',
    r'\\le\b', r'\\ge\b', r'\\neq\b', r'\\approx\b', r'\\equiv\b',
    r'\\in\b', r'\\notin\b', r'\\subset\b', r'\\subseteq\b',
    r'\\cup\b', r'\\cap\b', r'\\times\b', r'\\cdot\b', r'\\oplus\b',
    r'\\neg\b', r'\\land\b', r'\\lor\b',
    r'\\alpha\b', r'\\beta\b', r'\\gamma\b', r'\\delta\b', r'\\epsilon\b',
    r'\\lambda\b', r'\\sigma\b', r'\\theta\b', r'\\phi\b', r'\\omega\b',
    r'\\pi\b', r'\\mu\b', r'\\infty\b', r'\\partial\b', r'\\dots\b', r'\\cdots\b'
]
BARE_MATH_REGEX = re.compile('(' + '|'.join(MATH_MACROS) + ')')

def wrap_bare_math_outside_delimiters(text: str) -> str:
    """Wraps standalone LaTeX math macros that occur outside $...$ in $...$."""
    # Split by existing math blocks ($$...$$, $...$, \[...\], \(...\))
    math_pattern = r'(\$\$.*?\$\$|(?<!\\)\$.*?(?<!\\)\$|\\\[.*?\\\]|\\\(.*?\\\))'
    parts = re.split(math_pattern, text, flags=re.DOTALL)

    wrapped_parts = []
    for idx, part in enumerate(parts):
        if idx % 2 == 1:
            # Already inside math environment
            wrapped_parts.append(part)
        else:
            # Outside math: wrap any isolated math macros
            p = BARE_MATH_REGEX.sub(r'$\1$', part)
            wrapped_parts.append(p)
    return "".join(wrapped_parts)

def balance_math_delimiters(text: str) -> str:
    """Ensures an even count of unescaped $ delimiters so math mode never leaks."""
    # Count unescaped dollars
    dollars = re.findall(r'(?<!\\)\$', text)
    if len(dollars) % 2 != 0:
        # Close open math mode at the end
        text = text + "$"
    return text

def clean_markdown_text(text: str) -> str:
    """Pre-cleans markdown: strips leading blockquote markers and headings."""
    if not text:
        return ""

    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        s = line.strip()
        # Strip blockquote '>'
        if s.startswith(">"):
            s = s[1:].strip()
        # Convert Markdown headings '### Heading' to bold text
        if s.startswith("### "):
            s = f"**{s[4:].strip()}**"
        elif s.startswith("## "):
            s = f"**{s[3:].strip()}**"
        elif s.startswith("# "):
            s = f"**{s[2:].strip()}**"
        cleaned_lines.append(s)

    return "\n".join(cleaned_lines)

def convert_markdown_lists(text: str) -> str:
    """Converts bullet points (- item, * item) to clean LaTeX bullets."""
    lines = text.split("\n")
    out = []
    for line in lines:
        s = line.strip()
        if s.startswith("- ") or s.startswith("* "):
            bullet_body = s[2:].strip()
            out.append(f"\\par\\quad \\textbullet\\quad {bullet_body}")
        else:
            out.append(line)
    return "\n".join(out)

def sanitize_latex(text: str) -> str:
    """
    Academic LaTeX converter:
    1. Pre-cleans markdown structures (quotes, lists, headings).
    2. Wraps bare math macros in $...$.
    3. Handles code blocks and inline code `code`.
    4. Escapes active TeX characters outside math.
    5. Converts Markdown bold/italic.
    6. Balances delimiters.
    """
    if not text:
        return ""

    # Repair LaTeX commands corrupted by JSON escape sequence decodings
    text = re.sub(r'[\x0c]rac\b', r'\\frac', text)
    text = re.sub(r'[\t]imes\b', r'\\times', text)
    text = re.sub(r'[\t]heta\b', r'\\theta', text)
    text = re.sub(r'[\t]au\b', r'\\tau', text)
    text = re.sub(r'[\t]o\b', r'\\to', text)
    text = re.sub(r'[\r\n]ight\b', r'\\right', text)
    text = re.sub(r'[\x08]eta\b', r'\\beta', text)

    # Clean markdown blockquotes and headings
    text = clean_markdown_text(text)

    # Convert markdown bullet lists
    text = convert_markdown_lists(text)

    # Wrap bare math macros that lack $ delimiters
    text = wrap_bare_math_outside_delimiters(text)

    # Convert inline code `code` to \texttt{...} before splitting
    def code_repl(m):
        code_str = m.group(1)
        code_str = code_str.replace('\\', '\\textbackslash{}')
        code_str = code_str.replace('_', r'\_').replace('&', r'\&').replace('%', r'\%')
        code_str = code_str.replace('#', r'\#').replace('^', r'\^{}').replace('~', r'\~{}')
        return r'\texttt{' + code_str + '}'

    text = re.sub(r'`([^`\n]+)`', code_repl, text)

    # Split into math vs text segments
    math_pattern = r'(\$\$.*?\$\$|(?<!\\)\$.*?(?<!\\)\$|\\\[.*?\\\]|\\\(.*?\\\)|\\begin\{[a-zA-Z*]+\}.*?\\end\{[a-zA-Z*]+\})'
    parts = re.split(math_pattern, text, flags=re.DOTALL)

    escaped = []
    for idx, part in enumerate(parts):
        if idx % 2 == 1:
            # Inside math environment - preserve verbatim
            escaped.append(part)
        else:
            p = part
            # Escape active TeX characters
            p = re.sub(r'(?<!\\)&', r'\&', p)
            p = re.sub(r'(?<!\\)%', r'\%', p)
            p = re.sub(r'(?<!\\)#', r'\#', p)
            p = re.sub(r'(?<!\\)_', r'\_', p)
            p = re.sub(r'(?<!\\)\^', r'\^{}', p)
            p = p.replace('~', r'\~{}')
            # Handle Indian Rupee symbol
            p = p.replace('₹', 'Rs.~')

            # Convert markdown **bold** to \textbf{...}
            p = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', p)
            p = re.sub(r'__(.*?)__', r'\\textbf{\1}', p)

            # Convert markdown *italic* only when surrounded by non-alphanumeric
            p = re.sub(r'(?<![a-zA-Z0-9*])\*([^\n*]+)\*(?![a-zA-Z0-9*])', r'\\textit{\1}', p)
            escaped.append(p)

    out = "".join(escaped)
    return balance_math_delimiters(out)

def convert_markdown_table_to_latex(text: str) -> str:
    """Converts Markdown tables (| col1 | col2 |) to booktabs tabular environments."""
    lines = text.split("\n")
    out_lines = []
    table_lines = []
    in_table = False

    for line in lines:
        sline = line.strip()
        if sline.startswith("|") and sline.endswith("|"):
            in_table = True
            table_lines.append(sline)
        else:
            if in_table:
                out_lines.append(format_clean_table(table_lines))
                table_lines = []
                in_table = False
            out_lines.append(line)
    if in_table and table_lines:
        out_lines.append(format_clean_table(table_lines))

    return "\n".join(out_lines)

def format_clean_table(table_lines):
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
        alignments = ["c"] * num_cols

    col_spec = "".join(alignments)
    res = [
        r"\begin{center}\small",
        f"\\begin{{tabular}}{{@{{}}{col_spec}@{{}}}}",
        r"\toprule"
    ]
    # Header row
    header_cells = [sanitize_latex(c) for c in rows[0]]
    while len(header_cells) < num_cols:
        header_cells.append("")
    res.append(" & ".join([f"\\textbf{{{c}}}" if c else "" for c in header_cells]) + r" \\")
    res.append(r"\midrule")

    # Body rows
    for r in rows[1:]:
        cells = [sanitize_latex(c) for c in r]
        while len(cells) < num_cols:
            cells.append("")
        res.append(" & ".join(cells) + r" \\")

    res.append(r"\bottomrule")
    res.append(r"\end{tabular}\end{center}")
    return "\n".join(res)

def convert_code_blocks(text: str) -> str:
    """Converts markdown ```code``` fences to listings environments."""
    code_pattern = r'```(?:c|C|cpp|sql|text|python)?\s*\n(.*?)\n```'
    def replacer(m):
        content = m.group(1)
        return "\\begin{lstlisting}\n" + content + "\n\\end{lstlisting}"
    return re.sub(code_pattern, replacer, text, flags=re.DOTALL)

def clean_option_text(opt_str: str, key_letter: str) -> str:
    """Strips duplicate leading option letters like '(A) ', 'A. ', 'A) '."""
    s = opt_str.strip()
    prefix_patterns = [
        rf'^\({key_letter}\)\s*',
        rf'^{key_letter}\.\s*',
        rf'^{key_letter}\)\s*',
        rf'^\({key_letter.lower()}\)\s*',
        rf'^{key_letter.lower()}\.\s*'
    ]
    for p in prefix_patterns:
        s = re.sub(p, '', s)
    return s.strip()

def dump_media_images(q, media_dir):
    r"""Extracts and writes base64 embedded diagrams to disk for LaTeX \includegraphics."""
    image_paths = []
    media_dict = q.get("media")
    if not media_dict or not isinstance(media_dict, dict):
        return image_paths
    for key, item in media_dict.items():
        if isinstance(item, dict) and "data" in item:
            data_str = item["data"]
            if "," in data_str:
                b64_part = data_str.split(",", 1)[1]
            else:
                b64_part = data_str
            try:
                raw_bytes = base64.b64decode(b64_part)
                out_name = f"media_{q.get('question_number', 'q')}_{key}.png"
                out_path = os.path.join(media_dir, out_name)
                with open(out_path, "wb") as img_f:
                    img_f.write(raw_bytes)
                image_paths.append(out_path)
            except Exception as e:
                print(f"Error decoding media {key}: {e}")
    return image_paths

def generate_latex(data, media_dir):
    year = data.get("year", 2011)
    subject = data.get("subject", "Computer Science and Information Technology")

    tex = [
        r"\documentclass[11pt,a4paper]{article}",
        r"\usepackage{fontspec}",
        r"\usepackage{amsmath,amssymb}",
        r"\usepackage{graphicx}",
        r"\usepackage[export]{adjustbox}",
        r"\usepackage{geometry}",
        r"\usepackage{enumitem}",
        r"\usepackage{booktabs}",
        r"\usepackage{listings}",
        r"\usepackage{needspace}",
        r"",
        r"% Typography: DejaVu Sans for text, Computer Modern cursive for math",
        r"\setmainfont{DejaVu Sans}[Scale=0.95]",
        r"\setsansfont{DejaVu Sans}[Scale=0.95]",
        r"\setmonofont{DejaVu Sans Mono}[Scale=0.85]",
        r"\renewcommand{\familydefault}{\sfdefault}",
        r"",
        r"\geometry{top=20mm, bottom=20mm, left=20mm, right=20mm}",
        r"\setlength{\parindent}{0pt}",
        r"\setlength{\parskip}{5pt}",
        r"",
        r"\lstset{",
        r"  basicstyle=\small\ttfamily,",
        r"  frame=none,",
        r"  tabsize=2,",
        r"  breaklines=true,",
        r"  numbers=none,",
        r"  xleftmargin=12pt",
        r"}",
        r"",
        r"\begin{document}",
        r"",
        r"{\Large \textbf{GATE " + str(year) + r": " + subject + r"}}\\[3pt]",
        r"\rule{\linewidth}{0.6pt}",
        r"\vspace{10pt}"
    ]

    current_section = None

    for q in data.get("questions", []):
        sec_name = q.get("section", "Computer Science and Information Technology")
        q_num = q.get("question_number", 0)

        # Section Divider
        if sec_name != current_section:
            current_section = sec_name
            tex.append(r"\vspace{14pt}")
            tex.append(f"{{\\large \\textbf{{{sanitize_latex(sec_name)}}}}}\\\\[2pt]")
            tex.append(r"\rule{\linewidth}{0.4pt}")
            tex.append(r"\vspace{8pt}")

        # Question Prompt
        raw_text = q.get("question_text", "")
        # Remove lingering markdown image links
        raw_text = re.sub(r'!\[.*?\]\(.*?\)', '', raw_text)

        body = convert_code_blocks(raw_text)
        body = convert_markdown_table_to_latex(body)
        body = sanitize_latex(body)
        body = body.replace("\n\n", "\n\\par\\vspace{3pt}\n")

        tex.append(r"\needspace{6\baselineskip}")
        tex.append(f"\\textbf{{Q.{q_num}}} \\quad {body}\\par\\vspace{{4pt}}")

        # Visual Media / Diagrams
        img_paths = dump_media_images(q, media_dir)
        for ip in img_paths:
            p_clean = ip.replace("\\", "/")
            tex.append(r"\begin{center}")
            tex.append(f"\\includegraphics[max width=0.65\\linewidth, max height=60mm, keepaspectratio]{{{p_clean}}}")
            tex.append(r"\end{center}\vspace{4pt}")

        # Multiple Choice Options
        options = q.get("options")
        if options and isinstance(options, dict) and any(options.values()):
            tex.append(r"\begin{enumerate}[label=(\textbf{\Alph*}), leftmargin=24pt, itemsep=2pt, topsep=2pt]")
            for k in ["A", "B", "C", "D"]:
                if k in options and options[k]:
                    clean_str = clean_option_text(str(options[k]), k)
                    sanitized_opt = sanitize_latex(clean_str)
                    tex.append(f"\\item {sanitized_opt}")
            tex.append(r"\end{enumerate}\vspace{4pt}")

        # Answer and Explanation
        ans = q.get("answer", "")
        exp = q.get("explaination", "")
        if exp:
            exp_clean = convert_code_blocks(exp)
            exp_clean = sanitize_latex(exp_clean)
            exp_clean = exp_clean.replace("\n\n", "\n\\par\\vspace{2pt}\n")
        else:
            exp_clean = "Answer directly deduced from official answer key."

        tex.append(f"\\textbf{{Answer:}} {sanitize_latex(str(ans))}\\par\\vspace{{2pt}}")
        tex.append(f"\\textbf{{Explanation:}} {exp_clean}\\par\\vspace{{10pt}}")
        tex.append(r"\hrule\vspace{10pt}")

    tex.append(r"\end{document}")
    return "\n".join(tex)

def compile_pdf(json_path: str, output_pdf: str) -> bool:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    temp_dir = tempfile.mkdtemp(prefix="gate_clean_pdf_")
    media_dir = os.path.join(temp_dir, "media")
    os.makedirs(media_dir, exist_ok=True)

    tex_content = generate_latex(data, media_dir)
    tex_path = os.path.join(temp_dir, "paper.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex_content)

    print(f"Compiling publication-grade PDF using XeLaTeX for: {json_path}")
    res = subprocess.run(
        ["xelatex", "-interaction=nonstopmode", "-output-directory=" + temp_dir, tex_path],
        capture_output=True,
        text=True
    )

    pdf_temp = os.path.join(temp_dir, "paper.pdf")
    if os.path.exists(pdf_temp):
        os.makedirs(os.path.dirname(os.path.abspath(output_pdf)), exist_ok=True)
        shutil.copy(pdf_temp, output_pdf)
        print(f"Successfully generated clean PDF: {output_pdf}")
        success = True
    else:
        print(f"Compilation failed for {json_path}!")
        log_file = os.path.join(temp_dir, "paper.log")
        if os.path.exists(log_file):
            with open(log_file) as lf:
                lines = lf.readlines()
                print("".join(lines[-50:]))
        success = False

    shutil.rmtree(temp_dir, ignore_errors=True)
    return success

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Academic Q&A PDF Generator for GATE CS PYQ")
    parser.add_argument("--input", required=True, help="Input paper JSON file")
    parser.add_argument("--output", required=True, help="Output PDF file path")
    args = parser.parse_args()

    compile_pdf(args.input, args.output)
