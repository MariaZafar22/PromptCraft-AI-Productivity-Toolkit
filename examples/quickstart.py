"""Minimal tour of the toolkit.  Run:  python examples/quickstart.py [--mock]"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # run without installing
import sys

from ai_productivity_toolkit import (
    HFBackend, MockLLM, classify, extract_fields, improve_resume_bullet, summarize, write_email,
)

llm = MockLLM(fn=lambda p: "[mock output]") if "--mock" in sys.argv else HFBackend("google/flan-t5-base")

print("Summary :", summarize(llm, "Remote work saves commuting time but makes spontaneous talks harder.",
                              style="one sentence", max_words=20))
print("Label   :", classify(llm, "The package arrived broken.", ["complaint", "praise", "question"],
                             examples=[("Thanks, great help!", "praise"), ("Where is my order?", "question")]))
print("JSON    :", extract_fields(llm, "I am Sara from Karachi.",
                                   {"name": "What is the name?", "city": "Which city?"}))
print("Email   :", write_email(llm, "ask for a deadline extension", recipient="my manager",
                                points=["two extra days"]))
print("Resume  :", improve_resume_bullet(llm, "helped with a website project", role="Web Developer"))
