# Coding Standards

## Language

Python 3.12+

---

## Style Guide

- PEP8
- Black formatting
- Ruff linting

---

## Naming

Classes

PascalCase

Functions

snake_case

Variables

snake_case

Constants

UPPER_CASE

Private Methods

_prefix

---

## Folder Rules

One responsibility per module.

One responsibility per class.

One responsibility per function.

---

## Imports

Standard Library

↓

Third Party

↓

Internal Modules

---

## Docstrings

Use Google Style.

Example

def create_project():

    """
    Creates a new project.

    Args:
        ...

    Returns:
        ...
    """

---

## Error Handling

Never silently ignore exceptions.

Raise meaningful custom exceptions.

---

## Logging

Never use print().

Always use logger.

---

## Database

Never execute SQL inside commands.

Database operations belong to repositories.

---

## Configuration

Never read config.json directly.

Always use Config class.

---

## Path

Always use pathlib.Path.