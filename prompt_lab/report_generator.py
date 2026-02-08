"""Report generation: markdown comparison tables and benchmark summaries."""

from __future__ import annotations

from prompt_lab.ab_tester import ABTestResult
from prompt_lab.benchmark import BenchmarkReport


class ReportGenerator:
    """Generate markdown reports from benchmark and A/B test results."""

    def benchmark_table(self, report: BenchmarkReport) -> str:
        """Generate a markdown comparison table from benchmark results."""
        lines = ["# Benchmark Results\n"]
        lines.append("| Pattern | Task | Faithfulness | Relevance | Completeness | Overall | Latency (ms) |")
        lines.append("|---------|------|--------------|-----------|--------------|---------|-------------|")

        for r in report.results:
            lines.append(
                f"| {r.pattern_name} | {r.task_name} | "
                f"{r.evaluation.faithfulness:.4f} | {r.evaluation.relevance:.4f} | "
                f"{r.evaluation.completeness:.4f} | {r.evaluation.overall:.4f} | "
                f"{r.latency_ms:.1f} |"
            )

        lines.append(f"\n**Best Pattern**: {report.best_pattern} (overall: {report.best_overall:.4f})")
        return "\n".join(lines)

    def summary_table(self, report: BenchmarkReport) -> str:
        """Generate a summary table with per-pattern averages."""
        lines = ["# Pattern Summary\n"]
        lines.append("| Pattern | Avg Faith. | Avg Relev. | Avg Compl. | Avg Overall | Tasks |")
        lines.append("|---------|------------|------------|------------|-------------|-------|")

        for pname, scores in report.summary.items():
            lines.append(
                f"| {pname} | {scores['avg_faithfulness']:.4f} | "
                f"{scores['avg_relevance']:.4f} | {scores['avg_completeness']:.4f} | "
                f"{scores['avg_overall']:.4f} | {scores['num_tasks']} |"
            )

        return "\n".join(lines)

    def ab_test_report(self, result: ABTestResult) -> str:
        """Generate a markdown report from an A/B test result."""
        lines = ["# A/B Test Results\n"]
        lines.append(f"**Variant A**: {result.variant_a.pattern_name} (n={result.variant_a.n})")
        lines.append(f"**Variant B**: {result.variant_b.pattern_name} (n={result.variant_b.n})\n")

        lines.append("| Metric | Variant A | Variant B |")
        lines.append("|--------|-----------|-----------|")
        lines.append(f"| Mean | {result.variant_a.mean:.4f} | {result.variant_b.mean:.4f} |")
        lines.append(f"| Std Dev | {result.variant_a.std:.4f} | {result.variant_b.std:.4f} |")
        lines.append(f"| N | {result.variant_a.n} | {result.variant_b.n} |")

        lines.append(f"\n**Z-Score**: {result.z_score:.4f}")
        lines.append(f"**P-Value**: {result.p_value:.6f}")
        lines.append(f"**Significant**: {'Yes' if result.is_significant else 'No'}")
        lines.append(f"**Winner**: {result.winner}")
        if result.lift > 0:
            lines.append(f"**Lift**: {result.lift:.2f}%")

        return "\n".join(lines)
