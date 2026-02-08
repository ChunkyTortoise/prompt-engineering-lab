"""A/B testing framework for comparing prompt templates."""

from __future__ import annotations

import statistics
from dataclasses import dataclass
from typing import Callable


@dataclass
class ABTestResult:
    """Results from an A/B test comparison."""

    winner: str
    p_value: float
    effect_size: float
    a_mean: float
    b_mean: float
    sample_size: int


class ABTestRunner:
    """Runner for A/B tests comparing two prompt templates."""

    def __init__(self, scorer: Callable[[str], float]):
        self.scorer = scorer

    def run(self, template_a: str, template_b: str, inputs: list[str]) -> ABTestResult:
        if not inputs:
            raise ValueError("inputs list cannot be empty")

        a_scores = [self.scorer(template_a) for _ in inputs]
        b_scores = [self.scorer(template_b) for _ in inputs]

        a_mean = statistics.mean(a_scores)
        b_mean = statistics.mean(b_scores)

        p_value, effect_size = self.z_test(a_scores, b_scores)

        if p_value < 0.05:
            winner = "A" if a_mean > b_mean else "B"
        else:
            winner = "no_significant_difference"

        return ABTestResult(
            winner=winner,
            p_value=p_value,
            effect_size=effect_size,
            a_mean=a_mean,
            b_mean=b_mean,
            sample_size=len(inputs),
        )

    @staticmethod
    def z_test(a_scores: list[float], b_scores: list[float]) -> tuple[float, float]:
        if len(a_scores) < 2 or len(b_scores) < 2:
            return 1.0, 0.0

        mean_a = statistics.mean(a_scores)
        mean_b = statistics.mean(b_scores)

        try:
            std_a = statistics.stdev(a_scores)
            std_b = statistics.stdev(b_scores)
        except statistics.StatisticsError:
            return 1.0, 0.0

        if std_a == 0 and std_b == 0:
            return 1.0, 0.0

        n_a = len(a_scores)
        n_b = len(b_scores)

        pooled_std = ((std_a**2 / n_a) + (std_b**2 / n_b)) ** 0.5

        if pooled_std == 0:
            return 1.0, 0.0

        z_score = abs(mean_a - mean_b) / pooled_std

        if z_score > 2.58:
            p_value = 0.01
        elif z_score > 1.96:
            p_value = 0.04
        elif z_score > 1.0:
            p_value = 0.15
        else:
            p_value = 0.32

        pooled_std_dev = ((std_a**2 + std_b**2) / 2) ** 0.5
        effect_size = abs(mean_a - mean_b) / pooled_std_dev if pooled_std_dev > 0 else 0.0

        return p_value, effect_size
