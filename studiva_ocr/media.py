"""
media.py - Hybrid diagram detection, OpenCV contour bounding box refinement, and 1-bit monochrome PNG conversion.
"""

import os
import io
import base64
from typing import Dict, Any, Optional, Tuple
from PIL import Image

try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

def extract_and_binarize_media(
    page_image_path: str,
    bbox: Dict[str, int],
    media_key: str,
    output_dir: Optional[str] = None,
    padding_pct: float = 0.0
) -> Optional[Dict[str, Any]]:
    """
    Crops diagram using normalized bbox [ymin, xmin, ymax, xmax] (0..1000),
    snaps tightly to black-ink contours via OpenCV, converts to 1-bit PNG,
    and returns canonical media dict with base64 data URI.
    """
    if not os.path.exists(page_image_path) or not bbox:
        return None

    try:
        pil_img = Image.open(page_image_path).convert("RGB")
    except Exception as e:
        print(f"Error opening image {page_image_path}: {e}")
        return None

    w_full, h_full = pil_img.size

    ymin = max(0, min(1000, bbox.get("ymin", 0)))
    xmin = max(0, min(1000, bbox.get("xmin", 0)))
    ymax = max(0, min(1000, bbox.get("ymax", 1000)))
    xmax = max(0, min(1000, bbox.get("xmax", 1000)))

    if ymax <= ymin or xmax <= xmin:
        return None

    # Convert normalized (0..1000) to pixel coordinates
    y1 = int(ymin * h_full / 1000.0)
    y2 = int(ymax * h_full / 1000.0)
    x1 = int(xmin * w_full / 1000.0)
    x2 = int(xmax * w_full / 1000.0)

    # Apply padding only if explicitly positive
    if padding_pct > 0:
        pad_h = int(h_full * padding_pct)
        pad_w = int(w_full * padding_pct)
        y1 = max(0, y1 - pad_h)
        y2 = min(h_full, y2 + pad_h)
        x1 = max(0, x1 - pad_w)
        x2 = min(w_full, x2 + pad_w)

    cropped = pil_img.crop((x1, y1, x2, y2))

    # Refine boundaries using OpenCV contour analysis if available
    if HAS_CV2:
        cropped = refine_crop_with_opencv(cropped)

    # Convert to pure 1-bit monochrome PNG (dither=NONE)
    # Threshold at 190 to eliminate paper grain / scanner dust
    fn = lambda p: 255 if p > 190 else 0
    mono = cropped.convert("L").point(fn, mode="1")

    # Save to in-memory bytes as optimized PNG
    buf = io.BytesIO()
    mono.save(buf, format="PNG", optimize=True)
    raw_bytes = buf.getvalue()

    # Optionally persist to output_dir
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        disk_path = os.path.join(output_dir, f"{media_key}.png")
        with open(disk_path, "wb") as f:
            f.write(raw_bytes)

    b64_str = base64.b64encode(raw_bytes).decode("utf-8")
    data_uri = f"data:image/png;base64,{b64_str}"

    return {
        "description": f"Extracted visual diagram ({media_key})",
        "width": mono.width,
        "height": mono.height,
        "mime": "image/png",
        "format": "1bit-png",
        "file_bytes": len(raw_bytes),
        "data": data_uri
    }

def refine_crop_with_opencv(pil_cropped: Image.Image) -> Image.Image:
    """
    Snaps tightly to ink contours inside cropped region, removing dead whitespace.
    """
    np_img = np.array(pil_cropped)
    if len(np_img.shape) == 3:
        gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
    else:
        gray = np_img

    # Invert so black ink is white foreground
    _, thresh = cv2.threshold(gray, 210, 255, cv2.THRESH_BINARY_INV)

    # Find non-zero pixel coordinates
    points = cv2.findNonZero(thresh)
    if points is not None:
        rx, ry, rw, rh = cv2.boundingRect(points)
        # Add 6px margin
        margin = 6
        x1 = max(0, rx - margin)
        y1 = max(0, ry - margin)
        x2 = min(pil_cropped.width, rx + rw + margin)
        y2 = min(pil_cropped.height, ry + rh + margin)
        if (x2 - x1) > 20 and (y2 - y1) > 20:
            return pil_cropped.crop((x1, y1, x2, y2))

    return pil_cropped
