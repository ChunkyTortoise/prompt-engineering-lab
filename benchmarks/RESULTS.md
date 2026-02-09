# Prompt Engineering Lab Benchmark Results

**Date**: 2026-02-09 03:34:57

| Operation | Iterations | P50 (ms) | P95 (ms) | P99 (ms) | Throughput |
|-----------|-----------|----------|----------|----------|------------|
| Template Rendering (3 templates) | 1,000 | 0.0072 | 0.0122 | 0.029 | 124,360 ops/sec |
| Token Counting (51 texts) | 1,000 | 0.0532 | 0.0591 | 0.1102 | 18,186 ops/sec |
| Safety Pattern Matching (300 inputs, 10 patterns) | 500 | 0.9127 | 1.1507 | 1.3654 | 1,052 ops/sec |
| A/B Test Z-Test (50 experiments) | 1,000 | 0.0194 | 0.0198 | 0.0224 | 51,146 ops/sec |

> All benchmarks use synthetic data. No external services required.
