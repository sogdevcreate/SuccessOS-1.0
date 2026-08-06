from __future__ import annotations

import unittest

from enums.handler_type import HandlerType
from enums.operation_type import OperationType
from infrastructure.ai.ai_planner import AIPlanner
from models.ai_response import AIResponse
from prompts.browser_prompt import BROWSER_PROMPT
from prompts.examples_prompt import EXAMPLES_PROMPT
from prompts.filesystem_prompt import FILESYSTEM_PROMPT
from prompts.memory_prompt import MEMORY_PROMPT
from prompts.rules_prompt import RULES_PROMPT
from prompts.system_prompt import SYSTEM_PROMPT
from prompts.youtube_prompt import YOUTUBE_PROMPT


class _FakeAIService:
    def __init__(self, content: str) -> None:
        self.content = content
        self.request = None

    def generate(self, request):
        self.request = request
        return AIResponse(
            content=self.content,
            provider="test",
            model="test-model",
        )


class _FailingAIService:
    def generate(self, request):
        raise AssertionError("Exact browser commands must not call the AI service.")


class AIPlannerTests(unittest.TestCase):
    def test_create_plan_preserves_action_order_and_parameters(self) -> None:
        service = _FakeAIService(
            """
            {"actions": [
              {"handler": "BROWSER", "operation": "OPEN_TAB", "parameters": {"url": "https://example.com"}},
              {"handler": "BROWSER", "operation": "PRESS", "parameters": {"key": "ENTER"}}
            ]}
            """
        )

        plan = AIPlanner(service).create_plan("Open a tab and press Enter")

        self.assertEqual(len(plan.actions), 2)
        self.assertEqual(plan.actions[0].handler, HandlerType.BROWSER)
        self.assertEqual(plan.actions[0].operation, OperationType.OPEN_TAB)
        self.assertEqual(
            plan.actions[0].parameters,
            {"url": "https://example.com"},
        )
        self.assertEqual(plan.actions[1].operation, OperationType.PRESS)
        self.assertEqual(plan.actions[1].parameters, {"key": "ENTER"})

    def test_create_plan_uses_composed_system_prompt(self) -> None:
        service = _FakeAIService('{"actions": []}')

        AIPlanner(service).create_plan("Do nothing")

        self.assertEqual(service.request.system_prompt, SYSTEM_PROMPT)
        self.assertEqual(service.request.temperature, 0)
        self.assertEqual(service.request.max_tokens, 500)

    def test_system_prompt_includes_each_dedicated_component_once(self) -> None:
        for component in (
            MEMORY_PROMPT,
            FILESYSTEM_PROMPT,
            BROWSER_PROMPT,
            YOUTUBE_PROMPT,
            EXAMPLES_PROMPT,
            RULES_PROMPT,
        ):
            with self.subTest(component=component[:30]):
                self.assertEqual(SYSTEM_PROMPT.count(component), 1)

    def test_browser_examples_cover_supported_common_commands(self) -> None:
        for operation in (
            "OPEN_URL",
            "OPEN_TAB",
            "CLICK",
            "TYPE",
            "PRESS",
            "SCROLL",
            "SELECT",
            "UPLOAD_FILE",
        ):
            with self.subTest(operation=operation):
                self.assertIn(f'"operation": "{operation}"', EXAMPLES_PROMPT)

    def test_exact_browser_commands_have_correct_regression_operations(self) -> None:
        planner = AIPlanner(_FailingAIService())
        cases = (
            ("Open https://example.com", OperationType.OPEN_URL),
            ("Open new tab https://example.com", OperationType.OPEN_TAB),
            ("Click Search", OperationType.CLICK),
            ("Type OpenAI into Search", OperationType.TYPE),
            ("Press Enter", OperationType.PRESS),
            ("Scroll down", OperationType.SCROLL),
            ("Select Public", OperationType.SELECT),
            ("Upload file C:\\work\\report.pdf", OperationType.UPLOAD_FILE),
        )

        for command, operation in cases:
            with self.subTest(command=command):
                plan = planner.create_plan(command)
                self.assertEqual(len(plan.actions), 1)
                self.assertEqual(plan.actions[0].handler, HandlerType.BROWSER)
                self.assertEqual(plan.actions[0].operation, operation)

    def test_type_command_preserves_text_and_selector(self) -> None:
        plan = AIPlanner(_FailingAIService()).create_plan(
            "Type OpenAI into Search"
        )

        self.assertEqual(
            plan.actions[0].parameters,
            {"selector": "Search", "text": "OpenAI"},
        )


if __name__ == "__main__":
    unittest.main()
