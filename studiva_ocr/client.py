"""
client.py - Gemini API client with thread-safe rate limiting and robust JSON parsing.
"""

import os
import re
import json
import time
import base64
import threading
from typing import Dict, Any, Optional
import requests

class GlobalRateLimiter:
    """Thread-safe rate limiter enforcing a minimum interval between requests."""
    def __init__(self, rpm: int = 12):
        self.min_interval = 60.0 / float(rpm) if rpm > 0 else 5.0
        self.lock = threading.Lock()
        self.last_call_time = 0.0

    def wait(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_call_time
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self.last_call_time = time.time()

def load_api_key(explicit_key: Optional[str] = None) -> str:
    """Resolve Gemini API key from explicit flag, environment, or .env file."""
    if explicit_key and explicit_key.strip():
        return explicit_key.strip()

    env_key = os.getenv("GEMINI_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()

    # Try .env
    dotenv_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(dotenv_path):
        with open(dotenv_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "GEMINI_API_KEY=" in line:
                    val = line.split("GEMINI_API_KEY=", 1)[1].strip()
                    val = val.strip("'\"")
                    if val:
                        return val

    raise ValueError("GEMINI_API_KEY not found. Pass --api-key or set GEMINI_API_KEY in environment or .env file.")

def robust_json_load(raw_text: str) -> Dict[str, Any]:
    """Parse JSON produced by Gemini, fixing unescaped LaTeX backslashes."""
    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()

    # Pre-emptively escape common LaTeX macros starting with valid JSON escape characters
    # (b, f, n, r, t) so that json.loads doesn't decode \frac to form-feed, \times to tab, etc.
    text = re.sub(
        r'\\(?=(?:frac|times|to|theta|tau|text|right|rho|beta|bar|binom|begin|neq|not|in\b))',
        r'\\\\',
        text
    )

    # First attempt: direct json.loads
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Escape invalid single backslashes in JSON strings
    # Match backslashes that are NOT followed by valid JSON escape chars: ", \, /, b, f, n, r, t, uXXXX
    cleaned = re.sub(r'\\(?![/\\\"bfnrtu])', r'\\\\', text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Second fallback: double every backslash inside string values
        def fix_quotes(match):
            val = match.group(0)
            # preserve valid quotes
            return val.replace('\\', '\\\\')
        cleaned2 = re.sub(r'"([^"\\]*(\\.[^"\\]*)*)"', fix_quotes, text)
        return json.loads(cleaned2)

def call_gemini_page(
    image_path: str,
    prompt: str,
    system_instruction: str,
    api_key: str,
    model: str = "gemini-3.5-flash-lite",
    rate_limiter: Optional[GlobalRateLimiter] = None,
    max_retries: int = 3,
    page_label: str = ""
) -> Dict[str, Any]:
    """
    Calls Gemini API with the page image and prompt, returning parsed JSON.
    Provides verbose logging and stops immediately on hard API rejections.
    """
    page_tag = f"[{page_label}] " if page_label else ""
    with open(image_path, "rb") as img_f:
        img_b64 = base64.b64encode(img_f.read()).decode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}

    payload = {
        "systemInstruction": {
            "parts": [{"text": system_instruction}]
        },
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "inlineData": {
                            "mimeType": "image/png",
                            "data": img_b64
                        }
                    },
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 1,
            "responseMimeType": "application/json"
        }
    }

    last_exc = None
    for attempt in range(1, max_retries + 1):
        if rate_limiter:
            rate_limiter.wait()

        print(f"{page_tag}Dispatching request to {model} (Attempt {attempt}/{max_retries})...")
        t_start = time.time()

        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=90)
            elapsed = time.time() - t_start

            # Check for Google AI Studio rejection codes
            if resp.status_code == 429:
                err_data = {}
                try:
                    err_data = resp.json().get("error", {})
                except Exception:
                    pass
                err_msg = err_data.get("message", resp.text[:120])
                print(f"{page_tag}Google AI Studio rate limit (429): {err_msg}")

                if "Resource has been exhausted" in err_msg or "daily" in err_msg.lower():
                    print(f"{page_tag}FATAL: Google AI Studio Daily Quota Exhausted. Stopping immediately.")
                    raise RuntimeError(f"Google AI Studio Daily Quota Exhausted: {err_msg}")

                wait_time = 15 * attempt
                print(f"{page_tag}Backing off for {wait_time}s before retry...")
                time.sleep(wait_time)
                continue

            if resp.status_code in (400, 401, 403, 404):
                err_text = resp.text[:300]
                print(f"{page_tag}FATAL: Google AI Studio rejected request with HTTP {resp.status_code}: {err_text}")
                raise RuntimeError(f"Google AI Studio hard rejection ({resp.status_code}): {err_text}")

            resp.raise_for_status()
            data = resp.json()
            candidates = data.get("candidates", [])
            if not candidates:
                prompt_feedback = data.get("promptFeedback", {})
                print(f"{page_tag}FATAL: No candidates returned. Prompt feedback: {prompt_feedback}")
                raise RuntimeError(f"Google AI Studio blocked prompt: {prompt_feedback}")

            first_candidate = candidates[0]
            finish_reason = first_candidate.get("finishReason", "UNKNOWN")

            if finish_reason == "RECITATION":
                print(f"{page_tag}FATAL: Google AI Studio rejected request with RECITATION filter on {model}. Halting immediately.")
                raise RuntimeError(f"Google AI Studio Recitation rejection on {model}")

            if finish_reason == "SAFETY":
                safety_ratings = first_candidate.get("safetyRatings", [])
                print(f"{page_tag}FATAL: Google AI Studio safety filter triggered: {safety_ratings}. Halting immediately.")
                raise RuntimeError(f"Safety filter triggered on {model}")

            text_content = first_candidate["content"]["parts"][0]["text"]
            usage = data.get("usageMetadata", {})
            prompt_tokens = usage.get("promptTokenCount", 0)
            cand_tokens = usage.get("candidatesTokenCount", 0)

            parsed_json = robust_json_load(text_content)
            num_qs = len(parsed_json.get("questions", []))
            print(f"{page_tag}Success in {elapsed:.2f}s ({num_qs} Qs, {prompt_tokens} in / {cand_tokens} out tokens)")
            return parsed_json

        except Exception as e:
            last_exc = e
            if "hard rejection" in str(e) or "Daily Quota" in str(e) or "safety filter" in str(e) or "Recitation" in str(e):
                raise
            print(f"{page_tag}Exception on attempt {attempt}: {e}")
            time.sleep(3 * attempt)

    raise RuntimeError(f"Failed to process {image_path} after {max_retries} attempts: {last_exc}")
