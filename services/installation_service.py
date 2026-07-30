"""
Installation Service.

Defines the business operations for software installation management.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class InstallationService(ABC):
    """
    Contract for software installation operations.
    """

    @abstractmethod
    def install(self, application: str) -> bool:
        """
        Install an application.
        """
        raise NotImplementedError

    @abstractmethod
    def uninstall(self, application: str) -> bool:
        """
        Uninstall an application.
        """
        raise NotImplementedError