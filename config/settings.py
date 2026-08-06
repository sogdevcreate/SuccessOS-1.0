"""
Application settings.

Centralized configuration for SuccessOS.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


class Settings:
    """
    Loads and provides application configuration.
    """

    DEFAULTS: dict[str, Any] = {
        "database": {
            "path": "data/successos.db",
        },
        "memory": {
            "path": "data/memory.db",
        },
        "filesystem": {
            "allowed_roots": ["."],
        },
        "news": {
            "provider": "newsapi",
            "api_key": "",
            "page_size": 10,
        },
        "ai": {
            "provider": "openai",
            "model": "gpt-5",
            "api_key": "",
        },
        "logging": {
            "level": "INFO",
            "file": "logs/successos.log",
        },
    }

    def __init__(
        self,
        config_path: str = "config.json",
        env_path: str = ".env",
    ) -> None:
        self._config_path = Path(config_path)
        self._env_path = Path(env_path)
        self._settings = self.DEFAULTS.copy()

        self._load_env()
        self._load_config()
        self._load_environment()

    def _load_env(self) -> None:
        """
        Load a .env file into environment variables.
        """

        if not self._env_path.exists():
            return

        with self._env_path.open(
            "r",
            encoding="utf-8",
        ) as file:

            for line in file:

                line = line.strip()

                if (
                    not line
                    or line.startswith("#")
                    or "=" not in line
                ):
                    continue

                key, value = line.split("=", 1)

                os.environ.setdefault(
                    key.strip(),
                    value.strip(),
                )

    def _load_config(self) -> None:
        """
        Load config.json if present.
        """

        if not self._config_path.exists():
            return

        with self._config_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        self._merge(self._settings, data)

    def _load_environment(self) -> None:
        """
        Override configuration using environment variables.
        """

        mapping = {
            "OPENAI_API_KEY": ("ai", "api_key"),
            "OPENAI_MODEL": ("ai", "model"),
            "NEWS_API_KEY": ("news", "api_key"),
            "LOG_LEVEL": ("logging", "level"),
        }

        for env_name, path in mapping.items():

            value = os.getenv(env_name)

            if not value:
                continue

            target = self._settings

            for key in path[:-1]:
                target = target[key]

            target[path[-1]] = value

    def _merge(
        self,
        target: dict[str, Any],
        source: dict[str, Any],
    ) -> None:

        for key, value in source.items():

            if (
                key in target
                and isinstance(target[key], dict)
                and isinstance(value, dict)
            ):
                self._merge(target[key], value)
            else:
                target[key] = value

    def get(
        self,
        *keys: str,
        default: Any = None,
    ) -> Any:

        value: Any = self._settings

        for key in keys:

            if not isinstance(value, dict):
                return default

            value = value.get(key)

            if value is None:
                return default

        return value
