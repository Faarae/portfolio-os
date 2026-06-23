"""New command for Portfolio OS.

CLI command layer - receives user input and delegates to ProjectService.
"""

from ..core import Filesystem
from ..services import ProjectService


class NewCommand:
    """Command to create a new portfolio project."""

    def __init__(self) -> None:
        """Initialize new command."""
        self.filesystem = Filesystem()
        self.project_service = ProjectService(self.filesystem)

    def execute(
        self,
        name: str,
        category: str,
        title: str | None = None,
        overwrite: bool = False,
    ) -> None:
        """Execute new command.

        Args:
            name: Project name.
            category: Category string.
            title: Optional custom display title.
            overwrite: Set to True to overwrite existing project files.
        """
        self.project_service.create_project(name, category, title, overwrite=overwrite)
