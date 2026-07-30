"""
Web News Service.

Implementation of the NewsService contract using an HTTP client.
"""

from __future__ import annotations

from services.http_client import HttpClient
from services.logging_service import LoggingService
from services.news_service import NewsService


class WebNewsService(NewsService):
    """
    Retrieves news articles from a web provider.
    """

    def __init__(
        self,
        http_client: HttpClient,
        logger: LoggingService,
        api_key: str,
    ) -> None:
        self._http_client = http_client
        self._logger = logger
        self._api_key = api_key

    def search(self, query: str) -> list[dict]:
        """
        Search for news articles.
        """

        self._logger.info(
            f"Searching news for '{query}'."
        )

        try:
            response = self._http_client.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": query,
                    "apiKey": self._api_key,
                    "pageSize": 10,
                    "sortBy": "publishedAt",
                },
            )

            articles = response.get("articles", [])

            self._logger.info(
                f"Retrieved {len(articles)} news articles."
            )

            return articles

        except Exception as ex:
            self._logger.error(
                f"News search failed for '{query}': {ex}"
            )

            return []