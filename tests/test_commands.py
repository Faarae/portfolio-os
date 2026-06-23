"""Unit tests for Portfolio OS CLI commands."""

import tempfile
from pathlib import Path

from src.commands import InitCommand
from src.constants import DIR_CONFIG, FILE_CONFIG


def test_init_command_execute() -> None:
    """Test that InitCommand delegates correctly and initializes portfolio."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = InitCommand()
        target = Path(tmpdir) / "test_cmd_portfolio"

        cmd.execute(str(target))

        assert (target / DIR_CONFIG / FILE_CONFIG).exists()
