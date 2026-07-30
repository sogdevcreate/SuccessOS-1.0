"""
News handler.
"""

from __future__ import annotations

from enums.operation_type import OperationType
from interfaces.handler import Handler
from models.action import Action
from models.execution_result import ExecutionResult
from services.news_service import NewsService


class NewsHandler(Handler):
    """
    Handles news-related actions.
    """

    def __init__(
        self,
        news_service: NewsService,
    ) -> None:
        self._news_service = news_service

    def execute(self, action: Action) -> ExecutionResult:
        """
        Execute a news action.
        """

        match action.operation:

            case OperationType.SEARCH:
                query = action.parameters.get("query")

                if not query:
                    return ExecutionResult.fail(
                        "Missing required parameter: 'query'."
                    )

                articles = self._news_service.search(query)

                return ExecutionResult.ok(
                    message="News retrieved successfully.",
                    payload=articles,
                )

            case _:
                return ExecutionResult.fail(
                    f"Unsupported operation: {action.operation.value}"
                )