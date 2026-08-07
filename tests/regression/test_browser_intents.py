from __future__ import annotations

from enums.operation_type import OperationType
from infrastructure.ai.browser_intent_classifier import BrowserIntentClassifier
from enums.handler_type import HandlerType
from enums.operation_type import OperationType
from handlers.news_handler import NewsHandler
from models.action import Action
from tests.helpers.reporting import ComponentTestCase


class BrowserIntentRegressionTests(ComponentTestCase):
    subsystem = "Planner"
    component = "BrowserIntentClassifier"
    recommended_location = "infrastructure/ai/browser_intent_classifier.py"

    def test_type_text_containing_open_is_not_navigation(self) -> None:
        plan = BrowserIntentClassifier().create_plan("Type OpenAI into Search")

        self.assertEqual(plan.actions[0].operation, OperationType.TYPE)
        self.assertEqual(plan.actions[0].parameters["text"], "OpenAI")

    def test_news_handler_accepts_planner_query_parameter(self) -> None:
        class NewsService:
            def __init__(self):
                self.query = None

            def search(self, query):
                self.query = query
                return []

        service = NewsService()
        result = NewsHandler(service).execute(
            Action(
                "search",
                HandlerType.NEWS,
                OperationType.SEARCH,
                {"query": "AI"},
            )
        )

        self.assertTrue(result.successful)
        self.assertEqual(service.query, "AI")
