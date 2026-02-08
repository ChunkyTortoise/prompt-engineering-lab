"""Prompt engineering patterns for advanced techniques."""

from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass
class ChainOfThought:
    """Chain of Thought pattern - encourages step-by-step reasoning."""

    prefix: str = "Let's think step by step."
    suffix: str = ""

    def apply(self, prompt: str) -> str:
        parts = [self.prefix, prompt]
        if self.suffix:
            parts.append(self.suffix)
        return "\n\n".join(parts)


@dataclass
class FewShotPattern:
    """Few-shot learning pattern - adds examples to prompts."""

    examples: list[dict] = field(default_factory=list)

    def apply(self, prompt: str, n_examples: int | None = None) -> str:
        if not self.examples:
            return prompt
        examples_to_use = self.examples if n_examples is None else self.select_random(n_examples)
        example_text = "\n\n".join(
            [f"Example {i + 1}:\nInput: {ex['input']}\nOutput: {ex['output']}" for i, ex in enumerate(examples_to_use)]
        )
        return f"{example_text}\n\nNow, {prompt}"

    def select_random(self, n: int) -> list[dict]:
        if n >= len(self.examples):
            return self.examples.copy()
        return random.sample(self.examples, n)

    def add_example(self, input_text: str, output_text: str) -> None:
        self.examples.append({"input": input_text, "output": output_text})


@dataclass
class RolePlayPattern:
    """Role-play pattern - adds system persona to prompts."""

    role: str
    expertise: str
    tone: str = "professional"

    def apply(self, prompt: str) -> str:
        persona = f"You are a {self.role} with expertise in {self.expertise}. "
        persona += f"Respond in a {self.tone} tone.\n\n"
        return persona + prompt


@dataclass
class SelfRefinePattern:
    """Self-refine pattern - generate, critique, and refine loop."""

    critique_prompt: str = "Review the above response and identify areas for improvement."
    refine_prompt: str = "Improve the response based on the critique above."

    def build_refinement_chain(self, original_prompt: str) -> list[str]:
        return [original_prompt, self.critique_prompt, self.refine_prompt]

    def apply(self, prompt: str) -> str:
        return (
            f"Step 1 - Generate:\n{prompt}\n\n"
            f"Step 2 - Critique:\n{self.critique_prompt}\n\n"
            f"Step 3 - Refine:\n{self.refine_prompt}"
        )


@dataclass
class MetaPromptPattern:
    """Meta-prompt pattern - prompts that generate prompts."""

    target_task: str
    constraints: list[str] = field(default_factory=list)

    def apply(self, base_requirements: str) -> str:
        prompt = f"Create a detailed prompt for the following task: {self.target_task}\n\n"
        prompt += f"Requirements:\n{base_requirements}\n\n"
        if self.constraints:
            prompt += "Constraints:\n"
            for i, constraint in enumerate(self.constraints, 1):
                prompt += f"{i}. {constraint}\n"
        prompt += "\nThe generated prompt should be clear, specific, and include examples where appropriate."
        return prompt
