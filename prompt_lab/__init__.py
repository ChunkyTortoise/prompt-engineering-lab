"""prompt-engineering-lab: Prompt patterns, evaluation, and A/B testing framework."""

__version__ = "0.1.0"

from prompt_lab.ab_tester import ABTester, ABTestResult, VariantResult
from prompt_lab.benchmark import BenchmarkReport, BenchmarkResult, BenchmarkRunner
from prompt_lab.categories import CategoryRegistry, TaskCategory, TaskExample
from prompt_lab.evaluator import EvaluationResult, PromptEvaluator
from prompt_lab.patterns import PatternLibrary, PromptPattern
from prompt_lab.report_generator import ReportGenerator

__all__ = [
    "ABTestResult",
    "ABTester",
    "BenchmarkReport",
    "BenchmarkResult",
    "BenchmarkRunner",
    "CategoryRegistry",
    "EvaluationResult",
    "PatternLibrary",
    "PromptEvaluator",
    "PromptPattern",
    "ReportGenerator",
    "TaskCategory",
    "TaskExample",
    "VariantResult",
]
