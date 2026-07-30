"""
Windows Application Service.

Windows implementation of the ApplicationService contract.
"""

from __future__ import annotations

import subprocess

from infrastructure.applications.application_resolver import ApplicationResolver
from services.application_service import ApplicationService
from services.logging_service import LoggingService


class WindowsApplicationService(ApplicationService):
    """
    Windows implementation for launching and closing applications.
    """

    def __init__(
        self,
        resolver: ApplicationResolver,
        logger: LoggingService,
    ) -> None:
        self._resolver = resolver
        self._logger = logger

    def open(self, application: str) -> bool:
        """
        Launch an application.
        """

        executable = self._resolver.resolve(application)

        if executable is None:
            self._logger.warning(
                f"Application '{application}' could not be resolved."
            )
            return False

        try:
            subprocess.Popen([executable])

            self._logger.info(
                f"Opened application '{application}'."
            )

            return True

        except Exception as ex:
            self._logger.error(
                f"Failed to open '{application}': {ex}"
            )
            return False

    def close(self, application: str) -> bool:
        """
        Close an application.
        """

        executable = self._resolver.resolve(application)

        if executable is None:
            self._logger.warning(
                f"Application '{application}' could not be resolved."
            )
            return False

        try:
            subprocess.run(
                [
                    "taskkill",
                    "/IM",
                    executable,
                    "/F",
                ],
                check=False,
                capture_output=True,
            )

            self._logger.info(
                f"Closed application '{application}'."
            )

            return True

        except Exception as ex:
            self._logger.error(
                f"Failed to close '{application}': {ex}"
            )
            return False