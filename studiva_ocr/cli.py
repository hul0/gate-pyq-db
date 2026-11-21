"""
cli.py - Command-line interface and master orchestrator for the Studiva OCR pipeline.
"""

import os
import sys
import json
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List

from studiva_ocr.renderer import get_pdf_page_count, parse_page_range, render_pdf_pages
from studiva_ocr.prompt import SYSTEM_INSTRUCTION, build_page_prompt
from studiva_ocr.client import GlobalRateLimiter, load_api_key, call_gemini_page
from studiva_ocr.media import extract_and_binarize_media
from studiva_ocr.schema import normalize_paper_json
from studiva_ocr.manifest import update_dataset_manifest

def parse_args():
    parser = argparse.ArgumentParser(
        description="Studiva OCR: Intelligent, rate-limited, multi-threaded GATE exam OCR pipeline."
    )
    parser.add_argument("--pdf", required=True, help="Path to input examination PDF (e.g. CS/2011_CS.pdf)")
    parser.add_argument("--answer-key", required=True, help="Path to digitized answer key JSON file")
    parser.add_argument("--api-key", default=None, help="Gemini API Key (or set GEMINI_API_KEY env / .env)")
    parser.add_argument("--model", default="gemini-3.5-flash-lite", help="Gemini model name (default: gemini-3.5-flash-lite)")
    parser.add_argument("--threads", type=int, default=5, help="Concurrent worker threads (default: 5)")
    parser.add_argument("--rpm", type=int, default=12, help="Max requests per minute rate limit (default: 12)")
    parser.add_argument("--pages", default="auto", help="Page range to process (e.g. '2-17', '2', or 'auto')")
    parser.add_argument("--dpi", type=int, default=200, help="Rendering DPI for PDF pages (default: 200)")
    parser.add_argument("--force", action="store_true", help="Force reprocessing, ignoring intermediate page cache")
    parser.add_argument("--output-dir", default=None, help="Directory to save final full_paper.json (default: data/dataset/papers/<paper_id>/)")
    parser.add_argument("--no-manifest", action="store_true", help="Skip updating data/dataset/manifest.json")
    return parser.parse_args()

def infer_paper_metadata(pdf_path: str) -> Dict[str, Any]:
    """Infers paper_id, year, subject, session from PDF filename."""
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    # e.g. 2011_CS -> year=2011, session=CS
    parts = base.split("_")
    year = int(parts[0]) if parts[0].isdigit() else 2011
    session = parts[1] if len(parts) > 1 else "CS"
    subject = "Computer Science and Information Technology"

    return {
        "paper_id": base,
        "year": year,
        "session": session,
        "subject": subject
    }

def load_keys_map(key_path: str) -> Dict[int, Dict[str, Any]]:
    """Loads digitized answer key JSON and indexes by question number."""
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"Answer key not found: {key_path}")

    with open(key_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    keys_list = data.get("keys", [])
    keys_map = {}
    for k in keys_list:
        qnum = k.get("question_number")
        if qnum is not None:
            keys_map[int(qnum)] = k

    return keys_map

def process_single_page(
    page_num: int,
    image_path: str,
    keys_for_page: List[Dict[str, Any]],
    cache_path: str,
    api_key: str,
    model: str,
    rate_limiter: GlobalRateLimiter,
    force: bool = False
) -> Dict[str, Any]:
    """Processes a single page through Gemini or returns cached JSON."""
    if not force and os.path.exists(cache_path) and os.path.getsize(cache_path) > 20:
        with open(cache_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"[Page {page_num:02d}] Loaded from cache ({len(data.get('questions', []))} Qs)")
        return data

    prompt = build_page_prompt(page_num, keys_for_page)
    t0 = time.time()
    result = call_gemini_page(
        image_path=image_path,
        prompt=prompt,
        system_instruction=SYSTEM_INSTRUCTION,
        api_key=api_key,
        model=model,
        rate_limiter=rate_limiter,
        page_label=f"Page {page_num:02d}"
    )
    elapsed = time.time() - t0

    qs = result.get("questions", [])
    print(f"[Page {page_num:02d}] Success: {len(qs)} Qs in {elapsed:.2f}s")

    # Cache to disk
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    return result

def run_pipeline():
    args = parse_args()
    api_key = load_api_key(args.api_key)

    meta = infer_paper_metadata(args.pdf)
    paper_id = meta["paper_id"]
    year = meta["year"]
    session = meta["session"]
    subject = meta["subject"]

    print(f"=== Starting Studiva OCR Pipeline for {paper_id} ===")
    print(f"Model: {args.model} | Threads: {args.threads} | RPM: {args.rpm}")

    # 1. Answer Key Loading
    keys_map = load_keys_map(args.answer_key)
    print(f"Loaded {len(keys_map)} official answer keys from {args.answer_key}")

    # 2. Page Range and Rendering
    total_pdf_pages = get_pdf_page_count(args.pdf)
    target_pages = parse_page_range(args.pages, total_pdf_pages)
    print(f"Target pages to process ({len(target_pages)}): {target_pages}")

    temp_base = os.path.join("temp", paper_id)
    pages_dir = os.path.join(temp_base, "pages")
    cache_dir = os.path.join(temp_base, "api_pages")
    media_dir = os.path.join(temp_base, "media")
    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(media_dir, exist_ok=True)

    print("Rendering PDF pages to PNG (200 DPI)...")
    rendered_pages = render_pdf_pages(
        pdf_path=args.pdf,
        pages=target_pages,
        output_dir=pages_dir,
        dpi=args.dpi,
        force=args.force
    )

    # 3. Parallel Page OCR Dispatch
    rate_limiter = GlobalRateLimiter(rpm=args.rpm)
    all_extracted_questions = []

    print(f"Executing parallel Gemini OCR with up to {args.threads} threads...")
    futures = {}
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for p in target_pages:
            img_path = rendered_pages[p]
            cache_file = os.path.join(cache_dir, f"page_{p:02d}.json")

            # Find keys that likely belong to this page
            # Estimate question range: roughly 4-6 questions per page
            # For 2011_CS: Q1-Q25 on pages 2-7, Q26-Q55 on pages 8-15, Q56-Q65 on pages 16-17
            # We pass all keys or a window of keys
            page_keys = list(keys_map.values())

            fut = executor.submit(
                process_single_page,
                page_num=p,
                image_path=img_path,
                keys_for_page=page_keys,
                cache_path=cache_file,
                api_key=api_key,
                model=args.model,
                rate_limiter=rate_limiter,
                force=args.force
            )
            futures[fut] = p

        for fut in as_completed(futures):
            p = futures[fut]
            try:
                page_data = fut.result()
                qs = page_data.get("questions", [])
                for q in qs:
                    q["_page_number"] = p
                    q["page_start"] = p
                    q["page_end"] = p
                    all_extracted_questions.append(q)
            except Exception as e:
                print(f"Error processing page {p}: {e}")

    # Deduplicate questions by question_number if overlapping
    unique_qs_map = {}
    for q in all_extracted_questions:
        qnum = q.get("question_number")
        if qnum is not None:
            unique_qs_map[int(qnum)] = q
    sorted_unique_qs = [unique_qs_map[k] for k in sorted(unique_qs_map.keys())]

    print(f"\nExtracted {len(sorted_unique_qs)} distinct questions across all pages.")

    # 4. Media Extraction Pass (Hybrid Gemini Bbox + OpenCV Snapping)
    diagrams_extracted = 0
    print("\nRunning Media Extraction & 1-bit PNG Binarization...")
    for q in sorted_unique_qs:
        qnum = q.get("question_number")
        page_num = q.get("_page_number", 0)
        has_images = q.get("has_images", False)
        bbox = q.get("diagram_bounding_box")

        if has_images and bbox and page_num in rendered_pages:
            img_path = rendered_pages[page_num]
            media_key = f"q{qnum:02d}_diagram"
            media_entry = extract_and_binarize_media(
                page_image_path=img_path,
                bbox=bbox,
                media_key=media_key,
                output_dir=media_dir
            )
            if media_entry:
                q["media"] = {media_key: media_entry}
                q["has_images"] = True
                diagrams_extracted += 1
                print(f"  [Q{qnum:02d}] Extracted 1-bit diagram: {media_entry['width']}x{media_entry['height']} ({media_entry['file_bytes']} bytes)")
            else:
                q["has_images"] = False
        else:
            q["has_images"] = False

    print(f"Total visual diagrams embedded: {diagrams_extracted}")

    # 5. Assemble Canonical Schema
    final_paper_data = normalize_paper_json(
        paper_id=paper_id,
        year=year,
        subject=subject,
        session=session,
        questions=sorted_unique_qs,
        answer_keys=keys_map
    )

    # 6. Save final output
    out_dir = args.output_dir or os.path.join("data", "dataset", "papers", paper_id)
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "full_paper.json")

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(final_paper_data, f, indent=2)
    print(f"\nSuccessfully wrote final paper dataset: {out_file}")

    # 7. Update manifest
    if not args.no_manifest:
        manifest_path = os.path.join("data", "dataset", "manifest.json")
        update_dataset_manifest(manifest_path, final_paper_data)

    print(f"=== Pipeline completed successfully for {paper_id} ===")

if __name__ == "__main__":
    run_pipeline()
