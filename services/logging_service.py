"""
Logging Service contract.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from enums.log_level import LogLevel


class LoggingService(ABC):
    """
    Contract for application logging.
    """

    @abstractmethod
    def log(
        self,
        level: LogLevel,
        message: str,
    ) -> None:
        """
        Write a log entry.
        """
        raise NotImplementedError

    def debug(
        self,
        message: str,
    ) -> None:
        self.log(
            LogLevel.DEBUG,
            message,
        )

    def info(
        self,
        message: str,
    ) -> None:
        self.log(
            LogLevel.INFO,
            message,
        )

    def warning(
        self,
        message: str,
    ) -> None:
        self.log(
            LogLevel.WARNING,
            message,
        )

    def error(
        self,
        message: str,
    ) -> None:
        self.log(
            LogLevel.ERROR,
            message,
        )

    def critical(
        self,
        message: str,
    ) -> None:
        self.log(
            LogLevel.CRITICAL,
            message,
        )