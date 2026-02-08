"""Prompt Engineering Lab - Toolkit for prompt engineering techniques."""

from __future__ import annotations

__version__ = "0.1.0"
__author__ = "ChunkyTortoise"

from prompt_engineering_lab.ab_tester import ABTestResult, ABTestRunner
from prompt_engineering_lab.cost_calculator import CostCalculator, CostEstimate
from prompt_engineering_lab.optimizer import OptimizationResult, PromptOptimizer
from prompt_engineering_lab.patterns import ChainOfThought, FewShotPattern, RolePlayPattern, SelfRefinePattern
from prompt_engineering_lab.template import PromptChain, PromptTemplate, TemplateRegistry
from prompt_engineering_lab.token_counter import TokenCounter

__all__ = [
    "ABTestResult",
    "ABTestRunner",
    "ChainOfThought",
    "CostCalculator",
    "CostEstimate",
    "FewShotPattern",
    "OptimizationResult",
    "PromptChain",
    "PromptOptimizer",
    "PromptTemplate",
    "RolePlayPattern",
    "SelfRefinePattern",
    "TemplateRegistry",
    "TokenCounter",
]
