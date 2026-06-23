"""CLI Bootstrap for Portfolio OS.

Main entry point for the command-line application using Typer.
"""

import sys
from typing import Optional

import typer

from .commands import (
    DeleteCommand,
    InitCommand,
    MoveCommand,
    NewCommand,
    RenameCommand,
)
from .constants import APP_HELP, APP_NAME, VERSION_STRING
from .core import get_logger, setup_logger
from .core.exceptions import PortfolioOSError

# Setup logger
setup_logger()
logger = get_logger(__name__)

# Create Typer app
app = typer.Typer(
    name=APP_NAME,
    help=APP_HELP,
    no_args_is_help=True,
)


@app.command()
def init(directory: str = typer.Argument(".", help="Directory to initialize")) -> None:
    """Initialize a new portfolio project.

    Creates the necessary project structure and configuration files
    in the specified directory.

    Args:
        directory: Directory to initialize (default: current directory).
    """
    try:
        cmd = InitCommand()
        cmd.execute(directory)
        try:
            typer.echo(
                typer.style(
                    "✓ Portfolio initialized successfully!",
                    fg=typer.colors.GREEN,
                )
            )
        except UnicodeEncodeError:
            typer.echo(
                typer.style(
                    "[v] Portfolio initialized successfully!",
                    fg=typer.colors.GREEN,
                )
            )
    except PortfolioOSError as e:
        logger.error(f"Initialization failed: {e}")
        typer.echo(
            typer.style(f"✗ Error: {e}", fg=typer.colors.RED),
            err=True,
        )
        raise typer.Exit(code=1) from None
    except Exception as e:
        logger.error(f"Unexpected CLI error: {e}")
        typer.echo(
            typer.style(f"✗ Unexpected Error: {e}", fg=typer.colors.RED),
            err=True,
        )
        raise typer.Exit(code=1) from None


@app.command()
def new(
    name: str = typer.Argument(..., help="The project name"),
    category: str = typer.Argument(..., help="Project category"),
    title: Optional[str] = typer.Option(
        None, "--title", "-t", help="Optional project display title"
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", help="Overwrite existing files"
    ),
) -> None:
    """Create a new portfolio project."""
    try:
        cmd = NewCommand()
        cmd.execute(name, category, title, overwrite)
        try:
            typer.echo(
                typer.style("✓ Project created successfully!", fg=typer.colors.GREEN)
            )
        except UnicodeEncodeError:
            typer.echo(
                typer.style("[v] Project created successfully!", fg=typer.colors.GREEN)
            )
    except PortfolioOSError as e:
        logger.error(f"Creation failed: {e}")
        typer.echo(
            typer.style(f"✗ Error: {e}", fg=typer.colors.RED),
            err=True,
        )
        raise typer.Exit(code=1) from None
    except Exception as e:
        logger.error(f"Unexpected CLI error: {e}")
        typer.echo(
            typer.style(f"✗ Unexpected Error: {e}", fg=typer.colors.RED),
            err=True,
        )
        raise typer.Exit(code=1) from None


@app.command()
def delete(
    name: str = typer.Argument(..., help="The project name or slug"),
    category: str = typer.Argument(..., help="Project category"),
    hard: bool = typer.Option(
        False, "--hard", help="Permanently delete project folder"
    ),
) -> None:
    """Delete a portfolio project (soft delete by default)."""
    try:
        cmd = DeleteCommand()
        cmd.execute(name, category, hard)
        try:
            typer.echo(
                typer.style("✓ Project deleted successfully!", fg=typer.colors.GREEN)
            )
        except UnicodeEncodeError:
            typer.echo(
                typer.style("[v] Project deleted successfully!", fg=typer.colors.GREEN)
            )
    except PortfolioOSError as e:
        logger.error(f"Deletion failed: {e}")
        typer.echo(
            typer.style(f"✗ Error: {e}", fg=typer.colors.RED),
            err=True,
        )
        raise typer.Exit(code=1) from None
    except Exception as e:
        logger.error(f"Unexpected CLI error: {e}")
        typer.echo(
            typer.style(f"✗ Unexpected Error: {e}", fg=typer.colors.RED),
            err=True,
        )
        raise typer.Exit(code=1) from None


@app.command()
def rename(
    name: str = typer.Argument(..., help="Current project name or slug"),
    category: str = typer.Argument(..., help="Project category"),
    new_name: str = typer.Argument(..., help="New project name"),
) -> None:
    """Rename a portfolio project."""
    try:
        cmd = RenameCommand()
        cmd.execute(name, category, new_name)
        try:
            typer.echo(
                typer.style("✓ Project renamed successfully!", fg=typer.colors.GREEN)
            )
        except UnicodeEncodeError:
            typer.echo(
                typer.style("[v] Project renamed successfully!", fg=typer.colors.GREEN)
            )
    except PortfolioOSError as e:
        logger.error(f"Rename failed: {e}")
        typer.echo(
            typer.style(f"✗ Error: {e}", fg=typer.colors.RED),
            err=True,
        )
        raise typer.Exit(code=1) from None
    except Exception as e:
        logger.error(f"Unexpected CLI error: {e}")
        typer.echo(
            typer.style(f"✗ Unexpected Error: {e}", fg=typer.colors.RED),
            err=True,
        )
        raise typer.Exit(code=1) from None


@app.command()
def move(
    name: str = typer.Argument(..., help="Project name or slug to move"),
    source_category: str = typer.Argument(..., help="Source category"),
    dest_category: str = typer.Argument(..., help="Destination category"),
) -> None:
    """Move a project between categories."""
    try:
        cmd = MoveCommand()
        cmd.execute(name, source_category, dest_category)
        try:
            typer.echo(
                typer.style("✓ Project moved successfully!", fg=typer.colors.GREEN)
            )
        except UnicodeEncodeError:
            typer.echo(
                typer.style("[v] Project moved successfully!", fg=typer.colors.GREEN)
            )
    except PortfolioOSError as e:
        logger.error(f"Move failed: {e}")
        typer.echo(
            typer.style(f"✗ Error: {e}", fg=typer.colors.RED),
            err=True,
        )
        raise typer.Exit(code=1) from None
    except Exception as e:
        logger.error(f"Unexpected CLI error: {e}")
        typer.echo(
            typer.style(f"✗ Unexpected Error: {e}", fg=typer.colors.RED),
            err=True,
        )
        raise typer.Exit(code=1) from None


@app.command()
def version() -> None:
    """Display version information."""
    typer.echo(VERSION_STRING)


def main() -> None:
    """Main entry point for CLI."""
    try:
        app()
    except Exception as e:
        logger.error(f"CLI error: {e}")
        typer.echo(
            typer.style(f"✗ CLI Error: {e}", fg=typer.colors.RED),
            err=True,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
