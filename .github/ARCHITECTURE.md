# Portfolio OS Architecture

## Layers

CLI

↓

Commands

↓

Services

↓

Core

↓

Repositories

↓

MySQL

---

## Data Flow

User

↓

CLI

↓

Command

↓

Service

↓

Core

↓

Database

↓

Filesystem

---

## Responsibilities

Commands

Receive user input.

Services

Business logic.

Core

Infrastructure.

Repositories

Database access.

Models

Data representation.

Utils

Helpers.

---

## Single Source of Truth

Metadata stored in project.json.

Database stores indexed information.

Website reads metadata.

AI reads metadata.

Export reads metadata.

No duplicated data.

---

## Future Modules

Website Builder

Dashboard

Analytics

AI Assistant

GitHub Sync