"""Prompt evaluation: test cases, check helpers, comparison and markdown reports."""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Dict, List, Sequence

from .structured import extract_json


Check = Callable[[str], bool]


def contains_any(*words: str) -> Check:
    return lambda out: any(w.lower() in out.lower() for w in words)


def max_words(n: int) -> Check:
    return lambda out: 0 < len(out.split()) <= n


def equals_label(label: str) -> Check:
    return lambda out: out.strip().lower() == label.lower()


def valid_json_with(*keys: str) -> Check:
    def _check(out: str) -> bool:
        data = extract_json(out)
        return data is not None and all(k in data for k in keys)
    return _check


@dataclass
class TestCase:
    name: str
    prompt: str
    check: Check
    check_desc: str = ""


@dataclass
class TestResult:
    name: str
    passed: bool
    seconds: float
    output: str
    check_desc: str


def run_suite(llm, cases: Sequence[TestCase]) -> List[TestResult]:
    results = []
    for c in cases:
        start = time.time()
        try:
            out = llm.generate(c.prompt)
        except Exception as e:  # keep the suite running
            out = f"[ERROR] {e}"
        results.append(TestResult(c.name, bool(c.check(out)), time.time() - start, out, c.check_desc))
    return results


def compare_prompts(llm, variants: Dict[str, str], check: Check) -> List[TestResult]:
    """Run the same task with several prompt wordings and score each."""
    return run_suite(llm, [TestCase(n, p, check) for n, p in variants.items()])


def to_markdown(results: Sequence[TestResult], backend_name: str = "unknown",
                title: str = "Prompt Testing Report") -> str:
    total = len(results)
    ok = sum(r.passed for r in results)
    lines = [f"# {title}", "",
             f"- Model/backend: `{backend_name}`",
             f"- Generated: {time.strftime('%Y-%m-%d %H:%M')}",
             f"- Result: **{ok}/{total} passed** ({(100 * ok // total) if total else 0}%)", "",
             "| # | Test | Check | Result | Time (s) |", "|---|------|-------|--------|----------|"]
    for i, r in enumerate(results, 1):
        lines.append(f"| {i} | {r.name} | {r.check_desc or '-'} | {'PASS' if r.passed else 'FAIL'} | {r.seconds:.2f} |")
    lines += ["", "## Outputs", ""]
    for r in results:
        out = r.output.replace("\n", " ").strip()
        lines.append(f"**{r.name}** ({'PASS' if r.passed else 'FAIL'}): {out[:300]}")
        lines.append("")
    return "\n".join(lines)
