"""Prompt Engineering Lab - Toolkit for prompt engineering techniques."""

from __future__ import annotations

__version__ = "0.1.0"
__author__ = "ChunkyTortoise"

from prompt_engineering_lab.ab_tester import ABTestResult, ABTestRunner
from prompt_engineering_lab.cost_calculator import CostCalculator, CostEstimate
from prompt_engineering_lab.evaluator import (
    EvaluationReport,
    PromptEvaluator,
    RougeScore,
    RougeScorer,
    SemanticSimilarity,
    TokenEfficiencyMetric,
)
from prompt_engineering_lab.optimizer import OptimizationResult, PromptOptimizer
from prompt_engineering_lab.patterns import ChainOfThought, FewShotPattern, RolePlayPattern, SelfRefinePattern
from prompt_engineering_lab.safety import PromptSafetyChecker, SafetyResult
from prompt_engineering_lab.template import PromptChain, PromptTemplate, TemplateRegistry
from prompt_engineering_lab.token_counter import TokenCounter
from prompt_engineering_lab.versioning import PromptVersion, PromptVersionManager, VersionDiff

__all__ = [
    "ABTestResult",
    "ABTestRunner",
    "ChainOfThought",
    "CostCalculator",
    "CostEstimate",
    "EvaluationReport",
    "FewShotPattern",
    "OptimizationResult",
    "PromptChain",
    "PromptEvaluator",
    "PromptOptimizer",
    "PromptTemplate",
    "RolePlayPattern",
    "RougeScore",
    "RougeScorer",
    "SemanticSimilarity",
    "SelfRefinePattern",
    "TemplateRegistry",
    "TokenCounter",
    "TokenEfficiencyMetric",
    "PromptSafetyChecker",
    "PromptVersion",
    "PromptVersionManager",
    "SafetyResult",
    "VersionDiff",
]
