"""Unit tests for Portfolio OS custom exceptions."""

import pytest

from src.core.exceptions import (
    ConfigFileNotFoundError,
    ConfigFormatError,
    ConfigurationError,
    DatabaseError,
    FilesystemError,
    PathNotFoundError,
    PermissionDeniedError,
    PortfolioOSError,
    ProjectError,
    ProjectValidationError,
    TemplateError,
    ValidationError,
)


def test_exception_hierarchy() -> None:
    """Test that all custom exceptions inherit from PortfolioOSError."""
    # Base error
    assert issubclass(PortfolioOSError, Exception)

    # Core branches
    assert issubclass(ConfigurationError, PortfolioOSError)
    assert issubclass(FilesystemError, PortfolioOSError)
    assert issubclass(ValidationError, PortfolioOSError)
    assert issubclass(DatabaseError, PortfolioOSError)
    assert issubclass(TemplateError, PortfolioOSError)
    assert issubclass(ProjectError, PortfolioOSError)

    # Sub-branches
    assert issubclass(ConfigFileNotFoundError, ConfigurationError)
    assert issubclass(ConfigFormatError, ConfigurationError)
    assert issubclass(PathNotFoundError, FilesystemError)
    assert issubclass(PermissionDeniedError, FilesystemError)
    assert issubclass(ProjectValidationError, ValidationError)


def test_exception_message() -> None:
    """Test that custom exceptions store their message."""
    msg = "Test error message"
    err = PortfolioOSError(msg)
    assert err.message == msg
    assert str(err) == msg

    with pytest.raises(PortfolioOSError) as excinfo:
        raise ConfigFileNotFoundError("Config missing")
    assert excinfo.value.message == "Config missing"
