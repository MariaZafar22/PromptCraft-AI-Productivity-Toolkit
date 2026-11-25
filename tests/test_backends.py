import unittest

from ai_productivity_toolkit import CallableLLM, MockLLM


class BackendTests(unittest.TestCase):
    def test_callable_llm_wraps_function(self):
        llm = CallableLLM(lambda p: p.upper(), name="up")
        self.assertEqual(llm.generate("hi", max_new_tokens=5), "HI")

    def test_mock_cycles_replies_and_records_calls(self):
        llm = MockLLM(replies=["a", "b"])
        self.assertEqual([llm.generate("x"), llm.generate("y"), llm.generate("z")], ["a", "b", "a"])
        self.assertEqual(llm.calls, ["x", "y", "z"])


if __name__ == "__main__":
    unittest.main()
