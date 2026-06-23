"""Init command for Portfolio OS.

CLI command layer - receives user input and delegates to services.
Contains zero business logic.
"""

from pathlib import Path

from ..core import Filesystem
from ..services import InitService


class InitCommand:
    """Initialize a new portfolio project.

    Pure CLI command - only receives input and calls service layer.
    """

    def __init__(self) -> None:
        """Initialize command."""
        self.filesystem = Filesystem()
        self.init_service = InitService(self.filesystem)

    def execute(self, directory: str) -> None:
        """Execute init command.

        Args:
            directory: Directory path to initialize.

        Raises:
            Exception: If initialization fails (propagated from service).
        """
        target_dir = Path(directory).resolve()
        self.init_service.initialize(target_dir)
