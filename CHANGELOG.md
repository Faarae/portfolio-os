# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-06-23

### Added
- Project management CLI subcommands (`porto new`, `porto delete`, `porto rename`, and `porto move`).
- `ProjectCategory` as a `StrEnum` instead of a list of constants, supporting `academic`, `competition`, `freelance`, `organization`, `personal`, and `research`.
- Default project structure layout inside `templates/` with README template and custom `project.json` schema.
- Global slug-uniqueness validation checking for duplication across all categories before creation or move.
- Safe folder and project name validation blocking illegal characters (`\/:*?"<>|`) and reserved system names.
- Soft delete operations transferring project folders to `.porto/trash/{category}/{slug}_{timestamp}/`, alongside a `--hard` option for permanent deletion.
- Extensive unit and integration test suite in `tests/test_project.py` covering all CLI and Service interfaces.

### Changed
- Configured Pydantic `Project` metadata model to place `project.json` inside the project's `metadata/` folder instead of the root.
- Separated `move.py` command handling from synchronization logic.
- Configured Ruff parser options in `pyproject.toml` to support Typer default CLI parameters without lint warnings.
- Expanded project code coverage target to 95% overall, including 100% on the core project service, CLI commands, and filesystem interfaces.

## [1.5.0] - 2026-06-23

### Added
- Centralized constants package under `src/constants/` partitioned into `app`, `config`, `filesystem`, and `project` modules.
- Custom exception hierarchy in `src/core/exceptions.py` with `PortfolioOSError` as root error.
- Integration of `python-dotenv` for loading configuration overrides from environment variables.
- Project-level static analysis configuration in `pyproject.toml` for Black, Ruff, MyPy, and Pytest.
- Dev dependency management using `requirements-dev.txt`.
- Pre-commit hook configurations (`.pre-commit-config.yaml`) for Git automation.
- Task runner scripts: `Makefile` for Unix systems and `run.ps1` for Windows.
- GitHub Actions CI workflow (`.github/workflows/ci.yml`) to validate formatting, linting, type safety, and test suites on push/pull requests.
- Architecture Decision Records (ADRs) documenting Clean Architecture, Typer, Rich, and Project Structure.
- Comprehensive test coverage expansions for constants, custom exceptions, InitService, utilities, and main.py entry points.

### Changed
- Refactored `src/main.py` to utilize app constants and custom exceptions.
- Refactored `src/core/config.py` to prioritize environment variables, raise custom exceptions, and fallback to default constants.
- Refactored `src/core/filesystem.py` to raise `PathNotFoundError` and use encoding constants.
- Refactored `src/core/logger.py` to cache logger instances and reuse a single Console instance.
- Refactored `src/services/init.py` to raise custom exceptions and eliminate magic strings.
- Upgraded `requirements.txt` to UTF-8 encoding.
- Expanded existing unit test suite in `tests/test_core.py`.
