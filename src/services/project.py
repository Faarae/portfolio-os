"""Project management service for Portfolio OS.

Handles all project filesystem operations, category routing, templates,
and metadata generation.
"""

import json
import re
from datetime import datetime
from pathlib import Path

from ..constants import DIR_META, DIR_PROJECTS, DIR_TEMPLATES
from ..core import get_logger
from ..core.exceptions import (
    ConfigurationError,
    InvalidCategoryError,
    InvalidProjectNameError,
    ProjectAlreadyExistsError,
    ProjectNotFoundError,
)
from ..models import Project, ProjectCategory, ProjectStatus
from ..services.base import BaseService
from ..utils.helpers import generate_id, slugify

logger = get_logger(__name__)

# List of reserved system names that cannot be used as project names
RESERVED_NAMES = {
    "con",
    "prn",
    "aux",
    "nul",
    "com1",
    "com2",
    "com3",
    "com4",
    "com5",
    "com6",
    "com7",
    "com8",
    "com9",
    "lpt1",
    "lpt2",
    "lpt3",
    "lpt4",
    "lpt5",
    "lpt6",
    "lpt7",
    "lpt8",
    "lpt9",
    "projects",
    "templates",
    "config",
    "trash",
}


class ProjectService(BaseService):
    """Service for managing portfolio projects."""

    def _validate_workspace(self) -> None:
        """Verify that operations are executed inside a valid Portfolio OS workspace.

        Raises:
            ConfigurationError: If the workspace is invalid.
        """
        if not self.filesystem.dir_exists_relative(
            DIR_META
        ) or not self.filesystem.dir_exists_relative(DIR_PROJECTS):
            raise ConfigurationError(
                "Not in a valid Portfolio OS workspace. Please run 'porto init' first."
            )

    def validate_project_name(self, name: str) -> str:
        """Validate project name against illegal characters and reserved names.

        Args:
            name: The project name to validate.

        Returns:
            The validated and cleaned project name.

        Raises:
            InvalidProjectNameError: If name is empty, illegal, or reserved.
        """
        cleaned_name = name.strip()
        if not cleaned_name:
            raise InvalidProjectNameError("Project name cannot be empty.")

        # Check for illegal filesystem characters
        if re.search(r'[\\/:*?"<>|]', cleaned_name):
            raise InvalidProjectNameError(
                f"Project name contains illegal characters: {cleaned_name}"
            )

        # Check for reserved system names (case-insensitive)
        if cleaned_name.lower() in RESERVED_NAMES:
            raise InvalidProjectNameError(
                f"Project name '{cleaned_name}' is a reserved system name."
            )

        return cleaned_name

    def validate_category(self, category: str) -> ProjectCategory:
        """Validate and parse category string to ProjectCategory enum.

        Args:
            category: The category string to validate.

        Returns:
            The ProjectCategory enum value.

        Raises:
            InvalidCategoryError: If the category is invalid.
        """
        try:
            return ProjectCategory(category.lower().strip())
        except ValueError:
            valid_cats = ", ".join([c.value for c in ProjectCategory])
            raise InvalidCategoryError(
                f"Invalid category '{category}'. Must be one of: {valid_cats}"
            ) from None

    def create_project(
        self,
        name: str,
        category_str: str,
        title: str | None = None,
        overwrite: bool = False,
    ) -> Path:
        """Create a new portfolio project with standardized structure and metadata.

        Args:
            name: Project name.
            category_str: Category string.
            title: Optional custom display title.
            overwrite: Set to True to overwrite existing project files.

        Returns:
            The absolute path of the created project directory.

        Raises:
            ConfigurationError: If not inside a valid workspace.
            InvalidProjectNameError: If name is invalid.
            InvalidCategoryError: If category is invalid.
            ProjectAlreadyExistsError: If project already exists and overwrite is False.
        """
        self._validate_workspace()
        valid_name = self.validate_project_name(name)
        category = self.validate_category(category_str)
        slug = slugify(valid_name)

        project_dir = self.filesystem.root_dir / DIR_PROJECTS / category.value / slug

        # Check if project already exists in any category to prevent duplicates
        for cat in ProjectCategory:
            exist_check = self.filesystem.root_dir / DIR_PROJECTS / cat.value / slug
            if self.filesystem.dir_exists(exist_check) and not overwrite:
                raise ProjectAlreadyExistsError(
                    f"Project '{valid_name}' (slug: {slug}) "
                    f"already exists in '{cat.value}'."
                )

        # Create folder structure
        self.filesystem.ensure_dir(project_dir)
        self.filesystem.ensure_dir(project_dir / "assets")
        self.filesystem.ensure_dir(project_dir / "assets" / "documents")
        self.filesystem.ensure_dir(project_dir / "assets" / "images")
        self.filesystem.ensure_dir(project_dir / "assets" / "screenshots")
        self.filesystem.ensure_dir(project_dir / "assets" / "videos")
        self.filesystem.ensure_dir(project_dir / "assets" / "presentations")
        self.filesystem.ensure_dir(project_dir / "source")
        self.filesystem.ensure_dir(project_dir / "metadata")

        # Copy and populate templates
        readme_dest = project_dir / "README.md"
        meta_dest = project_dir / "metadata" / "project.json"

        project_title = title or valid_name

        # Read template or fallback
        readme_tmpl_path = self.filesystem.root_dir / DIR_TEMPLATES / "README.md"
        if self.filesystem.file_exists(readme_tmpl_path):
            readme_content = self.filesystem.read_file(readme_tmpl_path)
        else:
            readme_content = "# {title}\n\n{subtitle}\n"

        formatted_readme = readme_content.format(
            title=project_title,
            subtitle=f"Category: {category.value}",
            description="Details about this project...",
            category=category.value,
            status=ProjectStatus.DRAFT.value,
            year=str(datetime.now().year),
            role="Developer",
            technologies="",
            github="",
            website="",
            demo="",
        )

        if not self.filesystem.file_exists(readme_dest) or overwrite:
            self.filesystem.write_file(readme_dest, formatted_readme)

        # Generate Pydantic Project metadata model
        proj_metadata = Project(
            id=generate_id("proj"),
            slug=slug,
            title=project_title,
            category=category,
            status=ProjectStatus.DRAFT,
            year=str(datetime.now().year),
        )

        if not self.filesystem.file_exists(meta_dest) or overwrite:
            self.filesystem.write_file(
                meta_dest,
                json.dumps(proj_metadata.model_dump(), indent=2, default=str),
            )

        logger.success(
            f"Created project '{project_title}' under categories '{category.value}'"
        )
        return project_dir

    def delete_project(self, name: str, category_str: str, hard: bool = False) -> None:
        """Delete a project (either soft delete to trash or hard delete permanently).

        Args:
            name: Project name or slug.
            category_str: Project category.
            hard: If True, deletes files permanently. If False, moves to trash.

        Raises:
            ConfigurationError: If not inside a valid workspace.
            ProjectNotFoundError: If the project does not exist.
        """
        self._validate_workspace()
        category = self.validate_category(category_str)
        slug = slugify(name)

        project_dir = self.filesystem.root_dir / DIR_PROJECTS / category.value / slug

        if not self.filesystem.dir_exists(project_dir):
            raise ProjectNotFoundError(
                f"Project '{name}' not found under category '{category.value}'."
            )

        if hard:
            self.filesystem.remove_dir(project_dir)
            logger.success(
                f"Permanently deleted project '{slug}' from category '{category.value}'"
            )
        else:
            # Soft delete - move to .porto/trash/{category}/{slug}_{timestamp}/
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            trash_dir = (
                self.filesystem.root_dir
                / DIR_META
                / "trash"
                / category.value
                / f"{slug}_{timestamp}"
            )
            self.filesystem.move_dir(project_dir, trash_dir)
            logger.success(f"Soft deleted project '{slug}' (moved to .porto/trash)")

    def rename_project(self, name: str, category_str: str, new_name: str) -> Path:
        """Rename a project directory safely and update its metadata.

        Args:
            name: Current project name or slug.
            category_str: Category string.
            new_name: New project name.

        Returns:
            The absolute path of the renamed project directory.

        Raises:
            ConfigurationError: If not inside a valid workspace.
            ProjectNotFoundError: If the project does not exist.
            ProjectAlreadyExistsError: If a project with the new name already exists.
        """
        self._validate_workspace()
        category = self.validate_category(category_str)
        old_slug = slugify(name)
        new_slug = slugify(self.validate_project_name(new_name))

        old_dir = self.filesystem.root_dir / DIR_PROJECTS / category.value / old_slug
        new_dir = self.filesystem.root_dir / DIR_PROJECTS / category.value / new_slug

        if not self.filesystem.dir_exists(old_dir):
            raise ProjectNotFoundError(
                f"Project '{name}' not found under category '{category.value}'."
            )

        if old_slug == new_slug:
            # Slugs are identical, no path changes needed
            return old_dir

        # Ensure destination path does not exist
        if self.filesystem.dir_exists(new_dir):
            raise ProjectAlreadyExistsError(
                f"Cannot rename; project '{new_name}' "
                f"(slug: {new_slug}) already exists."
            )

        # Perform filesystem move
        self.filesystem.move_dir(old_dir, new_dir)

        # Update metadata project.json file
        meta_file = new_dir / "metadata" / "project.json"
        if self.filesystem.file_exists(meta_file):
            try:
                meta_content = self.filesystem.read_file(meta_file)
                meta_dict = json.loads(meta_content)
                meta_dict["slug"] = new_slug
                # Update title only if it matches the original name (not custom title)
                if meta_dict.get("title") == name:
                    meta_dict["title"] = new_name
                meta_dict["updated_at"] = datetime.now().isoformat()

                # Re-validate with Pydantic model
                proj = Project(**meta_dict)
                self.filesystem.write_file(
                    meta_file,
                    json.dumps(proj.model_dump(), indent=2, default=str),
                )
            except Exception as e:
                logger.warning(
                    f"Renamed directory but failed to update metadata file: {e}"
                )

        logger.success(f"Renamed project '{old_slug}' to '{new_slug}'")
        return new_dir

    def move_project(
        self, name: str, source_category_str: str, dest_category_str: str
    ) -> Path:
        """Move a project between categories and update its category metadata.

        Args:
            name: Project name or slug.
            source_category_str: The current category.
            dest_category_str: The target category.

        Returns:
            The absolute path of the moved project directory.

        Raises:
            ConfigurationError: If not inside a valid workspace.
            ProjectNotFoundError: If the project does not exist.
            ProjectAlreadyExistsError: If the project already exists in
                destination category.
        """
        self._validate_workspace()
        src_category = self.validate_category(source_category_str)
        dest_category = self.validate_category(dest_category_str)
        slug = slugify(name)

        if src_category == dest_category:
            # Source and destination are the same
            return self.filesystem.root_dir / DIR_PROJECTS / src_category.value / slug

        src_dir = self.filesystem.root_dir / DIR_PROJECTS / src_category.value / slug
        dest_dir = self.filesystem.root_dir / DIR_PROJECTS / dest_category.value / slug

        if not self.filesystem.dir_exists(src_dir):
            raise ProjectNotFoundError(
                f"Project '{name}' not found under category '{src_category.value}'."
            )

        if self.filesystem.dir_exists(dest_dir):
            raise ProjectAlreadyExistsError(
                f"Project '{name}' already exists in "
                f"destination category '{dest_category.value}'."
            )

        # Perform filesystem move
        self.filesystem.move_dir(src_dir, dest_dir)

        # Update metadata project.json file
        meta_file = dest_dir / "metadata" / "project.json"
        if self.filesystem.file_exists(meta_file):
            try:
                meta_content = self.filesystem.read_file(meta_file)
                meta_dict = json.loads(meta_content)
                meta_dict["category"] = dest_category.value
                meta_dict["updated_at"] = datetime.now().isoformat()

                proj = Project(**meta_dict)
                self.filesystem.write_file(
                    meta_file,
                    json.dumps(proj.model_dump(), indent=2, default=str),
                )
            except Exception as e:
                logger.warning(
                    f"Moved directory but failed to update metadata file: {e}"
                )

        logger.success(
            f"Moved project '{slug}' from '{src_category.value}' "
            f"to '{dest_category.value}'"
        )
        return dest_dir
