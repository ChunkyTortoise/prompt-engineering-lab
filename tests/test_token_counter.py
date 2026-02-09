"""Tests for token_counter module."""

from __future__ import annotations

import pytest

from prompt_engineering_lab.token_counter import TokenCounter


class TestTokenCounter:
    """Test TokenCounter class."""

    def test_count_basic(self):
        """Test basic token counting."""
        counter = TokenCounter()
        text = "Hello world"
        tokens = counter.count(text)
        assert tokens > 0
        assert isinstance(tokens, int)

    def test_count_empty(self):
        """Test counting empty text."""
        counter = TokenCounter()
        assert counter.count("") == 0

    def test_count_different_providers(self):
        """Test counting with different providers."""
        counter = TokenCounter()
        text = "This is a test" * 10
        claude_tokens = counter.count(text, "claude")
        openai_tokens = counter.count(text, "openai")
        _gemini_tokens = counter.count(text, "gemini")
        # Claude should have more tokens (lower chars per token)
        assert claude_tokens >= openai_tokens

    def test_count_messages_basic(self):
        """Test counting tokens in messages."""
        counter = TokenCounter()
        messages = [{"content": "Hello"}, {"content": "World"}]
        tokens = counter.count_messages(messages)
        assert tokens > counter.count("Hello") + counter.count("World")  # Includes overhead

    def test_count_messages_empty(self):
        """Test counting empty messages."""
        counter = TokenCounter()
        assert counter.count_messages([]) == 0

    def test_count_messages_invalid_format(self):
        """Test counting messages with invalid format."""
        counter = TokenCounter()
        with pytest.raises(ValueError, match="must be a dict with 'content' key"):
            counter.count_messages([{"text": "invalid"}])

    def test_estimate_cost_basic(self):
        """Test basic cost estimation."""
        counter = TokenCounter()
        cost = counter.estimate_cost(1000, 500)
        assert cost > 0
        assert isinstance(cost, float)

    def test_estimate_cost_zero_tokens(self):
        """Test cost estimation with zero tokens."""
        counter = TokenCounter()
        cost = counter.estimate_cost(0, 0)
        assert cost == 0.0
