# Contributing Guidelines

Thank you for contributing to Portfolio OS! To maintain code quality, please adhere to the following development standards.

## Project Architecture

We follow a strict layered clean architecture:
```text
CLI (main.py)
   ↓
Commands (src/commands/)
   ↓
Services (src/services/)
   ↓
Core / Infrastructure (src/core/)
```

## Setup Environment

1. Ensure Python 3.11+ is installed.
2. Initialize virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Install dependencies and setup git hooks using our task runner:
   *   **Windows**:
       ```powershell
       .\run.ps1 install
       ```
   *   **Linux/macOS**:
       ```bash
       ./bootstrap.sh install
       ```

## Task Runner Commands

We provide a cross-platform task runner script (`run.ps1` or `bootstrap.sh`) and a standard `Makefile` to simplify developers' workflow:

*   **Install dependencies**:
    *   Windows: `.\run.ps1 install`
    *   Unix: `./bootstrap.sh install` (or `make install`)
*   **Format code**:
    *   Windows: `.\run.ps1 format`
    *   Unix: `./bootstrap.sh format` (or `make format`)
*   **Lint code**:
    *   Windows: `.\run.ps1 lint`
    *   Unix: `./bootstrap.sh lint` (or `make lint`)
*   **Run unit tests**:
    *   Windows: `.\run.ps1 test`
    *   Unix: `./bootstrap.sh test` (or `make test`)
*   **Run application CLI**:
    *   Windows: `.\run.ps1 run -ArgsList "init ."`
    *   Unix: `./bootstrap.sh run init .` (or `make run ARGS="init ."`)

## Coding Standards

*   **Formatting**: Keep line lengths under 88 characters. We use `black`.
*   **Linting**: We check code using `ruff`. Keep imports sorted using isort (configured in ruff).
*   **Type Hinting**: All public and private functions must have complete type signatures. Run `mypy` before committing.
*   **Docstrings**: All public modules, functions, classes, and methods must have Google-Style docstrings.
*   **Exceptions**: Never raise generic `Exception`. Always subclass and raise custom exceptions from `src.core.exceptions`.
*   **Constants**: Never use magic strings. Organize and define constants inside the `src/constants/` package.
*   **Paths & Encodings**: Always use `pathlib.Path` for path manipulations. Always use the `DEFAULT_ENCODING` constant for file I/O operations.
