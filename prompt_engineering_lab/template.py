"""Template management for prompt engineering."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class PromptTemplate:
    """A prompt template with variable placeholders."""

    name: str
    template: str

    def format(self, **kwargs) -> str:
        """Format the template with provided variables."""
        required_vars = self.variables()
        missing_vars = [var for var in required_vars if var not in kwargs]

        if missing_vars:
            raise ValueError(f"Missing required variables: {', '.join(missing_vars)}")

        return self.template.format(**kwargs)

    def variables(self) -> list[str]:
        """Extract variable names from the template."""
        pattern = r"\{([^}]+)\}"
        return list(set(re.findall(pattern, self.template)))


@dataclass
class PromptChain:
    """A chain of prompt templates for sequential execution."""

    templates: list[PromptTemplate]

    def run(self, initial_vars: dict) -> list[str]:
        """Execute templates sequentially."""
        results = []
        current_vars = initial_vars.copy()

        for i, template in enumerate(self.templates):
            formatted = template.format(**current_vars)
            results.append(formatted)
            current_vars["previous_output"] = formatted
            current_vars[f"step_{i}_output"] = formatted

        return results


class TemplateRegistry:
    """Registry for managing prompt templates."""

    def __init__(self):
        self._templates: dict[str, PromptTemplate] = {}
        self._load_builtins()

    def _load_builtins(self) -> None:
        builtins = {
            "summarize": PromptTemplate(
                name="summarize",
                template="Summarize the following text in {word_count} words or less:\n\n{text}",
            ),
            "extract": PromptTemplate(
                name="extract",
                template="Extract {entity_type} from the following text:\n\n{text}",
            ),
            "analyze": PromptTemplate(
                name="analyze",
                template="Analyze the following {content_type} and provide insights on {aspect}:\n\n{content}",
            ),
            "compare": PromptTemplate(
                name="compare",
                template="Compare {item_a} and {item_b} in terms of {criteria}.",
            ),
        }
        for template in builtins.values():
            self._templates[template.name] = template

    def register(self, template: PromptTemplate) -> None:
        self._templates[template.name] = template

    def get(self, name: str) -> PromptTemplate:
        if name not in self._templates:
            raise KeyError(f"Template '{name}' not found in registry")
        return self._templates[name]

    def list_templates(self) -> list[str]:
        return sorted(self._templates.keys())

    def get_builtin(self, name: str) -> PromptTemplate:
        builtin_names = ["summarize", "extract", "analyze", "compare"]
        if name not in builtin_names:
            raise KeyError(f"Builtin template '{name}' not found. Available: {', '.join(builtin_names)}")
        return self.get(name)
