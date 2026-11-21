---
name: diagram-extraction-vectorization
description: Locates question diagrams, circuits, and charts in exam PDFs, crops and cleans them, vectorizes with svgsmith, and encodes them into optimized 1-bit PNG base64 for JSON embedding.
---

# Diagram Extraction & Media Vectorization Skill

This skill documents the end-to-end workflow for detecting, extracting, vectorizing, and formatting question media (diagrams, circuits, charts, finite state automata, and graphs) from exam PDFs (scanned or digital) into JSON-embeddable formats.

## 1. Locating Question Diagrams in Exam PDFs

### Detection Strategy
Exam papers (e.g. GATE CS) often embed question diagrams inside scanned full-page images or as vector drawings.
To find all diagram assets:

1. **Text Scan**: Look for reference keywords in question text:
   - `"shown below"`, `"following figure"`, `"circuit"`, `"DAG"`, `"automaton"`, `"FSA"`, `"poset"`, `"graph"`, `"table"`, `"tree"`.
2. **Visual Feature Extraction (PyMuPDF + SciPy / OpenCV)**:
   - Extract raw embedded page images via `pymupdf`:
     ```python
     import pymupdf, io
     from PIL import Image

     doc = pymupdf.open("paper.pdf")
     page = doc[page_index]
     xref = page.get_images()[0][0]
     raw_img = Image.open(io.BytesIO(doc.extract_image(xref)["image"])).convert("L")
     ```
   - Run connected component labeling (`scipy.ndimage.label`) to find non-text graphic elements:
     - Normal text characters: bounding box width < 40 px, height < 35 px.
     - Diagrams/circuits: contiguous bounding box width > 60 px and height > 55 px.
3. **Boundaries via OCR Anchor Words**:
   - Use `pytesseract.image_to_data` to locate text immediately preceding and following the diagram.
   - The graphic is isolated strictly between the surrounding question text lines.

---

## 2. Precise Cropping and Cleaning

Do not vectorize or save noisy full pages. Only crop the diagram area:

```python
import numpy as np
from PIL import Image

def crop_and_clean_diagram(raw_img, box, pad=12, thresh=185):
    # 1. Crop to bounding box
    crop = raw_img.crop(box)
    arr = np.array(crop)

    # 2. Tight auto-crop to non-white pixels
    black_y, black_x = np.where(arr < 200)
    if len(black_x) > 0:
        x1 = max(0, np.min(black_x) - pad)
        y1 = max(0, np.min(black_y) - pad)
        x2 = min(arr.shape[1], np.max(black_x) + pad)
        y2 = min(arr.shape[0], np.max(black_y) + pad)
        arr = arr[y1:y2, x1:x2]

    # 3. Clean thresholding (removes scan noise / grain)
    clean_arr = np.where(arr < thresh, 0, 255).astype(np.uint8)
    return Image.fromarray(clean_arr)
```

---

## 3. SVG Vectorization with `svgsmith`

To vectorize cropped diagrams into clean, transparent black-and-white SVGs:

```bash
svgsmith convert <input.png> --mode binary --transparent-background --out <output.svg>
```

Key attributes produced:
- Clean `<svg viewBox="..." style="width:100%;height:100%" preserveAspectRatio="xMidYMid meet">`
- Single `<g fill="#000000">` with vector path contours.
- No background rect (completely transparent).

---

## 4. Media Format Selection for JSON Embedding

### Empirical Comparison (Based on GATE CS 2007 Diagrams)

| Format | Avg Size / Diagram | Total (8 items) | Quality & Zoom | Frontend Compatibility |
| :--- | :---: | :---: | :--- | :--- |
| **1-bit PNG Base64** | **~2.5 KB** | **27.5 KB** | 100% pixel-perfect, crisp lines | 100% Universal (Web, Flutter, RN, iOS, Android) |
| **Lossless WebP Base64** | **~1.5 KB** | **18.7 KB** | 100% pixel-perfect, alpha transparency | Modern Web, Flutter, React Native (API 18+ / iOS 14+) |
| **Standard 8-bit PNG Base64** | **~5.2 KB** | **41.5 KB** | Pixel-perfect, unindexed overhead | 100% Universal |
| **Raw Minified SVG** | **~10.5 KB** | **84.3 KB** | Vector (infinite zoom), contour wobble | Requires SVG renderer (`flutter_svg`, `react-native-svg`) |

### Approved Production Choice: 1-Bit PNG Base64
1. **Lowest Complexity**: Renders natively everywhere with zero extra dependencies (`<img src="...">` in HTML, `Image.memory` in Flutter).
2. **Compact Payload**: Sub-3 KB per diagram; 3x to 5x smaller than autotraced SVG.
3. **Scan Fidelity**: Preserves small text labels (`A0`, `A1`, `Clock`, subscripts) without Bezier autotracing distortion.

---

## 5. Converting to 1-Bit PNG & Encoding Base64

```python
import base64
from PIL import Image

def encode_1bit_png(img: Image.Image) -> dict:
    # Mode '1' is 1-bit monochrome (1 pixel = 1 bit in memory)
    bw = img.convert('L').point(lambda p: 255 if p > 185 else 0, mode='1')
    
    import io
    buf = io.BytesIO()
    bw.save(buf, format='PNG', optimize=True)
    png_bytes = buf.getvalue()
    
    b64_str = base64.b64encode(png_bytes).decode('ascii')
    
    return {
        "width": bw.width,
        "height": bw.height,
        "mime": "image/png",
        "format": "1bit-png",
        "file_bytes": len(png_bytes),
        "data": f"data:image/png;base64,{b64_str}"
    }
```

---

## 6. Standard Question JSON Schema with `"media"`

```json
{
  "id": "2007_CS_CS_Q05",
  "question_number": 5,
  "question_type": "MCQ",
  "question_text": "Consider the DAG with V = {1,2,3,4,5,6}, shown below...",
  "has_images": true,
  "media": {
    "q05_dag": {
      "description": "Directed Acyclic Graph with 6 nodes",
      "width": 245,
      "height": 190,
      "mime": "image/png",
      "format": "1bit-png",
      "file_bytes": 1364,
      "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPUAAAC+AQAAAADFVXRn..."
    }
  }
}
```
