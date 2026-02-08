"""Prompt evaluation: faithfulness, relevance, and quality scoring via TF-IDF."""

from __future__ import annotations

import re
from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class EvaluationResult:
    """Result of evaluating a prompt output."""

    faithfulness: float  # 0-1, how much output comes from context
    relevance: float  # 0-1, how relevant output is to input
    completeness: float  # 0-1, fraction of input topics addressed
    overall: float  # weighted average


class PromptEvaluator:
    """Evaluate prompt outputs for quality without calling an LLM.

    Uses TF-IDF cosine similarity for semantic comparison.
    """

    def faithfulness(self, output: str, context: str) -> float:
        """Score how faithful the output is to its source context.

        Uses keyword overlap: fraction of output keywords found in context.
        Returns 0.0 for empty strings.
        """
        if not output.strip() or not context.strip():
            return 0.0
        output_words = set(self._tokenize(output))
        context_words = set(self._tokenize(context))
        if not output_words:
            return 0.0
        overlap = output_words & context_words
        return len(overlap) / len(output_words)

    def relevance(self, output: str, query: str) -> float:
        """Score how relevant the output is to the original query.

        Uses TF-IDF cosine similarity.
        Returns 0.0 for empty strings.
        """
        if not output.strip() or not query.strip():
            return 0.0
        return self._cosine_sim(output, query)

    def completeness(self, output: str, expected_topics: list[str]) -> float:
        """Score how many expected topics are addressed in the output.

        Checks if each topic keyword appears in the output.
        """
        if not expected_topics:
            return 1.0
        output_lower = output.lower()
        found = sum(1 for t in expected_topics if t.lower() in output_lower)
        return found / len(expected_topics)

    def evaluate(
        self,
        output: str,
        query: str = "",
        context: str = "",
        expected_topics: list[str] | None = None,
        weights: dict[str, float] | None = None,
    ) -> EvaluationResult:
        """Full evaluation combining all metrics.

        Default weights: faithfulness=0.4, relevance=0.4, completeness=0.2
        """
        w = weights or {"faithfulness": 0.4, "relevance": 0.4, "completeness": 0.2}

        faith = self.faithfulness(output, context) if context else 0.0
        rel = self.relevance(output, query) if query else 0.0
        comp = self.completeness(output, expected_topics or [])

        overall = (
            w.get("faithfulness", 0.4) * faith
            + w.get("relevance", 0.4) * rel
            + w.get("completeness", 0.2) * comp
        )

        return EvaluationResult(
            faithfulness=round(faith, 4),
            relevance=round(rel, 4),
            completeness=round(comp, 4),
            overall=round(overall, 4),
        )

    def _tokenize(self, text: str) -> list[str]:
        """Tokenize text into lowercase words, filtering short words."""
        words = re.findall(r"\b\w+\b", text.lower())
        return [w for w in words if len(w) > 2]

    def _cosine_sim(self, text_a: str, text_b: str) -> float:
        """Compute TF-IDF cosine similarity between two texts."""
        try:
            vectorizer = TfidfVectorizer()
            tfidf = vectorizer.fit_transform([text_a, text_b])
            sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
            return float(max(0.0, min(1.0, sim)))
        except ValueError:
            return 0.0
