"""Tests for prompt_lab.patterns module."""

from __future__ import annotations

import pytest

from prompt_lab.patterns import PatternLibrary, PromptPattern


class TestPromptPattern:
    def test_render_basic(self):
        pattern = PromptPattern(
            name="test",
            description="Test pattern",
            template="Hello {{name}}, welcome to {{place}}!",
            variables=["name", "place"],
        )
        result = pattern.render(name="Alice", place="Wonderland")
        assert result == "Hello Alice, welcome to Wonderland!"

    def test_render_missing_variable(self):
        pattern = PromptPattern(
            name="test",
            description="Test",
            template="Hello {{name}}!",
            variables=["name"],
        )
        with pytest.raises(ValueError, match="Missing variables"):
            pattern.render()

    def test_render_example(self):
        pattern = PromptPattern(
            name="test",
            description="Test",
            template="Solve: {{problem}}",
            variables=["problem"],
            example_input={"problem": "2+2"},
        )
        result = pattern.render_example()
        assert "2+2" in result

    def test_variables_extracted(self):
        pattern = PromptPattern(
            name="test",
            description="Test",
            template="{{a}} and {{b}}",
            variables=["a", "b"],
        )
        assert pattern.variables == ["a", "b"]

    def test_empty_example(self):
        pattern = PromptPattern(
            name="test",
            description="Test",
            template="No variables here",
            variables=[],
            example_input={},
        )
        result = pattern.render_example()
        assert result == "No variables here"


class TestPatternLibrary:
    def test_builtin_count(self):
        lib = PatternLibrary()
        assert len(lib.list_patterns()) == 8

    def test_get_chain_of_thought(self):
        lib = PatternLibrary()
        pattern = lib.get("chain_of_thought")
        assert pattern is not None
        assert "problem" in pattern.variables

    def test_get_nonexistent(self):
        lib = PatternLibrary()
        assert lib.get("nonexistent_pattern") is None

    def test_search_by_tag(self):
        lib = PatternLibrary()
        results = lib.search("reasoning")
        assert len(results) >= 1
        assert any(p.name == "chain_of_thought" for p in results)

    def test_register_custom(self):
        lib = PatternLibrary()
        custom = PromptPattern(
            name="custom_pattern",
            description="Custom",
            template="Custom: {{input}}",
            variables=["input"],
        )
        lib.register(custom)
        assert lib.get("custom_pattern") is not None

    def test_get_names(self):
        lib = PatternLibrary()
        names = lib.get_names()
        assert len(names) == 8
        assert "chain_of_thought" in names
        assert "few_shot" in names

    def test_list_patterns(self):
        lib = PatternLibrary()
        patterns = lib.list_patterns()
        assert all(isinstance(p, PromptPattern) for p in patterns)
