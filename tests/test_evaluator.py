"""Tests for prompt_lab.evaluator module."""

from __future__ import annotations

from prompt_lab.evaluator import EvaluationResult, PromptEvaluator


class TestFaithfulness:
    def test_high_faithfulness(self):
        evaluator = PromptEvaluator()
        context = "The Eiffel Tower was built in 1889 and is 330 meters tall."
        output = "The Eiffel Tower was built in 1889. It is 330 meters tall."
        score = evaluator.faithfulness(output, context)
        assert score > 0.5

    def test_low_faithfulness(self):
        evaluator = PromptEvaluator()
        context = "The Eiffel Tower was built in 1889."
        output = "Python is a programming language used for web development."
        score = evaluator.faithfulness(output, context)
        assert score < 0.3

    def test_empty_output(self):
        evaluator = PromptEvaluator()
        score = evaluator.faithfulness("", "Some context here")
        assert score == 0.0

    def test_empty_context(self):
        evaluator = PromptEvaluator()
        score = evaluator.faithfulness("Some output here", "")
        assert score == 0.0


class TestRelevance:
    def test_relevant_output(self):
        evaluator = PromptEvaluator()
        query = "What is the return policy for electronics?"
        output = "Electronics can be returned within 30 days with receipt."
        score = evaluator.relevance(output, query)
        assert score > 0.0

    def test_irrelevant_output(self):
        evaluator = PromptEvaluator()
        query = "What is the return policy for electronics?"
        output = "The weather today is sunny with a high of 75 degrees."
        score = evaluator.relevance(output, query)
        # May not be exactly 0 due to TF-IDF, but should be low
        assert score < 0.3

    def test_empty_strings(self):
        evaluator = PromptEvaluator()
        assert evaluator.relevance("", "query") == 0.0
        assert evaluator.relevance("output", "") == 0.0
        assert evaluator.relevance("", "") == 0.0


class TestCompleteness:
    def test_all_topics_found(self):
        evaluator = PromptEvaluator()
        output = "The return policy allows 30 days for electronics with receipt."
        topics = ["return", "days", "electronics"]
        score = evaluator.completeness(output, topics)
        assert score == 1.0

    def test_partial_topics(self):
        evaluator = PromptEvaluator()
        output = "The return policy is 30 days."
        topics = ["return", "days", "electronics", "receipt"]
        score = evaluator.completeness(output, topics)
        assert 0.0 < score < 1.0
        assert score == 0.5  # 2 out of 4

    def test_no_topics(self):
        evaluator = PromptEvaluator()
        score = evaluator.completeness("any output", [])
        assert score == 1.0


class TestEvaluate:
    def test_full_evaluation(self):
        evaluator = PromptEvaluator()
        result = evaluator.evaluate(
            output="Electronics can be returned within 30 days with receipt.",
            query="What is the return policy for electronics?",
            context="Return policy: Electronics 30 days with receipt.",
            expected_topics=["return", "days", "receipt"],
        )
        assert isinstance(result, EvaluationResult)
        assert 0 <= result.faithfulness <= 1
        assert 0 <= result.relevance <= 1
        assert 0 <= result.completeness <= 1
        assert 0 <= result.overall <= 1

    def test_overall_range(self):
        evaluator = PromptEvaluator()
        result = evaluator.evaluate(
            output="The sky is blue on a clear day.",
            query="What color is the sky?",
            context="The sky appears blue due to Rayleigh scattering.",
            expected_topics=["blue", "sky"],
        )
        assert 0 <= result.overall <= 1
