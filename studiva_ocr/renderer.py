"""
renderer.py - High-fidelity PDF page rendering and page-range resolution.
"""

import os
import subprocess
from typing import List, Dict

def get_pdf_page_count(pdf_path: str) -> int:
    """Return total number of pages in the PDF using pdfinfo."""
    try:
        out = subprocess.check_output(["pdfinfo", pdf_path], text=True)
        for line in out.splitlines():
            if line.startswith("Pages:"):
                return int(line.split(":")[1].strip())
    except Exception as e:
        raise RuntimeError(f"Failed to inspect PDF with pdfinfo: {e}")
    raise RuntimeError("Could not find 'Pages:' entry in pdfinfo output")

def parse_page_range(range_str: str, max_pages: int) -> List[int]:
    """
    Parse page ranges like '2-17', '2,4,6-10', or 'all'.
    Defaults to skipping page 1 (instructions/cover) if range_str is empty.
    """
    if not range_str or range_str.strip().lower() == "auto":
        if max_pages <= 1:
            return [1]
        return list(range(2, max_pages + 1))

    if range_str.strip().lower() == "all":
        return list(range(1, max_pages + 1))

    pages = set()
    parts = [p.strip() for p in range_str.split(",") if p.strip()]
    for part in parts:
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start = int(start_s.strip())
            end = int(end_s.strip())
            for p in range(start, end + 1):
                if 1 <= p <= max_pages:
                    pages.add(p)
        else:
            p = int(part)
            if 1 <= p <= max_pages:
                pages.add(p)

    return sorted(list(pages))

def render_pdf_pages(
    pdf_path: str,
    pages: List[int],
    output_dir: str,
    dpi: int = 200,
    force: bool = False
) -> Dict[int, str]:
    """
    Renders specified PDF pages to PNG using pdftoppm.
    Returns mapping: {page_number: image_path}.
    """
    os.makedirs(output_dir, exist_ok=True)
    rendered_map = {}

    for p in pages:
        expected_path = os.path.join(output_dir, f"page_{p:02d}.png")
        if not force and os.path.exists(expected_path) and os.path.getsize(expected_path) > 1000:
            rendered_map[p] = expected_path
            continue

        temp_prefix = os.path.join(output_dir, f"tmp_p{p}")
        cmd = [
            "pdftoppm",
            "-png",
            "-r", str(dpi),
            "-f", str(p),
            "-l", str(p),
            pdf_path,
            temp_prefix
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"pdftoppm failed on page {p}: {res.stderr}")

        # pdftoppm produces e.g. tmp_p2-2.png or tmp_p2-02.png
        generated_candidates = [
            f for f in os.listdir(output_dir)
            if f.startswith(f"tmp_p{p}-") and f.endswith(".png")
        ]
        if not generated_candidates:
            raise FileNotFoundError(f"pdftoppm did not produce image for page {p}")

        actual_file = os.path.join(output_dir, generated_candidates[0])
        os.replace(actual_file, expected_path)
        rendered_map[p] = expected_path

    return rendered_map
