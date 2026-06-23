"""Unit and CLI integration tests for ProjectService in Portfolio OS."""

import json
import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from typer.testing import CliRunner

from src.constants import DIR_META, DIR_PROJECTS, DIR_TEMPLATES
from src.core import Filesystem
from src.core.exceptions import (
    ConfigurationError,
    InvalidCategoryError,
    InvalidProjectNameError,
    ProjectAlreadyExistsError,
    ProjectNotFoundError,
)
from src.main import app
from src.models import ProjectCategory
from src.services import InitService, ProjectService

runner = CliRunner()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory Path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def initialized_workspace(temp_dir: Path) -> Path:
    """Provide a Path to an initialized workspace."""
    fs = Filesystem(temp_dir)
    init_service = InitService(fs)
    init_service.initialize(temp_dir)
    return temp_dir


class TestProjectService:
    """Test ProjectService operations."""

    def test_validate_workspace_raises_without_init(self, temp_dir: Path) -> None:
        """Test workspace validation raises ConfigurationError if not initialized."""
        fs = Filesystem(temp_dir)
        service = ProjectService(fs)
        with pytest.raises(ConfigurationError):
            service.create_project("My Project", "personal")

    def test_validate_project_name(self, initialized_workspace: Path) -> None:
        """Test validate_project_name with valid, empty, illegal, and reserved names."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)

        # Valid names
        assert service.validate_project_name("My Project") == "My Project"
        assert service.validate_project_name("test-project") == "test-project"
        assert service.validate_project_name("Project_1") == "Project_1"
        assert service.validate_project_name("  Trimmed Name  ") == "Trimmed Name"

        # Empty name
        with pytest.raises(InvalidProjectNameError, match="cannot be empty"):
            service.validate_project_name("")
        with pytest.raises(InvalidProjectNameError, match="cannot be empty"):
            service.validate_project_name("   ")

        # Illegal characters
        illegal_chars = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
        for char in illegal_chars:
            with pytest.raises(InvalidProjectNameError, match="illegal characters"):
                service.validate_project_name(f"Proj{char}ect")

        # Reserved names
        reserved = [
            "con",
            "prn",
            "aux",
            "nul",
            "projects",
            "templates",
            "trash",
            "config",
        ]
        for name in reserved:
            with pytest.raises(InvalidProjectNameError, match="reserved system name"):
                service.validate_project_name(name)
            with pytest.raises(InvalidProjectNameError, match="reserved system name"):
                service.validate_project_name(name.upper())

    def test_validate_category(self, initialized_workspace: Path) -> None:
        """Test validate_category parses category strings to enum, or raises error."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)

        # Valid categories
        assert service.validate_category("personal") == ProjectCategory.PERSONAL
        assert service.validate_category("  Personal  ") == ProjectCategory.PERSONAL
        assert service.validate_category("ACADEMIC") == ProjectCategory.ACADEMIC
        assert service.validate_category("freelance") == ProjectCategory.FREELANCE

        # Invalid category
        with pytest.raises(InvalidCategoryError, match="Invalid category"):
            service.validate_category("invalid_category_name")

    def test_create_project_success(self, initialized_workspace: Path) -> None:
        """Test successful project creation with folders and templates."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)

        project_path = service.create_project("My Super Project", "personal")

        expected_dir = (
            initialized_workspace / DIR_PROJECTS / "personal" / "my-super-project"
        )
        assert project_path == expected_dir
        assert project_path.exists()

        # Check subdirectories
        assert (project_path / "assets" / "documents").is_dir()
        assert (project_path / "assets" / "images").is_dir()
        assert (project_path / "assets" / "screenshots").is_dir()
        assert (project_path / "assets" / "videos").is_dir()
        assert (project_path / "assets" / "presentations").is_dir()
        assert (project_path / "source").is_dir()
        assert (project_path / "metadata").is_dir()

        # Check README.md
        readme_file = project_path / "README.md"
        assert readme_file.exists()
        readme_content = readme_file.read_text(encoding="utf-8")
        assert "My Super Project" in readme_content
        assert "Category: personal" in readme_content

        # Check project.json in metadata/
        meta_file = project_path / "metadata" / "project.json"
        assert meta_file.exists()
        with open(meta_file, encoding="utf-8") as f:
            meta = json.load(f)
            assert meta["title"] == "My Super Project"
            assert meta["slug"] == "my-super-project"
            assert meta["category"] == "personal"
            assert meta["status"] == "draft"
            assert "id" in meta

    def test_create_project_fallback_readme_template(
        self, initialized_workspace: Path
    ) -> None:
        """Test fallback README when template README.md does not exist."""
        fs = Filesystem(initialized_workspace)
        # Remove template README
        tmpl_readme = initialized_workspace / DIR_TEMPLATES / "README.md"
        if tmpl_readme.exists():
            tmpl_readme.unlink()

        service = ProjectService(fs)
        project_path = service.create_project("Fallback Proj", "personal")
        readme_file = project_path / "README.md"
        assert readme_file.exists()
        readme_content = readme_file.read_text(encoding="utf-8")
        assert "# Fallback Proj" in readme_content

    def test_create_project_custom_title(self, initialized_workspace: Path) -> None:
        """Test custom display title works correctly."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)

        project_path = service.create_project(
            "custom-slug", "personal", title="Custom Display Title"
        )
        readme_content = (project_path / "README.md").read_text(encoding="utf-8")
        assert "Custom Display Title" in readme_content

        meta_file = project_path / "metadata" / "project.json"
        with open(meta_file, encoding="utf-8") as f:
            meta = json.load(f)
            assert meta["title"] == "Custom Display Title"
            assert meta["slug"] == "custom-slug"

    def test_create_project_already_exists(self, initialized_workspace: Path) -> None:
        """Test that creating existing project raises ProjectAlreadyExistsError."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)

        service.create_project("Duplicate", "personal")

        # Duplicate same category
        with pytest.raises(ProjectAlreadyExistsError, match="already exists"):
            service.create_project("Duplicate", "personal")

        # Duplicate different category
        with pytest.raises(ProjectAlreadyExistsError, match="already exists"):
            service.create_project("Duplicate", "academic")

        # Overwrite works
        new_path = service.create_project("Duplicate", "personal", overwrite=True)
        assert new_path.exists()

    def test_delete_project_not_found(self, initialized_workspace: Path) -> None:
        """Test delete raises ProjectNotFoundError if project doesn't exist."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)
        with pytest.raises(ProjectNotFoundError):
            service.delete_project("nonexistent", "personal")

    def test_delete_project_soft(self, initialized_workspace: Path) -> None:
        """Test soft delete moves project to .porto/trash."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)

        project_path = service.create_project("Trash Me", "personal")
        assert project_path.exists()

        service.delete_project("Trash Me", "personal", hard=False)
        assert not project_path.exists()

        trash_root = initialized_workspace / DIR_META / "trash" / "personal"
        assert trash_root.exists()
        trashed_folders = list(trash_root.glob("trash-me_*"))
        assert len(trashed_folders) == 1
        assert (trashed_folders[0] / "README.md").exists()

    def test_delete_project_hard(self, initialized_workspace: Path) -> None:
        """Test hard delete removes project directory completely."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)

        project_path = service.create_project("Hard Delete Me", "personal")
        assert project_path.exists()

        service.delete_project("Hard Delete Me", "personal", hard=True)
        assert not project_path.exists()

        trash_root = initialized_workspace / DIR_META / "trash" / "personal"
        assert (
            not trash_root.exists()
            or len(list(trash_root.glob("hard-delete-me_*"))) == 0
        )

    def test_rename_project_same_slug(self, initialized_workspace: Path) -> None:
        """Test renaming to same name/slug returns immediately."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)

        project_path = service.create_project("Rename Match", "personal")
        new_path = service.rename_project("Rename Match", "personal", "Rename Match")
        assert project_path == new_path

    def test_rename_project_not_found(self, initialized_workspace: Path) -> None:
        """Test renaming nonexistent project raises ProjectNotFoundError."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)
        with pytest.raises(ProjectNotFoundError):
            service.rename_project("nonexistent", "personal", "new-name")

    def test_rename_project_already_exists(self, initialized_workspace: Path) -> None:
        """Test rename raises ProjectAlreadyExistsError if target exists."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)

        service.create_project("First Project", "personal")
        service.create_project("Second Project", "personal")

        with pytest.raises(ProjectAlreadyExistsError, match="already exists"):
            service.rename_project("First Project", "personal", "Second Project")

    def test_rename_project_success(self, initialized_workspace: Path) -> None:
        """Test successful rename updates directory structure and metadata."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)

        old_path = service.create_project("Old Name", "personal")
        new_path = service.rename_project("Old Name", "personal", "New Name")

        assert not old_path.exists()
        assert new_path.exists()
        assert new_path.name == "new-name"

        meta_file = new_path / "metadata" / "project.json"
        assert meta_file.exists()
        with open(meta_file, encoding="utf-8") as f:
            meta = json.load(f)
            assert meta["slug"] == "new-name"
            # Title should be updated if it matched the original name
            assert meta["title"] == "New Name"

    def test_rename_project_success_custom_title_retained(
        self, initialized_workspace: Path
    ) -> None:
        """Test successful rename does not change a custom display title."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)

        old_path = service.create_project(
            "old-slug", "personal", title="Custom Unique Title"
        )
        new_path = service.rename_project("old-slug", "personal", "new-slug")

        assert not old_path.exists()
        assert new_path.exists()

        meta_file = new_path / "metadata" / "project.json"
        with open(meta_file, encoding="utf-8") as f:
            meta = json.load(f)
            assert meta["slug"] == "new-slug"
            assert meta["title"] == "Custom Unique Title"

    def test_rename_project_corrupted_metadata_logs_warning(
        self, initialized_workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test rename continues and logs warning if metadata JSON is corrupted."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)

        old_path = service.create_project("Bad Meta", "personal")
        meta_file = old_path / "metadata" / "project.json"
        # Overwrite with invalid JSON
        meta_file.write_text("invalid json contents")

        # Spy on logger.warning
        warnings: list[str] = []
        monkeypatch.setattr(service.logger, "warning", warnings.append)

        new_path = service.rename_project("Bad Meta", "personal", "Good Meta")
        assert not old_path.exists()
        assert new_path.exists()
        # Verify warning log contains error info
        assert len(warnings) == 1
        assert "failed to update metadata file" in warnings[0]

    def test_move_project_same_category(self, initialized_workspace: Path) -> None:
        """Test moving to same category returns immediately."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)

        project_path = service.create_project("Move Same", "personal")
        moved_path = service.move_project("Move Same", "personal", "personal")
        assert project_path == moved_path

    def test_move_project_not_found(self, initialized_workspace: Path) -> None:
        """Test moving nonexistent project raises ProjectNotFoundError."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)
        with pytest.raises(ProjectNotFoundError):
            service.move_project("nonexistent", "personal", "academic")

    def test_move_project_already_exists_in_dest(
        self, initialized_workspace: Path
    ) -> None:
        """Test moving raises ProjectAlreadyExistsError if target exists."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)

        service.create_project("Overlap", "personal")
        # Manually create conflicting folder in academic
        (initialized_workspace / DIR_PROJECTS / "academic" / "overlap").mkdir(
            parents=True, exist_ok=True
        )

        with pytest.raises(
            ProjectAlreadyExistsError, match="already exists in destination category"
        ):
            service.move_project("Overlap", "personal", "academic")

    def test_move_project_success(self, initialized_workspace: Path) -> None:
        """Test successful move updates directory location and category metadata."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)

        src_path = service.create_project("Move Me", "personal")
        dest_path = service.move_project("Move Me", "personal", "academic")

        assert not src_path.exists()
        assert dest_path.exists()
        assert (
            dest_path == initialized_workspace / DIR_PROJECTS / "academic" / "move-me"
        )

        meta_file = dest_path / "metadata" / "project.json"
        assert meta_file.exists()
        with open(meta_file, encoding="utf-8") as f:
            meta = json.load(f)
            assert meta["category"] == "academic"

    def test_move_project_corrupted_metadata_logs_warning(
        self, initialized_workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test move continues and logs warning if metadata JSON is corrupted."""
        fs = Filesystem(initialized_workspace)
        service = ProjectService(fs)

        src_path = service.create_project("Bad Move Meta", "personal")
        meta_file = src_path / "metadata" / "project.json"
        # Overwrite with invalid JSON
        meta_file.write_text("invalid json contents")

        # Spy on logger.warning
        warnings: list[str] = []
        monkeypatch.setattr(service.logger, "warning", warnings.append)

        dest_path = service.move_project("Bad Move Meta", "personal", "academic")
        assert not src_path.exists()
        assert dest_path.exists()
        # Verify warning log contains error info
        assert len(warnings) == 1
        assert "failed to update metadata file" in warnings[0]


class TestProjectCLI:
    """Test CLI commands (new, delete, rename, move) delegation and output."""

    def test_cli_new_success(
        self, initialized_workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test CLI 'new' command executes successfully."""
        # Change Cwd to test workspace so default Filesystem finds it
        monkeypatch.chdir(initialized_workspace)

        result = runner.invoke(app, ["new", "CLI Project", "personal"])
        assert result.exit_code == 0
        assert (
            "Project created successfully!" in result.stdout
            or "[v] Project created successfully!" in result.stdout
        )

        # Verify created folder
        assert (
            initialized_workspace / DIR_PROJECTS / "personal" / "cli-project"
        ).exists()

    def test_cli_new_custom_title_and_overwrite(
        self, initialized_workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test CLI 'new' command with custom title and overwrite options."""
        monkeypatch.chdir(initialized_workspace)

        # Create initially
        runner.invoke(app, ["new", "CLI Project", "personal"])

        # Re-create without overwrite should fail
        result = runner.invoke(app, ["new", "CLI Project", "personal"])
        assert result.exit_code == 1
        assert "Error:" in result.stdout

        # Re-create with overwrite should succeed
        result = runner.invoke(
            app,
            ["new", "CLI Project", "personal", "--title", "Updated CLI", "--overwrite"],
        )
        assert result.exit_code == 0
        assert (
            "Project created successfully!" in result.stdout
            or "[v] Project created successfully!" in result.stdout
        )

        meta_file = (
            initialized_workspace
            / DIR_PROJECTS
            / "personal"
            / "cli-project"
            / "metadata"
            / "project.json"
        )
        with open(meta_file, encoding="utf-8") as f:
            meta = json.load(f)
            assert meta["title"] == "Updated CLI"

    def test_cli_new_invalid_category(
        self, initialized_workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test CLI 'new' command with invalid category exits with code 1."""
        monkeypatch.chdir(initialized_workspace)

        result = runner.invoke(app, ["new", "Invalid Cat Proj", "nonsense_category"])
        assert result.exit_code == 1
        assert "Error:" in result.stdout
        assert "nonsense_category" in result.stdout

    def test_cli_new_unexpected_error(
        self, initialized_workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test CLI handles unexpected non-PortfolioOS exceptions gracefully."""
        monkeypatch.chdir(initialized_workspace)

        def mock_create(*args: Any, **kwargs: Any) -> None:
            raise RuntimeError("Unexpected file system failure")

        monkeypatch.setattr(ProjectService, "create_project", mock_create)

        result = runner.invoke(app, ["new", "Unexpected Proj", "personal"])
        assert result.exit_code == 1
        assert "Unexpected Error: Unexpected file system failure" in result.stdout

    def test_cli_delete_soft_success(
        self, initialized_workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test CLI 'delete' command executes soft delete successfully."""
        monkeypatch.chdir(initialized_workspace)

        # Create project first
        runner.invoke(app, ["new", "CLI Del", "personal"])
        assert (initialized_workspace / DIR_PROJECTS / "personal" / "cli-del").exists()

        result = runner.invoke(app, ["delete", "CLI Del", "personal"])
        assert result.exit_code == 0
        assert (
            "Project deleted successfully!" in result.stdout
            or "[v] Project deleted successfully!" in result.stdout
        )
        assert not (
            initialized_workspace / DIR_PROJECTS / "personal" / "cli-del"
        ).exists()

    def test_cli_delete_hard_success(
        self, initialized_workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test CLI 'delete' command executes hard delete successfully."""
        monkeypatch.chdir(initialized_workspace)

        # Create project first
        runner.invoke(app, ["new", "CLI Del Hard", "personal"])

        result = runner.invoke(app, ["delete", "CLI Del Hard", "personal", "--hard"])
        assert result.exit_code == 0
        assert (
            "Project deleted successfully!" in result.stdout
            or "[v] Project deleted successfully!" in result.stdout
        )
        assert not (
            initialized_workspace / DIR_PROJECTS / "personal" / "cli-del-hard"
        ).exists()

    def test_cli_delete_error(
        self, initialized_workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test CLI 'delete' command prints error on missing project."""
        monkeypatch.chdir(initialized_workspace)

        result = runner.invoke(app, ["delete", "Nonexistent CLI Del", "personal"])
        assert result.exit_code == 1
        assert "Error:" in result.stdout

    def test_cli_delete_unexpected_error(
        self, initialized_workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test CLI delete handles unexpected exception."""
        monkeypatch.chdir(initialized_workspace)

        def mock_delete(*args: Any, **kwargs: Any) -> None:
            raise RuntimeError("Unexpected failure")

        monkeypatch.setattr(ProjectService, "delete_project", mock_delete)

        result = runner.invoke(app, ["delete", "Some Proj", "personal"])
        assert result.exit_code == 1
        assert "Unexpected Error: Unexpected failure" in result.stdout

    def test_cli_rename_success(
        self, initialized_workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test CLI 'rename' command executes successfully."""
        monkeypatch.chdir(initialized_workspace)

        # Create project first
        runner.invoke(app, ["new", "CLI Rename", "personal"])

        result = runner.invoke(app, ["rename", "CLI Rename", "personal", "CLI Renamed"])
        assert result.exit_code == 0
        assert (
            "Project renamed successfully!" in result.stdout
            or "[v] Project renamed successfully!" in result.stdout
        )
        assert not (
            initialized_workspace / DIR_PROJECTS / "personal" / "cli-rename"
        ).exists()
        assert (
            initialized_workspace / DIR_PROJECTS / "personal" / "cli-renamed"
        ).exists()

    def test_cli_rename_error(
        self, initialized_workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test CLI 'rename' command prints error on failure."""
        monkeypatch.chdir(initialized_workspace)

        result = runner.invoke(
            app, ["rename", "Nonexistent CLI Rename", "personal", "New CLI Name"]
        )
        assert result.exit_code == 1
        assert "Error:" in result.stdout

    def test_cli_rename_unexpected_error(
        self, initialized_workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test CLI rename handles unexpected exception."""
        monkeypatch.chdir(initialized_workspace)

        def mock_rename(*args: Any, **kwargs: Any) -> None:
            raise RuntimeError("Unexpected rename crash")

        monkeypatch.setattr(ProjectService, "rename_project", mock_rename)

        result = runner.invoke(app, ["rename", "Some Proj", "personal", "New Name"])
        assert result.exit_code == 1
        assert "Unexpected Error: Unexpected rename crash" in result.stdout

    def test_cli_move_success(
        self, initialized_workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test CLI 'move' command executes successfully."""
        monkeypatch.chdir(initialized_workspace)

        # Create project first
        runner.invoke(app, ["new", "CLI Move", "personal"])

        result = runner.invoke(app, ["move", "CLI Move", "personal", "academic"])
        assert result.exit_code == 0
        assert (
            "Project moved successfully!" in result.stdout
            or "[v] Project moved successfully!" in result.stdout
        )
        assert not (
            initialized_workspace / DIR_PROJECTS / "personal" / "cli-move"
        ).exists()
        assert (initialized_workspace / DIR_PROJECTS / "academic" / "cli-move").exists()

    def test_cli_move_error(
        self, initialized_workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test CLI 'move' command prints error on failure."""
        monkeypatch.chdir(initialized_workspace)

        result = runner.invoke(
            app, ["move", "Nonexistent CLI Move", "personal", "academic"]
        )
        assert result.exit_code == 1
        assert "Error:" in result.stdout

    def test_cli_move_unexpected_error(
        self, initialized_workspace: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test CLI move handles unexpected exception."""
        monkeypatch.chdir(initialized_workspace)

        def mock_move(*args: Any, **kwargs: Any) -> None:
            raise RuntimeError("Unexpected move crash")

        monkeypatch.setattr(ProjectService, "move_project", mock_move)

        result = runner.invoke(app, ["move", "Some Proj", "personal", "academic"])
        assert result.exit_code == 1
        assert "Unexpected Error: Unexpected move crash" in result.stdout
