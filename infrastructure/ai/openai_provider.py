"""
OpenAI Provider.

Implementation of the AIProvider contract using the OpenAI REST API.
"""

from __future__ import annotations

from time import perf_counter

from models.ai_request import AIRequest
from models.ai_response import AIResponse

from services.ai_provider import AIProvider
from services.http_client import HttpClient
from services.logging_service import LoggingService


class OpenAIProvider(AIProvider):
    """
    OpenAI implementation of the AIProvider contract.
    """

    def __init__(
        self,
        http_client: HttpClient,
        logger: LoggingService,
        api_key: str,
        model: str,
    ) -> None:
        self._http_client = http_client
        self._logger = logger
        self._api_key = api_key
        self._model = model

    def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:
        """
        Generate a response using the OpenAI Chat Completions API.
        """

        self._logger.info(
            f"Sending AI request using model '{self._model}'."
        )

        start = perf_counter()

        try:
            response = self._http_client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self._model,
                    "messages": [
                        {
                            "role": "system",
                            "content": request.system_prompt,
                        },
                        {
                            "role": "user",
                            "content": request.prompt,
                        },
                    ],
                    "temperature": request.temperature,
                    "max_tokens": request.max_tokens,
                },
            )

            elapsed = perf_counter() - start

            choice = response["choices"][0]

            self._logger.info(
                f"AI response received in {elapsed:.2f}s."
            )

            return AIResponse(
                content=choice["message"]["content"],
                provider="OpenAI",
                model=response["model"],
                finish_reason=choice.get(
                    "finish_reason",
                    "",
                ),
                usage=response.get(
                    "usage",
                    {},
                ),
                metadata={
                    "duration_seconds": elapsed,
                },
            )

        except Exception as ex:
            elapsed = perf_counter() - start

            self._logger.error(
                f"AI request failed after {elapsed:.2f}s: {ex}"
            )

            raise