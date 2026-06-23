"""Base service class for Portfolio OS.

Provides common foundation for business logic services.
"""

from ..core import Filesystem, get_logger


class BaseService:
    """Base service class.

    All business services should inherit from this class.
    Provides common filesystem access and logger.
    """

    def __init__(self, filesystem: Filesystem) -> None:
        """Initialize base service.

        Args:
            filesystem: Filesystem manager instance.
        """
        self.filesystem = filesystem
        self.logger = get_logger(self.__class__.__module__)
