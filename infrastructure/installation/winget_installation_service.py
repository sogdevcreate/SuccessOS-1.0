"""
Winget Installation Service.

Windows implementation of the InstallationService contract.
"""

from __future__ import annotations

import subprocess

from infrastructure.installation.installation_resolver import (
    InstallationResolver,
)
from services.installation_service import InstallationService
from services.logging_service import LoggingService


class WingetInstallationService(InstallationService):
    """
    Windows Package Manager implementation.
    """

    def __init__(
        self,
        resolver: InstallationResolver,
        logger: LoggingService,
    ) -> None:
        self._resolver = resolver
        self._logger = logger

    def install(self, application: str) -> bool:
        """
        Install an application using Winget.
        """

        package_id = self._resolver.resolve(application)

        if package_id is None:
            self._logger.warning(
                f"Package '{application}' could not be resolved."
            )
            return False

        try:
            subprocess.run(
                [
                    "winget",
                    "install",
                    "--id",
                    package_id,
                    "--exact",
                    "--accept-package-agreements",
                    "--accept-source-agreements",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self._logger.info(
                f"Installed '{application}'."
            )

            return True

        except Exception as ex:
            self._logger.error(
                f"Failed to install '{application}': {ex}"
            )
            return False

    def uninstall(self, application: str) -> bool:
        """
        Uninstall an application using Winget.
        """

        package_id = self._resolver.resolve(application)

        if package_id is None:
            self._logger.warning(
                f"Package '{application}' could not be resolved."
            )
            return False

        try:
            subprocess.run(
                [
                    "winget",
                    "uninstall",
                    "--id",
                    package_id,
                    "--exact",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self._logger.info(
                f"Uninstalled '{application}'."
            )

            return True

        except Exception as ex:
            self._logger.error(
                f"Failed to uninstall '{application}': {ex}"
            )
            return False