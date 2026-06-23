"""Unit tests for core modules.

Tests for Config, Logger, and Filesystem classes.
"""

import json
import tempfile
from pathlib import Path

import pytest

from src.constants import (
    DEFAULT_OWNER,
    DEFAULT_PORTFOLIO_NAME,
    DEFAULT_PORTFOLIO_VERSION,
)
from src.core import (
    Config,
    ConfigFileNotFoundError,
    ConfigurationError,
    Filesystem,
    PathNotFoundError,
    get_logger,
    setup_logger,
)
from src.core.logger import Logger


class TestLogger:
    """Test Logger class."""

    def test_get_logger_returns_logger_instance(self) -> None:
        """Test that get_logger returns a Logger instance."""
        logger = get_logger("test")
        assert isinstance(logger, Logger)

    def test_logger_has_log_methods(self) -> None:
        """Test that logger has all logging methods."""
        logger = get_logger("test")
        assert hasattr(logger, "info")
        assert hasattr(logger, "success")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")
        assert hasattr(logger, "debug")

    def test_logger_name_is_set(self) -> None:
        """Test that logger name is properly set."""
        logger = get_logger("test_name")
        assert logger.name == "test_name"

    def test_logger_calls_methods(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that logger methods print to console without error."""
        logger = get_logger("test_logs")
        logger.info("info msg")
        logger.success("success msg")
        logger.warning("warning msg")
        logger.error("error msg")
        logger.debug("debug msg")
        setup_logger()  # Call setup_logger for coverage
        captured = capsys.readouterr()
        assert "info msg" in captured.out
        assert "success msg" in captured.out
        assert "warning msg" in captured.out
        assert "error msg" in captured.out
        assert "debug msg" in captured.out


class TestFilesystem:
    """Test Filesystem class."""

    def test_filesystem_initializes_with_root_dir(self) -> None:
        """Test filesystem initialization with root directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            fs = Filesystem(root)
            assert fs.root_dir == root

    def test_filesystem_defaults_to_cwd(self) -> None:
        """Test filesystem defaults to current working directory."""
        fs = Filesystem()
        assert fs.root_dir == Path.cwd()

    def test_ensure_dir_creates_directory(self) -> None:
        """Test that ensure_dir creates directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            test_dir = fs.root_dir / "test_dir"
            result = fs.ensure_dir(test_dir)
            assert result.exists()
            assert result.is_dir()

    def test_ensure_dir_relative_creates_directory(self) -> None:
        """Test that ensure_dir_relative creates relative directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            fs.ensure_dir_relative("relative/path")
            assert (fs.root_dir / "relative/path").exists()

    def test_write_file_creates_file(self) -> None:
        """Test that write_file creates file with content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            test_file = fs.root_dir / "test.txt"
            fs.write_file(test_file, "test content")
            assert test_file.exists()
            assert test_file.read_text() == "test content"

    def test_write_file_relative_creates_file(self) -> None:
        """Test that write_file_relative creates file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            result = fs.write_file_relative("test.txt", "content")
            assert result.exists()
            assert result.read_text() == "content"

    def test_read_file_returns_content(self) -> None:
        """Test that read_file returns file content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            test_file = fs.root_dir / "test.txt"
            test_file.write_text("test content")
            content = fs.read_file(test_file)
            assert content == "test content"

    def test_read_file_raises_on_missing_file(self) -> None:
        """Test that read_file raises PathNotFoundError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            missing_file = fs.root_dir / "missing.txt"
            with pytest.raises(PathNotFoundError):
                fs.read_file(missing_file)

    def test_file_exists_returns_true_for_existing_file(self) -> None:
        """Test that file_exists returns True for existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            test_file = fs.root_dir / "test.txt"
            test_file.write_text("content")
            assert fs.file_exists(test_file) is True

    def test_file_exists_returns_false_for_missing_file(self) -> None:
        """Test that file_exists returns False for missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            missing_file = fs.root_dir / "missing.txt"
            assert fs.file_exists(missing_file) is False

    def test_dir_exists_returns_true_for_existing_dir(self) -> None:
        """Test that dir_exists returns True for existing directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            test_dir = fs.root_dir / "test_dir"
            test_dir.mkdir()
            assert fs.dir_exists(test_dir) is True

    def test_dir_exists_returns_false_for_missing_dir(self) -> None:
        """Test that dir_exists returns False for missing directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            missing_dir = fs.root_dir / "missing_dir"
            assert fs.dir_exists(missing_dir) is False

    def test_remove_file_deletes_file(self) -> None:
        """Test that remove_file deletes file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            test_file = fs.root_dir / "test.txt"
            test_file.write_text("content")
            fs.remove_file(test_file)
            assert not test_file.exists()

    def test_remove_dir_deletes_directory(self) -> None:
        """Test that remove_dir deletes directory and contents."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            test_dir = fs.root_dir / "test_dir"
            test_dir.mkdir()
            (test_dir / "file.txt").write_text("content")
            fs.remove_dir(test_dir)
            assert not test_dir.exists()

    def test_copy_file_creates_copy(self) -> None:
        """Test that copy_file creates file copy."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            src = fs.root_dir / "src.txt"
            dest = fs.root_dir / "dest.txt"
            src.write_text("content")
            fs.copy_file(src, dest)
            assert dest.exists()
            assert dest.read_text() == "content"

    def test_list_files_returns_files(self) -> None:
        """Test that list_files returns file list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            (fs.root_dir / "file1.txt").write_text("content")
            (fs.root_dir / "file2.txt").write_text("content")
            (fs.root_dir / "subdir").mkdir()
            files = fs.list_files(fs.root_dir)
            assert len(files) == 2
            assert any(f.name == "file1.txt" for f in files)
            assert any(f.name == "file2.txt" for f in files)

    def test_list_dirs_returns_directories(self) -> None:
        """Test that list_dirs returns directory list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            (fs.root_dir / "dir1").mkdir()
            (fs.root_dir / "dir2").mkdir()
            (fs.root_dir / "file.txt").write_text("content")
            dirs = fs.list_dirs(fs.root_dir)
            assert len(dirs) == 2
            assert any(d.name == "dir1" for d in dirs)
            assert any(d.name == "dir2" for d in dirs)

    def test_remove_nonexistent_file_does_not_raise(self) -> None:
        """Test that remove_file does not raise on nonexistent file."""
        fs = Filesystem()
        fs.remove_file(Path("nonexistent_file_123.txt"))

    def test_remove_nonexistent_dir_does_not_raise(self) -> None:
        """Test that remove_dir does not raise on nonexistent directory."""
        fs = Filesystem()
        fs.remove_dir(Path("nonexistent_dir_123"))

    def test_copy_dir_copies_all_contents(self) -> None:
        """Test that copy_dir copies all contents and deletes destination if exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            src = fs.root_dir / "src_dir"
            dest = fs.root_dir / "dest_dir"
            src.mkdir()
            (src / "file.txt").write_text("hello")
            fs.copy_dir(src, dest)
            assert dest.exists()
            assert (dest / "file.txt").read_text() == "hello"

            # Test copy_dir when dest already exists (should remove dest first)
            (src / "file.txt").write_text("hello updated")
            fs.copy_dir(src, dest)
            assert (dest / "file.txt").read_text() == "hello updated"

    def test_read_file_relative_returns_content(self) -> None:
        """Test that read_file_relative returns correct content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            fs.write_file_relative("relative.txt", "rel content")
            assert fs.read_file_relative("relative.txt") == "rel content"

    def test_read_file_relative_raises_on_missing(self) -> None:
        """Test that read_file_relative raises PathNotFoundError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            with pytest.raises(PathNotFoundError):
                fs.read_file_relative("missing.txt")

    def test_file_exists_relative(self) -> None:
        """Test file_exists_relative resolves and checks path correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            assert fs.file_exists_relative("file.txt") is False
            fs.write_file_relative("file.txt", "content")
            assert fs.file_exists_relative("file.txt") is True

    def test_dir_exists_relative(self) -> None:
        """Test dir_exists_relative resolves and checks path correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            assert fs.dir_exists_relative("dir") is False
            fs.ensure_dir_relative("dir")
            assert fs.dir_exists_relative("dir") is True

    def test_move_dir_success(self) -> None:
        """Test moving a directory successfully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            src = fs.root_dir / "src"
            dest = fs.root_dir / "dest"
            src.mkdir()
            (src / "test.txt").write_text("hello")

            fs.move_dir(src, dest)
            assert not src.exists()
            assert dest.exists()
            assert (dest / "test.txt").read_text() == "hello"

    def test_move_dir_source_missing_raises(self) -> None:
        """Test that move_dir raises PathNotFoundError when source does not exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fs = Filesystem(Path(tmpdir))
            src = fs.root_dir / "nonexistent"
            dest = fs.root_dir / "dest"
            with pytest.raises(PathNotFoundError):
                fs.move_dir(src, dest)


class TestConfig:
    """Test Config class."""

    def test_config_loads_from_file(self) -> None:
        """Test that Config loads configuration from file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            config_data = {"owner": "Test Owner", "portfolio_name": "Test"}
            config_file.write_text(json.dumps(config_data))

            config = Config(config_file)
            assert config.get_owner() == "Test Owner"
            assert config.get_portfolio_name() == "Test"

    def test_config_raises_on_missing_file(self) -> None:
        """Test that Config raises ConfigFileNotFoundError on missing file."""
        with pytest.raises(ConfigFileNotFoundError):
            Config(Path("/nonexistent/config.json"))

    def test_config_get_method(self) -> None:
        """Test that Config.get retrieves values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            config_data = {"owner": "Test", "version": "1.0.0"}
            config_file.write_text(json.dumps(config_data))

            config = Config(config_file)
            assert config.get("owner") == "Test"
            assert config.get("version") == "1.0.0"

    def test_config_get_with_default(self) -> None:
        """Test that Config.get returns default for missing keys."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            config_data = {"owner": "Test"}
            config_file.write_text(json.dumps(config_data))

            config = Config(config_file)
            assert config.get("missing", "default") == "default"

    def test_config_get_owner_returns_default_when_missing(self) -> None:
        """Test that get_owner returns DEFAULT_OWNER when missing from file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            config_data: dict[str, str] = {}
            config_file.write_text(json.dumps(config_data))

            config = Config(config_file)
            assert config.get_owner() == DEFAULT_OWNER

    def test_config_get_owner_raises_on_empty(self) -> None:
        """Test that get_owner raises ConfigurationError when empty."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            config_data = {"owner": ""}
            config_file.write_text(json.dumps(config_data))

            config = Config(config_file)
            with pytest.raises(ConfigurationError):
                config.get_owner()

    def test_config_get_portfolio_name_returns_default_when_missing(self) -> None:
        """Test that get_portfolio_name returns default when missing from file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            config_data: dict[str, str] = {}
            config_file.write_text(json.dumps(config_data))

            config = Config(config_file)
            assert config.get_portfolio_name() == DEFAULT_PORTFOLIO_NAME

    def test_config_get_portfolio_name_raises_on_empty(self) -> None:
        """Test that get_portfolio_name raises ConfigurationError when empty."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            config_data = {"portfolio_name": ""}
            config_file.write_text(json.dumps(config_data))

            config = Config(config_file)
            with pytest.raises(ConfigurationError):
                config.get_portfolio_name()

    def test_config_get_version_returns_default(self) -> None:
        """Test that get_version returns default if not set."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            config_data: dict[str, str] = {}
            config_file.write_text(json.dumps(config_data))

            config = Config(config_file)
            assert config.get_version() == DEFAULT_PORTFOLIO_VERSION

    def test_config_to_dict(self) -> None:
        """Test that to_dict returns configuration including fallbacks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "config.json"
            config_data = {"owner": "Test", "version": "1.0.0"}
            config_file.write_text(json.dumps(config_data))

            config = Config(config_file)
            result = config.to_dict()
            assert result["owner"] == "Test"
            assert result["version"] == "1.0.0"
            assert result["portfolio_name"] == DEFAULT_PORTFOLIO_NAME
