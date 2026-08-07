from __future__ import annotations

import unittest

from core.execution_engine import ExecutionEngine
from enums.handler_type import HandlerType
from enums.operation_type import OperationType
from models.action import Action
from models.execution_plan import ExecutionPlan
from models.execution_result import ExecutionResult
from tests.helpers.reporting import ComponentTestCase


class _Router:
    def route(self, action):
        if action.name == "fail":
            return ExecutionResult.fail("failed action")
        return ExecutionResult.ok("ok")


class ExecutionTraceTests(ComponentTestCase):
    subsystem = "Execution"
    component = "ExecutionEngine trace"
    recommended_location = "core/execution_engine.py and models/execution_trace_entry.py"

    def test_trace_records_each_completed_action_and_failure(self) -> None:
        plan = ExecutionPlan([
            Action("first", HandlerType.CLIPBOARD, OperationType.READ),
            Action("fail", HandlerType.CLIPBOARD, OperationType.CLEAR),
        ])

        result = ExecutionEngine(_Router()).execute(plan)

        self.assertFalse(result.successful)
        self.assertEqual(result.completed_actions, 1)
        self.assertEqual(len(result.trace), 2)
        self.assertEqual(result.trace[0].action_name, "first")
        self.assertTrue(result.trace[0].duration_seconds >= 0)
        self.assertEqual(result.trace[1].error, "failed action")
        self.assertEqual(result.trace[1].status, result.status)
