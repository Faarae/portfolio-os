# Active Tasks

## Phase 1

### Core Architecture Refactoring

- [x] Replace Click with Typer - Modern async-ready CLI framework
- [x] Rename command package to commands - Proper naming convention
- [x] Extract business logic to services - InitService handles initialization
- [x] Pure command layer - Commands only receive input and call services
- [x] Replace logging with Rich - Beautiful console output with colors
- [x] Pure Filesystem layer - No logging, pure infrastructure operations
- [x] Expand Project model - Complete metadata fields for all portfolio elements
- [x] Unit test coverage - 28 comprehensive tests for Config, Logger, Filesystem
- [x] Update dependencies - requirements.txt with Typer, Rich, pytest

### Validation

- [x] All imports successful
- [x] CLI help displays correctly (Typer formatting)
- [x] Init command creates proper structure
- [x] Unit tests pass (28/28)
- [x] Rich logger works with colored output
- [x] Clean Architecture principles followed
- [x] SOLID principles validated
- [x] Type hints on all functions
- [x] Google docstrings on all public items

---

Phase 1 is complete when every checklist above is finished.

---

## Sprint 1.5 (Hardening)

### Tasks
- [x] Configure pyproject.toml with Black, Ruff, MyPy, and Pytest
- [x] Separate dependencies into pyproject.toml and requirements-dev.txt
- [x] Build custom exception hierarchy in core/exceptions.py
- [x] Establish multi-module constants package under src/constants/
- [x] Support priority-based configurations with python-dotenv
- [x] Improve Rich-based logger with caching and console reuse
- [x] Automate linting, formatting, and type-checks with pre-commit
- [x] Provide cross-platform task scripts (run.ps1, bootstrap.sh, Makefile)
- [x] Set up CI/CD pipeline using GitHub Actions (ci.yml)
- [x] Create CHANGELOG.md, CONTRIBUTING.md, and Architecture Decision Records (ADRs)

### Validation
- [x] All 61/61 unit and integration tests pass successfully
- [x] Code coverage exceeds 90% target for implemented modules (overall 93%)
- [x] Full static analysis passes Ruff and strict MyPy check without any errors
- [x] Standard formatting conforms to Black
- [x] Pre-commit configurations are successfully verified
- [x] Windows encoding issues with Unicode console icons are fixed natively and defensively
- [x] Clean Architecture, DRY, KISS, and SOLID principles maintained

---

## Phase 2: Project & Filesystem Management

### Tasks
- [x] Create project subcommands (`new`, `delete`, `rename`, `move`) in CLI
- [x] Define `ProjectCategory` as `StrEnum` instead of list of string constants
- [x] Standardize directories (`assets/`, `source/`, `metadata/`) and template files
- [x] Place `project.json` inside `metadata/` folder for every project
- [x] Implement robust service logic in `ProjectService`
- [x] Separate Move operations (`move.py`) from synchronization scripts
- [x] Enforce reserved names and character restrictions in folder/project names
- [x] Implement soft delete moving folders to `.porto/trash/` and hard delete operations
- [x] Handle slug-uniqueness constraints across all categories globally
- [x] Expand unit and CLI integration tests in `tests/test_project.py`

### Validation
- [x] All 99/99 unit and integration tests pass successfully (overall 95% coverage)
- [x] Python `-X utf8` flag and terminal encoding fallback support Windows terminals
- [x] Ruff and strict MyPy static analysis succeed without warning or error
- [x] Black formatting verified
