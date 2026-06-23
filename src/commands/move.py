"""Move command for Portfolio OS.

CLI command layer - receives user input and delegates to ProjectService.
"""

from ..core import Filesystem
from ..services import ProjectService


class MoveCommand:
    """Command to move a project to a different category."""

    def __init__(self) -> None:
        """Initialize move command."""
        self.filesystem = Filesystem()
        self.project_service = ProjectService(self.filesystem)

    def execute(self, name: str, source_category: str, dest_category: str) -> None:
        """Execute move command.

        Args:
            name: Project name or slug.
            source_category: Source category.
            dest_category: Destination category.
        """
        self.project_service.move_project(name, source_category, dest_category)
