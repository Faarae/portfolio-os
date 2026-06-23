"""Unit tests for Portfolio OS utility helper functions."""

from pathlib import Path

import pytest

from src.utils.helpers import (
    ensure_parent_dir,
    generate_id,
    get_timestamp,
    merge_dicts,
    safe_dict_get,
    validate_path,
)


def test_generate_id() -> None:
    """Test generating unique IDs."""
    id1 = generate_id()
    id2 = generate_id()
    assert id1 != id2
    assert len(id1) == 8

    prefixed_id = generate_id("proj")
    assert prefixed_id.startswith("proj-")
    assert len(prefixed_id) == 13  # "proj-" (5) + unique (8)


def test_validate_path() -> None:
    """Test validating paths and converting to Path object."""
    p1 = Path("test")
    assert validate_path(p1) is p1

    p2 = validate_path("test/path")
    assert isinstance(p2, Path)
    assert p2 == Path("test/path")

    with pytest.raises(TypeError):
        validate_path(12345)


def test_get_timestamp() -> None:
    """Test get_timestamp format."""
    ts = get_timestamp()
    assert isinstance(ts, str)
    # Basic ISO validation
    assert "T" in ts


def test_ensure_parent_dir() -> None:
    """Test ensuring parent directory is created."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        test_path = Path(tmpdir) / "subdir" / "file.txt"
        assert not test_path.parent.exists()

        res = ensure_parent_dir(test_path)
        assert res is test_path
        assert test_path.parent.exists()


def test_safe_dict_get() -> None:
    """Test safely getting values from dictionary."""
    d = {"key": "val"}
    assert safe_dict_get(d, "key") == "val"
    assert safe_dict_get(d, "missing", "default") == "default"
    assert safe_dict_get(None, "key", "default") == "default"  # type: ignore


def test_merge_dicts() -> None:
    """Test merging dictionaries."""
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 3, "c": 4}
    res = merge_dicts(d1, d2)
    assert res == {"a": 1, "b": 3, "c": 4}
    # Verify d1 and d2 are not mutated
    assert d1 == {"a": 1, "b": 2}
    assert d2 == {"b": 3, "c": 4}


def test_slugify() -> None:
    """Test slugify helper function."""
    from src.utils.helpers import slugify

    assert slugify("Hello World") == "hello-world"
    assert slugify("Hello   World!!!") == "hello-world"
    assert slugify("---Hello-World---") == "hello-world"
    assert slugify("Project_A-123") == "project_a-123"
    assert slugify("   ") == ""
