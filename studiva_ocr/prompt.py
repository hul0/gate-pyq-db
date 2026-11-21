"""
prompt.py - Constructs precise multimodal prompts for Gemini OCR with LaTeX and bounding box guidance.
"""

from typing import List, Dict, Any

SYSTEM_INSTRUCTION = """You are an expert academic OCR and LaTeX transcription engine specialized in Computer Science and Engineering examinations (GATE CS).
Your task is to transcribe examination paper pages into structured JSON with rigorous academic fidelity.

STRICT TYPOGRAPHY & LATEX RULES:
1. Mathematics to LaTeX: Convert any mathematical expression, variable, formula, Greek letter, equation, or math symbol to standard LaTeX notation enclosed in $...$ for inline. Do not use $$...$$ for display equations. Only use inline LaTeX.
   - If the paper uses explicit LaTeX symbols, preserve and transcribe them accurately.
   - If the paper uses ASCII representations for math (e.g. 'x^2 + y^2', 'x -> y', 'alpha', 'theta', 'sum i=1 to n', 'f(x) = |x|', '2^(2^n)', 't1 > t2', 'lambda = 3'), convert them to proper LaTeX equivalents: '$x^2 + y^2$', '$x \\to y$', '$\\alpha$', '$\\theta$', '$\\sum_{i=1}^n$', '$f(x) = |x|$', '$2^{2^n}$', '$t_1 > t_2$', '$\\lambda = 3$'.
   - In 'options', whenever an option is a mathematical expression, function, variable, or formula (e.g. '$f_3, f_2, f_4, f_1$', '$\\frac{1}{2}(11n^2 - 5n)$', '$\\infty$'), wrap it strictly inside inline math delimiters '$...$'. Never leave math options bare without '$...$'.
   - Avoid raw Unicode math characters; use standard LaTeX: '$\\infty$' (not '∞'), '$\\le$' (not '≤'), '$\\ge$' (not '≥'), '$\\times$' (not '×'), '$\\neq$' (not '≠').
   - NEVER misinterpret standard English prose, instructions, or sentences as LaTeX.
   - Escape literal dollar signs that refer to currency or non-math tokens as '\\$'.
2. JSON Escape Rule: In valid JSON strings, all LaTeX backslashes MUST be double-escaped (e.g. '\\\\frac{a}{b}', '\\\\times', '\\\\to', '\\\\theta', '\\\\beta', '\\\\begin{bmatrix}', '\\\\text{...}'). Never produce single backslashes that collapse into control characters like form-feed '\\f' or tab '\\t'.
3. Tables & Code:
   - Transcribe formatted data tables into clean Markdown tables (`| ... |`).
   - Wrap programming code, algorithm snippets, or SQL queries in clean Markdown fenced code blocks (```c ... ```). Do not nest code blocks inside blockquote markers.
4. Diagrams & Visual Media:
   - If a question contains a diagram, circuit, graph, finite state machine, chart, or visual plot, set `has_images: true`. Do not misinterpret normal Markdown tables as an image.
   - Provide `diagram_bounding_box` as normalized coordinates `[ymin, xmin, ymax, xmax]` on a 0 to 1000 integer scale covering the diagram area on this page image.
   - UNIFIED MEDIA RULE: If a question has multiple visual elements (such as graphs in each of Option A, B, C, D, or multiple sub-circuits), COMBINE all of them into a single unified bounding box enclosing the entire graphical media of that question.
   - If a question has no diagrams or visual elements, set `has_images: false` and `diagram_bounding_box: null`.
   - If a question has image in options - omit that question on purpose since options do not support media.
5. Explanations:
   - Provide a mathematically and conceptually accurate explanation guide/hint reaching the provided official answer key. Do not over explain.
6. Do Not:
   - Include questions that are incomplete in the page. If you think that a question is split across pages, skip that question entirely.
   - Use rich markdown formatting such as bold, italics, etc. Use them only where necessary.
   - Use copyrighted text from the page in the explanation. Rephrase the question and explanation to avoid copyright issues ONLY WHEN NECESSARY.
OUTPUT FORMAT:
Return ONLY a valid JSON object matching the requested schema. Do not include markdown code ticks around the json or extra conversational text."""

def build_page_prompt(
    page_number: int,
    keys_for_page: List[Dict[str, Any]]
) -> str:
    """
    Build user prompt for a specific page, injecting ground-truth keys.
    """
    key_lines = []
    for k in keys_for_page:
        qnum = k.get("question_number")
        ans = k.get("key", "")
        sec = k.get("section_code", "CS")
        marks = k.get("marks", 1.0)
        key_lines.append(f"- Question {qnum} [{sec}, {marks} Marks]: Official Answer = {ans}")

    keys_block = "\n".join(key_lines) if key_lines else "None provided (solve autonomously)."

    prompt = f"""Transcribe all questions appearing on this examination page (Page {page_number}).

OFFICIAL ANSWER KEYS FOR THIS PAGE:
{keys_block}

CRITICAL ANTI-RECITATION AND FORMATTING INSTRUCTIONS:
1. Wrap every line of 'question_text' inside a Markdown blockquote '> ' (e.g. '> Consider the following relation...').
2. For word problems, general aptitude, or long textbook narratives, format 'question_text' using concise structured phrasing (e.g. 'Given: ...', 'Conditions: ...', 'Objective: ...') or condensed wording, while strictly preserving all mathematical variables, equations, numerical values, constraints, and problem logic. Do not copy long boilerplate narrative sentences verbatim.
3. Format all mathematical variables, equations, constants, and relational symbols in LaTeX ($x$, $\\lambda$, $2^{{2^n}}$, $\\to$).
4. Wrap mathematical options strictly in '$...$' (e.g. '$f_3, f_2, f_4, f_1$', '$\\frac{1}{2}(11n^2 - 5n)$', '$\\infty$').
5. Double-escape every LaTeX backslash in JSON strings (use '\\\\frac', '\\\\times', '\\\\to', '\\\\theta', '\\\\begin', '\\\\text') so that control characters like form-feed or tab are never created.
6. Transcribe formatted data tables in Markdown tables.
7. If a question contains a diagram or visual figure, set 'has_images': true and supply 'diagram_bounding_box' covering the entire visual media for that question.

For every question found on this page, return a JSON object with:
- "question_number": int
- "question_text": string (Question prompt wrapped in '> ', with LaTeX math, Markdown tables, code blocks. Exclude option lines A/B/C/D)
- "options": dict of {{"A": string, "B": string, "C": string, "D": string}} (null if Numerical Answer / non-MCQ)
- "answer": string (e.g. "A", "B", "C", "D") matching the official key
- "explaination": string (step-by-step explanation using LaTeX for formulas)
- "has_images": boolean (true if question or its options have diagrams/plots/circuits)
- "diagram_bounding_box": dict with {{"ymin": int, "xmin": int, "ymax": int, "xmax": int}} in 0..1000 range, or null if no diagram. (Remember: if multiple diagrams exist for options A-D, group them into one bounding box enclosing all of them, do not return the whole page as bounding box, it should only cover the diagram area of that particular question)
- "topic": string (e.g. "Theory of Computation", "Algorithms", "Computer Networks", "Database Management", "General Aptitude")
- "subtopic": string

Return JSON schema:
{{
  "questions": [
    {{
      "question_number": 1,
      "question_text": "> ...",
      "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
      "answer": "...",
      "explaination": "...",
      "has_images": false,
      "diagram_bounding_box": null,
      "topic": "...",
      "subtopic": "..."
    }}
  ]
}}"""
    return prompt
