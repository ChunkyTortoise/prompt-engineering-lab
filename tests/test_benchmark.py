"""Tests for prompt_lab.benchmark module."""

from __future__ import annotations

from prompt_lab.benchmark import BenchmarkReport, BenchmarkResult, BenchmarkRunner
from prompt_lab.evaluator import EvaluationResult
from prompt_lab.patterns import PromptPattern


def _make_pattern(name: str = "test_pattern") -> PromptPattern:
    return PromptPattern(
        name=name,
        description="Test",
        template="Solve: {{problem}}",
        variables=["problem"],
    )


class TestBenchmarkRunner:
    def test_run_single(self):
        runner = BenchmarkRunner()
        pattern = _make_pattern()
        result = runner.run_single(
            pattern=pattern,
            task_name="math",
            variables={"problem": "2+2"},
            mock_output="The answer is 4",
            query="What is 2+2?",
        )
        assert isinstance(result, BenchmarkResult)
        assert result.pattern_name == "test_pattern"
        assert result.task_name == "math"

    def test_latency_recorded(self):
        runner = BenchmarkRunner()
        pattern = _make_pattern()
        result = runner.run_single(
            pattern=pattern,
            task_name="math",
            variables={"problem": "2+2"},
            mock_output="4",
        )
        assert result.latency_ms >= 0

    def test_evaluation_present(self):
        runner = BenchmarkRunner()
        pattern = _make_pattern()
        result = runner.run_single(
            pattern=pattern,
            task_name="math",
            variables={"problem": "2+2"},
            mock_output="The answer is 4",
            query="What is 2+2?",
            expected_topics=["answer"],
        )
        assert isinstance(result.evaluation, EvaluationResult)


class TestBenchmarkComparison:
    def _make_tasks(self) -> list[dict]:
        return [
            {
                "name": "task1",
                "query": "What is 2+2?",
                "context": "Basic arithmetic.",
                "expected_topics": ["answer"],
                "variables": {
                    "pattern_a": {"problem": "What is 2+2?"},
                    "pattern_b": {"problem": "What is 2+2?"},
                },
                "mock_outputs": {
                    "pattern_a": "The answer is 4",
                    "pattern_b": "2+2 equals 4",
                },
            },
        ]

    def test_run_comparison(self):
        runner = BenchmarkRunner()
        patterns = [_make_pattern("pattern_a"), _make_pattern("pattern_b")]
        tasks = self._make_tasks()
        report = runner.run_comparison(patterns, tasks)
        assert isinstance(report, BenchmarkReport)
        assert len(report.results) > 0

    def test_best_pattern_selected(self):
        runner = BenchmarkRunner()
        patterns = [_make_pattern("pattern_a"), _make_pattern("pattern_b")]
        tasks = self._make_tasks()
        report = runner.run_comparison(patterns, tasks)
        if report.summary:
            assert report.best_pattern in report.summary

    def test_summary_has_metrics(self):
        runner = BenchmarkRunner()
        patterns = [_make_pattern("pattern_a"), _make_pattern("pattern_b")]
        tasks = self._make_tasks()
        report = runner.run_comparison(patterns, tasks)
        for scores in report.summary.values():
            assert "avg_faithfulness" in scores
            assert "avg_relevance" in scores
            assert "avg_completeness" in scores
            assert "avg_overall" in scores
            assert "avg_latency_ms" in scores
            assert "num_tasks" in scores

    def test_empty_tasks(self):
        runner = BenchmarkRunner()
        patterns = [_make_pattern()]
        report = runner.run_comparison(patterns, [])
        assert isinstance(report, BenchmarkReport)
        assert len(report.results) == 0


class TestBenchmarkReport:
    def _make_report(self) -> BenchmarkReport:
        runner = BenchmarkRunner()
        patterns = [_make_pattern("alpha"), _make_pattern("beta")]
        tasks = [
            {
                "name": "task1",
                "query": "Explain gravity",
                "context": "Physics concept about gravitational force.",
                "expected_topics": ["gravity", "force"],
                "variables": {
                    "alpha": {"problem": "Explain gravity"},
                    "beta": {"problem": "Explain gravity"},
                },
                "mock_outputs": {
                    "alpha": "Gravity is a fundamental force that attracts objects with mass.",
                    "beta": "Gravity pulls things down toward the earth.",
                },
            },
            {
                "name": "task2",
                "query": "What is photosynthesis?",
                "context": "Biological process in plants converting light to energy.",
                "expected_topics": ["plants", "light", "energy"],
                "variables": {
                    "alpha": {"problem": "What is photosynthesis?"},
                    "beta": {"problem": "What is photosynthesis?"},
                },
                "mock_outputs": {
                    "alpha": "Photosynthesis converts light energy into chemical energy in plants.",
                    "beta": "Plants use light to make food through photosynthesis.",
                },
            },
        ]
        return runner.run_comparison(patterns, tasks)

    def test_report_fields(self):
        report = self._make_report()
        assert hasattr(report, "results")
        assert hasattr(report, "best_pattern")
        assert hasattr(report, "summary")

    def test_summary_averages(self):
        report = self._make_report()
        for scores in report.summary.values():
            assert 0 <= scores["avg_faithfulness"] <= 1
            assert 0 <= scores["avg_relevance"] <= 1
            assert 0 <= scores["avg_completeness"] <= 1
            assert 0 <= scores["avg_overall"] <= 1

    def test_multiple_patterns(self):
        report = self._make_report()
        assert len(report.summary) == 2
