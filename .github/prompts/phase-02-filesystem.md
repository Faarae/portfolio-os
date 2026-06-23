# Phase 2 — Project & Filesystem Management

## Objective

Implement the Project Management foundation of Portfolio OS.

This phase focuses on managing project directories, metadata, templates, and project assets.

The goal is to provide a production-ready filesystem abstraction that will become the Single Source of Truth for future database indexing and website generation.

Do NOT implement MySQL.

Do NOT implement website generation.

Do NOT implement AI features.

Do NOT implement portfolio rendering.

---

# Existing Architecture

The architecture must remain:

CLI

↓

Commands

↓

Services

↓

Core

↓

Filesystem

↓

Storage

Business logic belongs only inside Services.

Filesystem must never contain business rules.

Commands only delegate requests.

---

# Portfolio Structure

Portfolio OS manages projects using the following structure:

projects/

├── academic/

├── competition/

├── freelance/

├── organization/

├── personal/

└── research/

Each project must follow this structure:

project-name/

├── assets/

│   ├── documents/

│   ├── images/

│   ├── screenshots/

│   ├── videos/

│   └── presentations/

│

├── source/

│

├── metadata/

│

├── project.json

└── README.md

The structure must be generated automatically.

---

# Features

## 1. Create Project

Implement project creation.

The system must:

- validate project name
- validate category
- prevent duplicate projects
- generate default folder structure
- create README.md
- create project.json
- generate empty asset folders

---

## 2. Delete Project

Support:

- soft delete
- hard delete

Filesystem executes deletion only.

Business rules belong in ProjectService.

---

## 3. Rename Project

Support renaming safely.

Prevent duplicate names.

Update metadata paths if necessary.

---

## 4. Move Project

Allow moving projects between categories.

Example:

academic/

↓

competition/

Maintain metadata integrity.

---

## 5. Copy Templates

Implement template copying.

Copy:

README template

project.json template

future assets

Support overwrite flag.

---

## 6. Safe Overwrite

Before overwriting:

- verify file exists
- verify overwrite permission
- preserve existing files when overwrite=False

Never overwrite silently.

---

## 7. Path Validation

Validate:

- illegal characters
- reserved names
- invalid nesting
- duplicate folders
- empty names

Raise custom exceptions.

---

## 8. Metadata Generation

Automatically generate:

README.md

project.json

with placeholder values only.

Do NOT generate portfolio content.

Do NOT generate website content.

---

# Project Metadata

Create an initial project.json template.

Example fields:

- id
- slug
- title
- subtitle
- description
- category
- status
- year
- technologies
- tags
- github
- website
- demo
- role
- featured
- created_at
- updated_at

Leave values empty when appropriate.

---

# Filesystem Responsibilities

Filesystem MAY:

- create directories
- delete directories
- rename directories
- move directories
- copy files
- copy templates
- read files
- write files
- validate paths

Filesystem MUST NOT:

- know business rules
- communicate with database
- communicate with CLI
- generate HTML
- generate websites
- generate portfolios
- manage users

---

# Service Responsibilities

ProjectService should:

- validate requests
- coordinate filesystem
- generate metadata
- call filesystem
- raise business exceptions

---

# Commands

Prepare support for:

porto new

porto delete

porto rename

porto move

porto validate

The CLI implementation may remain minimal.

Focus on Services and Filesystem.

---

# Exceptions

Use custom exceptions only.

Examples:

ProjectAlreadyExistsError

ProjectNotFoundError

InvalidProjectNameError

InvalidCategoryError

FilesystemError

ValidationError

Never raise generic Exception.

---

# Testing

Create comprehensive unit tests.

Minimum coverage:

- create project
- rename project
- delete project
- move project
- template copy
- overwrite protection
- metadata generation
- path validation

Coverage target:

90%+

---

# Constraints

Do NOT implement:

MySQL

Repository Pattern

SQLAlchemy

Alembic

Website Builder

Dashboard

Analytics

Search Engine

Portfolio Generator

AI

Resume Builder

Export Engine

These belong to future phases.

---

# Code Quality

Follow:

- Clean Architecture
- SOLID
- DRY
- KISS

Every function must include:

- type hints
- Google-style docstring

Use pathlib everywhere.

Never hardcode paths.

Never use print().

Use Rich logger.

Use constants package.

Use custom exceptions.

---

# Acceptance Criteria

Phase 2 is complete only if:

✔ Projects can be created.

✔ Projects can be renamed.

✔ Projects can be moved.

✔ Projects can be deleted.

✔ Templates are copied correctly.

✔ Metadata is generated.

✔ Path validation works.

✔ Tests pass.

✔ Ruff passes.

✔ Black passes.

✔ MyPy passes.

✔ CLI remains functional.

---

# Deliverables

When complete:

1. Explain every created file.

2. Explain every modified file.

3. Explain every architectural decision.

4. Explain how Services and Filesystem interact.

5. Update TASKS.md.

6. Update CHANGELOG.md.

7. Generate a summary table:

| Category | Status |
|----------|--------|
| Project Creation | ✅ |
| Rename | ✅ |
| Move | ✅ |
| Delete | ✅ |
| Templates | ✅ |
| Metadata | ✅ |
| Validation | ✅ |
| Testing | ✅ |
| Documentation | ✅ |

Do not mark Phase 2 complete until every acceptance criterion has been verified.