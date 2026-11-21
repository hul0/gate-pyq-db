# Build a High-Performance Document OCR & Digitization Engine for Studiva

## 1. Project Objective

Build a lightweight, intelligent document digitization engine in Python for converting educational PDFs and scanned images into structured Markdown, LaTeX and diagram assets.

The primary use case is digitizing GATE CSE/IT Previous Year Questions (PYQs), including mathematical expressions, computer science diagrams, tables, algorithms and technical text.

The system must run efficiently on consumer hardware without requiring a dedicated GPU.

### Hardware constraints

Primary development and inference machine:

- CPU: AMD Ryzen 5 5500U
- RAM: 16 GB DDR4
- GPU: Integrated AMD Radeon Vega
- OS: Linux (Parrot OS / Debian-based)
- Inference: CPU-first

Strict requirements:

- Every ML model must have fewer than 100 million parameters.
- No large vision-language models or LLMs.
- No cloud OCR APIs.
- No mandatory CUDA.
- Prefer ONNX Runtime CPU inference.
- Minimize RAM consumption and model loading overhead.
- Optimize for throughput when processing large collections of PDFs.

The selected ML models are already decided. Do not replace them with larger alternatives.

---

## 2. Selected Models

Use the following models:

| Task | Model |
|---|---|
| Text detection and recognition | PP-OCRv6-Small |
| Mathematical formula recognition | PP-FormulaNet-S |
| Document layout detection | PP-DocLayout-S |
| Diagram extraction | OpenCV (no ML model) |

Use official pretrained weights and compatible inference implementations.

Before implementation, verify the exact model architecture, parameter counts, available model formats, input dimensions, output tensors and supported CPU inference backends.

Prefer ONNX versions when officially supported and validated. Otherwise, use the official Paddle inference implementation.

Do not assume that every Paddle model has an ONNX conversion available.

---

## 3. Technology Stack

Choose stable, efficient and well-maintained libraries.

### Core processing

- Python 3.11+
- PyMuPDF (fitz): PDF parsing, native text extraction, page rendering and coordinate extraction.
- OpenCV: image preprocessing, thresholding, cropping and diagram extraction.
- NumPy: image and tensor operations.
- Pillow: image encoding and 1-bit PNG generation.
- ONNX Runtime: CPU inference where supported.
- PaddleOCR / PaddlePaddle: official model inference where ONNX is unavailable or incompatible.
- Pydantic: output schema validation.
- orjson: fast JSON serialization.

### Additional libraries

- RapidFuzz: optional OCR correction matching against known text dictionaries.
- scikit-image: optional image processing operations if OpenCV is insufficient.
- pytest: unit and integration testing.
- psutil: RAM, CPU and resource monitoring.
- Rich: CLI progress and diagnostic output.

Avoid unnecessary dependencies.

---

## 4. Overall Architecture

Implement the application as independent processing modules connected through a central document-processing orchestrator.

Pipeline:

PDF / IMAGE
    |
    v
Input Inspection
    |
    v
PDF Native Text Extraction
    |
    +---- Native text sufficient? ---- YES ---> Extract text and coordinates
    |                                      |
    NO                                     |
    |                                      |
    v                                      |
Image Preprocessing                        |
    |                                      |
    v                                      |
Document Layout Detection <----------------+
    |
    v
Region Classification
    |
    +---- TEXT ------> PP-OCRv6-Small
    |
    +---- FORMULA ---> PP-FormulaNet-S
    |
    +---- DIAGRAM ---> OpenCV Crop + 1-bit PNG
    |
    +---- TABLE -----> Table extraction / structural reconstruction
    |
    v
Reading Order Reconstruction
    |
    v
Markdown + LaTeX + Asset Generation
    |
    v
JSON Schema Validation
    |
    v
Final Document Output

The architecture must support independent processing of each page and region.

---

## 5. Module A: PDF and Image Input Processing

Implement `input/`.

Responsibilities:

1. Accept PDF, PNG, JPEG and WebP.
2. Inspect PDF metadata, dimensions and page count.
3. Detect whether a PDF page contains an existing text layer.
4. Extract native text and bounding boxes using PyMuPDF.
5. Detect image-heavy or scanned pages.
6. Render only pages requiring OCR.
7. Avoid rendering pages unnecessarily.
8. Normalize page coordinates.

### Intelligent PDF handling

Do not assume that a PDF is either entirely digital or entirely scanned.

Some PDFs contain a mixture of:
- Native selectable text.
- Embedded scanned images.
- Rasterized equations.
- Vector diagrams.

Make processing decisions at the page and region level wherever practical.

Do not blindly trust an existing PDF text layer. Detect empty, corrupted, incomplete or suspiciously sparse extraction.

---

## 6. Module B: Image Preprocessing

Implement `preprocessing/`.

Use OpenCV.

Required operations:

- Grayscale conversion.
- Deskewing.
- Noise removal.
- Contrast enhancement.
- Adaptive thresholding.
- Resolution normalization.
- Image orientation detection where necessary.

### Smart preprocessing

Do not apply every operation to every image.

Implement conditional preprocessing based on image characteristics.

For example:
- Clean digital scans should skip aggressive denoising.
- Low-contrast scans should receive contrast enhancement.
- Skewed pages should be corrected.
- Already sharp pages should avoid unnecessary resizing.

Preserve the original page image for coordinate mapping and fallback processing.

---

## 7. Module C: Document Layout Detection

Implement `layout/`.

Use PP-DocLayout-S.

Responsibilities:

- Detect text regions.
- Detect mathematical formula regions.
- Detect diagrams and figures.
- Detect tables.
- Detect headers and footers.
- Return bounding boxes and region classifications.

Normalize all bounding boxes to a consistent coordinate system.

Required internal representation:

{
  "region_id": "r001",
  "type": "formula",
  "bbox": [x1, y1, x2, y2],
  "confidence": 0.97,
  "page": 1
}

### Important requirements

1. Use padding when cropping regions.
2. Avoid cutting off mathematical symbols or diagram labels.
3. Handle overlapping bounding boxes.
4. Merge fragmented text regions where appropriate.
5. Preserve the original coordinates.
6. Provide a fallback when layout detection fails.
7. Support multiple columns and mixed content.

Do not assume all mathematical expressions are independently detected. Implement a fallback for inline mathematics embedded inside text regions.

---

## 8. Module D: Text OCR

Implement `ocr/text/`.

Use PP-OCRv6-Small.

Responsibilities:

- Text detection.
- Text recognition.
- Bounding box extraction.
- Reading-order estimation.
- Paragraph reconstruction.
- Recognition of question numbers and answer options.
- Preservation of punctuation and special characters.

### Requirements

- Process only regions that need OCR.
- Reuse OCR results when possible.
- Preserve line and paragraph relationships.
- Do not automatically rewrite or paraphrase recognized content.
- Avoid aggressive language correction that could alter technical meaning.
- Preserve mathematical symbols where recognized.
- Retain confidence scores.

Output should be plain structured text, not a generated explanation.

---

## 9. Module E: Mathematical Formula Recognition

Implement `ocr/formula/`.

Use PP-FormulaNet-S.

This is a critical component.

The output must be actual LaTeX source code, never ASCII approximations of equations.

Examples:

Input: Image of a mathematical expression.

Output:

\[
\int_0^1 x^2\,dx
\]

```latex
\int_0^1 x^2\,dx
```

The system must preserve:

- Fractions.
- Superscripts and subscripts.
- Summations.
- Integrals.
- Matrices.
- Determinants.
- Greek symbols.
- Set notation.
- Boolean algebra.
- Logic operators.
- Mathematical relations.
- Multi-line equations.

### Requirements

1. Crop formulas using layout bounding boxes.
2. Add sufficient padding.
3. Apply appropriate image preprocessing.
4. Run FormulaNet only on formula regions.
5. Preserve inline versus display equation classification.
6. Associate LaTeX with the original page coordinates.
7. Validate generated LaTeX syntax.
8. Never silently replace invalid LaTeX with ASCII.
9. Retain the original formula crop for debugging and correction.

### Formula validation

Use a lightweight LaTeX syntax validation mechanism.

Where practical, render generated LaTeX using KaTeX or another compatible renderer for visual review.

Do not automatically assume that syntactically valid LaTeX is mathematically correct.

---

## 10. Module F: Diagram Extraction

Implement `ocr/diagrams/`.

No ML model is required.

Use OpenCV and Pillow.

The objective is to extract diagram regions into compact 1-bit PNG images rather than converting diagrams into SVG.

### Processing steps

1. Obtain diagram bounding boxes from PP-DocLayout-S.
2. Crop the original page using the bounding box.
3. Add configurable padding.
4. Convert to grayscale.
5. Apply Otsu or adaptive thresholding.
6. Remove isolated noise where safe.
7. Convert to monochrome 1-bit PNG.
8. Save as an independent asset.

### Important

Not every diagram should be aggressively binarized.

Preserve:
- Thin circuit wires.
- Small text labels.
- Dotted connections.
- Arrowheads.
- Mathematical annotations.

Maintain the original crop as a fallback whenever binarization loses important details.

### Output

- PNG.
- 1-bit depth where appropriate.
- Base64 only when explicitly requested by an API.
- Otherwise store assets separately and reference them in JSON.

Do not use SVG tracing or vectorization in this pipeline.

---

## 11. Module G: Table Extraction

Tables must not be treated as ordinary paragraphs.

Use layout detection to identify table regions.

Where a table is digitally embedded in a PDF, inspect native PDF text and coordinates first.

For scanned tables, reconstruct rows and columns using available PaddleOCR table recognition capabilities if compatible with the selected lightweight architecture.

Output tables as Markdown tables where possible.

If the table structure cannot be recovered reliably, preserve its original crop as an image rather than inventing cell relationships.

---

## 12. Module H: Reading Order Reconstruction

Implement `reconstruction/`.

This module combines the outputs from the different processors.

Use:

- Original bounding boxes.
- Page coordinates.
- Region classifications.
- Column detection.
- Reading-order heuristics.
- Parent-child relationships.

It must reconstruct a logical document from independent OCR results.

Example:

1. Question statement.
2. Inline mathematical expression.
3. Diagram.
4. Remaining question text.
5. Answer options.

Do not simply sort every element by its vertical coordinate. Support multi-column pages, inline equations and interleaved diagrams.

Every element must retain its original page number and position.

---

## 13. Output Structure

Use JSON as the canonical structured representation.

Markdown should be generated from the JSON structure.

Example:

{
  "document_id": "gate-cse-2025",
  "metadata": {
    "source": "gate-2025.pdf",
    "pages": 1
  },
  "pages": [
    {
      "page": 1,
      "dimensions": {
        "width": 2480,
        "height": 3508
      },
      "elements": [
        {
          "id": "e001",
          "type": "text",
          "text": "Consider the following expression:",
          "bbox": [100, 200, 1800, 300],
          "confidence": 0.98
        },
        {
          "id": "e002",
          "type": "math",
          "latex": "\\sum_{i=1}^{n} x_i^2",
          "display": true,
          "bbox": [400, 320, 1500, 500],
          "confidence": 0.96
        },
        {
          "id": "e003",
          "type": "diagram",
          "asset": "assets/e003.png",
          "format": "png",
          "bit_depth": 1,
          "bbox": [300, 600, 1700, 1200]
        }
      ]
    }
  ]
}

Use a proper Pydantic schema.

Support:
- JSON export.
- Markdown export.
- Separate diagram assets.
- Optional Base64 image embedding.
- Original page references.
- Bounding boxes.
- OCR confidence metadata.

---

## 14. Performance and Resource Optimization

Performance is a primary requirement.

Implement:

### Model management

- Lazy-load models.
- Avoid loading unused models.
- Reuse model sessions.
- Avoid repeated model initialization.
- Release resources when appropriate.
- Use optimized CPU inference providers.
- Benchmark different inference thread counts.

### Processing optimization

- Skip OCR on native text regions.
- Avoid processing diagrams through text OCR.
- Avoid formula recognition on ordinary text.
- Batch compatible regions when beneficial.
- Cache page-level preprocessing.
- Cache region-level OCR results.
- Process pages incrementally.
- Avoid retaining unnecessary full-resolution images in RAM.

### CPU inference

Benchmark:
- ONNX Runtime CPU.
- Paddle inference CPU.
- Different quantization levels where supported.

Use INT8 quantization only when supported and verify that it does not significantly degrade mathematical recognition.

Do not assume all models support the same quantization format.

### Memory

Target:
- Keep peak RAM usage below 4 GB for normal document processing where feasible.
- Avoid loading all PDF pages into memory.
- Support long PDFs through streaming page processing.
- Provide configurable worker counts.

These are engineering targets, not guaranteed hardware benchmarks.

---

## 15. Error Handling and Confidence

Every processed region should have:

- Recognition result.
- Model confidence where available.
- Bounding box.
- Processing status.
- Error information where applicable.

Implement a review mechanism for:
- Low-confidence text.
- Invalid LaTeX.
- Missing formula results.
- Failed diagram extraction.
- Suspiciously empty pages.
- Incorrect reading order.

Never silently discard failed regions.

Keep original crops so individual regions can be corrected or reprocessed without rerunning the entire PDF.

---

## 16. Project Structure

Use a modular project structure:

studiva-ocr/
│
├── models/
│   ├── text/
│   ├── formula/
│   └── layout/
│
├── src/
│   ├── input/
│   │   ├── pdf_reader.py
│   │   └── image_reader.py
│   │
│   ├── preprocessing/
│   │   ├── image_cleaner.py
│   │   └── deskew.py
│   │
│   ├── layout/
│   │   └── detector.py
│   │
│   ├── ocr/
│   │   ├── text/
│   │   ├── formula/
│   │   └── diagrams/
│   │
│   ├── tables/
│   │   └── extractor.py
│   │
│   ├── reconstruction/
│   │   ├── reading_order.py
│   │   ├── markdown.py
│   │   └── serializer.py
│   │
│   ├── validation/
│   │   ├── latex.py
│   │   └── schema.py
│   │
│   ├── orchestration/
│   │   └── pipeline.py
│   │
│   └── utils/
│       ├── cache.py
│       └── profiling.py
│
├── tests/
├── benchmarks/
├── output/
├── config.yaml
├── requirements.txt
└── README.md

---

## 17. Testing and Benchmarking

Before considering the system complete, create a representative benchmark dataset containing:

- Ordinary paragraphs.
- MCQ questions.
- Mathematical equations.
- Matrices and determinants.
- Boolean algebra.
- Logic circuits.
- Trees and graphs.
- Tables.
- Multi-column layouts.
- Low-resolution scanned pages.

Measure:

1. Text recognition accuracy.
2. Formula recognition accuracy using normalized LaTeX and exact-match rates.
3. Bounding-box accuracy.
4. Diagram crop completeness.
5. Markdown reconstruction accuracy.
6. Processing time per page.
7. Peak RAM consumption.
8. CPU utilization.

Maintain separate benchmark results for digitally generated and scanned PDFs.

---

## 18. Development Instructions

Implement the project incrementally.

### Phase 1: Environment and model verification
- Verify exact model repositories.
- Download pretrained weights.
- Verify model licenses.
- Confirm CPU inference.
- Verify parameter counts.
- Confirm ONNX compatibility.
- Create individual model benchmarks.

### Phase 2: Input and layout
- Implement PDF inspection.
- Implement native text extraction.
- Implement page rendering.
- Integrate layout detection.
- Verify region coordinates.

### Phase 3: Specialized OCR
- Integrate text OCR.
- Integrate formula recognition.
- Integrate diagram extraction.
- Implement table extraction.

### Phase 4: Reconstruction
- Implement reading order.
- Build canonical JSON output.
- Generate Markdown.
- Preserve asset references and coordinates.

### Phase 5: Optimization
- Profile CPU and RAM.
- Implement caching.
- Optimize model loading.
- Benchmark batch sizes.
- Test large PDFs.

### Phase 6: Quality assurance
- Run GATE PYQ benchmark dataset.
- Validate mathematical expressions.
- Inspect diagram crops.
- Test mixed-content pages.
- Fix reconstruction errors.

### Important development rules

1. Do not replace the selected models without explicit approval.
2. Do not introduce an LLM into the OCR pipeline.
3. Do not use cloud APIs.
4. Do not convert diagrams into SVG.
5. Never approximate mathematical expressions using ASCII.
6. Do not generate fabricated OCR results when recognition fails.
7. Prioritize deterministic processing and traceable outputs.
8. Document every model's actual parameter count, file size, license and runtime requirements.
9. Avoid unnecessary abstractions and dependencies.
10. Deliver a working CLI prototype before building a GUI or API.

## Final Goal

Deliver a fully local, CPU-efficient educational document digitization engine that converts GATE PYQ PDFs and images into accurate structured Markdown, actual LaTeX expressions, and compact 1-bit PNG diagram assets.

The system must be modular, testable, resource-efficient and suitable for eventual integration into Studiva's backend.