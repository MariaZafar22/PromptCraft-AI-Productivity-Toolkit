"""Reusable prompt templates (role, context, instruction, constraints, examples)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


_VAR = re.compile(r"\{(\w+)\}")


def _fill(text: str, values: Dict[str, object]) -> str:
    """Single-pass {var} substitution (safe for code / braces inside values)."""
    return _VAR.sub(lambda m: str(values.get(m.group(1), m.group(0))), text)


@dataclass
class PromptTemplate:
    name: str
    instruction: str
    role: str = ""
    context: str = ""
    constraints: List[str] = field(default_factory=list)
    examples: List[Tuple[str, str]] = field(default_factory=list)  # few-shot
    input_label: str = "Input"
    output_label: str = "Output"

    def with_examples(self, examples: List[Tuple[str, str]]) -> "PromptTemplate":
        """Return a copy turned into a few-shot template."""
        return PromptTemplate(self.name + "+fewshot", self.instruction, self.role,
                              self.context, list(self.constraints), list(examples),
                              self.input_label, self.output_label)

    def render(self, **values) -> str:
        parts: List[str] = []
        if self.role:
            parts.append(f"Role: {_fill(self.role, values)}")
        if self.context:
            parts.append(f"Context: {_fill(self.context, values)}")
        parts.append(f"Task: {_fill(self.instruction, values)}")
        if self.constraints:
            parts.append("Constraints:\n" + "\n".join(f"- {_fill(c, values)}" for c in self.constraints))
        for ex_in, ex_out in self.examples:
            parts.append(f"{self.input_label}: {ex_in}\n{self.output_label}: {ex_out}")
        parts.append(f"{self.input_label}: {values.get('input', '')}\n{self.output_label}:")
        return "\n\n".join(parts)

    @property
    def kind(self) -> str:
        return "few-shot" if self.examples else "zero-shot"
