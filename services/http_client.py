"""
HTTP Client.

Reusable HTTP client for infrastructure services.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class HttpClient(ABC):
    """
    Contract for making HTTP requests.
    """

    @abstractmethod
    def get(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: int = 30,
    ) -> dict[str, Any]:
        """
        Perform an HTTP GET request.
        """
        raise NotImplementedError

    @abstractmethod
    def post(
        self,
        url: str,
        *,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: int = 30,
    ) -> dict[str, Any]:
        """
        Perform an HTTP POST request.
        """
        raise NotImplementedError