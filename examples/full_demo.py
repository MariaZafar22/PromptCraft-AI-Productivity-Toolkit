"""Run every toolkit workflow once.

    python examples/full_demo.py         # uses google/flan-t5-base (downloads ~1 GB on first run)
    python demo.py --mock     # offline, fake model: only checks the plumbing
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # run without installing
import argparse
import json

from ai_productivity_toolkit import (
    HFBackend, MockLLM, classify, debug_code, explain_code, extract_fields,
    improve_resume_bullet, research_outline, summarize, write_email,
)

ARTICLE = ("Remote work has changed how teams collaborate. Companies save on office costs, "
           "and employees save commuting time. However, managers report that spontaneous "
           "communication is harder, and new hires take longer to settle in.")
CODE = "def add(a, b):\n    return a - b\n"
NOTE = "Hi, I am Sara Ahmed from Karachi. I would like to book a demo on Monday."


def section(title: str) -> None:
    print(f"\n=== {title} ===")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="use a fake model (offline)")
    args = parser.parse_args()
    llm = MockLLM(fn=lambda p: "[mock output]") if args.mock else HFBackend("google/flan-t5-base")

    section("Summarize")
    print(summarize(llm, ARTICLE, style="2 short bullet points", max_words=40))

    section("Classify (few-shot)")
    print(classify(llm, "The package arrived broken.", ["complaint", "praise", "question"],
                   examples=[("Thanks, great help!", "praise"), ("Where is my order?", "question")]))

    section("Structured output (field by field)")
    print(json.dumps(extract_fields(llm, NOTE, {
        "name": "What is the person's name?",
        "city": "Which city is the person from?",
        "request": "What does the person want?",
    }), indent=2))

    section("Email")
    print(write_email(llm, "ask for a project deadline extension", recipient="my manager",
                      points=["two extra days", "quality will improve"]))

    section("Resume bullet")
    print(improve_resume_bullet(llm, "helped with a website project", role="Web Developer"))

    section("Explain + debug code")
    print(explain_code(llm, CODE))
    print(debug_code(llm, CODE, error="add(2, 3) returns -1, expected 5"))

    section("Research outline")
    print(research_outline(llm, "Effects of remote work on team productivity"))


if __name__ == "__main__":
    main()
