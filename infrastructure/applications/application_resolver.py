"""
Application Resolver.

Resolves user-friendly application names to executable names.
"""

from __future__ import annotations


class ApplicationResolver:
    """
    Resolves application names to Windows executables.
    """

    _APPLICATIONS: dict[str, str] = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "calc": "calc.exe",
        "paint": "mspaint.exe",
        "cmd": "cmd.exe",
        "command prompt": "cmd.exe",
        "powershell": "powershell.exe",
        "explorer": "explorer.exe",
        "file explorer": "explorer.exe",
        "task manager": "taskmgr.exe",
        "registry editor": "regedit.exe",
        "chrome": "chrome.exe",
        "google chrome": "chrome.exe",
        "edge": "msedge.exe",
        "microsoft edge": "msedge.exe",
        "firefox": "firefox.exe",
        "opera": "opera.exe",
        "brave": "brave.exe",
        "vscode": "Code.exe",
        "visual studio code": "Code.exe",
        "discord": "Discord.exe",
        "spotify": "Spotify.exe",
        "steam": "steam.exe",
    }

    def resolve(self, application: str) -> str | None:
        """
        Resolve an application name to its executable.
        """

        return self._APPLICATIONS.get(application.strip().lower())