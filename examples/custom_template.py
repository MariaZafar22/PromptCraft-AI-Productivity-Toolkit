"""Build your own reusable template and test it with the evaluation harness."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # run without installing
import sys

from ai_productivity_toolkit import (
    HFBackend, MockLLM, PromptTemplate, TestCase, contains_any, max_words, run_suite, to_markdown,
)

llm = MockLLM(fn=lambda p: "Learning prompt engineering #AI #Prompts") if "--mock" in sys.argv \
    else HFBackend("google/flan-t5-base")

tweet = PromptTemplate(
    name="tweet",
    role="You are a social media writer.",
    instruction="Write a tweet about: {topic}",
    constraints=["Max 30 words", "Add 2 hashtags"],
)
prompt = tweet.render(input="", topic="learning prompt engineering")
print(prompt, "\n")

cases = [
    TestCase("short enough", prompt, max_words(30), "<= 30 words"),
    TestCase("has hashtag", prompt, contains_any("#"), "contains #"),
]
print(to_markdown(run_suite(llm, cases), backend_name=llm.name))
