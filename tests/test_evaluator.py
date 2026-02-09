"""Tests for prompt_engineering_lab.evaluator module."""

from __future__ import annotations

from prompt_engineering_lab.evaluator import (
    EvaluationReport,
    PromptEvaluator,
    RougeScore,
    RougeScorer,
    SemanticSimilarity,
    TokenEfficiencyMetric,
)


class TestRougeScorer:
    def test_rouge1_identical(self):
        scorer = RougeScorer()
        result = scorer.rouge1("the cat sat on the mat", "the cat sat on the mat")
        assert result.precision == 1.0
        assert result.recall == 1.0
        assert result.f1 == 1.0

    def test_rouge1_partial_overlap(self):
        scorer = RougeScorer()
        result = scorer.rouge1("the cat sat", "the cat sat on the mat")
        assert result.precision == 1.0  # 3/3 candidate words found in ref
        assert result.recall < 1.0  # not all ref words covered
        assert 0 < result.f1 < 1.0

    def test_rouge1_no_overlap(self):
        scorer = RougeScorer()
        result = scorer.rouge1("hello world", "foo bar baz")
        assert result.precision == 0.0
        assert result.recall == 0.0
        assert result.f1 == 0.0

    def test_rouge1_empty_candidate(self):
        scorer = RougeScorer()
        result = scorer.rouge1("", "some reference text")
        assert result.f1 == 0.0

    def test_rouge1_empty_reference(self):
        scorer = RougeScorer()
        result = scorer.rouge1("some candidate", "")
        assert result.f1 == 0.0

    def test_rouge2_identical(self):
        scorer = RougeScorer()
        result = scorer.rouge2("the cat sat on the mat", "the cat sat on the mat")
        assert result.f1 == 1.0

    def test_rouge2_partial_overlap(self):
        scorer = RougeScorer()
        result = scorer.rouge2("the cat sat on", "the cat sat on the mat")
        assert 0 < result.f1 < 1.0

    def test_rouge2_no_overlap(self):
        scorer = RougeScorer()
        result = scorer.rouge2("hello world", "foo bar baz")
        assert result.f1 == 0.0

    def test_rouge2_single_word(self):
        scorer = RougeScorer()
        result = scorer.rouge2("hello", "world")
        assert result.f1 == 0.0

    def test_rouge_l_identical(self):
        scorer = RougeScorer()
        result = scorer.rouge_l("the cat sat on the mat", "the cat sat on the mat")
        assert result.f1 == 1.0

    def test_rouge_l_subsequence(self):
        scorer = RougeScorer()
        result = scorer.rouge_l("the cat mat", "the cat sat on the mat")
        assert 0 < result.f1 < 1.0

    def test_rouge_l_empty(self):
        scorer = RougeScorer()
        result = scorer.rouge_l("", "some text")
        assert result.f1 == 0.0

    def test_rouge_score_dataclass(self):
        score = RougeScore(precision=0.5, recall=0.8, f1=0.615)
        assert score.precision == 0.5
        assert score.recall == 0.8
        assert score.f1 == 0.615

    def test_rouge1_duplicate_tokens(self):
        scorer = RougeScorer()
        result = scorer.rouge1("the the the", "the cat")
        # candidate has 3 'the', reference has 1 'the', overlap=1
        assert result.precision < 1.0


class TestSemanticSimilarity:
    def test_identical_texts(self):
        sim = SemanticSimilarity()
        score = sim.score("the quick brown fox", "the quick brown fox")
        assert score > 0.99

    def test_similar_texts(self):
        sim = SemanticSimilarity()
        score = sim.score(
            "the quick brown fox jumps over the lazy dog",
            "the fast brown fox leaps over the lazy dog",
        )
        assert score > 0.3

    def test_different_texts(self):
        sim = SemanticSimilarity()
        score = sim.score("machine learning algorithms", "chocolate cake recipe")
        assert score < 0.3

    def test_empty_candidate(self):
        sim = SemanticSimilarity()
        assert sim.score("", "some text") == 0.0

    def test_empty_reference(self):
        sim = SemanticSimilarity()
        assert sim.score("some text", "") == 0.0

    def test_fallback_similarity(self):
        sim = SemanticSimilarity()
        score = sim._fallback_similarity("hello world", "hello earth")
        assert 0 < score < 1.0

    def test_fallback_empty(self):
        sim = SemanticSimilarity()
        assert sim._fallback_similarity("", "text") == 0.0


class TestTokenEfficiencyMetric:
    def test_normal_efficiency(self):
        metric = TokenEfficiencyMetric()
        assert metric.score(0.8, 100) == 0.008

    def test_zero_tokens(self):
        metric = TokenEfficiencyMetric()
        assert metric.score(0.9, 0) == 0.0

    def test_negative_tokens(self):
        metric = TokenEfficiencyMetric()
        assert metric.score(0.9, -5) == 0.0


class TestEvaluationReport:
    def test_default_report(self):
        report = EvaluationReport()
        assert report.rouge_scores == {}
        assert report.similarity == 0.0
        assert report.efficiency == 0.0
        assert report.overall == 0.0

    def test_report_with_values(self):
        report = EvaluationReport(similarity=0.85, efficiency=0.01, overall=0.7)
        assert report.similarity == 0.85
        assert report.overall == 0.7


class TestPromptEvaluator:
    def test_evaluate_returns_report(self):
        evaluator = PromptEvaluator()
        report = evaluator.evaluate(
            candidate="the cat sat on the mat",
            reference="the cat sat on the mat",
            token_count=6,
        )
        assert isinstance(report, EvaluationReport)
        assert "rouge1" in report.rouge_scores
        assert "rouge2" in report.rouge_scores
        assert "rougeL" in report.rouge_scores

    def test_evaluate_identical_high_scores(self):
        evaluator = PromptEvaluator()
        report = evaluator.evaluate(
            candidate="the cat sat on the mat",
            reference="the cat sat on the mat",
            token_count=6,
        )
        assert report.rouge_scores["rouge1"].f1 == 1.0
        assert report.similarity > 0.9
        assert report.overall > 0.8

    def test_evaluate_batch(self):
        evaluator = PromptEvaluator()
        reports = evaluator.evaluate_batch(
            candidates=["hello world", "foo bar"],
            references=["hello world", "baz qux"],
            token_counts=[2, 2],
        )
        assert len(reports) == 2
        assert reports[0].rouge_scores["rouge1"].f1 == 1.0
        assert reports[1].rouge_scores["rouge1"].f1 == 0.0

    def test_compare_a_better(self):
        evaluator = PromptEvaluator()
        report_a = EvaluationReport(overall=0.9)
        report_b = EvaluationReport(overall=0.3)
        assert evaluator.compare(report_a, report_b) == "a"

    def test_compare_b_better(self):
        evaluator = PromptEvaluator()
        report_a = EvaluationReport(overall=0.2)
        report_b = EvaluationReport(overall=0.8)
        assert evaluator.compare(report_a, report_b) == "b"

    def test_compare_tie(self):
        evaluator = PromptEvaluator()
        report_a = EvaluationReport(overall=0.5)
        report_b = EvaluationReport(overall=0.5)
        assert evaluator.compare(report_a, report_b) == "tie"
