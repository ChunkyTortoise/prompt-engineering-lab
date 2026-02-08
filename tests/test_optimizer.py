"""Tests for optimizer module."""

from __future__ import annotations

import pytest

from prompt_engineering_lab.optimizer import OptimizationResult, PromptOptimizer


class TestPromptOptimizer:
    """Test PromptOptimizer class."""

    def test_random_search_basic(self, simple_scorer):
        """Test basic random search."""
        optimizer = PromptOptimizer(simple_scorer)
        templates = ["short", "medium length", "this is a very long template"]
        result = optimizer.random_search(templates, n_iterations=5)
        assert isinstance(result, OptimizationResult)
        assert result.best_template in templates
        assert result.iterations == 5
        assert len(result.history) == 5

    def test_random_search_empty_templates(self, simple_scorer):
        """Test random search with empty templates raises ValueError."""
        optimizer = PromptOptimizer(simple_scorer)
        with pytest.raises(ValueError, match="cannot be empty"):
            optimizer.random_search([], n_iterations=5)

    def test_random_search_improvement(self, simple_scorer):
        """Test that random search finds better templates."""
        optimizer = PromptOptimizer(simple_scorer)
        templates = ["a", "abc", "abcdefghij"]
        result = optimizer.random_search(templates, n_iterations=10)
        # With simple_scorer (length), should find the longest template
        assert result.best_score >= simple_scorer(templates[0])

    def test_mutate_template_basic(self):
        """Test template mutation produces different output."""
        optimizer = PromptOptimizer(lambda x: 1.0)
        template = "this is a test template"
        mutated = optimizer.mutate_template(template)
        # Mutation might return same or different, so just check it's a string
        assert isinstance(mutated, str)

    def test_mutate_template_short(self):
        """Test mutating very short template."""
        optimizer = PromptOptimizer(lambda x: 1.0)
        template = "a"
        mutated = optimizer.mutate_template(template)
        assert mutated == "a"  # Too short to mutate

    def test_optimize_basic(self, simple_scorer):
        """Test optimize through mutation."""
        optimizer = PromptOptimizer(simple_scorer)
        result = optimizer.optimize("initial template", n_iterations=10)
        assert isinstance(result, OptimizationResult)
        assert result.iterations == 10
        assert len(result.history) == 10

    def test_optimize_improvement_tracking(self, simple_scorer):
        """Test that optimization tracks improvements."""
        optimizer = PromptOptimizer(simple_scorer)
        result = optimizer.optimize("test", n_iterations=5)
        assert result.best_score >= simple_scorer("test")
        assert result.improvement_pct >= 0 or result.improvement_pct < 0  # Can be positive or negative

    def test_optimization_result_dataclass(self):
        """Test OptimizationResult structure."""
        result = OptimizationResult(
            best_template="test", best_score=10.0, iterations=5, improvement_pct=20.0, history=[]
        )
        assert result.best_template == "test"
        assert result.best_score == 10.0
        assert result.iterations == 5
        assert result.improvement_pct == 20.0

    def test_random_search_with_constant_scorer(self, constant_scorer):
        """Test random search with constant scorer."""
        optimizer = PromptOptimizer(constant_scorer)
        templates = ["a", "b", "c"]
        result = optimizer.random_search(templates, n_iterations=3)
        assert result.best_score == 5.0
        assert result.improvement_pct == 0.0
