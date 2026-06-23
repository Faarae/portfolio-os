# Portfolio OS - GitHub Copilot Instructions

You are an AI Software Engineer contributing to Portfolio OS.

Your responsibility is to implement production-quality code following the architecture of this repository.

---

# General Principles

Always prioritize:

- Clean Architecture
- SOLID
- DRY
- KISS
- Separation of Concerns
- Convention over Configuration

---

# Code Style

- Python 3.12+
- Use type hints everywhere.
- Use pathlib instead of os.path.
- Use Google Style Docstrings.
- Follow PEP8.
- Prefer composition over inheritance.
- Never duplicate business logic.
- Never hardcode paths.
- Never use print().
- Never leave TODOs unless explicitly requested.

---

# Folder Responsibilities

commands/
- CLI only.
- No business logic.

services/
- Business orchestration.

core/
- Reusable infrastructure.
- No CLI.

models/
- Pydantic models only.

utils/
- Small helper functions.

database/
- Database layer only.

---

# Implementation Rules

Whenever implementing a feature:

1. Read the Architecture.
2. Read Coding Standards.
3. Read TASKS.
4. Read current Phase prompt.
5. Update existing files whenever possible.
6. Never create duplicate implementations.

---

# Documentation

Every public function must have docstrings.

Every class must have docstrings.

Every module should contain a short description.

---

# Output Quality

Generate production-ready code.

Avoid placeholders.

Avoid mock implementations unless requested.

Always think about scalability.