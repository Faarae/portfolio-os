"""Filesystem layer for Portfolio OS.

Provides centralized file and directory operations.
Pure infrastructure - no logging, no side effects beyond filesystem.
"""

import shutil
from pathlib import Path

from ..constants import DEFAULT_ENCODING
from .exceptions import PathNotFoundError


class Filesystem:
    """Filesystem operations manager.

    All file operations go through this class for centralization.
    Pure operations only - no logging or business logic.
    """

    def __init__(self, root_dir: Path | None = None) -> None:
        """Initialize filesystem manager.

        Args:
            root_dir: Root directory for operations.
                Defaults to current working directory.
        """
        self.root_dir: Path = root_dir or Path.cwd()

    def ensure_dir(self, path: Path) -> Path:
        """Ensure directory exists, create if needed.

        Args:
            path: Directory path to ensure.

        Returns:
            The directory path.
        """
        path.mkdir(parents=True, exist_ok=True)
        return path

    def ensure_dir_relative(self, relative_path: str) -> Path:
        """Ensure directory exists relative to root.

        Args:
            relative_path: Relative path to directory.

        Returns:
            The absolute directory path.
        """
        path = self.root_dir / relative_path
        return self.ensure_dir(path)

    def write_file(
        self, path: Path, content: str, encoding: str = DEFAULT_ENCODING
    ) -> None:
        """Write content to file.

        Args:
            path: File path.
            content: File content.
            encoding: Text encoding (default utf-8).
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding=encoding)

    def write_file_relative(
        self,
        relative_path: str,
        content: str,
        encoding: str = DEFAULT_ENCODING,
    ) -> Path:
        """Write content to file relative to root.

        Args:
            relative_path: Relative file path.
            content: File content.
            encoding: Text encoding (default utf-8).

        Returns:
            The absolute file path.
        """
        path = self.root_dir / relative_path
        self.write_file(path, content, encoding)
        return path

    def read_file(self, path: Path, encoding: str = DEFAULT_ENCODING) -> str:
        """Read file content.

        Args:
            path: File path.
            encoding: Text encoding (default utf-8).

        Returns:
            File content.

        Raises:
            PathNotFoundError: If file does not exist.
        """
        if not path.exists():
            raise PathNotFoundError(f"File not found: {path}")
        return path.read_text(encoding=encoding)

    def read_file_relative(
        self, relative_path: str, encoding: str = DEFAULT_ENCODING
    ) -> str:
        """Read file relative to root.

        Args:
            relative_path: Relative file path.
            encoding: Text encoding (default utf-8).

        Returns:
            File content.

        Raises:
            PathNotFoundError: If file does not exist.
        """
        path = self.root_dir / relative_path
        return self.read_file(path, encoding)

    def file_exists(self, path: Path) -> bool:
        """Check if file exists.

        Args:
            path: File path.

        Returns:
            True if file exists, False otherwise.
        """
        return path.is_file()

    def file_exists_relative(self, relative_path: str) -> bool:
        """Check if file exists relative to root.

        Args:
            relative_path: Relative file path.

        Returns:
            True if file exists, False otherwise.
        """
        path = self.root_dir / relative_path
        return self.file_exists(path)

    def dir_exists(self, path: Path) -> bool:
        """Check if directory exists.

        Args:
            path: Directory path.

        Returns:
            True if directory exists, False otherwise.
        """
        return path.is_dir()

    def dir_exists_relative(self, relative_path: str) -> bool:
        """Check if directory exists relative to root.

        Args:
            relative_path: Relative directory path.

        Returns:
            True if directory exists, False otherwise.
        """
        path = self.root_dir / relative_path
        return self.dir_exists(path)

    def remove_file(self, path: Path) -> None:
        """Remove a file.

        Args:
            path: File path.
        """
        if path.exists():
            path.unlink()

    def remove_dir(self, path: Path) -> None:
        """Remove a directory and all contents.

        Args:
            path: Directory path.
        """
        if path.exists():
            shutil.rmtree(path)

    def copy_file(self, src: Path, dest: Path) -> None:
        """Copy a file.

        Args:
            src: Source file path.
            dest: Destination file path.
        """
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

    def copy_dir(self, src: Path, dest: Path) -> None:
        """Copy a directory and all contents.

        Args:
            src: Source directory path.
            dest: Destination directory path.
        """
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)

    def list_files(self, path: Path, pattern: str = "*") -> list[Path]:
        """List files in directory.

        Args:
            path: Directory path.
            pattern: File pattern (default all files).

        Returns:
            List of file paths.
        """
        return [p for p in path.glob(pattern) if p.is_file()]

    def list_dirs(self, path: Path) -> list[Path]:
        """List subdirectories.

        Args:
            path: Directory path.

        Returns:
            List of directory paths.
        """
        return [p for p in path.iterdir() if p.is_dir()]

    def move_dir(self, src: Path, dest: Path) -> None:
        """Move a directory and all its contents to a new location.

        Args:
            src: Source directory path.
            dest: Destination directory path.

        Raises:
            PathNotFoundError: If the source path does not exist.
        """
        if not src.exists():
            raise PathNotFoundError(f"Source directory not found: {src}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))
