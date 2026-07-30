"""
Requests HTTP Client.

Implementation of the HttpClient contract using the requests library.
"""

from __future__ import annotations

import time
from typing import Any

import requests

from services.http_client import HttpClient


class RequestsHttpClient(HttpClient):
    """
    HTTP client implementation using requests.
    """

    def __init__(self) -> None:
        self._session = requests.Session()

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

        response = self._request(
            method="GET",
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
        )

        return response.json()

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

        response = self._request(
            method="POST",
            url=url,
            json=json,
            headers=headers,
            timeout=timeout,
        )

        return response.json()

    def _request(
        self,
        *,
        method: str,
        url: str,
        timeout: int,
        **kwargs: Any,
    ) -> requests.Response:
        """
        Execute an HTTP request with retry support.
        """

        retries = 3
        delay = 1.0

        for attempt in range(retries):

            try:
                response = self._session.request(
                    method=method,
                    url=url,
                    timeout=timeout,
                    **kwargs,
                )

                response.raise_for_status()

                return response

            except requests.HTTPError as ex:
                message = ex.response.text if ex.response is not None else ""
                raise RuntimeError(
                    f"HTTP {ex.response.status_code if ex.response else ''} request failed."
                    + (f"\n\n{message}" if message else "")
                ) from ex

            except (
                requests.ConnectionError,
                requests.Timeout,
            ) as ex:

                if attempt < retries - 1:
                    time.sleep(delay)
                    delay *= 2
                    continue

                raise RuntimeError(
                    "Unable to connect to the AI service. "
                    "Please check your internet connection and try again."
                ) from ex

            except requests.RequestException as ex:
                raise RuntimeError(
                    "An unexpected network error occurred while contacting the AI service."
                ) from ex