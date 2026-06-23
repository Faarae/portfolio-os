"""Portfolio OS - CLI tool for managing software engineering portfolios."""

__version__ = "1.0.0"
__author__ = "Portfolio OS Contributors"

from .core import Config, Filesystem, get_logger, setup_logger
from .models import Project, ProjectCategory, ProjectModel, ProjectStatus
from .services import BaseService

__all__ = [
    "Config",
    "Filesystem",
    "setup_logger",
    "get_logger",
    "Project",
    "ProjectModel",
    "ProjectStatus",
    "ProjectCategory",
    "BaseService",
]
