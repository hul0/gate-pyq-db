"""Image and diagram detection for GATE question papers.

Identifies both raster images (figures, option diagrams) and vector drawings
(circuit diagrams, state machines, graphs) belonging to questions, while filtering
out recurring document-level watermarks, text box borders, and header/footer institute logos.
"""

from __future__ import annotations

from collections import Counter
from typing import Dict, List, Set, Tuple
import pymupdf


class ImageDetector:
    """Detects images and diagrams within pages and question boundaries."""

    def __init__(self, doc: pymupdf.Document):
        self.doc = doc
        self.recurring_xrefs: Set[int] = self._detect_recurring_xrefs()
        self.recurring_drawings: Set[Tuple[float, float, float, float]] = (
            self._detect_recurring_drawings()
        )
        self.page_visual_elements: Dict[int, List[pymupdf.Rect]] = {}
        self._precompute_page_visuals()

    def _detect_recurring_xrefs(self) -> Set[int]:
        """Identifies image xrefs that appear repeatedly across pages (logos/watermarks)."""
        img_counts: Counter[int] = Counter()
        for page in self.doc:
            for img in page.get_images():
                xref = img[0]
                img_counts[xref] += 1

        recurring = set()
        for xref, count in img_counts.items():
            if count > 2:
                recurring.add(xref)

        return recurring

    def _detect_recurring_drawings(self) -> Set[Tuple[float, float, float, float]]:
        """Identifies vector drawing bounding boxes that appear repeatedly across pages (watermarks)."""
        drawing_counts: Counter[Tuple[float, float, float, float]] = Counter()
        for page in self.doc:
            try:
                for d in page.get_drawings():
                    r = d["rect"]
                    if r.width >= 20 and r.height >= 20:
                        key = (
                            round(r.x0, 1),
                            round(r.y0, 1),
                            round(r.x1, 1),
                            round(r.y1, 1),
                        )
                        drawing_counts[key] += 1
            except Exception:
                pass

        recurring = set()
        for key, count in drawing_counts.items():
            if count > 2:
                recurring.add(key)

        return recurring

    def _precompute_page_visuals(self) -> None:
        """Finds non-watermark raster images and significant vector diagrams for each page."""
        for p_idx in range(len(self.doc)):
            page = self.doc[p_idx]
            page_rect = page.rect
            visual_rects: List[pymupdf.Rect] = []

            # 1. Raster images
            for img in page.get_images():
                xref = img[0]
                if xref in self.recurring_xrefs:
                    continue

                for r in page.get_image_rects(xref):
                    if r.width < 15 and r.height < 15:
                        continue
                    if r.y1 < 75 or r.y0 > (page_rect.height - 50):
                        continue
                    visual_rects.append(r)

            # 2. Vector drawings (circuits, graphs, state machines)
            try:
                for d in page.get_drawings():
                    r = d["rect"]
                    if r.width >= 25 and r.height >= 25:
                        if r.y1 < 75 or r.y0 > (page_rect.height - 50):
                            continue
                        if (
                            r.width > (page_rect.width * 0.95)
                            and r.height > (page_rect.height * 0.95)
                        ):
                            continue

                        # Filter out table/box text borders (full-width rectangles)
                        item_types = {item[0] for item in d.get("items", [])}
                        if r.width > 350 and item_types == {"re"}:
                            continue

                        key = (
                            round(r.x0, 1),
                            round(r.y0, 1),
                            round(r.x1, 1),
                            round(r.y1, 1),
                        )
                        if key in self.recurring_drawings:
                            continue

                        visual_rects.append(r)
            except Exception:
                pass

            self.page_visual_elements[p_idx] = visual_rects

    def question_has_image(
        self,
        page_idx: int,
        y0: float,
        y1: float,
        buffer: float = 5.0,
    ) -> bool:
        """
        Determines whether any raster image or significant drawing overlaps with
        the question's vertical bounding box [y0 - buffer, y1 + buffer] on page `page_idx`.
        """
        visuals = self.page_visual_elements.get(page_idx, [])
        if not visuals:
            return False

        q_top = y0 - buffer
        q_bottom = y1 + buffer

        for r in visuals:
            if not (r.y1 < q_top or r.y0 > q_bottom):
                return True

        return False

    def is_page_scanned(self, page_idx: int) -> bool:
        """Detects if the page is a pure scanned raster image with no extractable text."""
        page = self.doc[page_idx]
        text_len = len(page.get_text().strip())
        return text_len < 30
