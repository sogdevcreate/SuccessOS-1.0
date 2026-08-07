from __future__ import annotations

import unittest
from unittest.mock import patch

from core.application import Application
from core.context_builder import ContextBuilder
from core.handler_registry import HandlerRegistry
from core.intent_engine import IntentEngine
from core.interpreter import Interpreter
from core.plan_validator import PlanValidator
from core.router import Router
from enums.handler_type import HandlerType
from enums.operation_type import OperationType
from exceptions.plan_validation_error import PlanValidationError
from models.action import Action
from models.execution_plan import ExecutionPlan
from models.execution_result import ExecutionResult
from models.user_profile import UserProfile
from tests.fixtures.fakes import FakeMemoryService, FakeProfileService, FakeSystemService
from tests.helpers.reporting import ComponentTestCase


class CoreComponentTests(ComponentTestCase):
    subsystem = "Execution"
    component = "Core classes"
    recommended_location = "core/"

    def test_interpreter_normalizes_whitespace(self) -> None:
        self.assertEqual(Interpreter().interpret("  open   notepad  "), "open notepad")

    def test_context_builder_combines_dependencies(self) -> None:
        memory = FakeMemoryService()
        profile = UserProfile(name="Ada")
        context = ContextBuilder(
            memory,
            FakeProfileService(profile),
            FakeSystemService(),
        ).build("status")

        self.assertEqual(context.user_input, "status")
        self.assertEqual(context.profile, profile)
        self.assertEqual(context.system_status.cpu_usage, 12.5)

    def test_registry_and_router_execute_registered_handler(self) -> None:
        class Handler:
            def execute(self, action):
                return ExecutionResult.ok(action.name)

        registry = HandlerRegistry()
        registry.register(HandlerType.SYSTEM, Handler())
        result = Router(registry).route(
            Action("status", HandlerType.SYSTEM, OperationType.QUERY)
        )

        self.assertTrue(result.successful)
        self.assertEqual(result.message, "status")

    def test_registry_reports_missing_handler(self) -> None:
        with self.assertRaises(ValueError):
            HandlerRegistry().resolve(HandlerType.BROWSER)

    def test_plan_validator_rejects_missing_required_parameter(self) -> None:
        plan = ExecutionPlan([
            Action("open", HandlerType.APPLICATION, OperationType.OPEN),
        ])

        with self.assertRaises(PlanValidationError):
            PlanValidator().validate(plan)

    def test_intent_engine_is_an_explicit_extension_point(self) -> None:
        with self.assertRaises(NotImplementedError):
            IntentEngine().build_plan(None)

    def test_application_can_be_tested_with_a_container_fake(self) -> None:
        class Logger:
            def __init__(self):
                self.messages = []

            def info(self, message):
                self.messages.append(message)

        class Container:
            def __init__(self):
                self.logging_service = Logger()

        application = Application(Container())

        with patch("builtins.print"):
            application.start()
            application.shutdown()

        self.assertEqual(len(application.container.logging_service.messages), 3)
