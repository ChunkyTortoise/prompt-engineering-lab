# ADR 0001: Prompt Versioning Strategy

## Status
Accepted

## Context
Prompts change frequently during development and experimentation. Without versioning, it is impossible to reproduce past results, roll back to a known-good prompt, or maintain an audit trail of what changed and why. Traditional file-based versioning through Git alone does not capture prompt-specific metadata.

## Decision
Implement content-hash versioning where each prompt version is identified by a hash of its content. Each version stores metadata including author, creation date, description, and parent hash (forming a linked history). This provides Git-like version history specifically designed for prompt lifecycle management.

## Consequences
- **Positive**: Full audit trail of every prompt change. Reproducible experiments by referencing exact version hashes. Rollback to any previous version is trivial. Parent-hash linking enables branch-like prompt evolution tracking.
- **Negative**: Storage grows with every version since content-addressed storage does not deduplicate similar prompts. No automatic garbage collection means old versions accumulate indefinitely. Content hashing means identical prompts in different contexts share the same hash.
