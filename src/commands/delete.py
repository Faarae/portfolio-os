"""Delete command for Portfolio OS.

CLI command layer - receives user input and delegates to ProjectService.
"""

from ..core import Filesystem
from ..services import ProjectService


class DeleteCommand:
    """Command to delete an existing portfolio project."""

    def __init__(self) -> None:
        """Initialize delete command."""
        self.filesystem = Filesystem()
        self.project_service = ProjectService(self.filesystem)

    def execute(self, name: str, category: str, hard: bool = False) -> None:
        """Execute delete command.

        Args:
            name: Project name or slug.
            category: Category string.
            hard: True to permanently delete, False for soft delete.
        """
        self.project_service.delete_project(name, category, hard=hard)
