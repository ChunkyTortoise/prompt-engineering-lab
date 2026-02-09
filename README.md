[![Sponsor](https://img.shields.io/badge/Sponsor-💖-pink.svg)](https://github.com/sponsors/ChunkyTortoise)

# Prompt Engineering Lab

A comprehensive Python toolkit for prompt engineering techniques — template management, patterns (CoT, few-shot, role-play), optimization, A/B testing, token counting, and cost estimation.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ct-prompt-lab.streamlit.app)
![Tests](https://img.shields.io/badge/tests-190%2B%20passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

## What This Solves

- **Prompt iteration loops** — Create, test, and compare prompts without manual copy/paste
- **Cost uncertainty** — Estimate tokens and compare provider costs before deployment
- **Quality drift** — A/B testing and optimization to validate prompt changes

## Demo

Live demo: https://ct-prompt-lab.streamlit.app

## Features

- **Template Management**: Create, store, and chain prompt templates with variable substitution
- **Prompt Patterns**: Apply proven patterns like Chain-of-Thought, Few-Shot, Role-Play, and Self-Refine
- **Optimization**: Improve prompts through random search and mutation strategies
- **A/B Testing**: Compare template effectiveness with statistical significance testing
- **Token Counting**: Estimate token usage across Claude, OpenAI, and Gemini
- **Cost Calculation**: Calculate and compare costs across different AI providers and models
- **CLI Tool**: Command-line interface for quick prompt engineering workflows

## Architecture

```mermaid
flowchart LR
    PT[Prompt Templates] --> OPT[Optimizer]
    OPT --> AB[A/B Testing Engine]
    AB --> TC[Token Counter]
    TC --> SC[Safety Checker]
    SC --> VS[Versioning System]
    VS --> SD[Streamlit Demo]

    PT -->|Variables & Chains| OPT
    OPT -->|Mutation & Search| AB
    AB -->|Z-test p<0.05| TC
    TC -->|Claude/OpenAI/Gemini| SC
    SC -->|Injection & PII| VS
    VS -->|Hash + Metadata| SD
```

## Key Metrics

| Metric | Value |
|--------|-------|
| Tests | 190+ passing |
| Prompt Optimization | Random search + mutation strategies |
| A/B Testing | Z-test significance at p<0.05, Cohen's d effect size |
| Token Counting | Multi-provider (Claude, OpenAI, Gemini) |
| Safety Checking | Injection detection, PII masking, content policy |
| Version Control | Git-inspired hash + metadata, rollback, changelog |

## Installation

```bash
# Clone the repository
git clone https://github.com/ChunkyTortoise/prompt-engineering-lab.git
cd prompt-engineering-lab

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e ".[dev]"
```

## Quick Start

### Python API

```python
from prompt_engineering_lab import PromptTemplate, ChainOfThought, PromptOptimizer

# Create a template
template = PromptTemplate(
    name="summarize",
    template="Summarize the following text in {word_count} words:\n\n{text}"
)

# Format with variables
result = template.format(word_count="50", text="Long article...")

# Apply Chain-of-Thought pattern
cot = ChainOfThought()
enhanced = cot.apply("Explain quantum computing")
# Output: "Let's think step by step.\n\nExplain quantum computing"

# Optimize prompts
optimizer = PromptOptimizer(scorer=lambda x: len(x))
result = optimizer.optimize("Write a blog post", n_iterations=20)
print(f"Best template: {result.best_template}")
print(f"Improvement: {result.improvement_pct}%")
```

### CLI Usage

```bash
# List available templates
pel list

# Test a template
pel test summarize "Your text here" -v word_count=50

# Enhance a prompt with patterns
pel enhance "Explain AI" -p cot
pel enhance "Write code" -p role --role "senior developer" --expertise "Python"

# Compare two templates
pel compare "Template A" "Template B" "input text"

# Count tokens
pel count "Your prompt text" -p claude
```

## Module Overview

### Template Management (`template.py`)
- `PromptTemplate`: Define reusable templates with variable placeholders
- `PromptChain`: Chain multiple templates for sequential execution
- `TemplateRegistry`: Store and retrieve templates with 4 builtin templates

### Patterns (`patterns.py`)
- `ChainOfThought`: Add step-by-step reasoning guidance
- `FewShotPattern`: Include examples in prompts
- `RolePlayPattern`: Add persona and expertise context
- `SelfRefinePattern`: Generate → critique → refine workflow
- `MetaPromptPattern`: Create prompts that generate prompts

### Optimization (`optimizer.py`)
- `PromptOptimizer`: Improve prompts through search and mutation
- Random search over template candidates
- Mutation strategies: word swapping, emphasis, reordering
- Track optimization history and improvement metrics

### A/B Testing (`ab_tester.py`)
- `ABTestRunner`: Compare two templates statistically
- Z-test for significance (p < 0.05 threshold)
- Effect size calculation (Cohen's d)
- Winner determination with confidence metrics

### Token Counting (`token_counter.py`)
- `TokenCounter`: Estimate tokens for Claude, OpenAI, Gemini
- Message-level counting with overhead calculation
- Provider-specific character-per-token ratios

### Cost Calculation (`cost_calculator.py`)
- `CostCalculator`: Estimate API costs across providers
- Pricing data for Claude (Opus/Sonnet/Haiku), OpenAI (GPT-4/3.5), Gemini (Pro/Ultra)
- Compare providers to find the most cost-effective option

## Architecture Decisions

| ADR | Title | Status |
|-----|-------|--------|
| [ADR-0001](docs/adr/0001-prompt-versioning-strategy.md) | Prompt Versioning Strategy | Accepted |
| [ADR-0002](docs/adr/0002-ab-testing-framework.md) | A/B Testing Framework | Accepted |
| [ADR-0003](docs/adr/0003-safety-checker-design.md) | Safety Checker Design | Accepted |

## Benchmarks

See [BENCHMARKS.md](BENCHMARKS.md) for methodology, evaluation metrics, and reproduction steps.

## Development

```bash
# Run tests
make test

# Run tests with coverage
make coverage

# Lint code
make lint

# Format code
make format

# Clean build artifacts
make clean
```

## Testing

The project includes 190+ comprehensive tests covering all modules:

- **Template tests** (12): Template formatting, chaining, registry
- **Pattern tests** (14): CoT, few-shot, role-play, self-refine
- **Optimizer tests** (10): Random search, mutation, optimization
- **A/B testing tests** (10): Statistical testing, winner determination
- **Token counter tests** (8): Multi-provider counting, messages
- **Cost calculator tests** (6): Cost estimation, provider comparison
- **CLI tests** (6): Command-line interface functionality

Run tests:
```bash
pytest tests/ -v
pytest tests/ --cov=prompt_engineering_lab --cov-report=term-missing
```

## Project Structure

```
prompt-engineering-lab/
├── prompt_engineering_lab/
│   ├── __init__.py           # Package exports
│   ├── template.py           # Template management
│   ├── patterns.py           # Prompt patterns
│   ├── optimizer.py          # Optimization strategies
│   ├── ab_tester.py          # A/B testing framework
│   ├── token_counter.py      # Token counting
│   ├── cost_calculator.py    # Cost estimation
│   └── cli.py                # Command-line interface
├── tests/
│   ├── conftest.py           # Pytest fixtures
│   ├── test_template.py
│   ├── test_patterns.py
│   ├── test_optimizer.py
│   ├── test_ab_tester.py
│   ├── test_token_counter.py
│   ├── test_cost_calculator.py
│   └── test_cli.py
├── pyproject.toml            # Project configuration
├── Makefile                  # Development commands
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
└── README.md                 # This file
```

## Service Mapping

- Service 5: Prompt Engineering and System Optimization
- Service 6: AI-Powered Personal and Business Automation

## Certification Mapping

- Vanderbilt Prompt Engineering for ChatGPT
- Vanderbilt ChatGPT Personal Automation
- IBM Generative AI Engineering with PyTorch, LangChain & Hugging Face
- Google Cloud Generative AI Leader Certificate

## Examples

### Template Chaining

```python
from prompt_engineering_lab import PromptTemplate, PromptChain

# Define chain steps
step1 = PromptTemplate(name="outline", template="Create an outline for: {topic}")
step2 = PromptTemplate(name="expand", template="Expand on this outline: {previous_output}")

# Execute chain
chain = PromptChain(templates=[step1, step2])
results = chain.run({"topic": "Machine Learning"})
```

### A/B Testing

```python
from prompt_engineering_lab import ABTestRunner

# Define scorer (e.g., response quality)
def scorer(template):
    # Your scoring logic here
    return len(template)  # Simplified example

# Run A/B test
runner = ABTestRunner(scorer=scorer)
result = runner.run(
    template_a="Explain {topic} concisely.",
    template_b="Provide a detailed explanation of {topic}.",
    inputs=["AI", "blockchain", "quantum"]
)

print(f"Winner: {result.winner}")
print(f"P-value: {result.p_value}")
print(f"Effect size: {result.effect_size}")
```

### Cost Optimization

```python
from prompt_engineering_lab import TokenCounter, CostCalculator

# Count tokens
counter = TokenCounter()
input_tokens = counter.count("Your prompt here", provider="claude")
output_tokens = 500  # Expected output

# Compare providers
calc = CostCalculator()
estimates = calc.compare_providers(input_tokens, output_tokens)

for est in estimates[:3]:  # Top 3 cheapest
    print(f"{est.provider} {est.model}: ${est.total_cost:.4f}")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for release history.

## Related Projects

- [EnterpriseHub](https://github.com/ChunkyTortoise/EnterpriseHub) -- Real estate AI platform with BI dashboards and CRM integration
- [docqa-engine](https://github.com/ChunkyTortoise/docqa-engine) -- RAG document Q&A with hybrid retrieval and prompt engineering lab
- [ai-orchestrator](https://github.com/ChunkyTortoise/ai-orchestrator) -- AgentForge: unified async LLM interface (Claude, Gemini, OpenAI, Perplexity)
- [Portfolio](https://chunkytortoise.github.io) -- Project showcase and services

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## Author

**ChunkyTortoise**

## Acknowledgments

- Inspired by modern prompt engineering research and best practices
- Built with Python 3.11+ and Click for CLI functionality
- Follows test-driven development with 190+ comprehensive tests
