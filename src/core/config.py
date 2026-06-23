"""Configuration loader for Portfolio OS.

Manages application configuration from environment variables, config.json,
and default fallback values.
"""

import json
import os
from pathlib import Path
from typing import Any

import dotenv

from ..constants import (
    DEFAULT_ENCODING,
    DEFAULT_OWNER,
    DEFAULT_PORTFOLIO_NAME,
    DEFAULT_PORTFOLIO_VERSION,
    DIR_CONFIG,
    ENV_PREFIX,
    FILE_CONFIG,
)
from .exceptions import (
    ConfigFileNotFoundError,
    ConfigFormatError,
    ConfigurationError,
)

# Load environment variables from .env file if present
dotenv.load_dotenv()


class Config:
    """Configuration manager for Portfolio OS.

    Resolves configuration values based on the following priority:
    1. Environment Variables (prefixed with PORTO_)
    2. Configuration File (config.json)
    3. Default Fallback Values
    """

    def __init__(self, config_path: Path | None = None) -> None:
        """Initialize config loader.

        Args:
            config_path: Path to config.json. Defaults to config/config.json.

        Raises:
            ConfigFileNotFoundError: If config file does not exist.
            ConfigFormatError: If config file contains invalid JSON.
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / DIR_CONFIG / FILE_CONFIG

        if not config_path.exists():
            raise ConfigFileNotFoundError(f"Config file not found: {config_path}")

        self.config_path: Path = config_path
        self._data: dict[str, Any] = self._load_config()

    def _load_config(self) -> dict[str, Any]:
        """Load configuration from file.

        Returns:
            Configuration dictionary.

        Raises:
            ConfigFormatError: If file is not valid JSON.
        """
        try:
            with open(self.config_path, encoding=DEFAULT_ENCODING) as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    raise ConfigFormatError("Config file content must be a JSON object")
                return data
        except json.JSONDecodeError as e:
            raise ConfigFormatError(f"Invalid JSON in config file: {e}") from e

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with priority resolution.

        Priority order: Environment variable (PORTO_KEY) -> config.json -> default.

        Args:
            key: Configuration key.
            default: Default value if key is not found in env or config file.

        Returns:
            Resolved configuration value.
        """
        # 1. Environment Variable Priority (e.g., PORTO_OWNER)
        env_key = f"{ENV_PREFIX}{key.upper()}"
        env_value = os.getenv(env_key)
        if env_value is not None:
            return env_value

        # 2. Config File Priority
        if key in self._data:
            return self._data[key]

        # 3. Default fallback
        return default

    def get_owner(self) -> str:
        """Get portfolio owner.

        Returns:
            Owner name from config.

        Raises:
            ConfigurationError: If owner is empty or not configured.
        """
        owner = self.get("owner", DEFAULT_OWNER)
        if not owner:
            raise ConfigurationError("'owner' not configured in configuration")
        return str(owner)

    def get_portfolio_name(self) -> str:
        """Get portfolio name.

        Returns:
            Portfolio name from config.

        Raises:
            ConfigurationError: If portfolio_name is empty or not configured.
        """
        name = self.get("portfolio_name", DEFAULT_PORTFOLIO_NAME)
        if not name:
            raise ConfigurationError("'portfolio_name' not configured in configuration")
        return str(name)

    def get_version(self) -> str:
        """Get portfolio version.

        Returns:
            Version from config.
        """
        return str(self.get("version", DEFAULT_PORTFOLIO_VERSION))

    def to_dict(self) -> dict[str, Any]:
        """Export current resolved configuration as dictionary.

        Returns:
            Configuration dictionary.
        """
        # Resolve all active keys in the config file merged with env overrides
        resolved = {}
        for key in self._data:
            resolved[key] = self.get(key)
        # Ensure owner and portfolio_name are present (with defaults if missing)
        resolved["owner"] = self.get_owner()
        resolved["portfolio_name"] = self.get_portfolio_name()
        resolved["version"] = self.get_version()
        return resolved
