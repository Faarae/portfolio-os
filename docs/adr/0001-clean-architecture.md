# ADR 0001: Clean Architecture

## Context
Portfolio OS is a CLI tool intended to grow into a multi-interface platform (supporting a future Web app, SQLite/MySQL DB integrations, and AI generation features). To prevent logic leakage across interfaces and storage layers, we need a decoupled architectural approach.

## Decision
We adopt Clean Architecture principles. The application logic is divided into distinct, independent layers:
1.  **CLI/UI Layer**: Main bootstrap (`main.py`) which acts as the outer interface.
2.  **Commands Layer** (`src/commands/`): Pure orchestrators that handle input validation/parsing and delegate work.
3.  **Services Layer** (`src/services/`): Core business logic containing use cases (e.g. portfolio initialization, generation).
4.  **Core Infrastructure Layer** (`src/core/`): Lower-level technical details (filesystem actions, loggers, configuration loaders).
5.  **Models Layer** (`src/models/`): Pure data structures representing entities (like `Project`).

## Consequences
*   **Decoupling**: The business logic (Services) does not know how CLI inputs are structured or how database records are saved.
*   **Testability**: Each layer can be tested in isolation with mocks.
*   **Maintainability**: Changes in the CLI library (e.g., swapping Typer for another library) have zero impact on portfolio services.
