"""
System Service.

Defines the business operations for interacting with the operating system.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from models.system_status import SystemStatus


class SystemService(ABC):
    """
    Contract for system-related operations.
    """

    @abstractmethod
    def get_status(self) -> SystemStatus:
        """
        Retrieve the current system status.
        """
        raise NotImplementedError

    @abstractmethod
    def shutdown(self) -> bool:
        """
        Shut down the operating system.
        """
        raise NotImplementedError

    @abstractmethod
    def restart(self) -> bool:
        """
        Restart the operating system.
        """
        raise NotImplementedError

    @abstractmethod
    def sleep(self) -> bool:
        """
        Put the operating system into sleep mode.
        """
        raise NotImplementedError

    @abstractmethod
    def lock(self) -> bool:
        """
        Lock the current user session.
        """
        raise NotImplementedError