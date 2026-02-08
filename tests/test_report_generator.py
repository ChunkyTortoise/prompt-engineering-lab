"""Tests for prompt_lab.report_generator module."""

from __future__ import annotations

from prompt_lab.ab_tester import ABTester, ABTestResult
from prompt_lab.benchmark import BenchmarkRunner
from prompt_lab.patterns import PromptPattern
from prompt_lab.report_generator import ReportGenerator


def _make_report():
    runner = BenchmarkRunner()
    patterns = [
        PromptPattern(name="alpha", description="A", template="Solve: {{problem}}", variables=["problem"]),
        PromptPattern(name="beta", description="B", template="Solve: {{problem}}", variables=["problem"]),
    ]
    tasks = [
        {
            "name": "task1",
            "query": "What is gravity?",
            "context": "Gravity is a fundamental force.",
            "expected_topics": ["gravity", "force"],
            "variables": {
                "alpha": {"problem": "What is gravity?"},
                "beta": {"problem": "What is gravity?"},
            },
            "mock_outputs": {
                "alpha": "Gravity is the force that attracts objects with mass.",
                "beta": "Things fall down because of gravity.",
            },
        },
    ]
    return runner.run_comparison(patterns, tasks)


def _make_ab_result(significant: bool = True) -> ABTestResult:
    tester = ABTester()
    if significant:
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
    else:
        scores_a = [0.8, 0.82, 0.79, 0.81, 0.80]
        scores_b = [0.8, 0.82, 0.79, 0.81, 0.80]
    return tester.compare(scores_a, scores_b, "pattern_a", "pattern_b")


class TestBenchmarkTable:
    def test_generates_markdown(self):
        report = _make_report()
        gen = ReportGenerator()
        table = gen.benchmark_table(report)
        assert "# Benchmark Results" in table
        assert "|" in table

    def test_contains_headers(self):
        report = _make_report()
        gen = ReportGenerator()
        table = gen.benchmark_table(report)
        assert "Pattern" in table
        assert "Faithfulness" in table
        assert "Relevance" in table

    def test_contains_results(self):
        report = _make_report()
        gen = ReportGenerator()
        table = gen.benchmark_table(report)
        assert "alpha" in table or "beta" in table

    def test_best_pattern_shown(self):
        report = _make_report()
        gen = ReportGenerator()
        table = gen.benchmark_table(report)
        assert "Best Pattern" in table


class TestSummaryTable:
    def test_generates_summary(self):
        report = _make_report()
        gen = ReportGenerator()
        table = gen.summary_table(report)
        assert "# Pattern Summary" in table
        assert "Avg Faith." in table


class TestABTestReport:
    def test_generates_report(self):
        result = _make_ab_result()
        gen = ReportGenerator()
        report = gen.ab_test_report(result)
        assert "# A/B Test Results" in report

    def test_shows_winner(self):
        result = _make_ab_result(significant=True)
        gen = ReportGenerator()
        report = gen.ab_test_report(result)
        assert "Winner" in report

    def test_shows_significance(self):
        result = _make_ab_result(significant=True)
        gen = ReportGenerator()
        report = gen.ab_test_report(result)
        assert "Significant" in report

    def test_shows_metrics(self):
        result = _make_ab_result()
        gen = ReportGenerator()
        report = gen.ab_test_report(result)
        assert "Mean" in report
        assert "Std Dev" in report

    def test_empty_result(self):
        result = _make_ab_result(significant=False)
        gen = ReportGenerator()
        report = gen.ab_test_report(result)
        assert "tie" in report
