from __future__ import annotations

from enums.operation_type import OperationType
from infrastructure.ai.browser_intent_classifier import BrowserIntentClassifier
from tests.helpers.reporting import ComponentTestCase


class BrowserIntentRegressionTests(ComponentTestCase):
    subsystem = "Planner"
    component = "BrowserIntentClassifier"
    recommended_location = "infrastructure/ai/browser_intent_classifier.py"

    def test_type_text_containing_open_is_not_navigation(self) -> None:
        plan = BrowserIntentClassifier().create_plan("Type OpenAI into Search")

        self.assertEqual(plan.actions[0].operation, OperationType.TYPE)
        self.assertEqual(plan.actions[0].parameters["text"], "OpenAI")
