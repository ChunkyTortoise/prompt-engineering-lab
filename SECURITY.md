# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 0.2.x   | Yes                |
| < 0.2   | No                 |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public GitHub issue
2. Email **chunkytortoise@proton.me** with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 5 business days
- **Fix timeline**: Depends on severity
  - Critical: 24-48 hours
  - High: 7 days
  - Medium: 30 days
  - Low: Next release

## Scope

This policy covers the `prompt-engineering-lab` Python package, including:
- Prompt template processing
- Safety checker and injection detection
- Token counting and cost calculation
- CLI tool

## Security Best Practices

When using this library:
- Never pass untrusted user input directly to prompt templates without safety checking
- Use `PromptSafetyChecker.check()` before processing external prompts
- Keep dependencies updated
