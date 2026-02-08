"""A/B testing for prompt patterns with z-test statistical significance."""

from __future__ import annotations

import math
from dataclasses import dataclass

from prompt_lab.evaluator import PromptEvaluator


@dataclass
class VariantResult:
    """Results for one variant in an A/B test."""

    pattern_name: str
    scores: list[float]
    mean: float
    std: float
    n: int


@dataclass
class ABTestResult:
    """Result of an A/B test comparison."""

    variant_a: VariantResult
    variant_b: VariantResult
    z_score: float
    p_value: float
    is_significant: bool  # p < 0.05
    winner: str  # pattern name of winner, or "tie"
    lift: float  # percentage improvement of winner over loser


class ABTester:
    """A/B test prompt patterns with statistical significance.

    Compares two prompt patterns on the same tasks using z-test.
    """

    def __init__(self, significance_level: float = 0.05):
        self.significance_level = significance_level
        self._evaluator = PromptEvaluator()

    def compare(
        self,
        scores_a: list[float],
        scores_b: list[float],
        name_a: str = "variant_a",
        name_b: str = "variant_b",
    ) -> ABTestResult:
        """Compare two sets of scores using a two-sample z-test.

        Args:
            scores_a: Evaluation scores for variant A
            scores_b: Evaluation scores for variant B
            name_a: Name for variant A
            name_b: Name for variant B
        """
        va = self._compute_variant(name_a, scores_a)
        vb = self._compute_variant(name_b, scores_b)

        z_score = self._z_test(va, vb)
        p_value = self._p_value(z_score)
        is_significant = p_value < self.significance_level

        if not is_significant:
            winner = "tie"
            lift = 0.0
        elif va.mean > vb.mean:
            winner = name_a
            lift = ((va.mean - vb.mean) / vb.mean * 100) if vb.mean > 0 else 0.0
        else:
            winner = name_b
            lift = ((vb.mean - va.mean) / va.mean * 100) if va.mean > 0 else 0.0

        return ABTestResult(
            variant_a=va,
            variant_b=vb,
            z_score=round(z_score, 4),
            p_value=round(p_value, 4),
            is_significant=is_significant,
            winner=winner,
            lift=round(lift, 2),
        )

    def evaluate_and_compare(
        self,
        outputs_a: list[str],
        outputs_b: list[str],
        queries: list[str],
        contexts: list[str] | None = None,
        name_a: str = "variant_a",
        name_b: str = "variant_b",
        metric: str = "overall",
    ) -> ABTestResult:
        """Evaluate outputs and compare using the specified metric.

        Evaluates each output pair and extracts the specified metric for comparison.
        """
        contexts = contexts or [""] * len(queries)

        scores_a = []
        scores_b = []

        for out_a, out_b, query, ctx in zip(outputs_a, outputs_b, queries, contexts):
            eval_a = self._evaluator.evaluate(out_a, query=query, context=ctx)
            eval_b = self._evaluator.evaluate(out_b, query=query, context=ctx)
            scores_a.append(getattr(eval_a, metric))
            scores_b.append(getattr(eval_b, metric))

        return self.compare(scores_a, scores_b, name_a, name_b)

    def _compute_variant(self, name: str, scores: list[float]) -> VariantResult:
        """Compute statistics for a variant."""
        n = len(scores)
        if n == 0:
            return VariantResult(pattern_name=name, scores=[], mean=0.0, std=0.0, n=0)
        mean = sum(scores) / n
        variance = sum((s - mean) ** 2 for s in scores) / n if n > 1 else 0.0
        std = math.sqrt(variance)
        return VariantResult(
            pattern_name=name,
            scores=scores,
            mean=round(mean, 4),
            std=round(std, 4),
            n=n,
        )

    def _z_test(self, va: VariantResult, vb: VariantResult) -> float:
        """Two-sample z-test statistic."""
        if va.n == 0 or vb.n == 0:
            return 0.0
        se = math.sqrt((va.std**2 / va.n) + (vb.std**2 / vb.n))
        if se == 0:
            return 0.0
        return (va.mean - vb.mean) / se

    def _p_value(self, z: float) -> float:
        """Approximate two-tailed p-value from z-score using normal CDF approximation."""
        # Abramowitz and Stegun approximation
        x = abs(z)
        if x > 8:
            return 0.0
        t = 1.0 / (1.0 + 0.2316419 * x)
        d = 0.3989422804014327  # 1/sqrt(2*pi)
        p = (
            d
            * math.exp(-x * x / 2.0)
            * (
                t
                * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.8212560 + t * 1.3302744))))
            )
        )
        return round(2.0 * p, 6)  # two-tailed
