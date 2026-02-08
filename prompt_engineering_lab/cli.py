"""Command-line interface for prompt engineering lab."""

from __future__ import annotations

import click

from prompt_engineering_lab.patterns import ChainOfThought, FewShotPattern, RolePlayPattern
from prompt_engineering_lab.template import TemplateRegistry
from prompt_engineering_lab.token_counter import TokenCounter


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Prompt Engineering Lab - CLI toolkit for prompt engineering."""
    pass


@cli.command()
@click.argument("template_name")
@click.argument("input_text")
@click.option("--vars", "-v", multiple=True, help="Template variables in key=value format")
def test(template_name, input_text, vars):
    """Test a single template with input text."""
    registry = TemplateRegistry()
    try:
        template = registry.get(template_name)
    except KeyError:
        click.echo(f"Error: Template '{template_name}' not found.", err=True)
        click.echo(f"Available templates: {', '.join(registry.list_templates())}", err=True)
        return

    template_vars = {"text": input_text}
    for var in vars:
        if "=" not in var:
            click.echo(f"Error: Invalid variable format: {var}. Use key=value format.", err=True)
            return
        key, value = var.split("=", 1)
        template_vars[key] = value

    try:
        result = template.format(**template_vars)
        click.echo("\n" + "=" * 60)
        click.echo("Template Result:")
        click.echo("=" * 60)
        click.echo(result)
        click.echo("=" * 60)
        counter = TokenCounter()
        tokens = counter.count(result)
        click.echo(f"\nEstimated tokens: {tokens}")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)


@cli.command()
@click.argument("template_a")
@click.argument("template_b")
@click.argument("input_text")
def compare(template_a, template_b, input_text):
    """Compare two templates side-by-side."""
    counter = TokenCounter()
    click.echo("\n" + "=" * 60)
    click.echo("Template A:")
    click.echo("=" * 60)
    click.echo(template_a)
    click.echo(f"\nTokens: {counter.count(template_a)}")

    click.echo("\n" + "=" * 60)
    click.echo("Template B:")
    click.echo("=" * 60)
    click.echo(template_b)
    click.echo(f"\nTokens: {counter.count(template_b)}")

    click.echo("\n" + "=" * 60)
    click.echo("Comparison:")
    click.echo("=" * 60)
    diff = counter.count(template_b) - counter.count(template_a)
    click.echo(f"Token difference: {diff:+d} (B - A)")


@cli.command(name="list")
def list_templates():
    """List all available builtin templates."""
    registry = TemplateRegistry()
    templates = registry.list_templates()

    click.echo("\nAvailable Templates:")
    click.echo("=" * 60)

    for name in templates:
        template = registry.get(name)
        vars_list = ", ".join(template.variables())
        click.echo(f"\n{name}")
        click.echo(f"  Variables: {vars_list}")
        click.echo(f"  Template: {template.template[:80]}...")


@cli.command()
@click.argument("prompt")
@click.option("--pattern", "-p", type=click.Choice(["cot", "role", "few-shot"]), default="cot", help="Pattern to apply")
@click.option("--role", default="expert", help="Role for role-play pattern")
@click.option("--expertise", default="general", help="Expertise for role-play pattern")
def enhance(prompt, pattern, role, expertise):
    """Enhance a prompt with a pattern."""
    if pattern == "cot":
        cot = ChainOfThought()
        result = cot.apply(prompt)
    elif pattern == "role":
        rp = RolePlayPattern(role=role, expertise=expertise)
        result = rp.apply(prompt)
    elif pattern == "few-shot":
        fs = FewShotPattern(examples=[{"input": "Example 1", "output": "Response 1"}])
        result = fs.apply(prompt)
    else:
        result = prompt

    click.echo("\n" + "=" * 60)
    click.echo(f"Enhanced Prompt ({pattern}):")
    click.echo("=" * 60)
    click.echo(result)

    counter = TokenCounter()
    click.echo(f"\nEstimated tokens: {counter.count(result)}")


@cli.command()
@click.argument("text")
@click.option("--provider", "-p", default="claude", help="Provider: claude, openai, gemini")
def count(text, provider):
    """Count tokens in a text string."""
    counter = TokenCounter()
    tokens = counter.count(text, provider)

    click.echo(f"\nProvider: {provider}")
    click.echo(f"Text length: {len(text)} characters")
    click.echo(f"Estimated tokens: {tokens}")


if __name__ == "__main__":
    cli()
