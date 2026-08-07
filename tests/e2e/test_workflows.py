from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from core.execution_engine import ExecutionEngine
from core.handler_registry import HandlerRegistry
from core.permission_manager import PermissionManager
from core.router import Router
from enums.handler_type import HandlerType
from enums.operation_type import OperationType
from handlers.application_handler import ApplicationHandler
from handlers.browser_handler import BrowserHandler
from handlers.filesystem_handler import FilesystemHandler
from handlers.memory_handler import MemoryHandler
from infrastructure.browser.browser_policy_manager import (
    BrowserPolicyError,
    BrowserPolicyManager,
)
from infrastructure.filesystem.windows_filesystem_service import (
    WindowsFilesystemService,
)
from models.action import Action
from models.execution_plan import ExecutionPlan
from models.execution_result import ExecutionResult
from tests.fixtures.fakes import FakeBrowserService, FakeMemoryService
from tests.helpers.reporting import ComponentTestCase


def _engine(handler_type, handler, confirmation: bool = True) -> ExecutionEngine:
    registry = HandlerRegistry()
    registry.register(handler_type, handler)
    return ExecutionEngine(
        Router(registry),
        PermissionManager(confirmation_provider=lambda *_: confirmation),
    )


class BrowserWorkflowTests(ComponentTestCase):
    subsystem = "Browser"
    component = "Browser workflow"
    recommended_location = "handlers/browser_handler.py and infrastructure/browser/"

    def test_google_search_workflow_verifies_result_title(self) -> None:
        browser = FakeBrowserService()
        plan = ExecutionPlan([
            Action("open", HandlerType.BROWSER, OperationType.OPEN_URL, {"url": "https://www.google.com"}),
            Action("click", HandlerType.BROWSER, OperationType.CLICK, {"selector": "Search"}),
            Action("type", HandlerType.BROWSER, OperationType.TYPE, {"selector": "Search", "text": "OpenAI"}),
            Action("press", HandlerType.BROWSER, OperationType.PRESS, {"key": "ENTER"}),
            Action("title", HandlerType.BROWSER, OperationType.PAGE_TITLE),
        ])

        result = _engine(HandlerType.BROWSER, BrowserHandler(browser)).execute(plan)

        self.assertTrue(result.successful)
        self.assertIn("OpenAI", result.message)
        self.assertEqual(browser.last_selector, "Search")

    def test_tab_workflow_verifies_both_tabs(self) -> None:
        browser = FakeBrowserService()
        plan = ExecutionPlan([
            Action("open", HandlerType.BROWSER, OperationType.OPEN_URL, {"url": "https://one.test"}),
            Action("tab", HandlerType.BROWSER, OperationType.OPEN_TAB, {"url": "https://two.test"}),
            Action("list", HandlerType.BROWSER, OperationType.LIST_TABS),
        ])

        result = _engine(HandlerType.BROWSER, BrowserHandler(browser)).execute(plan)

        self.assertTrue(result.successful)
        self.assertIn("https://one.test", result.message)
        self.assertIn("https://two.test", result.message)


class FilesystemWorkflowTests(ComponentTestCase):
    subsystem = "Filesystem"
    component = "Sandboxed filesystem workflow"
    recommended_location = "handlers/filesystem_handler.py and infrastructure/filesystem/"

    def test_create_write_read_workflow_verifies_file_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "notes" / "todo.txt"
            service = WindowsFilesystemService([root])
            plan = ExecutionPlan([
                Action("mkdir", HandlerType.FILESYSTEM, OperationType.CREATE_DIRECTORY, {"path": str(target.parent)}),
                Action("write", HandlerType.FILESYSTEM, OperationType.WRITE, {"path": str(target), "content": "finish tests"}),
                Action("read", HandlerType.FILESYSTEM, OperationType.READ, {"path": str(target)}),
            ])

            result = _engine(HandlerType.FILESYSTEM, FilesystemHandler(service)).execute(plan)

            self.assertTrue(result.successful)
            self.assertEqual(result.message, "finish tests")
            self.assertEqual(target.read_text(encoding="utf-8"), "finish tests")


class MemoryWorkflowTests(ComponentTestCase):
    subsystem = "Memory"
    component = "Memory workflow"
    recommended_location = "handlers/memory_handler.py and infrastructure/memory/"

    def test_save_load_workflow_verifies_recalled_value(self) -> None:
        memory = FakeMemoryService()
        plan = ExecutionPlan([
            Action("save", HandlerType.MEMORY, OperationType.SAVE, {"category": "fact", "key": "language", "value": "Python"}),
            Action("load", HandlerType.MEMORY, OperationType.LOAD, {"category": "fact", "key": "language"}),
        ])

        result = _engine(HandlerType.MEMORY, MemoryHandler(memory)).execute(plan)

        self.assertTrue(result.successful)
        self.assertEqual(result.message, "Python")


class ApplicationWorkflowTests(ComponentTestCase):
    subsystem = "Application"
    component = "Application launch workflow"
    recommended_location = "handlers/application_handler.py and infrastructure/applications/"

    def test_launch_workflow_verifies_requested_application(self) -> None:
        class Service:
            def __init__(self):
                self.opened = []

            def open(self, application):
                self.opened.append(application)
                return True

            def close(self, application):
                return True

        service = Service()
        plan = ExecutionPlan([
            Action("open", HandlerType.APPLICATION, OperationType.OPEN, {"application": "notepad"}),
        ])

        result = _engine(HandlerType.APPLICATION, ApplicationHandler(service)).execute(plan)

        self.assertTrue(result.successful)
        self.assertEqual(service.opened, ["notepad"])


class SafetyWorkflowTests(ComponentTestCase):
    subsystem = "Authorization"
    component = "Authorization and browser policy workflows"
    recommended_location = "core/permission_manager.py and infrastructure/browser/browser_policy_manager.py"

    def test_authorization_prevents_handler_execution(self) -> None:
        class Handler:
            executed = False

            def execute(self, action):
                self.executed = True
                return ExecutionResult.ok()

        handler = Handler()
        plan = ExecutionPlan([
            Action("delete", HandlerType.FILESYSTEM, OperationType.DELETE, {"path": "safe.txt"}),
        ])

        result = _engine(HandlerType.FILESYSTEM, handler, confirmation=False).execute(plan)

        self.assertFalse(result.successful)
        self.assertFalse(handler.executed)

    def test_browser_policy_verifies_safe_and_unsafe_outcomes(self) -> None:
        policy = BrowserPolicyManager()

        self.assertEqual(
            policy.authorize_navigation("https://www.google.com"),
            "https://www.google.com/",
        )
        with self.assertRaises(BrowserPolicyError):
            policy.authorize_navigation("javascript:alert(1)")
