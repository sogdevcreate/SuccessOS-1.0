from __future__ import annotations

import unittest

from core.execution_engine import ExecutionEngine
from core.handler_registry import HandlerRegistry
from core.router import Router
from enums.handler_type import HandlerType
from enums.memory_category import MemoryCategory
from handlers.memory_handler import MemoryHandler
from infrastructure.ai.ai_planner import AIPlanner
from models.ai_response import AIResponse
from tests.fixtures.fakes import FakeMemoryService
from tests.helpers.reporting import ComponentTestCase


class _AIService:
    def generate(self, request):
        return AIResponse(
            content=(
                '{"actions": [{"handler": "MEMORY", "operation": "SAVE", '
                '"parameters": {"category": "fact", "key": "language", '
                '"value": "Python"}}]}'
            ),
            provider="test",
            model="test",
        )


class ExecutionPipelineIntegrationTests(ComponentTestCase):
    subsystem = "Execution"
    component = "Planner -> Engine -> Router -> MemoryHandler"
    recommended_location = "infrastructure/ai/ai_planner.py, core/, handlers/memory_handler.py"

    def test_planned_memory_action_reaches_service_with_expected_data(self) -> None:
        memory_service = FakeMemoryService()
        registry = HandlerRegistry()
        registry.register(HandlerType.MEMORY, MemoryHandler(memory_service))
        plan = AIPlanner(_AIService()).create_plan("remember a fact")

        result = ExecutionEngine(Router(registry)).execute(plan)
        memory = memory_service.recall(MemoryCategory.FACT, "language")

        self.assertTrue(result.successful)
        self.assertIsNotNone(memory)
        self.assertEqual(memory.value, "Python")
