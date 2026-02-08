"""Tests for CLI module."""

from __future__ import annotations

from click.testing import CliRunner

from prompt_engineering_lab.cli import cli


class TestCLI:
    """Test CLI commands."""

    def test_cli_help(self):
        """Test CLI help command."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Prompt Engineering Lab" in result.output

    def test_list_command(self):
        """Test list command."""
        runner = CliRunner()
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "Available Templates" in result.output
        assert "summarize" in result.output

    def test_test_command_missing_template(self):
        """Test test command with missing template."""
        runner = CliRunner()
        result = runner.invoke(cli, ["test", "nonexistent", "input text"])
        assert result.exit_code == 0
        assert "not found" in result.output

    def test_compare_command(self):
        """Test compare command."""
        runner = CliRunner()
        result = runner.invoke(cli, ["compare", "Template A", "Template B", "input"])
        assert result.exit_code == 0
        assert "Template A:" in result.output
        assert "Template B:" in result.output

    def test_enhance_command_cot(self):
        """Test enhance command with CoT pattern."""
        runner = CliRunner()
        result = runner.invoke(cli, ["enhance", "Explain AI", "-p", "cot"])
        assert result.exit_code == 0
        assert "Let's think step by step" in result.output

    def test_enhance_command_role(self):
        """Test enhance command with role pattern."""
        runner = CliRunner()
        result = runner.invoke(cli, ["enhance", "Write code", "-p", "role", "--role", "developer", "--expertise", "Python"])
        assert result.exit_code == 0
        assert "developer" in result.output
        assert "Python" in result.output

    def test_count_command(self):
        """Test count command."""
        runner = CliRunner()
        result = runner.invoke(cli, ["count", "Hello world", "-p", "claude"])
        assert result.exit_code == 0
        assert "Estimated tokens:" in result.output
