"""
Application Service.

Defines the business operations for application management.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class ApplicationService(ABC):
    """
    Contract for application-related operations.
    """

    @abstractmethod
    def open(self, application: str) -> bool:
        """
        Open an application.
        """
        raise NotImplementedError

    @abstractmethod
    def close(self, application: str) -> bool:
        """
        Close an application.
        """
        raise NotImplementedError