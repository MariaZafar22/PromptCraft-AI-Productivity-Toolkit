# Prompt Patterns Cheat Sheet

Reusable prompt patterns used in this toolkit. Fill the `{placeholders}` and test them with `run_suite` before relying on them.

## Anatomy of a good prompt

| Part | Question it answers | Example |
|------|--------------------|---------|
| Role | Who should the model act as? | `You are a careful editor.` |
| Context | What background does it need? | `The email is to my manager. Tone: polite.` |
| Instruction | What exactly should it do? | `Summarize the text below as 3 bullet points.` |
| Constraints | What limits apply? | `At most 60 words. Do not add new facts.` |
| Examples | What does a good answer look like? | `Input: ... Output: ...` (few-shot) |

## Patterns

### 1. Zero-shot instruction
```
Classify the text as positive, negative or neutral. Answer with the label only.
Text: {text}
Label:
```
Use when the task is common and the label set is obvious.

### 2. Few-shot
```
Text: The phone broke after two days.   Label: negative
Text: Great quality, fast delivery.     Label: positive
Text: {text}                            Label:
```
Use when the format or labels are easy to confuse. 3 to 5 varied examples are enough.

### 3. Role + audience
```
You are a {role}. Explain {topic} to {audience} in {n} sentences.
```

### 4. Constrained summary
```
Summarize the text as {style}. Use at most {max_words} words. Do not add facts that are not in the text.
```

### 5. Structured output
```
Extract the fields below from the text. Return ONLY a valid JSON object with keys: {keys}.
Text: {text}
```
Always validate the result (`ask_json`) and retry. For small models, ask one question per field (`extract_fields`).

### 6. Rewrite with a rubric
```
Rewrite the bullet: start with a strong action verb, show the result, one sentence, do not invent numbers.
Original: {bullet}
Improved:
```

### 7. Code review
```
You are a senior {language} developer. Find the bug, state it in one sentence, then show the fixed code.
Error message: {error}
Code: {code}
```

### 8. Research outline
```
Create a research outline for {topic}: 4 specific, numbered questions to investigate.
```

### 9. Step-by-step reasoning (for larger models)
```
Solve the problem. Think step by step, then give the final answer on a new line starting with "Answer:".
```

### 10. Self-check
```
Here is a draft answer: {draft}
Check it against the source text. List any claim that is not supported, then give a corrected version.
```

## Common mistakes
- Vague task ("Tell me about X") instead of a specific instruction.
- No length or format limit, so the output is hard to use or test.
- Trusting JSON output without validation.
- Changing several things at once, so you do not know what improved the result. Change one part per test.
