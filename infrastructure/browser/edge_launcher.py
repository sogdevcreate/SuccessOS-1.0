"""
Edge Launcher.

Starts Microsoft Edge with remote debugging enabled when needed.
"""

from __future__ import annotations

import socket
import subprocess
import time
from pathlib import Path


class EdgeLauncher:
    DEBUG_PORT = 9222

    def start(self) -> None:
        if self._is_port_open():
            return

        edge = Path(
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
        )

        profile = (
            Path.home()
            / "AppData"
            / "Local"
            / "SuccessOS"
            / "EdgeProfile"
        )

        profile.mkdir(
            parents=True,
            exist_ok=True,
        )

        subprocess.Popen(
            [
                str(edge),
                f"--remote-debugging-port={self.DEBUG_PORT}",
                f"--user-data-dir={profile}",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        self._wait_for_port()

    def _is_port_open(self) -> bool:
        try:
            with socket.create_connection(
                ("127.0.0.1", self.DEBUG_PORT),
                timeout=1,
            ):
                return True
        except OSError:
            return False

    def _wait_for_port(
        self,
        timeout: int = 15,
    ) -> None:
        end = time.time() + timeout

        while time.time() < end:
            if self._is_port_open():
                return
            time.sleep(0.25)

        raise RuntimeError(
            "Edge DevTools failed to start."
        )