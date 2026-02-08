"""Token counting utilities for different AI providers."""

from __future__ import annotations


class TokenCounter:
    """Token counter for estimating token usage across different providers."""

    CHARS_PER_TOKEN = {
        "claude": 3.5,
        "openai": 4.0,
        "gemini": 4.0,
        "default": 4.0,
    }

    def count(self, text: str, provider: str = "claude") -> int:
        if not text:
            return 0
        chars_per_token = self.CHARS_PER_TOKEN.get(provider.lower(), self.CHARS_PER_TOKEN["default"])
        return int(len(text) / chars_per_token)

    def count_messages(self, messages: list[dict], provider: str = "claude") -> int:
        if not messages:
            return 0

        total_tokens = 0
        for msg in messages:
            if not isinstance(msg, dict) or "content" not in msg:
                raise ValueError("Each message must be a dict with 'content' key")
            content = msg["content"]
            total_tokens += self.count(content, provider)
            total_tokens += 4

        return total_tokens

    def estimate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        provider: str = "claude",
        input_rate: float = 0.003,
        output_rate: float = 0.015,
    ) -> float:
        input_cost = (input_tokens / 1000) * input_rate
        output_cost = (output_tokens / 1000) * output_rate
        return input_cost + output_cost
