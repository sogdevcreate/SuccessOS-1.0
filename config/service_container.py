"""
Service Container.

Central dependency injection container for SuccessOS.
"""

from __future__ import annotations

from config.settings import Settings

from core.execution_engine import ExecutionEngine
from core.handler_registry import HandlerRegistry
from core.plan_validator import PlanValidator
from core.router import Router

from enums.handler_type import HandlerType

from handlers.application_handler import ApplicationHandler
from handlers.browser_handler import BrowserHandler
from handlers.clipboard_handler import ClipboardHandler
from handlers.filesystem_handler import FilesystemHandler
from handlers.installation_handler import InstallationHandler
from handlers.memory_handler import MemoryHandler
from handlers.news_handler import NewsHandler
from handlers.process_handler import ProcessHandler
from handlers.system_handler import SystemHandler

from infrastructure.ai.ai_planner import AIPlanner
from infrastructure.ai.default_ai_service import DefaultAIService
from infrastructure.ai.openai_provider import OpenAIProvider
from infrastructure.applications.application_resolver import ApplicationResolver
from infrastructure.applications.windows_application_service import (
    WindowsApplicationService,
)
from infrastructure.browser.windows_browser_service import (
    WindowsBrowserService,
)
from infrastructure.browser.browser_policy_manager import (
    BrowserPolicyManager,
)
from infrastructure.clipboard.windows_clipboard_service import (
    WindowsClipboardService,
)
from infrastructure.database.sqlite_database import SQLiteDatabase
from infrastructure.filesystem.windows_filesystem_service import (
    WindowsFilesystemService,
)
from infrastructure.http.requests_http_client import RequestsHttpClient
from infrastructure.installation.installation_resolver import InstallationResolver
from infrastructure.installation.winget_installation_service import (
    WingetInstallationService,
)
from infrastructure.logging.python_logging_service import (
    PythonLoggingService,
)
from infrastructure.memory.sqlite_memory_service import SQLiteMemoryService
from infrastructure.news.web_news_service import WebNewsService
from infrastructure.process.windows_process_service import (
    WindowsProcessService,
)
from infrastructure.profiles.json_profile_service import JsonProfileService
from infrastructure.system.windows_system_service import (
    WindowsSystemService,
)


class ServiceContainer:
    """
    Creates and owns all application dependencies.
    """

    def __init__(self) -> None:

        #
        # Configuration
        #

        self.settings = Settings()

        #
        # Infrastructure
        #

        self.database = SQLiteDatabase()

        self.http_client = RequestsHttpClient()

        self.logging_service = PythonLoggingService(
            log_file=self.settings.get(
                "logging",
                "file",
                default="logs/successos.log",
            ),
        )

        self.application_resolver = ApplicationResolver()

        self.installation_resolver = InstallationResolver()

        self.application_service = WindowsApplicationService(
            resolver=self.application_resolver,
            logger=self.logging_service,
        )

        self.installation_service = WingetInstallationService(
            resolver=self.installation_resolver,
            logger=self.logging_service,
        )

        self.memory_service = SQLiteMemoryService(
            database=self.database,
            logger=self.logging_service,
        )

        self.filesystem_service = WindowsFilesystemService(
            allowed_roots=self.settings.get(
                "filesystem",
                "allowed_roots",
                default=["."],
            ),
        )

        self.clipboard_service = WindowsClipboardService()

        self.process_service = WindowsProcessService()

        self.browser_policy_manager = BrowserPolicyManager(
            allowed_domains=self.settings.get(
                "browser",
                "allowed_domains",
                default=[],
            ),
            allowed_schemes=self.settings.get(
                "browser",
                "allowed_schemes",
                default=["https"],
            ),
        )

        self.browser_service = WindowsBrowserService(
            policy_manager=self.browser_policy_manager,
        )

        self.profile_service = JsonProfileService()

        self.system_service = WindowsSystemService(
            logger=self.logging_service,
        )

        self.news_service = WebNewsService(
            http_client=self.http_client,
            logger=self.logging_service,
            api_key=self.settings.get(
                "news",
                "api_key",
            ),
        )

        #
        # AI
        #

        self.ai_provider = OpenAIProvider(
            http_client=self.http_client,
            logger=self.logging_service,
            api_key=self.settings.get(
                "ai",
                "api_key",
            ),
            model=self.settings.get(
                "ai",
                "model",
            ),
        )

        self.ai_service = DefaultAIService(
            self.ai_provider,
        )

        self.planner = AIPlanner(
            self.ai_service,
        )

        self.plan_validator = PlanValidator()

        #
        # Handlers
        #

        self.application_handler = ApplicationHandler(
            self.application_service,
        )

        self.installation_handler = InstallationHandler(
            self.installation_service,
        )

        self.memory_handler = MemoryHandler(
            self.memory_service,
        )

        self.filesystem_handler = FilesystemHandler(
            self.filesystem_service,
        )

        self.clipboard_handler = ClipboardHandler(
            self.clipboard_service,
        )

        self.process_handler = ProcessHandler(
            self.process_service,
        )

        self.browser_handler = BrowserHandler(
            self.browser_service,
        )

        self.news_handler = NewsHandler(
            self.news_service,
        )

        self.system_handler = SystemHandler(
            self.system_service,
        )

        #
        # Registry
        #

        self.handler_registry = HandlerRegistry()

        self.handler_registry.register(
            HandlerType.APPLICATION,
            self.application_handler,
        )

        self.handler_registry.register(
            HandlerType.INSTALLATION,
            self.installation_handler,
        )

        self.handler_registry.register(
            HandlerType.MEMORY,
            self.memory_handler,
        )

        self.handler_registry.register(
            HandlerType.FILESYSTEM,
            self.filesystem_handler,
        )

        self.handler_registry.register(
            HandlerType.CLIPBOARD,
            self.clipboard_handler,
        )

        self.handler_registry.register(
            HandlerType.PROCESS,
            self.process_handler,
        )

        self.handler_registry.register(
            HandlerType.BROWSER,
            self.browser_handler,
        )

        self.handler_registry.register(
            HandlerType.NEWS,
            self.news_handler,
        )

        self.handler_registry.register(
            HandlerType.SYSTEM,
            self.system_handler,
        )

        #
        # Router
        #

        self.router = Router(
            self.handler_registry,
        )

        #
        # Execution Engine
        #

        self.execution_engine = ExecutionEngine(
            self.router,
        )
