"""
Browser Tab Service.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BrowserTabService(ABC):
    """
    Contract for browser tab management.
    """

    @abstractmethod
    def list_tabs(self) -> list[str]:
        """
        Return all open browser tabs.
        """
        raise NotImplementedError

    @abstractmethod
    def current_tab(self) -> int:
        """
        Return the current tab index.
        """
        raise NotImplementedError

    @abstractmethod
    def switch_tab(
        self,
        index: int,
    ) -> None:
        """
        Switch to the specified tab.
        """
        raise NotImplementedError

    @abstractmethod
    def close_tab(
        self,
        index: int,
    ) -> None:
        """
        Close the specified tab.
        """
        raise NotImplementedError

    @abstractmethod
    def page_title(self) -> str:
        """
        Return the current page title.
        """
        raise NotImplementedError