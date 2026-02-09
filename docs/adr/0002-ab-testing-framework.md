# ADR 0002: A/B Testing Framework

## Status
Accepted

## Context
Choosing between prompt variants based on intuition or small samples leads to suboptimal selections. We need statistical rigor when comparing prompt performance to ensure that observed differences are real and not due to random variation.

## Decision
Implement paired comparison A/B testing with z-test significance at p<0.05. Sample size is configurable per experiment. Variant assignment is deterministic (hash-based) to ensure reproducibility. Each experiment tracks metrics including response quality, latency, token usage, and custom evaluator scores.

## Consequences
- **Positive**: Data-driven prompt selection with statistical confidence. Deterministic assignment ensures consistent experiment results. Multi-metric tracking captures tradeoffs (e.g., quality vs. cost) rather than optimizing a single dimension.
- **Negative**: Requires minimum sample sizes to reach significance, which means experiments take time. Small effect sizes require large samples to detect. The z-test assumes normal distribution of metrics, which may not hold for all evaluation criteria.
