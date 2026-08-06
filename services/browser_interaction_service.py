"""
Browser Interaction Service.

Defines the contract for browser interaction.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class BrowserInteractionService(ABC):
    """
    Contract for browser interaction.
    """

    @abstractmethod
    def click(
        self,
        selector: str,
    ) -> None:
        """
        Click an element.
        """
        ...

    @abstractmethod
    def type(
        self,
        selector: str,
        text: str,
    ) -> None:
        """
        Type text into an element.
        """
        ...

    @abstractmethod
    def press(
        self,
        key: str,
    ) -> None:
        """
        Press a keyboard key.
        """
        ...

    @abstractmethod
    def wait_for(
        self,
        selector: str,
        timeout: int = 10,
    ) -> None:
        """
        Wait for an element.
        """
        ...

    @abstractmethod
    def scroll(
        self,
        pixels: int,
    ) -> None:
        """
        Scroll the current page.
        """
        ...

    @abstractmethod
    def select(
        self,
        selector: str,
        value: str,
    ) -> None:
        """
        Select an option from a dropdown.
        """
        ...

    @abstractmethod
    def upload_file(
        self,
        selector: str,
        path: str,
    ) -> None:
        """
        Upload a file.
        """
        ...

    @abstractmethod
    def screenshot(
        self,
        path: str,
    ) -> None:
        """
        Save a screenshot.
        """
        ...