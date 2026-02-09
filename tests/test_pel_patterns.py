"""Tests for patterns module - prompt engineering lab."""

from __future__ import annotations

from prompt_engineering_lab.patterns import (
    ChainOfThought,
    FewShotPattern,
    MetaPromptPattern,
    RolePlayPattern,
    SelfRefinePattern,
)


class TestChainOfThought:
    """Test ChainOfThought pattern."""

    def test_apply_basic(self):
        cot = ChainOfThought()
        result = cot.apply("What is 2+2?")
        assert "Let's think step by step" in result
        assert "What is 2+2?" in result

    def test_apply_custom_prefix(self):
        cot = ChainOfThought(prefix="Think carefully:")
        result = cot.apply("Solve this")
        assert "Think carefully:" in result

    def test_apply_with_suffix(self):
        cot = ChainOfThought(suffix="Show your work.")
        result = cot.apply("Calculate")
        assert "Let's think step by step" in result
        assert "Show your work." in result


class TestFewShotPattern:
    """Test FewShotPattern."""

    def test_apply_no_examples(self):
        fs = FewShotPattern()
        result = fs.apply("Translate this")
        assert result == "Translate this"

    def test_apply_with_examples(self):
        fs = FewShotPattern(examples=[{"input": "Hello", "output": "Bonjour"}])
        result = fs.apply("Translate: Hi")
        assert "Example 1" in result
        assert "Hello" in result
        assert "Bonjour" in result
        assert "Translate: Hi" in result

    def test_apply_n_examples(self):
        examples = [{"input": str(i), "output": str(i * 2)} for i in range(5)]
        fs = FewShotPattern(examples=examples)
        result = fs.apply("Test", n_examples=2)
        assert result.count("Example") == 2

    def test_select_random(self):
        examples = [{"input": str(i), "output": str(i * 2)} for i in range(10)]
        fs = FewShotPattern(examples=examples)
        selected = fs.select_random(3)
        assert len(selected) == 3

    def test_select_random_more_than_available(self):
        examples = [{"input": "1", "output": "2"}]
        fs = FewShotPattern(examples=examples)
        selected = fs.select_random(5)
        assert len(selected) == 1

    def test_add_example(self):
        fs = FewShotPattern()
        fs.add_example("input1", "output1")
        assert len(fs.examples) == 1
        assert fs.examples[0]["input"] == "input1"
        assert fs.examples[0]["output"] == "output1"


class TestRolePlayPattern:
    """Test RolePlayPattern."""

    def test_apply_basic(self):
        rp = RolePlayPattern(role="teacher", expertise="mathematics")
        result = rp.apply("Explain calculus")
        assert "teacher" in result
        assert "mathematics" in result
        assert "Explain calculus" in result

    def test_apply_custom_tone(self):
        rp = RolePlayPattern(role="comedian", expertise="jokes", tone="humorous")
        result = rp.apply("Tell me a joke")
        assert "humorous" in result


class TestSelfRefinePattern:
    """Test SelfRefinePattern."""

    def test_build_refinement_chain(self):
        sr = SelfRefinePattern()
        chain = sr.build_refinement_chain("Write an essay")
        assert len(chain) == 3
        assert chain[0] == "Write an essay"

    def test_apply(self):
        sr = SelfRefinePattern()
        result = sr.apply("Generate code")
        assert "Step 1" in result
        assert "Step 2" in result
        assert "Step 3" in result
        assert "Generate code" in result

    def test_custom_prompts(self):
        sr = SelfRefinePattern(critique_prompt="Check for errors", refine_prompt="Fix issues")
        result = sr.apply("Code")
        assert "Check for errors" in result
        assert "Fix issues" in result


class TestMetaPromptPattern:
    """Test MetaPromptPattern."""

    def test_apply_basic(self):
        mp = MetaPromptPattern(target_task="summarization")
        result = mp.apply("Summarize articles")
        assert "summarization" in result
        assert "Summarize articles" in result

    def test_apply_with_constraints(self):
        mp = MetaPromptPattern(target_task="translation", constraints=["Use formal language", "Keep it concise"])
        result = mp.apply("Translate documents")
        assert "Constraints:" in result
        assert "Use formal language" in result
        assert "Keep it concise" in result
