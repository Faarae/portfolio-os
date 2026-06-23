"""Unit tests for Portfolio OS services."""

import json
import tempfile
from pathlib import Path

import pytest

from src.constants import (
    DEFAULT_PORTFOLIO_NAME,
    DEFAULT_PORTFOLIO_VERSION,
    DIR_CONFIG,
    DIR_META,
    DIR_PROJECTS,
    DIR_TEMPLATES,
    FILE_CONFIG,
    FILE_PROJECT_INDEX,
)
from src.core import Filesystem
from src.core.exceptions import PortfolioOSError
from src.services import InitService


class TestInitService:
    """Test InitService class."""

    def test_create_project_structure(self) -> None:
        """Test creating directories structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            service = InitService(fs)
            target = Path(tmpdir) / "portfolio"

            service.create_project_structure(target)

            assert (target / DIR_PROJECTS).exists()
            assert (target / DIR_TEMPLATES).exists()
            assert (target / DIR_META).exists()

    def test_create_project_index(self) -> None:
        """Test creating project index json."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            service = InitService(fs)
            target = Path(tmpdir) / "portfolio"

            # Create projects directory first
            (target / DIR_PROJECTS).mkdir(parents=True, exist_ok=True)
            service.create_project_index(target)

            index_path = target / DIR_PROJECTS / FILE_PROJECT_INDEX
            assert index_path.exists()

            with open(index_path, encoding="utf-8") as f:
                data = json.load(f)
                assert "projects" in data
                assert "skills" in data
                assert "experience" in data
                assert "awards" in data

    def test_create_config_file(self) -> None:
        """Test creating portfolio configuration file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            service = InitService(fs)
            target = Path(tmpdir) / "portfolio"

            (target / DIR_CONFIG).mkdir(parents=True, exist_ok=True)
            service.create_config_file(target, "Jane Doe")

            config_path = target / DIR_CONFIG / FILE_CONFIG
            assert config_path.exists()

            with open(config_path, encoding="utf-8") as f:
                data = json.load(f)
                assert data["owner"] == "Jane Doe"
                assert data["portfolio_name"] == DEFAULT_PORTFOLIO_NAME
                assert data["version"] == DEFAULT_PORTFOLIO_VERSION

    def test_initialize_success(self) -> None:
        """Test complete successful initialization flow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            service = InitService(fs)
            target = Path(tmpdir) / "portfolio"

            service.initialize(target)

            assert (target / DIR_PROJECTS / FILE_PROJECT_INDEX).exists()
            assert (target / DIR_CONFIG / FILE_CONFIG).exists()

    def test_initialize_failure_raises_portfolio_os_error(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test that initialize raises PortfolioOSError on error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            service = InitService(fs)

            # Mock create_project_structure to raise an error
            def mock_create_structure(directory: Path) -> None:
                raise OSError("Simulated write failure")

            monkeypatch.setattr(
                service, "create_project_structure", mock_create_structure
            )

            with pytest.raises(PortfolioOSError):
                service.initialize(Path(tmpdir))
