"""Tests for prompt_lab.ab_tester module."""

from __future__ import annotations

from prompt_lab.ab_tester import ABTester, ABTestResult


class TestVariantResult:
    def test_compute_stats(self):
        tester = ABTester()
        variant = tester._compute_variant("test", [0.8, 0.9, 0.7, 0.85])
        assert variant.n == 4
        assert 0.8 <= variant.mean <= 0.82
        assert variant.std > 0

    def test_empty_scores(self):
        tester = ABTester()
        variant = tester._compute_variant("test", [])
        assert variant.n == 0
        assert variant.mean == 0.0
        assert variant.std == 0.0


class TestABTester:
    def test_significant_difference(self):
        tester = ABTester()
        scores_a = [
            0.9,
            0.88,
            0.92,
            0.91,
            0.89,
            0.93,
            0.90,
            0.87,
            0.91,
            0.92,
            0.88,
            0.90,
            0.91,
            0.89,
            0.93,
            0.90,
            0.92,
            0.88,
            0.91,
            0.90,
        ]
        scores_b = [
            0.5,
            0.52,
            0.48,
            0.51,
            0.49,
            0.53,
            0.50,
            0.47,
            0.51,
            0.52,
            0.48,
            0.50,
            0.51,
            0.49,
            0.53,
            0.50,
            0.52,
            0.48,
            0.51,
            0.50,
        ]
        result = tester.compare(scores_a, scores_b, "good", "bad")
        assert result.is_significant is True
        assert result.winner == "good"

    def test_no_difference(self):
        tester = ABTester()
        scores = [0.8, 0.82, 0.79, 0.81, 0.80]
        result = tester.compare(scores, scores, "a", "b")
        assert result.winner == "tie"

    def test_winner_selected(self):
        tester = ABTester()
        scores_a = [
            0.9,
            0.92,
            0.88,
            0.91,
            0.90,
            0.89,
            0.93,
            0.91,
            0.90,
            0.92,
            0.88,
            0.91,
            0.90,
            0.89,
            0.92,
            0.91,
            0.90,
            0.93,
            0.88,
            0.91,
        ]
        scores_b = [
            0.6,
            0.62,
            0.58,
            0.61,
            0.60,
            0.59,
            0.63,
            0.61,
            0.60,
            0.62,
            0.58,
            0.61,
            0.60,
            0.59,
            0.62,
            0.61,
            0.60,
            0.63,
            0.58,
            0.61,
        ]
        result = tester.compare(scores_a, scores_b, "winner", "loser")
        assert result.winner == "winner"

    def test_lift_calculated(self):
        tester = ABTester()
        scores_a = [
            0.9,
            0.92,
            0.88,
            0.91,
            0.90,
            0.89,
            0.93,
            0.91,
            0.90,
            0.92,
            0.88,
            0.91,
            0.90,
            0.89,
            0.92,
            0.91,
            0.90,
            0.93,
            0.88,
            0.91,
        ]
        scores_b = [
            0.6,
            0.62,
            0.58,
            0.61,
            0.60,
            0.59,
            0.63,
            0.61,
            0.60,
            0.62,
            0.58,
            0.61,
            0.60,
            0.59,
            0.62,
            0.61,
            0.60,
            0.63,
            0.58,
            0.61,
        ]
        result = tester.compare(scores_a, scores_b, "a", "b")
        assert result.lift > 0

    def test_p_value_range(self):
        tester = ABTester()
        scores_a = [0.7, 0.75, 0.72, 0.68, 0.74]
        scores_b = [0.65, 0.70, 0.67, 0.63, 0.69]
        result = tester.compare(scores_a, scores_b, "a", "b")
        assert 0 <= result.p_value <= 1


class TestZTest:
    def test_zero_variance(self):
        tester = ABTester()
        scores_a = [0.8, 0.8, 0.8, 0.8, 0.8]
        scores_b = [0.8, 0.8, 0.8, 0.8, 0.8]
        result = tester.compare(scores_a, scores_b, "a", "b")
        assert result.z_score == 0.0
        assert result.winner == "tie"

    def test_large_sample(self):
        tester = ABTester()
        scores_a = [0.8 + i * 0.001 for i in range(100)]
        scores_b = [0.5 + i * 0.001 for i in range(100)]
        result = tester.compare(scores_a, scores_b, "a", "b")
        assert isinstance(result, ABTestResult)
        assert result.z_score != 0.0

    def test_small_sample(self):
        tester = ABTester()
        scores_a = [0.9, 0.8]
        scores_b = [0.5, 0.4]
        result = tester.compare(scores_a, scores_b, "a", "b")
        assert isinstance(result, ABTestResult)


class TestEvaluateAndCompare:
    def test_evaluate_and_compare(self):
        tester = ABTester()
        outputs_a = [
            "Electronics return within 30 days with receipt.",
            "The product has great battery life and performance.",
        ]
        outputs_b = [
            "Return policy applies to electronics.",
            "Battery is good.",
        ]
        queries = [
            "What is the return policy for electronics?",
            "How is the battery life?",
        ]
        result = tester.evaluate_and_compare(
            outputs_a, outputs_b, queries, name_a="detailed", name_b="brief"
        )
        assert isinstance(result, ABTestResult)
        assert result.variant_a.n == 2
        assert result.variant_b.n == 2

    def test_with_contexts(self):
        tester = ABTester()
        outputs_a = ["30 day return for electronics with receipt."]
        outputs_b = ["Returns accepted."]
        queries = ["Return policy?"]
        contexts = ["Policy: 30 days for electronics with receipt."]
        result = tester.evaluate_and_compare(
            outputs_a,
            outputs_b,
            queries,
            contexts=contexts,
            name_a="a",
            name_b="b",
        )
        assert isinstance(result, ABTestResult)

    def test_metric_selection(self):
        tester = ABTester()
        outputs_a = ["Electronics can be returned within 30 days with receipt."]
        outputs_b = ["You can return stuff."]
        queries = ["What is the return policy?"]
        contexts = ["Return policy: Electronics 30 days with receipt."]

        result_overall = tester.evaluate_and_compare(
            outputs_a,
            outputs_b,
            queries,
            contexts=contexts,
            metric="overall",
        )
        result_faith = tester.evaluate_and_compare(
            outputs_a,
            outputs_b,
            queries,
            contexts=contexts,
            metric="faithfulness",
        )
        # Different metrics should produce results (may differ in scores)
        assert isinstance(result_overall, ABTestResult)
        assert isinstance(result_faith, ABTestResult)
