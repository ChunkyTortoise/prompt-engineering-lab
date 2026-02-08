"""Prompt optimization through random search and mutation strategies."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class OptimizationResult:
    """Results from prompt optimization."""

    best_template: str
    best_score: float
    iterations: int
    improvement_pct: float
    history: list[dict] = field(default_factory=list)


class PromptOptimizer:
    """Optimizer for prompt templates using various strategies."""

    def __init__(self, scorer: Callable[[str], float]):
        self.scorer = scorer

    def random_search(self, templates: list[str], n_iterations: int = 10) -> OptimizationResult:
        if not templates:
            raise ValueError("templates list cannot be empty")
        history = []
        best_template = templates[0]
        best_score = self.scorer(best_template)
        initial_score = best_score
        history.append({"iteration": 0, "template": best_template, "score": best_score})

        for i in range(1, n_iterations):
            candidate = random.choice(templates)
            score = self.scorer(candidate)
            history.append({"iteration": i, "template": candidate, "score": score})
            if score > best_score:
                best_score = score
                best_template = candidate

        improvement_pct = ((best_score - initial_score) / initial_score * 100) if initial_score != 0 else 0.0
        return OptimizationResult(
            best_template=best_template,
            best_score=best_score,
            iterations=n_iterations,
            improvement_pct=improvement_pct,
            history=history,
        )

    def mutate_template(self, template: str) -> str:
        words = template.split()
        if len(words) < 2:
            return template

        mutation_type = random.choice(["swap", "emphasize", "reorder"])

        if mutation_type == "swap":
            idx = random.randint(0, len(words) - 2)
            words[idx], words[idx + 1] = words[idx + 1], words[idx]
        elif mutation_type == "emphasize":
            idx = random.randint(0, len(words) - 1)
            word = words[idx]
            if not word.isupper() and "{" not in word:
                emphasis = random.choice(["**" + word + "**", word.upper()])
                words[idx] = emphasis
        elif mutation_type == "reorder":
            sentences = template.split(". ")
            if len(sentences) > 1:
                random.shuffle(sentences)
                return ". ".join(sentences)

        return " ".join(words)

    def optimize(self, base_template: str, n_iterations: int = 20) -> OptimizationResult:
        history = []
        best_template = base_template
        best_score = self.scorer(best_template)
        initial_score = best_score
        history.append({"iteration": 0, "template": best_template, "score": best_score})

        for i in range(1, n_iterations):
            candidate = self.mutate_template(best_template)
            score = self.scorer(candidate)
            history.append({"iteration": i, "template": candidate, "score": score})
            if score > best_score:
                best_score = score
                best_template = candidate

        improvement_pct = ((best_score - initial_score) / initial_score * 100) if initial_score != 0 else 0.0
        return OptimizationResult(
            best_template=best_template,
            best_score=best_score,
            iterations=n_iterations,
            improvement_pct=improvement_pct,
            history=history,
        )
