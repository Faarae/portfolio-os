"""Rename command for Portfolio OS.

CLI command layer - receives user input and delegates to ProjectService.
"""

from ..core import Filesystem
from ..services import ProjectService


class RenameCommand:
    """Command to rename an existing portfolio project."""

    def __init__(self) -> None:
        """Initialize rename command."""
        self.filesystem = Filesystem()
        self.project_service = ProjectService(self.filesystem)

    def execute(self, name: str, category: str, new_name: str) -> None:
        """Execute rename command.

        Args:
            name: Project name or slug.
            category: Category string.
            new_name: New project name.
        """
        self.project_service.rename_project(name, category, new_name)
