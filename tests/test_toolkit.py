"""Offline unit tests (no model download needed). Run:  python -m unittest -v"""
import unittest

from ai_productivity_toolkit import (
    MockLLM, PromptTemplate, SUMMARIZE, StructuredOutputError, TestCase,
    ask_json, classify, compare_prompts, contains_any, equals_label, extract_fields,
    extract_json, max_words, normalize_label, run_suite, summarize, to_markdown, valid_json_with,
)


class TemplateTests(unittest.TestCase):
    def test_zero_shot_render_has_role_task_constraints(self):
        p = SUMMARIZE.render(input="Hello world", style="1 line", max_words=10)
        self.assertIn("Role:", p)
        self.assertIn("Summarize the text below as 1 line.", p)
        self.assertIn("at most 10 words", p)
        self.assertTrue(p.rstrip().endswith("Summary:"))

    def test_few_shot_includes_examples(self):
        t = PromptTemplate("t", "Do X").with_examples([("a", "b")])
        p = t.render(input="c")
        self.assertEqual(t.kind, "few-shot")
        self.assertIn("Input: a\nOutput: b", p)
        self.assertIn("Input: c\nOutput:", p)

    def test_braces_in_input_are_safe(self):
        t = PromptTemplate("t", "Explain")
        p = t.render(input="def f(): return {x}")
        self.assertIn("{x}", p)


class StructuredTests(unittest.TestCase):
    def test_extract_json_from_noisy_text(self):
        self.assertEqual(extract_json('Sure! ```json\n{"a": 1}\n``` done'), {"a": 1})
        self.assertIsNone(extract_json("no json here"))

    def test_ask_json_retries_then_succeeds(self):
        llm = MockLLM(replies=["not json", '{"name": "Ali", "age": "20"}'])
        data = ask_json(llm, "Extract", ["name", "age"])
        self.assertEqual(data["name"], "Ali")
        self.assertEqual(len(llm.calls), 2)

    def test_ask_json_raises_after_retries(self):
        llm = MockLLM(replies=["bad"])
        with self.assertRaises(StructuredOutputError):
            ask_json(llm, "Extract", ["x"], retries=1)

    def test_extract_fields_builds_dict(self):
        llm = MockLLM(fn=lambda p: "Sara" if "name" in p else "Lahore")
        out = extract_fields(llm, "Sara lives in Lahore.", {"name": "What is the name?", "city": "Which city?"})
        self.assertEqual(out, {"name": "Sara", "city": "Lahore"})


class WorkflowTests(unittest.TestCase):
    def test_classify_normalizes_label(self):
        self.assertEqual(normalize_label("It is POSITIVE.", ["positive", "negative"]), "positive")
        self.assertEqual(normalize_label("???", ["positive", "negative"]), "unknown")

    def test_classify_with_examples_uses_few_shot_prompt(self):
        llm = MockLLM(replies=["negative"])
        label = classify(llm, "bad service", ["positive", "negative"], examples=[("great", "positive")])
        self.assertEqual(label, "negative")
        self.assertIn("Text: great\nLabel: positive", llm.calls[0])

    def test_summarize_calls_model_once(self):
        llm = MockLLM(replies=["short"])
        self.assertEqual(summarize(llm, "long text"), "short")
        self.assertEqual(len(llm.calls), 1)


class EvaluationTests(unittest.TestCase):
    def test_run_suite_and_report(self):
        llm = MockLLM(replies=["positive", "this is far too long " * 5])
        cases = [
            TestCase("label", "p1", equals_label("positive"), "equals 'positive'"),
            TestCase("length", "p2", max_words(5), "max 5 words"),
        ]
        results = run_suite(llm, cases)
        self.assertEqual([r.passed for r in results], [True, False])
        md = to_markdown(results, backend_name="mock")
        self.assertIn("1/2 passed", md)
        self.assertIn("| 2 | length |", md)

    def test_compare_prompts(self):
        llm = MockLLM(fn=lambda p: "yes" if "please" in p else "no")
        res = compare_prompts(llm, {"polite": "please answer", "plain": "answer"}, contains_any("yes"))
        self.assertEqual({r.name: r.passed for r in res}, {"polite": True, "plain": False})

    def test_valid_json_check(self):
        self.assertTrue(valid_json_with("a")('{"a": 1}'))
        self.assertFalse(valid_json_with("a")('{"b": 1}'))


if __name__ == "__main__":
    unittest.main()
