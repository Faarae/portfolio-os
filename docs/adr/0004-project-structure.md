# ADR 0004: Codebase Packaging and Project Structure

## Context
As Portfolio OS incorporates linters, type checkers, and formatters, we need a consistent and standard folder layout. Dependencies, constants, and custom exception classes must be placed logically so the layout scales.

## Decision
We enforce the following packaging standards:
1.  **Constants Package**: Constants must be structured inside a dedicated `src/constants/` directory, broken down by responsibility (`app.py`, `config.py`, `filesystem.py`, `project.py`) and exposed via `__init__.py`. This avoids a single massive configuration file.
2.  **Custom Exceptions**: Exceptions reside in `src/core/exceptions.py` and are re-exported in `src/core/__init__.py`.
3.  **Modern Configuration**: Tool rules are consolidated in `pyproject.toml` (PEP 621 metadata).
4.  **Dev Dependencies**: Development tools are separated from project core dependencies via `requirements-dev.txt`.

## Consequences
*   No magic strings or ad-hoc custom exception declarations are allowed in feature code.
*   Tool configurations are easy to locate in a single file (`pyproject.toml`).
*   Onboarding and CI setup is clean.
