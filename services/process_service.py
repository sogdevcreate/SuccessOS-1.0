"""
Process Service.

Defines the contract for process management.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class ProcessService(ABC):
    """
    Contract for process management.
    """

    @abstractmethod
    def list_processes(self) -> list[dict]:
        """
        Return information about all running processes.
        """
        ...

    @abstractmethod
    def start_process(
        self,
        command: str,
    ) -> None:
        """
        Start a new process.
        """
        ...

    @abstractmethod
    def kill_process(
        self,
        process: str,
    ) -> None:
        """
        Terminate a running process.
        """
        ...

    @abstractmethod
    def process_info(
        self,
        process: str,
    ) -> dict:
        """
        Return information about a running process.
        """
        ...