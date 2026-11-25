"""Command line interface:  python -m ai_productivity_toolkit <command> [options]"""
from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from . import __version__
from .backends import HFBackend, MockLLM
from .workflows import (
    classify, debug_code, explain_code, improve_resume_bullet,
    research_outline, summarize, write_email,
)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ai-toolkit", description="AI Productivity Toolkit")
    p.add_argument("--version", action="version", version=__version__)
    p.add_argument("--model", default="google/flan-t5-base", help="Hugging Face text2text model")
    p.add_argument("--mock", action="store_true", help="use a fake offline model (plumbing check)")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("summarize", help="summarize text")
    s.add_argument("text")
    s.add_argument("--style", default="3 short bullet points")
    s.add_argument("--max-words", type=int, default=60)

    c = sub.add_parser("classify", help="classify text into one label")
    c.add_argument("text")
    c.add_argument("--labels", required=True, help="comma separated, e.g. positive,negative,neutral")

    e = sub.add_parser("email", help="draft an email")
    e.add_argument("purpose")
    e.add_argument("--to", default="a colleague")
    e.add_argument("--tone", default="polite and professional")
    e.add_argument("--point", action="append", default=[], help="point to mention (repeatable)")

    r = sub.add_parser("resume", help="improve a resume bullet")
    r.add_argument("bullet")
    r.add_argument("--role", default="Software Engineer")

    x = sub.add_parser("explain", help="explain code")
    x.add_argument("code")
    x.add_argument("--language", default="Python")

    d = sub.add_parser("debug", help="find the bug in code")
    d.add_argument("code")
    d.add_argument("--error", default="none")
    d.add_argument("--language", default="Python")

    q = sub.add_parser("research", help="create a research outline")
    q.add_argument("topic")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    llm = MockLLM(fn=lambda prompt: "[mock output]") if args.mock else HFBackend(args.model)

    if args.command == "summarize":
        out = summarize(llm, args.text, args.style, args.max_words)
    elif args.command == "classify":
        out = classify(llm, args.text, [l.strip() for l in args.labels.split(",") if l.strip()])
    elif args.command == "email":
        out = write_email(llm, args.purpose, args.to, args.tone, args.point)
    elif args.command == "resume":
        out = improve_resume_bullet(llm, args.bullet, args.role)
    elif args.command == "explain":
        out = explain_code(llm, args.code, args.language)
    elif args.command == "debug":
        out = debug_code(llm, args.code, args.error, args.language)
    else:
        out = research_outline(llm, args.topic)
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
