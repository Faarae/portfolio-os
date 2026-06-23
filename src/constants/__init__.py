"""Centralized constants package for Portfolio OS.

Organized into sub-modules (app, config, filesystem, project) and re-exported here.
"""

from .app import APP_HELP, APP_NAME, APP_VERSION, AUTHOR, VERSION_STRING
from .config import (
    DEFAULT_OWNER,
    DEFAULT_PORTFOLIO_NAME,
    DEFAULT_PORTFOLIO_VERSION,
    DIR_CONFIG,
    ENV_PREFIX,
    FILE_CONFIG,
)
from .filesystem import (
    DEFAULT_ENCODING,
    DIR_META,
    DIR_PROJECTS,
    DIR_TEMPLATES,
    FILE_PROJECT_INDEX,
)
from .project import (
    STATUS_ARCHIVED,
    STATUS_COMPLETED,
    STATUS_DRAFT,
    STATUS_IN_PROGRESS,
)

__all__ = [
    "APP_NAME",
    "APP_HELP",
    "APP_VERSION",
    "VERSION_STRING",
    "AUTHOR",
    "DEFAULT_ENCODING",
    "DIR_PROJECTS",
    "DIR_TEMPLATES",
    "DIR_META",
    "FILE_PROJECT_INDEX",
    "DIR_CONFIG",
    "FILE_CONFIG",
    "DEFAULT_PORTFOLIO_NAME",
    "DEFAULT_PORTFOLIO_VERSION",
    "DEFAULT_OWNER",
    "ENV_PREFIX",
    "STATUS_DRAFT",
    "STATUS_IN_PROGRESS",
    "STATUS_COMPLETED",
    "STATUS_ARCHIVED",
]
