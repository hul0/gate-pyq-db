# Diagram Extraction, Vectorization, and Media Embedding Specification

> **Status:** Approved Standard  
> **Target Scope:** All GATE CS PYQ Question Diagrams, Circuits, Graphs, and Charts  
> **Last Updated:** 2026-11-21  

---

## 1. Objective

This specification details the standardized procedure for extracting, cleaning, vectorizing, and embedding question diagrams from exam question papers into the database JSON structure.

The primary goal is to ensure:
1. **Best Visual Quality**: Clean, sharp, high-contrast black-and-white lines without scanned JPEG compression noise or border artifacts.
2. **Lowest Payload Size**: Minimal byte impact when embedded directly inside JSON structures.
3. **Universal Compatibility**: Zero-dependency native rendering across Web, Flutter, React Native, iOS, and Android.

---

## 2. Diagram Discovery & Cropping Protocol

### Step 1: Raw Image Extraction
Never capture or downsample pages before diagram cropping. Extract the raw, uncompressed/lossless embedded image stream directly from the PDF via PyMuPDF:

```python
import pymupdf, io
from PIL import Image

doc = pymupdf.open("CS/2007_CS.pdf")
page = doc[page_num - 1]
xref = page.get_images()[0][0]
img_data = doc.extract_image(xref)
raw_page = Image.open(io.BytesIO(img_data["image"])).convert("L")
```

### Step 2: Spatial Isolation
Isolate diagrams strictly by anchoring bounding boxes between question header/prompt text and subsequent options or next question anchors using OCR word coordinates (`pytesseract.image_to_data`).

### Step 3: Thresholding & Denoising
Convert raw grayscale scans to pure monochrome binary bitmaps (threshold at `~185`). Non-content scan specks and yellowed/gray paper background pixels (`> 200`) are clipped to pure white (`255`), while ink strokes (`< 185`) are clipped to pure black (`0`).

---

## 3. Vectorization with `svgsmith`

The library `svgsmith` is used to convert cleaned raster diagrams into clean vector SVG:

```bash
svgsmith convert <crop.png> --mode binary --transparent-background --out <diagram.svg>
```

- **Output Mode**: `binary` (optimal for line art, circuit schematics, and graphs).
- **Background**: Transparent (no `<rect>` background, only vector `<path>` definitions).
- **Styling**: `style="width:100%;height:100%" preserveAspectRatio="xMidYMid meet"`.

---

## 4. Format Evaluation & Final Decision

An empirical benchmark across 8 question diagrams in `GATE 2007 CS` was conducted to compare payload size and rendering viability:

| Format | Avg Size / Diagram | Total Payload | Scalability | Universal Rendering | Decision |
| :--- | :---: | :---: | :--- | :--- | :--- |
| **1-bit PNG Base64** | **~2.5 KB** | **27.5 KB** | Fixed (High Res) | 100% Native | **Selected Standard** |
| **Lossless WebP Base64** | **~1.5 KB** | **18.7 KB** | Fixed (High Res) | Modern Clients | Alternative |
| **Raw Minified SVG** | **~10.5 KB** | **84.3 KB** | Infinite Vector | Requires SVG Parser | Vector-Only Use |
| **Standard 8-bit PNG** | **~5.2 KB** | **41.5 KB** | Fixed | 100% Native | Deprecated |
| **SVGZ (Gzip Base64)** | **~5.4 KB** | **43.6 KB** | Infinite Vector | Client Gzip Required | Not Recommended |

### Decision Rationale: 1-Bit PNG Base64
- **Payload efficiency**: Autotraced vector SVGs require thousands of Bezier control points for curved handwritten/scanned shapes, bloating text payloads to 10 KB - 24 KB per diagram. In contrast, 1-bit monochrome PNG stores 1 pixel per bit, compressed via DEFLATE, resulting in **1.3 KB - 3.4 KB** raw files (**1.8 KB - 4.5 KB Base64**).
- **Text Fidelity**: Scanned technical notations (e.g. `A0`, `A1`, `Clock`, subscripts, Greek letters) are preserved pixel-for-pixel without the contour wobbling inherent in autotracing algorithms.
- **Client Performance**: Decodes instantly on mobile and web clients via standard `<img>` or `Image.memory` with zero DOM or XML parsing overhead.

---

## 5. JSON Schema Integration

Each question that contains figures, diagrams, or charts must set `"has_images": true` and populate the `"media"` object:

```json
{
  "id": "2007_CS_CS_Q05",
  "question_number": 5,
  "section": "Computer Science and Information Technology",
  "section_code": "CS",
  "question_type": "MCQ",
  "marks": 1.0,
  "negative_marks": 0.25,
  "question_text": "Consider the DAG with V = {1,2,3,4,5,6}, shown below.\nWhich of the following is NOT a topological ordering?",
  "options": {
    "A": "123456",
    "B": "132456",
    "C": "132465",
    "D": "324165"
  },
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

---

## 6. Directory Conventions

- Cropped raster diagrams: `temp/<paper_id>/png/`
- Vectorized SVGs: `temp/<paper_id>/svg/`
- Optimized 1-bit PNGs: `temp/<paper_id>/png_1bit/`
- Paper media dictionary: `temp/<paper_id>/media_1bit.json`
