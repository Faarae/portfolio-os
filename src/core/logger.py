"""Logger module for Portfolio OS.

Provides centralized logging using Rich for beautiful console output.
Ensures logger instances are cached and reuse a single Console instance.
"""

from rich.console import Console

# Global console instance to avoid duplication
_console: Console = Console()

# Cache of logger instances
_loggers: dict[str, "Logger"] = {}


class Logger:
    """Rich-based logger for Portfolio OS.

    Provides colored, formatted console output with Rich.
    Reuses the global Console instance.
    """

    def __init__(self, name: str) -> None:
        """Initialize logger.

        Args:
            name: Logger name (typically __name__).
        """
        self.name: str = name
        self.console: Console = _console

    def info(self, message: str) -> None:
        """Log info message.

        Args:
            message: Message to log.
        """
        try:
            self.console.print(f"[blue]ℹ[/blue] {message}")
        except UnicodeEncodeError:
            safe_msg = message.encode("ascii", errors="replace").decode("ascii")
            self.console.print(f"[blue](i)[/blue] {safe_msg}")

    def success(self, message: str) -> None:
        """Log success message.

        Args:
            message: Message to log.
        """
        try:
            self.console.print(f"[green]✓[/green] {message}")
        except UnicodeEncodeError:
            safe_msg = message.encode("ascii", errors="replace").decode("ascii")
            self.console.print(f"[green](v)[/green] {safe_msg}")

    def warning(self, message: str) -> None:
        """Log warning message.

        Args:
            message: Message to log.
        """
        try:
            self.console.print(f"[yellow]⚠[/yellow] {message}")
        except UnicodeEncodeError:
            safe_msg = message.encode("ascii", errors="replace").decode("ascii")
            self.console.print(f"[yellow](!)[/yellow] {safe_msg}")

    def error(self, message: str) -> None:
        """Log error message.

        Args:
            message: Message to log.
        """
        try:
            self.console.print(f"[red]✗[/red] {message}")
        except UnicodeEncodeError:
            safe_msg = message.encode("ascii", errors="replace").decode("ascii")
            self.console.print(f"[red](x)[/red] {safe_msg}")

    def debug(self, message: str) -> None:
        """Log debug message.

        Args:
            message: Message to log.
        """
        self.console.print(f"[dim]{message}[/dim]")


def get_logger(name: str) -> Logger:
    """Get or create cached logger instance.

    Ensures that each logger name has only one initialized Logger instance.

    Args:
        name: Logger name (typically __name__).

    Returns:
        Logger instance.
    """
    if name not in _loggers:
        _loggers[name] = Logger(name)
    return _loggers[name]


def setup_logger() -> None:
    """Initialize logging system.

    Call once at application startup.
    """
    # Console and logging registry is initialized at import
    pass
