# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-02-09

### Added
- Prompt versioning system with hash-based tracking, rollback, and changelog
- Safety checker with injection detection, PII masking, and content policy enforcement
- 63 new tests for versioning and safety modules
- Docker and docker-compose support for Streamlit app
- Architecture Decision Records (ADRs)
- Benchmarks for core operations
- Governance files (SECURITY.md, CODE_OF_CONDUCT.md, CONTRIBUTING.md)

### Changed
- Updated architecture diagram to mermaid format
- Test count updated from 66+ to 190+

## [0.1.0] - 2026-02-08

### Added
- Initial release
- Template management with variable substitution and chaining
- Prompt patterns: Chain-of-Thought, Few-Shot, Role-Play, Self-Refine, Meta-Prompt
- Prompt optimizer with random search and mutation strategies
- A/B testing framework with z-test significance and Cohen's d effect size
- Token counting for Claude, OpenAI, and Gemini
- Cost calculator with multi-provider comparison
- CLI tool (`pel`) for command-line workflows
- Streamlit demo application
- 66+ comprehensive tests
- CI/CD with GitHub Actions
