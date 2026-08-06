from __future__ import annotations

import unittest

from core.execution_engine import ExecutionEngine
from core.permission_manager import PermissionManager
from enums.handler_type import HandlerType
from enums.operation_type import OperationType
from enums.permission_level import PermissionLevel
from models.action import Action
from models.execution_plan import ExecutionPlan
from models.execution_result import ExecutionResult


class PermissionManagerTests(unittest.TestCase):
    def test_sensitive_actions_require_confirmation(self) -> None:
        manager = PermissionManager(confirmation_provider=lambda *_: True)
        actions = (
            Action("delete", HandlerType.FILESYSTEM, OperationType.DELETE),
            Action("move", HandlerType.FILESYSTEM, OperationType.MOVE),
            Action("install", HandlerType.INSTALLATION, OperationType.INSTALL),
            Action("uninstall", HandlerType.INSTALLATION, OperationType.UNINSTALL),
            Action("kill", HandlerType.PROCESS, OperationType.KILL_PROCESS),
            Action("command", HandlerType.PROCESS, OperationType.START_PROCESS),
            Action("upload", HandlerType.BROWSER, OperationType.UPLOAD_FILE),
            Action("shutdown", HandlerType.SYSTEM, OperationType.SHUTDOWN),
            Action("restart", HandlerType.SYSTEM, OperationType.RESTART),
        )

        for action in actions:
            with self.subTest(action=action.name):
                self.assertEqual(
                    manager.required_level(action),
                    PermissionLevel.CONFIRM,
                )

    def test_denied_confirmation_returns_failure(self) -> None:
        manager = PermissionManager(confirmation_provider=lambda *_: False)
        action = Action(
            "delete",
            HandlerType.FILESYSTEM,
            OperationType.DELETE,
        )

        result = manager.authorize(action)

        self.assertIsNotNone(result)
        self.assertFalse(result.successful)
        self.assertEqual(result.metadata["permission"], "confirm")

    def test_action_confirmation_flag_is_enforced(self) -> None:
        manager = PermissionManager(confirmation_provider=lambda *_: True)
        action = Action(
            "read",
            HandlerType.FILESYSTEM,
            OperationType.READ,
            requires_confirmation=True,
        )

        self.assertEqual(
            manager.required_level(action),
            PermissionLevel.CONFIRM,
        )

    def test_admin_actions_require_elevation_and_confirmation(self) -> None:
        calls: list[tuple[Action, PermissionLevel]] = []
        manager = PermissionManager(
            confirmation_provider=lambda action, level: calls.append((action, level)) or True,
            admin_checker=lambda: False,
        )
        action = Action(
            "admin-read",
            HandlerType.FILESYSTEM,
            OperationType.READ,
            permission=PermissionLevel.ADMIN,
        )

        result = manager.authorize(action)

        self.assertIsNotNone(result)
        self.assertFalse(result.successful)
        self.assertEqual(calls, [])


class _Router:
    def __init__(self) -> None:
        self.routed: list[Action] = []

    def route(self, action: Action) -> ExecutionResult:
        self.routed.append(action)
        return ExecutionResult.ok("routed")


class _PermissionManager:
    def __init__(self, denied_action: str | None = None) -> None:
        self.checked: list[Action] = []
        self._denied_action = denied_action

    def authorize(self, action: Action) -> ExecutionResult | None:
        self.checked.append(action)
        if action.name == self._denied_action:
            return ExecutionResult.fail("denied")
        return None


class ExecutionEnginePermissionTests(unittest.TestCase):
    def test_engine_authorizes_every_action_before_routing(self) -> None:
        router = _Router()
        manager = _PermissionManager()
        plan = ExecutionPlan([
            Action("first", HandlerType.FILESYSTEM, OperationType.READ),
            Action("second", HandlerType.FILESYSTEM, OperationType.LIST),
        ])

        result = ExecutionEngine(router, manager).execute(plan)

        self.assertTrue(result.successful)
        self.assertEqual(manager.checked, plan.actions)
        self.assertEqual(router.routed, plan.actions)

    def test_engine_does_not_route_an_unauthorized_action(self) -> None:
        router = _Router()
        manager = _PermissionManager(denied_action="second")
        plan = ExecutionPlan([
            Action("first", HandlerType.FILESYSTEM, OperationType.READ),
            Action("second", HandlerType.FILESYSTEM, OperationType.DELETE),
        ])

        result = ExecutionEngine(router, manager).execute(plan)

        self.assertFalse(result.successful)
        self.assertEqual(result.completed_actions, 1)
        self.assertEqual([action.name for action in router.routed], ["first"])


if __name__ == "__main__":
    unittest.main()
