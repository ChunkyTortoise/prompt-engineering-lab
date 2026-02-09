# ADR 0003: Safety Checker Design

## Status
Accepted

## Context
Prompts can contain injection attacks (e.g., "ignore previous instructions") or be designed to generate harmful content. Without safety checks, the prompt engineering lab could be used to develop and refine adversarial prompts. A safety layer is needed to catch known attack patterns before prompts are executed.

## Decision
Implement a multi-layer safety checker: regex pattern matching for known injection phrases, token-level analysis for suspicious patterns (e.g., role-switching tokens), and a known-bad-pattern database that is updated as new attack vectors are discovered. Each check produces a severity level (info, warning, critical) and a description. Critical findings block execution.

## Consequences
- **Positive**: Catches common prompt injection attacks and known adversarial patterns. Configurable severity levels allow flexibility between strict and permissive modes. The pattern database can be updated without code changes as new attacks emerge.
- **Negative**: Cannot prevent novel zero-day injection techniques that do not match known patterns. False positives are possible, especially with regex-based detection on legitimate prompts that happen to contain flagged phrases. Determined adversaries can craft prompts that evade pattern matching.
