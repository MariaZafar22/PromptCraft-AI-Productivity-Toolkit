"""AI Productivity Toolkit: reusable prompt templates, structured output helpers,
productivity workflows and a prompt-testing harness. Model-agnostic."""
from .backends import CallableLLM, HFBackend, MockLLM
from .evaluation import (
    TestCase, TestResult, compare_prompts, contains_any, equals_label,
    max_words, run_suite, to_markdown, valid_json_with,
)
from .structured import StructuredOutputError, ask_json, extract_fields, extract_json
from .templates import PromptTemplate
from .workflows import (
    CLASSIFY, DEBUG_CODE, EMAIL, EXPLAIN_CODE, RESEARCH, RESUME, SUMMARIZE,
    classify, debug_code, explain_code, improve_resume_bullet, normalize_label,
    research_outline, summarize, write_email,
)

__version__ = "1.0.0"

__all__ = [
    "CallableLLM", "HFBackend", "MockLLM", "PromptTemplate",
    "StructuredOutputError", "ask_json", "extract_fields", "extract_json",
    "TestCase", "TestResult", "compare_prompts", "contains_any", "equals_label",
    "max_words", "run_suite", "to_markdown", "valid_json_with",
    "CLASSIFY", "DEBUG_CODE", "EMAIL", "EXPLAIN_CODE", "RESEARCH", "RESUME", "SUMMARIZE",
    "classify", "debug_code", "explain_code", "improve_resume_bullet", "normalize_label",
    "research_outline", "summarize", "write_email",
]
