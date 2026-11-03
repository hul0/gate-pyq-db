"""Text cleaning, LaTeX/Markdown formatting, and symbol decoding for GATE questions."""

from __future__ import annotations

import re
from typing import Dict, Optional, Tuple

# Mapping of Symbol font / Private Use Area Unicode codes to standard Unicode / LaTeX characters
SYMBOL_REPLACEMENTS: Dict[str, str] = {
    "\uf02d": "−",   # minus sign
    "\uf0b4": "×",   # multiplication
    "\uf0b8": "÷",   # division
    "\uf0a2": "′",   # prime
    "\uf0b1": "±",   # plus-minus
    "\uf0b9": "≠",   # not equal
    "\uf0a3": "≤",   # less than or equal
    "\uf0b3": "≥",   # greater than or equal
    "\uf0a5": "∞",   # infinity
    "\uf0ce": "∈",   # element of
    "\uf0cf": "∉",   # not an element of
    "\uf0cc": "⊆",   # subset of or equal to
    "\uf0cd": "⊂",   # proper subset
    "\uf0c7": "∩",   # intersection
    "\uf0c8": "∪",   # union
    "\uf0d9": "∨",   # logical OR
    "\uf0da": "∧",   # logical AND
    "\uf0ac": "¬",   # logical NOT
    "\uf0ae": "→",   # right arrow
    "\uf0ab": "↔",   # left-right arrow
    "\uf0e0": "→",   # right arrow variant
    "\uf0de": "⇒",   # implies
    "\uf0db": "⇔",   # equivalent
    "\uf053": "Σ",   # summation / sigma
    "\uf050": "Π",   # product / pi
    "\uf057": "Ω",   # omega
    "\uf044": "Δ",   # delta
    "\uf0d6": "√",   # square root
    "\uf070": "π",   # pi
    "\uf061": "α",   # alpha
    "\uf062": "β",   # beta
    "\uf067": "γ",   # gamma
    "\uf064": "δ",   # delta
    "\uf065": "ε",   # epsilon
    "\uf073": "σ",   # sigma
    "\uf06c": "λ",   # lambda
    "\uf06d": "μ",   # mu
    "\uf071": "θ",   # theta
    "\uf0c5": "⊕",   # XOR / circled plus
    "\uf020": " ",
    "\uf028": "(",
    "\uf029": ")",
    "\uf03c": "<",
    "\uf03e": ">",
    "\uf03d": "=",
    "\uf05b": "[",
    "\uf05d": "]",
    "\uf07b": "{",
    "\uf07d": "}",
}

# Regex patterns for GATE PDF header/footer artifacts
BOILERPLATE_PATTERNS = [
    re.compile(r"Organizing Institute:\s*IIT\s+[^\n]+", re.IGNORECASE),
    re.compile(r"Organizing Institute:\s*IISc\s+[^\n]+", re.IGNORECASE),
    re.compile(r"Page\s+\d+\s+of\s+\d+", re.IGNORECASE),
    re.compile(r"Computer Science\s*(&|and)\s*Information Technology.*", re.IGNORECASE),
    re.compile(r"GATE\s*\d{4}\s*(General Aptitude.*|General Instructions.*|Set-?\s*\d+.*)?", re.IGNORECASE),
    re.compile(r"CS-A\s*\n\s*\d+/\d+", re.IGNORECASE),
    re.compile(r"^\s*CS\s*\n\s*\d+/\d+", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\s*GA\s*\n\s*\d+/\d+", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^\s*\d+/\d+\s*$", re.MULTILINE),
    re.compile(r"END OF THE QUESTION PAPER", re.IGNORECASE),
    re.compile(r"Graduate Aptitude Test in Engineering.*", re.IGNORECASE),
    re.compile(r"Q\.\s*\d+\s*[–\-]\s*Q\.\s*\d+\s*(?:carry|Carry)\s*(?:one|two|ONE|TWO|\d+)\s*mark(?:s)?\s*(?:each|Each)?\.?", re.IGNORECASE),
    re.compile(r"Q\d+\s*-\s*Q\d+\s*carry\s*(?:one|two|\d+)\s*mark(?:s)?\s*each\.?", re.IGNORECASE),
]


def decode_symbols(text: str) -> str:
    """Replace font-encoded PUA symbols with standard mathematical Unicode/LaTeX characters."""
    for pua_char, replacement in SYMBOL_REPLACEMENTS.items():
        if pua_char in text:
            text = text.replace(pua_char, replacement)
    return text


def strip_boilerplate(text: str) -> str:
    """Remove GATE header, footer, page number, and section instruction lines."""
    for pattern in BOILERPLATE_PATTERNS:
        text = pattern.sub("", text)
    return text


def clean_math_notation(text: str) -> str:
    """Standardize common math constructs to readable LaTeX / Markdown syntax."""
    # Convert obvious exponents like x^2, 2^n
    text = re.sub(r"\b([a-zA-Z0-9])\s*\^\s*([a-zA-Z0-9]+)\b", r"\1^{\2}", text)
    # Convert != to ≠
    text = text.replace("!=", "≠")
    # Convert <= and >=
    text = text.replace("<=", "≤").replace(">=", "≥")
    # Clean multiple spaces while preserving single spaces
    text = re.sub(r"[ \t]+", " ", text)
    return text


def clean_markdown_formatting(text: str) -> str:
    """Format and clean whitespace, preserve code blocks, and normalize line endings."""
    lines = [line.strip() for line in text.split("\n")]
    cleaned_lines = []
    prev_blank = False

    for line in lines:
        if not line:
            if not prev_blank:
                cleaned_lines.append("")
                prev_blank = True
        else:
            cleaned_lines.append(line)
            prev_blank = False

    result = "\n".join(cleaned_lines).strip()
    return result


def parse_options(question_block: str) -> Tuple[str, Optional[Dict[str, str]]]:
    """
    Extracts options (A, B, C, D) from the question block if present.
    Returns:
        (question_stem, options_dict_or_none)
    """
    # Look for (A) marker that starts an options section
    match_a = re.search(r"(?:\n|^|\s+)\(A\)\s*", question_block)
    if not match_a:
        # No options found -> NAT (Numerical Answer Type)
        stem = clean_markdown_formatting(question_block)
        return stem, None

    stem_raw = question_block[: match_a.start()]
    options_raw = question_block[match_a.start() :]

    # Regex to split (A), (B), (C), (D)
    opt_pattern = re.compile(
        r"(?:\n|^|\s+)\(([A-D])\)\s*([\s\S]*?)(?=(?:\n|^|\s+)\([A-D]\)|$)"
    )
    matches = opt_pattern.findall(options_raw)

    if not matches:
        return clean_markdown_formatting(question_block), None

    options: Dict[str, str] = {}
    for key, val in matches:
        clean_val = clean_markdown_formatting(val)
        options[key] = clean_val

    # Ensure at least A, B, C, D were recognized, or return partial
    stem = clean_markdown_formatting(stem_raw)
    return stem, options
