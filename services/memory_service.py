"""
Memory Service.

Defines the business operations for assistant memory management.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from enums.memory_category import MemoryCategory
from models.memory_record import MemoryRecord


class MemoryService(ABC):
    """
    Contract for assistant memory operations.
    """

    @abstractmethod
    def remember(self, memory: MemoryRecord) -> bool:
        """
        Store or update a memory.
        """
        raise NotImplementedError

    @abstractmethod
    def recall(
        self,
        category: MemoryCategory,
        key: str,
    ) -> MemoryRecord | None:
        """
        Retrieve a specific memory.

        Returns:
            The matching memory if found; otherwise None.
        """
        raise NotImplementedError

    @abstractmethod
    def forget(
        self,
        category: MemoryCategory,
        key: str,
    ) -> bool:
        """
        Remove a specific memory.
        """
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[MemoryRecord]:
        """Return all stored memories."""
        raise NotImplementedError
