"""Ready-made productivity workflows built on prompt templates."""
from __future__ import annotations

import difflib
from typing import List, Optional, Sequence, Tuple

from .templates import PromptTemplate


SUMMARIZE = PromptTemplate(
    name="summarize",
    role="You are a careful editor.",
    instruction="Summarize the text below as {style}.",
    constraints=["Use at most {max_words} words.", "Do not add facts that are not in the text."],
    input_label="Text", output_label="Summary",
)

CLASSIFY = PromptTemplate(
    name="classify",
    instruction="Classify the text into exactly one label from: {labels}.",
    constraints=["Answer with the label only."],
    input_label="Text", output_label="Label",
)

EMAIL = PromptTemplate(
    name="email",
    role="You are a professional assistant who writes clear, polite emails.",
    context="The email is to {recipient}. Tone: {tone}.",
    instruction="Write a short email about: {purpose}.",
    constraints=["Include a subject line.", "Mention these points: {points}.", "Keep it under 120 words."],
    input_label="Request", output_label="Email",
)

RESUME = PromptTemplate(
    name="resume_bullet",
    role="You are a resume coach for the role of {role}.",
    instruction="Rewrite the resume bullet to be impactful: start with a strong action verb and show the result.",
    constraints=["One sentence.", "Do not invent numbers that are not given."],
    input_label="Original bullet", output_label="Improved bullet",
)

EXPLAIN_CODE = PromptTemplate(
    name="explain_code",
    role="You are a patient senior {language} developer.",
    instruction="Explain what the code does in simple words.",
    constraints=["Maximum 4 sentences."],
    input_label="Code", output_label="Explanation",
)

DEBUG_CODE = PromptTemplate(
    name="debug_code",
    role="You are a senior {language} developer doing code review.",
    instruction="Find the bug in the code and show the corrected line. Error message (if any): {error}.",
    constraints=["First state the bug in one sentence.", "Then give the fixed code."],
    input_label="Code", output_label="Review",
)

RESEARCH = PromptTemplate(
    name="research",
    role="You are a research assistant.",
    instruction="Create a short research outline for the topic with 4 key questions to investigate.",
    constraints=["Numbered list.", "Questions must be specific, not generic."],
    input_label="Topic", output_label="Outline",
)


def summarize(llm, text: str, style: str = "3 short bullet points", max_words: int = 60) -> str:
    return llm.generate(SUMMARIZE.render(input=text, style=style, max_words=max_words))


def classify(llm, text: str, labels: Sequence[str],
             examples: Optional[List[Tuple[str, str]]] = None) -> str:
    """Return one of `labels` (fuzzy-matched) or 'unknown'."""
    tpl = CLASSIFY.with_examples(examples) if examples else CLASSIFY
    raw = llm.generate(tpl.render(input=text, labels=", ".join(labels)))
    return normalize_label(raw, labels)


def normalize_label(raw: str, labels: Sequence[str]) -> str:
    low = raw.strip().lower()
    for lab in labels:
        if lab.lower() == low:
            return lab
    for lab in labels:
        if lab.lower() in low:
            return lab
    close = difflib.get_close_matches(low, [l.lower() for l in labels], n=1, cutoff=0.6)
    if close:
        return next(l for l in labels if l.lower() == close[0])
    return "unknown"


def write_email(llm, purpose: str, recipient: str = "a colleague", tone: str = "polite and professional",
                points: Sequence[str] = ()) -> str:
    prompt = EMAIL.render(input=purpose, purpose=purpose, recipient=recipient,
                          tone=tone, points="; ".join(points) or "none")
    return llm.generate(prompt, max_new_tokens=200)


def improve_resume_bullet(llm, bullet: str, role: str = "Software Engineer") -> str:
    return llm.generate(RESUME.render(input=bullet, role=role))


def explain_code(llm, code: str, language: str = "Python") -> str:
    return llm.generate(EXPLAIN_CODE.render(input=code, language=language))


def debug_code(llm, code: str, error: str = "none", language: str = "Python") -> str:
    return llm.generate(DEBUG_CODE.render(input=code, error=error, language=language))


def research_outline(llm, topic: str) -> str:
    return llm.generate(RESEARCH.render(input=topic))
