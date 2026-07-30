"""
News Service.

Defines the business operations for retrieving news.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class NewsService(ABC):
    """
    Contract for news operations.
    """

    @abstractmethod
    def search(self, query: str) -> list[dict]:
        """
        Search for news articles matching the query.
        """
        raise NotImplementedError