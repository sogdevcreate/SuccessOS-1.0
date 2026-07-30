"""
Python logging service implementation.
"""

from __future__ import annotations

import logging
from pathlib import Path

from enums.log_level import LogLevel
from services.logging_service import LoggingService


class PythonLoggingService(LoggingService):
    """
    Logging service backed by Python's standard logging module.
    """

    def __init__(
        self,
        log_file: str = "logs/successos.log",
    ) -> None:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        self._logger = logging.getLogger("SuccessOS")

        # Prevent duplicate handlers if the service is created more than once.
        if self._logger.handlers:
            return

        self._logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        file_handler = logging.FileHandler(
            log_path,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)

    def log(
        self,
        level: LogLevel,
        message: str,
    ) -> None:
        """
        Write a log entry.
        """

        mapping = {
            LogLevel.DEBUG: logging.DEBUG,
            LogLevel.INFO: logging.INFO,
            LogLevel.WARNING: logging.WARNING,
            LogLevel.ERROR: logging.ERROR,
            LogLevel.CRITICAL: logging.CRITICAL,
        }

        self._logger.log(
            mapping[level],
            message,
        )

    def debug(self, message: str) -> None:
        self._logger.debug(message)

    def info(self, message: str) -> None:
        self._logger.info(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def critical(self, message: str) -> None:
        self._logger.critical(message)

    def exception(self, message: str) -> None:
        self._logger.exception(message)