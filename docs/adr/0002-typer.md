# ADR 0002: Typer for CLI Framework

## Context
Portfolio OS is primarily a command-line interface tool. We need a modern, maintainable framework to define, parse, and invoke CLI commands without boilerplate code.

## Decision
We choose **Typer** (built on top of Click) as our primary CLI library.

## Rationale
*   **Type Safety**: Typer leverages standard Python type hints to generate command parameters, validation, and help text automatically.
*   **Developer Productivity**: Commands can be written as standard Python functions, eliminating heavy parser definitions common in libraries like `argparse`.
*   **Rich Integration**: Typer works natively with Rich for formatting command helper output and error logs.
*   **Maintainability**: Type declarations serve as single source of truth for options, flags, and arguments.

## Consequences
*   CLI code is highly declarative.
*   Commands are easily registered via Python decorators.
*   CLI arguments/options are strictly type-validated at the shell boundary.
