"""
Clipboard Service.

Abstract clipboard operations.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class ClipboardService(ABC):
    """
    Defines clipboard operations.
    """

    @abstractmethod
    def get_text(self) -> str:
        """
        Returns the current clipboard text.
        """
        raise NotImplementedError

    @abstractmethod
    def set_text(
        self,
        text: str,
    ) -> None:
        """
        Sets clipboard text.
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """
        Clears the clipboard.
        """
        raise NotImplementedError