"""Tests for prompt_lab.categories module."""

from __future__ import annotations

from prompt_lab.categories import CategoryRegistry, TaskCategory, TaskExample


class TestCategoryRegistry:
    def test_builtin_count(self):
        registry = CategoryRegistry()
        assert len(registry.list_categories()) == 7

    def test_get_classification(self):
        registry = CategoryRegistry()
        cat = registry.get("classification")
        assert cat is not None
        assert len(cat.examples) >= 1

    def test_get_nonexistent(self):
        registry = CategoryRegistry()
        assert registry.get("nonexistent_category") is None

    def test_get_names(self):
        registry = CategoryRegistry()
        names = registry.get_names()
        assert len(names) == 7
        expected = [
            "classification",
            "extraction",
            "generation",
            "summarization",
            "qa",
            "analysis",
            "transformation",
        ]
        for name in expected:
            assert name in names

    def test_get_examples(self):
        registry = CategoryRegistry()
        examples = registry.get_examples("extraction")
        assert len(examples) >= 1
        assert all(isinstance(e, TaskExample) for e in examples)

    def test_register_custom(self):
        registry = CategoryRegistry()
        custom = TaskCategory(
            name="custom_category",
            description="Custom category for testing",
            examples=[
                TaskExample(
                    name="custom_example",
                    input_text="Test input",
                    expected_output="Test output",
                )
            ],
        )
        registry.register(custom)
        assert registry.get("custom_category") is not None
        assert len(registry.list_categories()) == 8


class TestTaskExample:
    def test_example_fields(self):
        example = TaskExample(
            name="test_task",
            input_text="Analyze this text",
            expected_output="Analysis result",
        )
        assert example.name == "test_task"
        assert example.input_text == "Analyze this text"
        assert example.expected_output == "Analysis result"

    def test_example_topics(self):
        example = TaskExample(
            name="test_task",
            input_text="Input",
            expected_output="Output",
            expected_topics=["topic1", "topic2"],
        )
        assert example.expected_topics == ["topic1", "topic2"]


class TestTaskCategory:
    def test_category_fields(self):
        cat = TaskCategory(
            name="test_cat",
            description="A test category",
        )
        assert cat.name == "test_cat"
        assert cat.description == "A test category"

    def test_recommended_patterns(self):
        cat = TaskCategory(
            name="test_cat",
            description="Test",
            recommended_patterns=["chain_of_thought", "few_shot"],
        )
        assert cat.recommended_patterns == ["chain_of_thought", "few_shot"]
