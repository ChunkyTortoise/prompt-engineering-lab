# Prompt Engineering Lab

[![CI](https://github.com/chunkytortoise/prompt-engineering-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/chunkytortoise/prompt-engineering-lab/actions/workflows/ci.yml)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

A prompt engineering framework with **8 reusable patterns**, **7 business task categories**, TF-IDF evaluation metrics, z-test A/B testing, and reproducible benchmarks. Includes a Streamlit dashboard for interactive exploration.

## Quick Start

```bash
# Install
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/ -v

# Launch demo dashboard
streamlit run app.py
```

## Architecture

```
prompt_lab/
  patterns.py          8 built-in prompt patterns
  evaluator.py         TF-IDF faithfulness, relevance, completeness scoring
  benchmark.py         Reproducible benchmark runner with mock outputs
  categories.py        7 business task categories with sample tasks
  ab_tester.py         Z-test A/B comparison with significance testing
  report_generator.py  Markdown report and comparison table generation
```

### 8 Prompt Patterns

| Pattern | Description | Best For |
|---------|-------------|----------|
| Chain of Thought | Step-by-step reasoning | Complex problems, math |
| Few-Shot | Learning from examples | Classification, formatting |
| Structured Output | Specific format (JSON, table) | Data extraction |
| Role Play | Assign persona/role | Creative tasks, code review |
| Tool Use | Function calling instructions | Agent workflows |
| Self-Consistency | Multiple answers, pick consensus | Reliability-critical tasks |
| RAG | Context-grounded generation | Q&A with source material |
| Decomposition | Break into subtasks | Planning, complex projects |

### 7 Business Categories

Classification, Extraction, Generation, Summarization, Q&A, Analysis, Transformation

### Evaluation Metrics

- **Faithfulness**: Keyword overlap between output and source context (0-1)
- **Relevance**: TF-IDF cosine similarity between output and query (0-1)
- **Completeness**: Fraction of expected topics addressed (0-1)
- **Overall**: Weighted average (default: 40% faithfulness, 40% relevance, 20% completeness)

### A/B Testing

Two-sample z-test with configurable significance level (default p < 0.05). Reports winner, lift percentage, and full statistical breakdown.

## Usage

### Evaluate a prompt output

```python
from prompt_lab import PromptEvaluator

evaluator = PromptEvaluator()
result = evaluator.evaluate(
    output="Electronics can be returned within 30 days.",
    query="What is the return policy?",
    context="Return policy: 30 days for electronics.",
    expected_topics=["return", "days", "electronics"],
)
print(f"Overall: {result.overall:.2%}")
```

### Run an A/B test

```python
from prompt_lab import ABTester

tester = ABTester()
result = tester.compare(
    scores_a=[0.85, 0.90, 0.88],
    scores_b=[0.70, 0.72, 0.68],
    name_a="chain_of_thought",
    name_b="zero_shot",
)
print(f"Winner: {result.winner} (lift: {result.lift:.1f}%)")
```

### Browse patterns

```python
from prompt_lab import PatternLibrary

library = PatternLibrary()
for pattern in library.list_patterns():
    print(f"{pattern.name}: {pattern.description}")
```

## Streamlit Dashboard

Four interactive tabs:

1. **Pattern Library** -- Browse and preview all 8 patterns with examples
2. **Evaluate** -- Score any prompt output for faithfulness, relevance, completeness
3. **A/B Compare** -- Compare two patterns on category tasks with statistical significance
4. **Benchmarks** -- Run all patterns against all categories and view ranked results

## Development

```bash
make setup    # Install dependencies
make test     # Run tests
make lint     # Ruff check + format
make demo     # Launch Streamlit
make clean    # Remove caches
```

## License

MIT License. Copyright 2026 Cayman Roden.
