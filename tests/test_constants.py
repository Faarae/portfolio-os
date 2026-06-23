"""Unit tests for Portfolio OS constants package."""

from src import constants


def test_app_constants() -> None:
    """Test application constants have correct values."""
    assert constants.APP_NAME == "porto"
    assert "Portfolio OS" in constants.APP_HELP
    assert constants.APP_VERSION == "1.0.0"
    assert "Portfolio OS" in constants.VERSION_STRING


def test_filesystem_constants() -> None:
    """Test filesystem constants are defined."""
    assert constants.DEFAULT_ENCODING == "utf-8"
    assert constants.DIR_PROJECTS == "projects"
    assert constants.DIR_TEMPLATES == "templates"
    assert constants.DIR_META == ".porto"
    assert constants.FILE_PROJECT_INDEX == "index.json"


def test_config_constants() -> None:
    """Test configuration constants are defined."""
    assert constants.DIR_CONFIG == "config"
    assert constants.FILE_CONFIG == "config.json"
    assert constants.DEFAULT_PORTFOLIO_NAME == "Portfolio"
    assert constants.DEFAULT_PORTFOLIO_VERSION == "1.0.0"
    assert constants.DEFAULT_OWNER == "Your Name"
    assert constants.ENV_PREFIX == "PORTO_"


def test_project_constants() -> None:
    """Test project status constants match expectations."""
    assert constants.STATUS_DRAFT == "draft"
    assert constants.STATUS_IN_PROGRESS == "in_progress"
    assert constants.STATUS_COMPLETED == "completed"
    assert constants.STATUS_ARCHIVED == "archived"
