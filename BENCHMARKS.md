# Prompt Engineering Lab -- Benchmarks

Generated: 2026-02-08

## Test Suite Summary

67 tests across 6 modules. All tests run without network access or external API keys.

| Module | Test File | Tests | Description |
|--------|-----------|-------|-------------|
| Patterns | `test_patterns.py` | ~12 | Pattern library, template rendering, examples |
| Evaluator | `test_evaluator.py` | ~12 | TF-IDF scoring, faithfulness, relevance, completeness |
| Benchmark | `test_benchmark.py` | ~11 | Runner, all-combos execution, result ranking |
| Categories | `test_categories.py` | ~10 | Category listing, sample tasks, validation |
| A/B Tester | `test_ab_tester.py` | ~12 | Z-test, significance, lift, winner selection |
| Report Generator | `test_report_generator.py` | ~10 | Markdown tables, comparison output |
| **Total** | **6 files** | **67** | |

## Evaluation Metrics

| Metric | Range | Weight | Description |
|--------|-------|--------|-------------|
| Faithfulness | 0-1 | 40% | Keyword overlap between output and source context |
| Relevance | 0-1 | 40% | TF-IDF cosine similarity between output and query |
| Completeness | 0-1 | 20% | Fraction of expected topics addressed |
| Overall | 0-1 | -- | Weighted average of the above |

## How to Reproduce

```bash
git clone https://github.com/ChunkyTortoise/prompt-engineering-lab.git
cd prompt-engineering-lab
pip install -r requirements-dev.txt
make test
# or: python -m pytest tests/ -v
```

## Notes

- All evaluations use TF-IDF (no external LLM calls)
- Benchmark runner uses mock outputs for reproducibility
- A/B tester uses two-sample z-test with configurable significance (default p < 0.05)
