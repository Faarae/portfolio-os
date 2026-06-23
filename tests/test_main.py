"""Unit and integration tests for Portfolio OS CLI entry point."""

import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from src.main import app
from src.services.init import InitService

runner = CliRunner()


def test_version_command() -> None:
    """Test displaying version string via version command."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "Portfolio OS v" in result.stdout


def test_init_command_cli() -> None:
    """Test successful portfolio initialization via CLI command."""
    with tempfile.TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / "cli_portfolio"
        result = runner.invoke(app, ["init", str(target)])
        assert result.exit_code == 0
        assert "Portfolio initialized successfully" in result.stdout
        assert (target / "config" / "config.json").exists()


def test_init_command_cli_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test initialisation failure handling in CLI."""
    from src.core.exceptions import PortfolioOSError

    def mock_initialize(self: InitService, directory: Path) -> None:
        raise PortfolioOSError("Simulated CLI error")

    monkeypatch.setattr(InitService, "initialize", mock_initialize)

    result = runner.invoke(app, ["init", "some_dir"])
    assert result.exit_code == 1
    assert "Error: Simulated CLI error" in result.stdout


def test_init_command_cli_unexpected_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test unexpected error handling in CLI command."""

    def mock_initialize(self: InitService, directory: Path) -> None:
        raise ValueError("Unexpected validation failure")

    monkeypatch.setattr(InitService, "initialize", mock_initialize)

    result = runner.invoke(app, ["init", "some_dir"])
    assert result.exit_code == 1
    assert "Unexpected Error" in result.stdout


def test_app_main_no_args() -> None:
    """Test that app with no arguments displays help/usage."""
    result = runner.invoke(app)
    # Typer returns 0 when showing help, but we verify it shows help output
    assert "Show this message and exit" in result.stdout
