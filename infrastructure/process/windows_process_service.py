"""
Windows Process Service.

Windows implementation of the ProcessService contract.
"""

from __future__ import annotations

import subprocess

try:
    import psutil
except ImportError:
    psutil = None

from services.process_service import ProcessService


class WindowsProcessService(ProcessService):
    """
    Windows implementation of process management.
    """

    def list_processes(self) -> list[dict]:
        """
        Return all running processes.
        """

        if psutil is None:
            raise RuntimeError(
                "psutil is required for process management."
            )

        processes = []

        for process in psutil.process_iter(
            [
                "pid",
                "name",
                "status",
                "memory_info",
            ]
        ):
            try:
                info = process.info

                processes.append(
                    {
                        "pid": info["pid"],
                        "name": info["name"],
                        "status": info["status"],
                        "memory": info["memory_info"].rss,
                    }
                )

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
            ):
                continue

        return processes

    def start_process(
        self,
        command: str,
    ) -> None:
        """
        Start a new process.
        """

        subprocess.Popen(command, shell=True)

    def kill_process(
        self,
        process: str,
    ) -> None:
        """
        Kill all processes matching the supplied name.
        """

        if psutil is None:
            raise RuntimeError(
                "psutil is required for process management."
            )

        for proc in psutil.process_iter(
            [
                "name",
            ]
        ):
            try:
                if (
                    proc.info["name"]
                    and proc.info["name"].lower()
                    == process.lower()
                ):
                    proc.kill()

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
            ):
                continue

    def process_info(
        self,
        process: str,
    ) -> dict:
        """
        Return information for the first matching process.
        """

        if psutil is None:
            raise RuntimeError(
                "psutil is required for process management."
            )

        for proc in psutil.process_iter(
            [
                "pid",
                "name",
                "status",
                "memory_info",
                "cpu_percent",
            ]
        ):
            try:
                if (
                    proc.info["name"]
                    and proc.info["name"].lower()
                    == process.lower()
                ):
                    return {
                        "pid": proc.info["pid"],
                        "name": proc.info["name"],
                        "status": proc.info["status"],
                        "memory": proc.info["memory_info"].rss,
                        "cpu": proc.info["cpu_percent"],
                    }

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
            ):
                continue

        raise RuntimeError(
            f"Process '{process}' was not found."
        )