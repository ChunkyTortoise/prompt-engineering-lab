"""Tests for template module."""

from __future__ import annotations

import pytest

from prompt_engineering_lab.template import PromptChain, PromptTemplate, TemplateRegistry


class TestPromptTemplate:
    """Test PromptTemplate class."""

    def test_format_basic(self):
        """Test basic template formatting."""
        template = PromptTemplate(name="test", template="Hello {name}")
        result = template.format(name="World")
        assert result == "Hello World"

    def test_format_multiple_vars(self):
        """Test formatting with multiple variables."""
        template = PromptTemplate(name="test", template="{greeting} {name}, you have {count} messages")
        result = template.format(greeting="Hello", name="Alice", count="5")
        assert result == "Hello Alice, you have 5 messages"

    def test_format_missing_var(self):
        """Test formatting with missing variable raises ValueError."""
        template = PromptTemplate(name="test", template="Hello {name}")
        with pytest.raises(ValueError, match="Missing required variables"):
            template.format()

    def test_variables_extraction(self):
        """Test extracting variables from template."""
        template = PromptTemplate(name="test", template="Hello {name}, you are {age} years old")
        vars = template.variables()
        assert set(vars) == {"name", "age"}

    def test_variables_no_vars(self):
        """Test variables extraction when no variables present."""
        template = PromptTemplate(name="test", template="Hello world")
        vars = template.variables()
        assert vars == []

    def test_variables_duplicate(self):
        """Test variables extraction with duplicate variables."""
        template = PromptTemplate(name="test", template="{name} loves {name}")
        vars = template.variables()
        assert len(vars) == 1
        assert vars[0] == "name"


class TestPromptChain:
    """Test PromptChain class."""

    def test_chain_single_template(self):
        """Test chain with single template."""
        t1 = PromptTemplate(name="t1", template="Hello {name}")
        chain = PromptChain(templates=[t1])
        results = chain.run({"name": "World"})
        assert len(results) == 1
        assert results[0] == "Hello World"

    def test_chain_multiple_templates(self):
        """Test chain with multiple templates."""
        t1 = PromptTemplate(name="t1", template="Step 1: {input}")
        t2 = PromptTemplate(name="t2", template="Step 2: Based on {previous_output}")
        chain = PromptChain(templates=[t1, t2])
        results = chain.run({"input": "data"})
        assert len(results) == 2
        assert "Step 1: data" in results[0]
        assert "Step 2: Based on Step 1: data" in results[1]

    def test_chain_preserves_vars(self):
        """Test that chain preserves initial variables."""
        t1 = PromptTemplate(name="t1", template="{greeting} {name}")
        t2 = PromptTemplate(name="t2", template="Goodbye {name}")
        chain = PromptChain(templates=[t1, t2])
        results = chain.run({"greeting": "Hello", "name": "Alice"})
        assert "Hello Alice" in results[0]
        assert "Goodbye Alice" in results[1]


class TestTemplateRegistry:
    """Test TemplateRegistry class."""

    def test_register_and_get(self):
        """Test registering and retrieving templates."""
        registry = TemplateRegistry()
        template = PromptTemplate(name="custom", template="Custom {var}")
        registry.register(template)
        retrieved = registry.get("custom")
        assert retrieved.name == "custom"
        assert retrieved.template == "Custom {var}"

    def test_get_nonexistent(self):
        """Test getting nonexistent template raises KeyError."""
        registry = TemplateRegistry()
        with pytest.raises(KeyError, match="not found"):
            registry.get("nonexistent")

    def test_list_templates(self):
        """Test listing all templates."""
        registry = TemplateRegistry()
        templates = registry.list_templates()
        assert "summarize" in templates
        assert "extract" in templates
        assert "analyze" in templates
        assert "compare" in templates

    def test_builtin_templates(self):
        """Test builtin templates are loaded."""
        registry = TemplateRegistry()
        summarize = registry.get_builtin("summarize")
        assert "word_count" in summarize.variables()
        assert "text" in summarize.variables()

    def test_get_builtin_invalid(self):
        """Test getting invalid builtin raises KeyError."""
        registry = TemplateRegistry()
        with pytest.raises(KeyError, match="not found"):
            registry.get_builtin("invalid")
