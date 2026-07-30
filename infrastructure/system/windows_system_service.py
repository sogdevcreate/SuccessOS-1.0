"""
Windows System Service.

Windows implementation of the SystemService contract.
"""

from __future__ import annotations

import subprocess

from models.system_status import SystemStatus
from services.logging_service import LoggingService
from services.system_service import SystemService


class WindowsSystemService(SystemService):
    """
    Windows implementation of system operations.
    """

    def __init__(
        self,
        logger: LoggingService,
    ) -> None:
        self._logger = logger

    def get_status(self) -> SystemStatus:
        """
        Retrieve the current system status.
        """

        self._logger.debug("Retrieving system status.")

        return SystemStatus()

    def shutdown(self) -> bool:
        """
        Shut down Windows.
        """

        try:
            subprocess.run(
                ["shutdown", "/s", "/t", "0"],
                check=True,
            )

            self._logger.info("Shutdown command issued.")

            return True

        except Exception as ex:
            self._logger.error(
                f"Failed to shut down Windows: {ex}"
            )
            return False

    def restart(self) -> bool:
        """
        Restart Windows.
        """

        try:
            subprocess.run(
                ["shutdown", "/r", "/t", "0"],
                check=True,
            )

            self._logger.info("Restart command issued.")

            return True

        except Exception as ex:
            self._logger.error(
                f"Failed to restart Windows: {ex}"
            )
            return False

    def sleep(self) -> bool:
        """
        Put Windows into sleep mode.
        """

        try:
            subprocess.run(
                [
                    "rundll32.exe",
                    "powrprof.dll,SetSuspendState",
                    "0,1,0",
                ],
                check=True,
            )

            self._logger.info("Sleep command issued.")

            return True

        except Exception as ex:
            self._logger.error(
                f"Failed to put Windows to sleep: {ex}"
            )
            return False

    def lock(self) -> bool:
        """
        Lock the current Windows session.
        """

        try:
            subprocess.run(
                [
                    "rundll32.exe",
                    "user32.dll,LockWorkStation",
                ],
                check=True,
            )

            self._logger.info("Lock workstation command issued.")

            return True

        except Exception as ex:
            self._logger.error(
                f"Failed to lock workstation: {ex}"
            )
            return False