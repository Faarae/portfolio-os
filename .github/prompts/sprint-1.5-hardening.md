# Sprint 1.5 — Foundation Hardening

## Context

Portfolio OS has completed Phase 1 (Core Architecture).

Before implementing any new features, the project foundation must be hardened to production quality.

This sprint focuses ONLY on engineering quality, maintainability, tooling, testing, and developer experience.

No new portfolio features should be introduced.

---

# Objective

Improve the project's engineering foundation without changing the application behavior.

The CLI should continue to work exactly as before.

No business logic should be added.

No portfolio generation should be implemented.

No MySQL implementation should be added.

No website builder should be implemented.

---

# Existing Architecture

The project already follows:

CLI

↓

Commands

↓

Services

↓

Core

↓

Models

↓

Utils

↓

Database (future)

Maintain this architecture.

Do not refactor the architecture unless required to improve quality.

---

# Tasks

## 1. Python Project Configuration

Create or improve:

- pyproject.toml

Configure:

- Black
- Ruff
- MyPy
- Pytest

Use modern Python standards.

Avoid deprecated configuration.

Do not duplicate configuration across multiple files.

---

## 2. Dependency Management

Move project dependencies to pyproject.toml whenever appropriate.

Developer tools should be grouped separately.

If requirements files are still required, explain why.

---

## 3. Custom Exception Hierarchy

Create a dedicated exception hierarchy.

Minimum:

PortfolioOSError

ConfigurationError

FilesystemError

ValidationError

DatabaseError

TemplateError

ProjectError

Each exception must have a clear responsibility.

Never raise generic Exception unless absolutely necessary.

---

## 4. Constants

Remove magic strings.

Create a centralized constants package.

Organize constants into logical modules instead of a single large file.

Suggested structure:

src/constants/

app.py

filesystem.py

config.py

project.py

Export everything through __init__.py.

---

## 5. Environment Configuration

Prepare the project for future MySQL integration.

Implement environment variable support using python-dotenv.

Configuration priority:

Environment Variables

↓

config.json

↓

Default Values

Do not hardcode sensitive information.

---

## 6. Logging

Improve logger.

Use Rich.

Expose methods:

info()

success()

warning()

error()

debug()

Logger should be initialized only once.

Avoid duplicated Console instances.

---

## 7. Testing

Improve test suite.

Use pytest.

Install pytest-cov.

Target at least 90% coverage for implemented modules.

Create missing unit tests for:

Config

Logger

Filesystem

Constants

Exceptions

---

## 8. Static Analysis

Configure:

Black

Ruff

MyPy

Ensure the repository passes:

black --check

ruff check

mypy src

without errors.

---

## 9. Git Hooks

Configure pre-commit.

Include:

black

ruff

mypy

trailing-whitespace

end-of-file-fixer

check-json

check-yaml

check-added-large-files

The repository should automatically validate code before commit.

---

## 10. Continuous Integration

Create GitHub Actions workflow.

Workflow should:

Install Python

Install dependencies

Run Black

Run Ruff

Run MyPy

Run Pytest

Fail on any error.

---

## 11. Scripts

Provide cross-platform developer scripts.

Windows:

run.ps1

Linux/macOS:

bootstrap.sh

The scripts should simplify:

install

format

lint

test

run

---

## 12. Documentation

Create:

CHANGELOG.md

CONTRIBUTING.md

docs/adr/

Inside ADR create:

0001-clean-architecture.md

0002-typer.md

0003-rich.md

0004-project-structure.md

Each ADR should briefly explain why the decision was made.

---

# Constraints

Do NOT implement:

Project creation

Project generator

Template engine

MySQL implementation

Website builder

AI

Dashboard

Analytics

Export

Resume generation

Portfolio generation

These belong to future phases.

---

# Code Quality Requirements

Every function must have:

- type hints
- Google-style docstring

Every public class must have:

- docstring

Avoid duplicated code.

Follow:

- Clean Architecture
- SOLID
- DRY
- KISS

Use pathlib.

Never use print().

Never hardcode paths.

Never hardcode encodings.

---

# Review Checklist

Before considering Sprint 1.5 complete, verify:

- All tests pass.
- CLI behavior is unchanged.
- No architecture violations exist.
- No duplicated logic exists.
- No TODO comments remain.
- Ruff passes.
- Black passes.
- MyPy passes.
- Coverage target is achieved.
- GitHub Actions succeeds.
- Pre-commit hooks work.

---

# Deliverables

When finished:

1. Explain every file that was created.
2. Explain every file that was modified.
3. Explain every architectural decision.
4. Explain why each change improves maintainability.
5. Update TASKS.md.
6. Update CHANGELOG.md.
7. Produce a summary table containing:

| Category | Status |
|----------|--------|
| Formatting | ✅ |
| Linting | ✅ |
| Typing | ✅ |
| Testing | ✅ |
| Logging | ✅ |
| Exceptions | ✅ |
| Constants | ✅ |
| CI/CD | ✅ |
| Documentation | ✅ |

Do not mark Sprint 1.5 as completed until every checklist item has been verified.