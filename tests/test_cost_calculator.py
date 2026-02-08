"""Tests for cost_calculator module."""

from __future__ import annotations

import pytest

from prompt_engineering_lab.cost_calculator import CostCalculator, CostEstimate


class TestCostCalculator:
    """Test CostCalculator class."""

    def test_estimate_basic(self):
        """Test basic cost estimation."""
        calc = CostCalculator()
        result = calc.estimate(1000, 500, "claude", "opus")
        assert isinstance(result, CostEstimate)
        assert result.total_cost > 0
        assert result.provider == "claude"
        assert result.model == "opus"

    def test_estimate_invalid_provider(self):
        """Test estimation with invalid provider."""
        calc = CostCalculator()
        with pytest.raises(ValueError, match="Unknown provider"):
            calc.estimate(1000, 500, "invalid", "model")

    def test_estimate_invalid_model(self):
        """Test estimation with invalid model."""
        calc = CostCalculator()
        with pytest.raises(ValueError, match="Unknown model"):
            calc.estimate(1000, 500, "claude", "invalid")

    def test_compare_providers_basic(self):
        """Test comparing providers."""
        calc = CostCalculator()
        results = calc.compare_providers(1000, 500)
        assert len(results) > 0
        assert all(isinstance(r, CostEstimate) for r in results)
        # Should be sorted by cost
        costs = [r.total_cost for r in results]
        assert costs == sorted(costs)

    def test_cost_estimate_dataclass(self):
        """Test CostEstimate structure."""
        estimate = CostEstimate(input_cost=0.01, output_cost=0.02, total_cost=0.03, provider="claude", model="sonnet")
        assert estimate.total_cost == 0.03
        assert estimate.provider == "claude"

    def test_estimate_different_models(self):
        """Test cost differences between models."""
        calc = CostCalculator()
        opus = calc.estimate(1000, 1000, "claude", "opus")
        haiku = calc.estimate(1000, 1000, "claude", "haiku")
        # Opus should be more expensive
        assert opus.total_cost > haiku.total_cost
