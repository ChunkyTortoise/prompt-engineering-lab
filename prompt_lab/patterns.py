"""Prompt patterns library: 8 built-in patterns for common LLM tasks."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PromptPattern:
    """A reusable prompt engineering pattern."""

    name: str
    description: str
    template: str
    variables: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    example_input: dict[str, str] = field(default_factory=dict)
    example_output: str = ""

    def render(self, **kwargs: str) -> str:
        """Render the pattern template with variables."""
        missing = [v for v in self.variables if v not in kwargs]
        if missing:
            raise ValueError(f"Missing variables: {missing}")
        result = self.template
        for key, value in kwargs.items():
            result = result.replace(f"{{{{{key}}}}}", str(value))
        return result

    def render_example(self) -> str:
        """Render the pattern with its built-in example input."""
        if not self.example_input:
            return self.template
        return self.render(**self.example_input)


class PatternLibrary:
    """Library of 8 built-in prompt engineering patterns."""

    def __init__(self):
        self._patterns: dict[str, PromptPattern] = {}
        self._register_builtins()

    def _register_builtins(self):
        """Register all 8 built-in patterns."""
        patterns = [
            PromptPattern(
                name="chain_of_thought",
                description="Step-by-step reasoning for complex problems",
                template=(
                    "Think through this step by step.\n\n"
                    "Problem: {{problem}}\n\n"
                    "Let's work through this:\nStep 1:"
                ),
                variables=["problem"],
                tags=["reasoning", "analysis"],
                example_input={
                    "problem": (
                        "If a store has 3 shelves with 8 items each, "
                        "and 5 items are sold, how many remain?"
                    )
                },
                example_output=(
                    "Step 1: Calculate total items: 3 x 8 = 24\n"
                    "Step 2: Subtract sold: 24 - 5 = 19\n"
                    "Answer: 19 items remain."
                ),
            ),
            PromptPattern(
                name="few_shot",
                description="Learning from examples before the actual task",
                template=(
                    "Here are some examples:\n\n{{examples}}\n\nNow do the same for:\n{{input}}"
                ),
                variables=["examples", "input"],
                tags=["learning", "examples"],
                example_input={
                    "examples": (
                        "Input: happy -> Output: positive\nInput: angry -> Output: negative"
                    ),
                    "input": "excited",
                },
                example_output="positive",
            ),
            PromptPattern(
                name="structured_output",
                description="Request output in a specific format (JSON, table, etc.)",
                template=(
                    "{{task}}\n\nRespond in the following format:\n{{format}}\n\nInput: {{input}}"
                ),
                variables=["task", "format", "input"],
                tags=["formatting", "structured"],
                example_input={
                    "task": "Extract contact information",
                    "format": '{"name": "...", "email": "...", "phone": "..."}',
                    "input": "John Smith, jsmith@example.com, 555-0100",
                },
                example_output=(
                    '{"name": "John Smith", "email": "jsmith@example.com", "phone": "555-0100"}'
                ),
            ),
            PromptPattern(
                name="role_play",
                description="Assign a specific role/persona to the LLM",
                template="You are {{role}}. {{context}}\n\n{{task}}",
                variables=["role", "context", "task"],
                tags=["persona", "role"],
                example_input={
                    "role": "a senior Python developer",
                    "context": "You specialize in writing clean, testable code.",
                    "task": "Review this function for improvements.",
                },
                example_output="As a senior Python developer, I'd suggest...",
            ),
            PromptPattern(
                name="tool_use",
                description="Instruct the LLM to use available tools/functions",
                template=(
                    "You have access to these tools:\n{{tools}}\n\n"
                    "To use a tool, write: TOOL: tool_name(args)\n\n"
                    "Task: {{task}}"
                ),
                variables=["tools", "task"],
                tags=["tools", "function_calling"],
                example_input={
                    "tools": ("- search(query): Search the web\n- calculate(expr): Evaluate math"),
                    "task": "What is the population of France times 2?",
                },
                example_output=(
                    "TOOL: search(population of France)\n"
                    "Result: 67.75 million\n"
                    "TOOL: calculate(67750000 * 2)\n"
                    "Result: 135,500,000"
                ),
            ),
            PromptPattern(
                name="self_consistency",
                description="Generate multiple answers and select the most common",
                template=(
                    "Answer this question {{num_attempts}} different ways, "
                    "then select the most consistent answer.\n\n"
                    "Question: {{question}}\n\nAttempt 1:"
                ),
                variables=["num_attempts", "question"],
                tags=["reliability", "consistency"],
                example_input={
                    "num_attempts": "3",
                    "question": "Is a tomato a fruit or vegetable?",
                },
                example_output=(
                    "Attempt 1: Fruit (botanically)\n"
                    "Attempt 2: Fruit\n"
                    "Attempt 3: Fruit (berry)\n"
                    "Consensus: Fruit"
                ),
            ),
            PromptPattern(
                name="rag",
                description="Retrieval-Augmented Generation with context grounding",
                template=(
                    "Answer the question based ONLY on the provided context. "
                    "If the context doesn't contain the answer, say so.\n\n"
                    "Context:\n{{context}}\n\nQuestion: {{question}}\n\nAnswer:"
                ),
                variables=["context", "question"],
                tags=["retrieval", "grounding"],
                example_input={
                    "context": (
                        "The Eiffel Tower was built in 1889 for the World's Fair. "
                        "It is 330 meters tall."
                    ),
                    "question": "When was the Eiffel Tower built?",
                },
                example_output="The Eiffel Tower was built in 1889 for the World's Fair.",
            ),
            PromptPattern(
                name="decomposition",
                description="Break complex tasks into subtasks",
                template=(
                    "Break this complex task into smaller subtasks, "
                    "then solve each one.\n\n"
                    "Task: {{task}}\n\nSubtasks:\n1."
                ),
                variables=["task"],
                tags=["decomposition", "planning"],
                example_input={"task": "Plan a company offsite for 50 people"},
                example_output=(
                    "1. Determine budget\n"
                    "2. Choose dates\n"
                    "3. Find venue\n"
                    "4. Plan activities\n"
                    "5. Arrange catering"
                ),
            ),
        ]
        for p in patterns:
            self._patterns[p.name] = p

    def get(self, name: str) -> PromptPattern | None:
        """Get a pattern by name."""
        return self._patterns.get(name)

    def list_patterns(self) -> list[PromptPattern]:
        """List all patterns."""
        return list(self._patterns.values())

    def search(self, tag: str) -> list[PromptPattern]:
        """Search patterns by tag."""
        return [p for p in self._patterns.values() if tag in p.tags]

    def register(self, pattern: PromptPattern) -> None:
        """Register a custom pattern."""
        self._patterns[pattern.name] = pattern

    def get_names(self) -> list[str]:
        """Get all pattern names."""
        return list(self._patterns.keys())
