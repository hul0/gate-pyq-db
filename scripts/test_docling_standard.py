import os
import sys
import time
import resource
from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TableFormerMode,
    AcceleratorOptions,
)

def main():
    pdf_path = "CS/2013_CS.pdf"
    page_num = 3  # Page 3 of 2013_CS.pdf
    out_dir = Path("./temp/2013_CS/docling_standard")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"--- Configuring Docling Standard Pipeline on {pdf_path} (Page {page_num}) ---")
    pipeline_options = PdfPipelineOptions()
    
    # Restrict threads to keep CPU cool and prevent overheating
    pipeline_options.accelerator_options = AcceleratorOptions(
        num_threads=4,
        device="cpu"
    )
    
    # Table structure extraction via TableFormer
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE
    
    # OCR options
    pipeline_options.do_ocr = True
    
    # Formula & Code enrichment
    pipeline_options.do_formula_enrichment = True
    pipeline_options.do_code_enrichment = True
    pipeline_options.code_formula_options.stop_on_repetition = True
    
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
                page_range=[page_num, page_num]
            )
        }
    )
    
    print("Starting conversion...")
    t0 = time.time()
    conv_res = converter.convert(pdf_path)
    elapsed = time.time() - t0
    
    doc = conv_res.document
    md_output = doc.export_to_markdown()
    
    out_md = out_dir / f"page_{page_num}_standard.md"
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(md_output)
        
    print("\n" + "="*60)
    print("--- CONVERSION BENCHMARK & PERFORMANCE ---")
    print(f"Elapsed time        : {elapsed:.2f} s")
    
    # Memory usage
    rusage = resource.getrusage(resource.RUSAGE_SELF)
    max_rss_mb = rusage.ru_maxrss / 1024
    print(f"Peak RAM usage (RSS): {max_rss_mb:.2f} MB")
    print(f"Saved Markdown to   : {out_md}")
    print("="*60 + "\n")
    
    print("=== EXTRACTED MARKDOWN PREVIEW ===")
    print(md_output)

if __name__ == "__main__":
    main()
