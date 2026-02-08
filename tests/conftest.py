"""Pytest configuration and fixtures."""

from __future__ import annotations

import pytest


@pytest.fixture
def simple_scorer():
    """Simple scorer that returns the length of the text."""
    return lambda text: float(len(text))


@pytest.fixture
def constant_scorer():
    """Scorer that always returns the same value."""
    return lambda text: 5.0


@pytest.fixture
def sample_template_vars():
    """Sample template variables for testing."""
    return {
        "text": "This is sample text",
        "word_count": "50",
        "entity_type": "names",
        "content_type": "article",
        "aspect": "quality",
        "content": "Sample content",
        "item_a": "Python",
        "item_b": "JavaScript",
        "criteria": "performance",
    }
