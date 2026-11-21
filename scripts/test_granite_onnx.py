import os
import sys
import time
import resource
import fitz  # PyMuPDF
from PIL import Image
import numpy as np
import onnxruntime as ort
from transformers import AutoConfig, AutoProcessor
from docling_core.types.doc.document import DocTagsDocument
from docling_core.types.doc import DoclingDocument

def render_pdf_page(pdf_path: str, page_num: int, output_img_path: str, dpi: int = 150):
    doc = fitz.open(pdf_path)
    page = doc[page_num - 1]
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    pix.save(output_img_path)
    print(f"Rendered page {page_num} to {output_img_path} ({pix.width}x{pix.height}) at {dpi} DPI")
    return output_img_path

def main():
    pdf_path = "CS/2013_CS.pdf"
    page_num = 3  # Page 3 contains math formulas, matrices, and a truth table
    out_dir = "./temp/2013_CS/docling"
    os.makedirs(out_dir, exist_ok=True)
    img_path = os.path.join(out_dir, f"page_{page_num}.png")
    
    # 1. Render page
    render_pdf_page(pdf_path, page_num, img_path, dpi=150)
    image = Image.open(img_path).convert("RGB")
    
    # 2. Paths
    model_dir = "./OCR/granite-docling-258M-ONNX"
    onnx_dir = os.path.join(model_dir, "onnx")
    
    vision_model_path = os.path.join(onnx_dir, "vision_encoder_int8.onnx")
    embed_model_path = os.path.join(onnx_dir, "embed_tokens_int8.onnx")
    decoder_model_path = os.path.join(onnx_dir, "decoder_model_merged_quantized.onnx")
    
    # Verify files exist
    for p in [vision_model_path, embed_model_path, decoder_model_path]:
        if not os.path.exists(p) or os.path.getsize(p) == 0:
            print(f"ERROR: Model file {p} does not exist or is empty.")
            sys.exit(1)
            
    print("\n--- Initializing ONNX Runtime Sessions (INT8) ---")
    sess_options = ort.SessionOptions()
    # Limit to 4 threads to prevent overheating while maintaining high throughput
    num_threads = min(4, os.cpu_count() or 4)
    sess_options.intra_op_num_threads = num_threads
    sess_options.inter_op_num_threads = 1
    sess_options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    print(f"ONNX Session thread count set to: {num_threads}")
    
    t0 = time.time()
    vision_session = ort.InferenceSession(vision_model_path, sess_options, providers=["CPUExecutionProvider"])
    embed_session = ort.InferenceSession(embed_model_path, sess_options, providers=["CPUExecutionProvider"])
    decoder_session = ort.InferenceSession(decoder_model_path, sess_options, providers=["CPUExecutionProvider"])
    load_time = time.time() - t0
    print(f"Loaded all 3 INT8 ONNX sessions in {load_time:.2f} seconds.")
    
    # 3. Load config and processor
    config = AutoConfig.from_pretrained(model_dir)
    processor = AutoProcessor.from_pretrained(model_dir)
    
    num_key_value_heads = config.text_config.num_key_value_heads
    head_dim = config.text_config.head_dim
    num_hidden_layers = config.text_config.num_hidden_layers
    eos_token_id = config.text_config.eos_token_id
    image_token_id = config.image_token_id
    
    # 4. Prepare inputs
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": "Convert this page to docling."}
            ]
        }
    ]
    
    print("\nApplying processor & chat template...")
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    # NOTE: do_image_splitting=True allows detailed patches for full page resolution
    inputs = processor(text=prompt, images=[image], return_tensors="np", do_image_splitting=True)
    
    batch_size = inputs['input_ids'].shape[0]
    past_key_values = {
        f'past_key_values.{layer}.{kv}': np.zeros([batch_size, num_key_value_heads, 0, head_dim], dtype=np.float32)
        for layer in range(num_hidden_layers)
        for kv in ('key', 'value')
    }
    
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']
    print(f"Initial input_ids shape: {input_ids.shape}, attention_mask shape: {attention_mask.shape}")
    
    # 5. Vision encoding
    print("\n--- Running Vision Encoder (INT8) ---")
    t_v0 = time.time()
    image_features = vision_session.run(None, dict(
        pixel_values=inputs['pixel_values'],
        pixel_attention_mask=inputs['pixel_attention_mask'].astype(np.bool_)
    ))[0]
    t_vision = time.time() - t_v0
    print(f"Vision encoding finished in {t_vision:.2f}s! image_features shape: {image_features.shape}")
    
    # 6. Autoregressive Decoding Loop with Live Streaming
    print("\n--- Starting Autoregressive Token Generation (Streaming) ---")
    max_new_tokens = 4096
    generated_tokens = np.array([[]], dtype=np.int64)
    
    t_gen_start = time.time()
    first_token_time = None
    
    for i in range(max_new_tokens):
        t_step0 = time.time()
        inputs_embeds = embed_session.run(None, {'input_ids': input_ids})[0]
        
        if i == 0:
            # Merge text and vision embeddings for prompt
            inputs_embeds[inputs['input_ids'] == image_token_id] = image_features.reshape(-1, image_features.shape[-1])
            
        logits, *present_key_values = decoder_session.run(None, dict(
            inputs_embeds=inputs_embeds,
            attention_mask=attention_mask,
            **past_key_values,
        ))
        
        if i == 0:
            first_token_time = time.time() - t_gen_start
            
        # Greedy decoding
        next_token = logits[:, -1].argmax(-1, keepdims=True)
        attention_mask = np.concatenate([attention_mask, np.ones((batch_size, 1), dtype=attention_mask.dtype)], axis=-1)
        for j, key in enumerate(past_key_values):
            past_key_values[key] = present_key_values[j]
            
        input_ids = next_token
        generated_tokens = np.concatenate([generated_tokens, input_ids], axis=-1)
        
        # Stream token live
        token_str = processor.decode(input_ids[0])
        sys.stdout.write(token_str)
        sys.stdout.flush()
        
        if (input_ids == eos_token_id).all():
            print("\n[EOS token reached]")
            break
            
    t_gen_total = time.time() - t_gen_start
    num_tokens = generated_tokens.shape[1]
    tps = num_tokens / t_gen_total if t_gen_total > 0 else 0
    
    print("\n" + "="*60)
    print("--- INFERENCE PERFORMANCE & RESOURCE USAGE ---")
    print(f"Total tokens generated : {num_tokens}")
    print(f"Vision encoder time    : {t_vision:.2f} s")
    print(f"Time to first token    : {first_token_time:.2f} s")
    print(f"Generation time        : {t_gen_total:.2f} s")
    print(f"Decoding speed         : {tps:.2f} tokens/sec")
    
    # Memory usage
    rusage = resource.getrusage(resource.RUSAGE_SELF)
    max_rss_mb = rusage.ru_maxrss / 1024  # Linux: ru_maxrss is in KB
    print(f"Peak RAM usage (RSS)   : {max_rss_mb:.2f} MB")
    print("="*60 + "\n")
    
    # 7. Convert DocTags to Docling Document & Markdown
    print("--- Converting DocTags to Markdown via docling-core ---")
    doctags = processor.batch_decode(generated_tokens, skip_special_tokens=False)[0].lstrip()
    
    doctags_path = os.path.join(out_dir, f"page_{page_num}_doctags.txt")
    with open(doctags_path, "w", encoding="utf-8") as f:
        f.write(doctags)
    print(f"Saved raw DocTags to: {doctags_path}")
    
    try:
        doctags_doc = DocTagsDocument.from_doctags_and_image_pairs([doctags], [image])
        doc = DoclingDocument.load_from_doctags(doctags_doc, document_name=f"2013_CS_Page_{page_num}")
        md_text = doc.export_to_markdown()
        
        md_path = os.path.join(out_dir, f"page_{page_num}_onnx.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_text)
        print(f"Saved Markdown to: {md_path}")
        print("\n=== GENERATED MARKDOWN SAMPLE ===")
        print(md_text[:2000])
    except Exception as e:
        print(f"Error during DocTagsDocument conversion: {e}")
        # Save raw doctags fallback
        with open(os.path.join(out_dir, f"page_{page_num}_fallback.txt"), "w", encoding="utf-8") as f:
            f.write(doctags)

if __name__ == "__main__":
    main()
