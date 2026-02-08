"""Cost estimation utilities for AI API calls."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CostEstimate:
    """Cost estimate for an AI API call."""

    input_cost: float
    output_cost: float
    total_cost: float
    provider: str
    model: str


class CostCalculator:
    """Calculator for estimating AI API costs across different providers."""

    PRICING = {
        "claude": {
            "opus": {"input_per_1k": 0.015, "output_per_1k": 0.075},
            "sonnet": {"input_per_1k": 0.003, "output_per_1k": 0.015},
            "haiku": {"input_per_1k": 0.00025, "output_per_1k": 0.00125},
        },
        "openai": {
            "gpt-4": {"input_per_1k": 0.03, "output_per_1k": 0.06},
            "gpt-4-turbo": {"input_per_1k": 0.01, "output_per_1k": 0.03},
            "gpt-3.5-turbo": {"input_per_1k": 0.0005, "output_per_1k": 0.0015},
        },
        "gemini": {
            "pro": {"input_per_1k": 0.00025, "output_per_1k": 0.0005},
            "ultra": {"input_per_1k": 0.01, "output_per_1k": 0.02},
        },
    }

    def estimate(self, input_tokens: int, output_tokens: int, provider: str, model: str) -> CostEstimate:
        provider_lower = provider.lower()
        model_lower = model.lower()

        if provider_lower not in self.PRICING:
            raise ValueError(f"Unknown provider: {provider}. Available: {', '.join(self.PRICING.keys())}")

        if model_lower not in self.PRICING[provider_lower]:
            raise ValueError(
                f"Unknown model: {model} for provider {provider}. "
                f"Available: {', '.join(self.PRICING[provider_lower].keys())}"
            )

        pricing = self.PRICING[provider_lower][model_lower]

        input_cost = (input_tokens / 1000) * pricing["input_per_1k"]
        output_cost = (output_tokens / 1000) * pricing["output_per_1k"]
        total_cost = input_cost + output_cost

        return CostEstimate(
            input_cost=input_cost, output_cost=output_cost, total_cost=total_cost, provider=provider, model=model
        )

    def compare_providers(self, input_tokens: int, output_tokens: int) -> list[CostEstimate]:
        estimates = []
        for provider, models in self.PRICING.items():
            for model in models:
                try:
                    estimate = self.estimate(input_tokens, output_tokens, provider, model)
                    estimates.append(estimate)
                except ValueError:
                    continue
        estimates.sort(key=lambda x: x.total_cost)
        return estimates
