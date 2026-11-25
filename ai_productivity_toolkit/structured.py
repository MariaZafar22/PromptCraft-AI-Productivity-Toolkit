"""Structured (JSON) output helpers for models that do not reliably emit JSON."""
from __future__ import annotations

import json
import re
from typing import Dict, Optional, Sequence


class StructuredOutputError(ValueError):
    pass


def extract_json(text: str) -> Optional[dict]:
    """Find the first valid JSON object in free-form model output."""
    cleaned = re.sub(r"```(?:json)?", "", text)
    decoder = json.JSONDecoder()
    for m in re.finditer(r"\{", cleaned):
        try:
            obj, _ = decoder.raw_decode(cleaned[m.start():])
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            continue
    return None


def ask_json(llm, prompt: str, required_keys: Sequence[str], retries: int = 2) -> dict:
    """Ask for JSON, validate required keys, retry with a corrective prompt."""
    keys = ", ".join(required_keys)
    ask = f"{prompt}\n\nReturn ONLY a valid JSON object with exactly these keys: {keys}."
    last = ""
    for attempt in range(retries + 1):
        last = llm.generate(ask)
        data = extract_json(last)
        if data is not None and all(k in data for k in required_keys):
            return data
        ask = (f"{prompt}\n\nYour previous reply was not valid JSON with keys [{keys}]. "
               f"Reply with ONLY the JSON object, no extra text.")
    raise StructuredOutputError(f"No valid JSON after {retries + 1} tries. Last reply: {last!r}")


def extract_fields(llm, text: str, fields: Dict[str, str]) -> dict:
    """Reliable structured output for small models: ask one question per field,
    then assemble the JSON ourselves (so the result is always valid JSON)."""
    result = {}
    for key, question in fields.items():
        answer = llm.generate(f"{text}\n\nQuestion: {question}\nAnswer:")
        result[key] = answer.strip()
    return result
