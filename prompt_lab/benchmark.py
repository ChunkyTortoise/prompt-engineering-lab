"""Benchmark runner: measure prompt pattern performance with reproducible results."""

from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass

from prompt_lab.evaluator import EvaluationResult, PromptEvaluator
from prompt_lab.patterns import PromptPattern


@dataclass
class BenchmarkResult:
    """Result of benchmarking a single prompt pattern on a task."""

    pattern_name: str
    task_name: str
    rendered_prompt: str
    mock_output: str
    evaluation: EvaluationResult
    latency_ms: float


@dataclass
class BenchmarkReport:
    """Complete benchmark report across patterns and tasks."""

    results: list[BenchmarkResult]
    best_pattern: str
    best_overall: float
    summary: dict[str, dict[str, float]]  # pattern -> {avg_faithfulness, avg_relevance, ...}


class BenchmarkRunner:
    """Run benchmarks across prompt patterns and tasks.

    Uses mock outputs (no LLM calls needed) for reproducible evaluation.
    """

    def __init__(self):
        self._evaluator = PromptEvaluator()

    def run_single(
        self,
        pattern: PromptPattern,
        task_name: str,
        variables: dict[str, str],
        mock_output: str,
        context: str = "",
        query: str = "",
        expected_topics: list[str] | None = None,
    ) -> BenchmarkResult:
        """Benchmark a single pattern on a single task."""
        start = time.perf_counter()
        rendered = pattern.render(**variables)
        elapsed = (time.perf_counter() - start) * 1000

        evaluation = self._evaluator.evaluate(
            output=mock_output,
            query=query or rendered,
            context=context,
            expected_topics=expected_topics,
        )

        return BenchmarkResult(
            pattern_name=pattern.name,
            task_name=task_name,
            rendered_prompt=rendered,
            mock_output=mock_output,
            evaluation=evaluation,
            latency_ms=round(elapsed, 3),
        )

    def run_comparison(
        self,
        patterns: list[PromptPattern],
        tasks: list[dict],
    ) -> BenchmarkReport:
        """Run all patterns against all tasks and generate a report.

        Each task dict should have: name, variables (dict per pattern name or default),
        mock_output (per pattern name or default), context, query, expected_topics.
        """
        results: list[BenchmarkResult] = []

        for task in tasks:
            for pattern in patterns:
                variables = task.get("variables", {}).get(pattern.name, task.get("default_variables", {}))
                mock_output = task.get("mock_outputs", {}).get(pattern.name, task.get("default_output", ""))

                if not variables:
                    continue

                try:
                    result = self.run_single(
                        pattern=pattern,
                        task_name=task.get("name", "unnamed"),
                        variables=variables,
                        mock_output=mock_output,
                        context=task.get("context", ""),
                        query=task.get("query", ""),
                        expected_topics=task.get("expected_topics"),
                    )
                    results.append(result)
                except (ValueError, KeyError):
                    continue

        summary = self._compute_summary(results)
        best_pattern = ""
        best_overall = 0.0

        for pname, scores in summary.items():
            if scores.get("avg_overall", 0) > best_overall:
                best_overall = scores["avg_overall"]
                best_pattern = pname

        return BenchmarkReport(
            results=results,
            best_pattern=best_pattern,
            best_overall=round(best_overall, 4),
            summary=summary,
        )

    def _compute_summary(self, results: list[BenchmarkResult]) -> dict[str, dict[str, float]]:
        """Compute per-pattern average metrics."""
        groups: dict[str, list[BenchmarkResult]] = defaultdict(list)
        for r in results:
            groups[r.pattern_name].append(r)

        summary = {}
        for pname, group in groups.items():
            n = len(group)
            summary[pname] = {
                "avg_faithfulness": round(sum(r.evaluation.faithfulness for r in group) / n, 4),
                "avg_relevance": round(sum(r.evaluation.relevance for r in group) / n, 4),
                "avg_completeness": round(sum(r.evaluation.completeness for r in group) / n, 4),
                "avg_overall": round(sum(r.evaluation.overall for r in group) / n, 4),
                "avg_latency_ms": round(sum(r.latency_ms for r in group) / n, 3),
                "num_tasks": n,
            }
        return summary
