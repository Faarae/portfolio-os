"""Utility helper functions for Portfolio OS.

Provides common utilities and helpers.
"""

import uuid
from datetime import datetime
from pathlib import Path
from typing import Any


def generate_id(prefix: str = "") -> str:
    """Generate unique identifier.

    Args:
        prefix: Optional prefix for the ID.

    Returns:
        Generated unique ID.
    """
    unique_part = str(uuid.uuid4())[:8]
    if prefix:
        return f"{prefix}-{unique_part}"
    return unique_part


def validate_path(path: Any) -> Path:
    """Validate and convert to Path object.

    Args:
        path: Path-like object or string.

    Returns:
        Path object.

    Raises:
        TypeError: If path cannot be converted.
    """
    if isinstance(path, Path):
        return path
    if isinstance(path, str):
        return Path(path)
    raise TypeError(f"Cannot convert {type(path)} to Path")


def get_timestamp() -> str:
    """Get current timestamp in ISO format.

    Returns:
        Current timestamp as ISO string.
    """
    return datetime.now().isoformat()


def ensure_parent_dir(path: Path) -> Path:
    """Ensure parent directory exists.

    Args:
        path: File path.

    Returns:
        The path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def safe_dict_get(data: dict, key: str, default: Any = None) -> Any:
    """Safely get value from dictionary.

    Args:
        data: Dictionary to search.
        key: Key to look up.
        default: Default value if key not found.

    Returns:
        Value from dictionary or default.
    """
    if not isinstance(data, dict):
        return default
    return data.get(key, default)


def merge_dicts(base: dict, override: dict) -> dict:
    """Merge two dictionaries (override takes precedence).

    Args:
        base: Base dictionary.
        override: Dictionary with values to override.

    Returns:
        Merged dictionary.
    """
    result = base.copy()
    result.update(override)
    return result


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug.

    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores), replaces spaces and hyphens with a single hyphen, and strips
    leading/trailing hyphens.

    Args:
        text: String to convert.

    Returns:
        The slugified string.
    """
    import re

    s = text.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", "-", s)
    return s.strip("-")
