# Prompt Engineering Lab

**A prompt engineering framework with 8 reusable patterns, 7 business task categories, TF-IDF evaluation metrics, z-test A/B testing, and reproducible benchmarks.**

![CI](https://github.com/ChunkyTortoise/prompt-engineering-lab/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)
![Tests](https://img.shields.io/badge/tests-67%20passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

## What This Solves

- **No systematic way to compare prompts** -- A/B testing with z-test significance tells you which prompt performs better
- **Prompt quality is subjective** -- TF-IDF scoring measures faithfulness, relevance, and completeness (0-1)
- **Prompt patterns are scattered** -- 8 battle-tested patterns in one library with templates and examples

## Architecture

```
+-------------------+    +------------------+    +------------------+
|  Pattern Library  |--->|    Evaluator     |--->| Report Generator |
|  8 built-in      |    |  TF-IDF scoring  |    |  Markdown tables |
|  patterns         |    |  faithfulness,   |    |  comparison      |
+-------------------+    |  relevance,      |    +------------------+
                         |  completeness    |
+-------------------+    +--------+---------+
|   Categories     |              |
|  7 business task |    +---------v--------+
|  types + samples |    |    A/B Tester    |
+-------------------+    |  z-test, lift,   |
                         |  significance    |
+-------------------+    +------------------+
|   Benchmark      |
|  all patterns x  |
|  all categories  |
+-------------------+
```

## Modules

| Module | File | Description |
|--------|------|-------------|
| **Pattern Library** | `patterns.py` | 8 prompt patterns with templates, descriptions, and examples |
| **Evaluator** | `evaluator.py` | TF-IDF faithfulness, relevance, and completeness scoring (0-1) |
| **Benchmark** | `benchmark.py` | Reproducible benchmark runner with mock outputs across all combos |
| **Categories** | `categories.py` | 7 business task categories with sample tasks |
| **A/B Tester** | `ab_tester.py` | Z-test comparison with significance testing and lift calculation |
| **Report Generator** | `report_generator.py` | Markdown report and comparison table generation |

## 8 Prompt Patterns

| Pattern | Best For |
|---------|----------|
| Chain of Thought | Complex problems, math, step-by-step reasoning |
| Few-Shot | Classification, formatting, learning from examples |
| Structured Output | Data extraction, specific format (JSON, table) |
| Role Play | Creative tasks, code review, persona-based generation |
| Tool Use | Agent workflows, function calling instructions |
| Self-Consistency | Reliability-critical tasks, consensus from multiple answers |
| RAG | Q&A with source material, context-grounded generation |
| Decomposition | Planning, complex projects, break into subtasks |

## Quick Start

```bash
git clone https://github.com/ChunkyTortoise/prompt-engineering-lab.git
cd prompt-engineering-lab
pip install -r requirements-dev.txt
make test
make demo
```

## Usage

```python
from prompt_lab import PromptEvaluator, ABTester

# Evaluate a prompt output (faithfulness, relevance, completeness)
evaluator = PromptEvaluator()
result = evaluator.evaluate(
    output="Electronics can be returned within 30 days.",
    query="What is the return policy?",
    context="Return policy: 30 days for electronics.",
    expected_topics=["return", "days", "electronics"],
)
print(f"Overall: {result.overall:.2%}")

# A/B test two prompt strategies
tester = ABTester()
ab = tester.compare(scores_a=[0.85, 0.90], scores_b=[0.70, 0.72],
                    name_a="chain_of_thought", name_b="zero_shot")
print(f"Winner: {ab.winner} (lift: {ab.lift:.1f}%)")
```

## Streamlit Dashboard

Four interactive tabs:

1. **Pattern Library** -- Browse and preview all 8 patterns with examples
2. **Evaluate** -- Score any prompt output for faithfulness, relevance, completeness
3. **A/B Compare** -- Compare two patterns on category tasks with statistical significance
4. **Benchmarks** -- Run all patterns against all categories and view ranked results

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| Evaluation | scikit-learn (TF-IDF cosine similarity) |
| Statistics | scipy (z-test) |
| Testing | pytest (67 tests) |
| CI | GitHub Actions (Python 3.11, 3.12) |
| Linting | Ruff |

## Project Structure

```
prompt-engineering-lab/
├── app.py                          # Streamlit dashboard (4 tabs)
├── prompt_lab/
│   ├── patterns.py                 # 8 prompt patterns
│   ├── evaluator.py                # TF-IDF scoring engine
│   ├── benchmark.py                # Benchmark runner
│   ├── categories.py               # 7 business task categories
│   ├── ab_tester.py                # Z-test A/B comparison
│   └── report_generator.py         # Markdown report generation
├── tests/                          # 6 test files, one per module
├── .github/workflows/ci.yml        # CI pipeline
├── Makefile                        # demo, test, lint, setup
└── requirements-dev.txt
```

## Testing

```bash
make test                           # Full suite (67 tests)
python -m pytest tests/ -v          # Verbose output
```

## Related Projects

- [EnterpriseHub](https://github.com/ChunkyTortoise/EnterpriseHub) -- Real estate AI platform with BI dashboards and CRM integration
- [docqa-engine](https://github.com/ChunkyTortoise/docqa-engine) -- RAG document Q&A with hybrid retrieval and prompt engineering lab
- [ai-orchestrator](https://github.com/ChunkyTortoise/ai-orchestrator) -- AgentForge: unified async LLM interface (Claude, Gemini, OpenAI, Perplexity)
- [insight-engine](https://github.com/ChunkyTortoise/insight-engine) -- Upload CSV/Excel, get instant dashboards, predictive models, and reports
- [scrape-and-serve](https://github.com/ChunkyTortoise/scrape-and-serve) -- Web scraping, price monitoring, Excel-to-web apps, and SEO tools
- [llm-integration-starter](https://github.com/ChunkyTortoise/llm-integration-starter) -- Production LLM patterns: completion, streaming, function calling, RAG, hardening
- [Portfolio](https://chunkytortoise.github.io) -- Project showcase and services

## License
MIT License. Copyright 2026 Cayman Roden.
