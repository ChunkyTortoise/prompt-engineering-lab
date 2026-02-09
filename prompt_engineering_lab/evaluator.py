"""Prompt evaluation metrics: ROUGE, semantic similarity, and token efficiency."""

from __future__ import annotations

import math
from dataclasses import dataclass, field


def _tokenize(text: str) -> list[str]:
    """Simple whitespace + lowercase tokenizer."""
    return text.lower().split()


def _ngrams(tokens: list[str], n: int) -> list[tuple[str, ...]]:
    """Extract n-grams from token list."""
    return [tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def _lcs_length(a: list[str], b: list[str]) -> int:
    """Compute longest common subsequence length via DP."""
    m, n = len(a), len(b)
    if m == 0 or n == 0:
        return 0
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]


@dataclass
class RougeScore:
    """Precision, recall, and F1 for a ROUGE variant."""

    precision: float = 0.0
    recall: float = 0.0
    f1: float = 0.0


class RougeScorer:
    """Compute ROUGE-1, ROUGE-2, and ROUGE-L scores from scratch."""

    def _ngram_score(self, candidate: str, reference: str, n: int) -> RougeScore:
        cand_tokens = _tokenize(candidate)
        ref_tokens = _tokenize(reference)
        if not cand_tokens or not ref_tokens:
            return RougeScore()

        cand_ngrams = _ngrams(cand_tokens, n)
        ref_ngrams = _ngrams(ref_tokens, n)
        if not cand_ngrams or not ref_ngrams:
            return RougeScore()

        # Count overlapping n-grams (handle duplicates correctly)
        ref_counts: dict[tuple[str, ...], int] = {}
        for ng in ref_ngrams:
            ref_counts[ng] = ref_counts.get(ng, 0) + 1

        cand_counts: dict[tuple[str, ...], int] = {}
        for ng in cand_ngrams:
            cand_counts[ng] = cand_counts.get(ng, 0) + 1

        overlap = 0
        for ng, count in cand_counts.items():
            overlap += min(count, ref_counts.get(ng, 0))

        precision = overlap / len(cand_ngrams)
        recall = overlap / len(ref_ngrams)
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        return RougeScore(precision=precision, recall=recall, f1=f1)

    def rouge1(self, candidate: str, reference: str) -> RougeScore:
        """Compute ROUGE-1 (unigram overlap)."""
        return self._ngram_score(candidate, reference, 1)

    def rouge2(self, candidate: str, reference: str) -> RougeScore:
        """Compute ROUGE-2 (bigram overlap)."""
        return self._ngram_score(candidate, reference, 2)

    def rouge_l(self, candidate: str, reference: str) -> RougeScore:
        """Compute ROUGE-L (LCS-based)."""
        cand_tokens = _tokenize(candidate)
        ref_tokens = _tokenize(reference)
        if not cand_tokens or not ref_tokens:
            return RougeScore()

        lcs = _lcs_length(cand_tokens, ref_tokens)
        precision = lcs / len(cand_tokens)
        recall = lcs / len(ref_tokens)
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        return RougeScore(precision=precision, recall=recall, f1=f1)


class SemanticSimilarity:
    """TF-IDF cosine similarity between candidate and reference text."""

    def score(self, candidate: str, reference: str) -> float:
        """Compute cosine similarity using TF-IDF vectors."""
        if not candidate.strip() or not reference.strip():
            return 0.0

        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity

            vectorizer = TfidfVectorizer()
            tfidf = vectorizer.fit_transform([candidate, reference])
            sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
            return float(sim)
        except ImportError:
            return self._fallback_similarity(candidate, reference)

    def _fallback_similarity(self, candidate: str, reference: str) -> float:
        """Pure Python TF-IDF cosine similarity fallback."""
        cand_tokens = _tokenize(candidate)
        ref_tokens = _tokenize(reference)
        if not cand_tokens or not ref_tokens:
            return 0.0

        # Build vocabulary
        vocab = sorted(set(cand_tokens) | set(ref_tokens))

        # Term frequency vectors
        def tf_vector(tokens: list[str]) -> list[float]:
            counts: dict[str, int] = {}
            for t in tokens:
                counts[t] = counts.get(t, 0) + 1
            return [counts.get(w, 0) / len(tokens) for w in vocab]

        # IDF: log(2 / df) since we only have 2 documents
        doc_freq: dict[str, int] = {}
        for w in vocab:
            df = (1 if w in set(cand_tokens) else 0) + (1 if w in set(ref_tokens) else 0)
            doc_freq[w] = df

        idf = [math.log((1.0 + 2.0) / (1.0 + doc_freq[w])) + 1.0 for w in vocab]

        cand_tf = tf_vector(cand_tokens)
        ref_tf = tf_vector(ref_tokens)

        # TF-IDF
        cand_tfidf = [tf * i for tf, i in zip(cand_tf, idf)]
        ref_tfidf = [tf * i for tf, i in zip(ref_tf, idf)]

        # Cosine similarity
        dot = sum(a * b for a, b in zip(cand_tfidf, ref_tfidf))
        mag_a = math.sqrt(sum(a * a for a in cand_tfidf))
        mag_b = math.sqrt(sum(b * b for b in ref_tfidf))

        if mag_a == 0 or mag_b == 0:
            return 0.0
        return dot / (mag_a * mag_b)


class TokenEfficiencyMetric:
    """Measure quality per token: quality_score / token_count."""

    def score(self, quality_score: float, token_count: int) -> float:
        """Compute token efficiency ratio."""
        if token_count <= 0:
            return 0.0
        return quality_score / token_count


@dataclass
class EvaluationReport:
    """Aggregated evaluation report."""

    rouge_scores: dict[str, RougeScore] = field(default_factory=dict)
    similarity: float = 0.0
    efficiency: float = 0.0
    overall: float = 0.0


class PromptEvaluator:
    """Orchestrate all evaluation metrics."""

    def __init__(self) -> None:
        self._rouge = RougeScorer()
        self._similarity = SemanticSimilarity()
        self._efficiency = TokenEfficiencyMetric()

    def evaluate(self, candidate: str, reference: str, token_count: int) -> EvaluationReport:
        """Evaluate a candidate against a reference."""
        rouge_scores = {
            "rouge1": self._rouge.rouge1(candidate, reference),
            "rouge2": self._rouge.rouge2(candidate, reference),
            "rougeL": self._rouge.rouge_l(candidate, reference),
        }

        similarity = self._similarity.score(candidate, reference)

        # Use ROUGE-1 F1 as quality proxy for efficiency
        quality = rouge_scores["rouge1"].f1
        efficiency = self._efficiency.score(quality, token_count)

        # Overall: weighted combination of ROUGE-1 F1, similarity, and efficiency
        # Normalize efficiency to [0, 1] via tanh
        norm_eff = math.tanh(efficiency * 100)
        overall = 0.4 * rouge_scores["rouge1"].f1 + 0.4 * similarity + 0.2 * norm_eff

        return EvaluationReport(
            rouge_scores=rouge_scores,
            similarity=similarity,
            efficiency=efficiency,
            overall=overall,
        )

    def evaluate_batch(
        self,
        candidates: list[str],
        references: list[str],
        token_counts: list[int],
    ) -> list[EvaluationReport]:
        """Evaluate multiple candidates against references."""
        return [self.evaluate(c, r, t) for c, r, t in zip(candidates, references, token_counts)]

    def compare(self, report_a: EvaluationReport, report_b: EvaluationReport) -> str:
        """Compare two reports. Returns 'a', 'b', or 'tie'."""
        if abs(report_a.overall - report_b.overall) < 1e-6:
            return "tie"
        return "a" if report_a.overall > report_b.overall else "b"
