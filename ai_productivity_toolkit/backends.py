"""Model backends. Anything with `generate(prompt, **kwargs) -> str` can be used."""
from __future__ import annotations

from typing import Callable, List, Optional, Sequence


class HFBackend:
    """Hugging Face text2text backend (instruction-tuned, runs on Colab CPU)."""

    def __init__(self, model_name: str = "google/flan-t5-base", max_new_tokens: int = 128):
        from transformers import pipeline  # imported lazily

        self.name = model_name
        self.max_new_tokens = max_new_tokens
        self._pipe = pipeline("text2text-generation", model=model_name)

    def generate(self, prompt: str, max_new_tokens: Optional[int] = None) -> str:
        out = self._pipe(
            prompt,
            max_new_tokens=max_new_tokens or self.max_new_tokens,
            do_sample=False,
        )
        return out[0]["generated_text"].strip()


class CallableLLM:
    """Wrap any function `fn(prompt) -> str` (e.g. an API client call)."""

    def __init__(self, fn: Callable[[str], str], name: str = "custom"):
        self.fn = fn
        self.name = name

    def generate(self, prompt: str, **_) -> str:
        return self.fn(prompt)


class MockLLM:
    """Fake model for tests. Pass a list of replies (cycled) or a function."""

    def __init__(self, replies: Optional[Sequence[str]] = None,
                 fn: Optional[Callable[[str], str]] = None, name: str = "mock"):
        self.replies = list(replies or [])
        self.fn = fn
        self.name = name
        self.calls: List[str] = []

    def generate(self, prompt: str, **_) -> str:
        self.calls.append(prompt)
        if self.fn:
            return self.fn(prompt)
        if not self.replies:
            return ""
        return self.replies[(len(self.calls) - 1) % len(self.replies)]
