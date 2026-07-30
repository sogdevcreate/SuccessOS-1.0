"""
Installation Resolver.

Resolves user-friendly application names to Winget package IDs.
"""

from __future__ import annotations


class InstallationResolver:
    """
    Resolves application names to Winget package IDs.
    """

    _PACKAGES: dict[str, str] = {
        "chrome": "Google.Chrome",
        "google chrome": "Google.Chrome",
        "edge": "Microsoft.Edge",
        "microsoft edge": "Microsoft.Edge",
        "firefox": "Mozilla.Firefox",
        "brave": "Brave.Brave",
        "opera": "Opera.Opera",
        "vscode": "Microsoft.VisualStudioCode",
        "visual studio code": "Microsoft.VisualStudioCode",
        "discord": "Discord.Discord",
        "spotify": "Spotify.Spotify",
        "steam": "Valve.Steam",
        "docker": "Docker.DockerDesktop",
        "git": "Git.Git",
        "python": "Python.Python.3",
        "nodejs": "OpenJS.NodeJS",
    }

    def resolve(self, application: str) -> str | None:
        """
        Resolve an application name to its Winget package ID.
        """

        return self._PACKAGES.get(application.strip().lower())