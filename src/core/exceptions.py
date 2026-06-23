"""Custom exceptions for Portfolio OS.

This module defines the complete hierarchy of exceptions used across the
application to ensure type-safe, meaningful error handling.
"""


class PortfolioOSError(Exception):
    """Base exception for all Portfolio OS errors.

    All custom exceptions in the application inherit from this class.
    """

    def __init__(self, message: str) -> None:
        """Initialize the base portfolio error.

        Args:
            message: Explanation of the error.
        """
        super().__init__(message)
        self.message = message


class ConfigurationError(PortfolioOSError):
    """Raised when there is an issue with application configuration."""

    pass


class ConfigFileNotFoundError(ConfigurationError):
    """Raised when the configuration file is not found."""

    pass


class ConfigFormatError(ConfigurationError):
    """Raised when the configuration file contains invalid format or JSON."""

    pass


class FilesystemError(PortfolioOSError):
    """Base exception for filesystem operations."""

    pass


class PathNotFoundError(FilesystemError):
    """Raised when a required file or directory path does not exist."""

    pass


class PermissionDeniedError(FilesystemError):
    """Raised when permission is denied for a filesystem operation."""

    pass


class ValidationError(PortfolioOSError):
    """Base exception for data validation errors."""

    pass


class ProjectValidationError(ValidationError):
    """Raised when project metadata or schema validation fails."""

    pass


class DatabaseError(PortfolioOSError):
    """Base exception for database-related operations."""

    pass


class TemplateError(PortfolioOSError):
    """Base exception for portfolio templates and template rendering."""

    pass


class ProjectError(PortfolioOSError):
    """Base exception for general project management issues."""

    pass


class ProjectAlreadyExistsError(ProjectError):
    """Raised when a project already exists with the same name/slug."""

    pass


class ProjectNotFoundError(ProjectError):
    """Raised when a specified project cannot be found."""

    pass


class InvalidProjectNameError(ProjectError):
    """Raised when project name is empty, illegal, or reserved."""

    pass


class InvalidCategoryError(ProjectError):
    """Raised when category is not a valid ProjectCategory value."""

    pass
