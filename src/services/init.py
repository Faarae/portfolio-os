"""Portfolio initialization service.

Contains business logic for initializing new portfolio projects.
"""

import json
from pathlib import Path

from ..constants import (
    DEFAULT_OWNER,
    DEFAULT_PORTFOLIO_NAME,
    DEFAULT_PORTFOLIO_VERSION,
    DIR_CONFIG,
    DIR_META,
    DIR_PROJECTS,
    DIR_TEMPLATES,
    FILE_CONFIG,
    FILE_PROJECT_INDEX,
)
from ..core import Filesystem, get_logger
from ..core.exceptions import PortfolioOSError

logger = get_logger(__name__)


class InitService:
    """Service for initializing portfolio projects.

    Handles all business logic for portfolio creation.
    """

    def __init__(self, filesystem: Filesystem) -> None:
        """Initialize service.

        Args:
            filesystem: Filesystem manager instance.
        """
        self.filesystem = filesystem

    def create_project_structure(self, directory: Path) -> None:
        """Create project directory structure.

        Args:
            directory: Directory to initialize.
        """
        # Create directories
        self.filesystem.ensure_dir(directory / DIR_PROJECTS)
        self.filesystem.ensure_dir(directory / DIR_TEMPLATES)
        self.filesystem.ensure_dir(directory / DIR_META)

    def create_project_index(self, directory: Path) -> None:
        """Create initial project index file.

        Args:
            directory: Directory containing projects folder.
        """
        from typing import Any

        index_data: dict[str, list[Any]] = {
            "projects": [],
            "skills": [],
            "experience": [],
            "awards": [],
        }
        index_path = directory / DIR_PROJECTS / FILE_PROJECT_INDEX
        content = json.dumps(index_data, indent=2)
        self.filesystem.write_file(index_path, content)

    def create_config_file(self, directory: Path, owner: str = DEFAULT_OWNER) -> None:
        """Create portfolio configuration file.

        Args:
            directory: Directory to initialize.
            owner: Portfolio owner name.
        """
        config_data = {
            "owner": owner,
            "portfolio_name": DEFAULT_PORTFOLIO_NAME,
            "version": DEFAULT_PORTFOLIO_VERSION,
        }
        config_path = directory / DIR_CONFIG / FILE_CONFIG
        content = json.dumps(config_data, indent=2)
        self.filesystem.write_file(config_path, content)

    def populate_templates(self, directory: Path) -> None:
        """Populate default templates in templates directory.

        Args:
            directory: Directory to initialize.
        """
        readme_content = (
            "# {title}\n\n"
            "{subtitle}\n\n"
            "## Description\n"
            "{description}\n\n"
            "## Project Specifications\n"
            "*   **Category**: {category}\n"
            "*   **Status**: {status}\n"
            "*   **Year**: {year}\n"
            "*   **Role**: {role}\n\n"
            "## Technologies Used\n"
            "*   {technologies}\n\n"
            "## Links\n"
            "*   **GitHub**: {github}\n"
            "*   **Website**: {website}\n"
            "*   **Demo**: {demo}\n"
        )
        project_json_content = (
            "{\n"
            '  "id": "",\n'
            '  "slug": "",\n'
            '  "title": "",\n'
            '  "subtitle": "",\n'
            '  "description": "",\n'
            '  "category": "",\n'
            '  "status": "draft",\n'
            '  "year": "",\n'
            '  "technologies": [],\n'
            '  "tags": [],\n'
            '  "github": "",\n'
            '  "website": "",\n'
            '  "demo": "",\n'
            '  "role": "",\n'
            '  "featured": false,\n'
            '  "created_at": "",\n'
            '  "updated_at": ""\n'
            "}\n"
        )
        self.filesystem.write_file(
            directory / DIR_TEMPLATES / "README.md", readme_content
        )
        self.filesystem.write_file(
            directory / DIR_TEMPLATES / "project.json", project_json_content
        )

    def initialize(self, directory: Path) -> None:
        """Initialize a new portfolio project.

        Creates the complete project structure and necessary configuration files.

        Args:
            directory: Directory to initialize portfolio in.

        Raises:
            PortfolioOSError: If initialization fails.
        """
        try:
            self.create_project_structure(directory)
            self.create_project_index(directory)
            self.create_config_file(directory)
            self.populate_templates(directory)
            logger.success(f"Portfolio initialized in {directory}")
        except Exception as e:
            logger.error(f"Failed to initialize portfolio: {e}")
            raise PortfolioOSError(f"Failed to initialize portfolio: {e}") from e
