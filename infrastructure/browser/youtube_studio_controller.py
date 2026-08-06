"""
YouTube Studio Controller.

Handles YouTube Studio automation.
"""

from __future__ import annotations

from infrastructure.browser.browser_session import BrowserSession


class YouTubeStudioController:
    """
    Provides YouTube Studio automation.
    """

    def __init__(
        self,
        session: BrowserSession,
    ) -> None:
        self._session = session
        self._base_url: str | None = None

    def open_studio(
        self,
    ) -> None:
        """
        Open YouTube Studio.
        """

        driver = self._session.driver

        driver.get(
            "https://studio.youtube.com/",
        )

        self._remember_base_url()

    def dashboard(
        self,
    ) -> None:
        """
        Open Dashboard.
        """

        self._open(
            "",
        )

    def content(
        self,
    ) -> None:
        """
        Open Content.
        """

        self._open(
            "/videos",
        )

    def analytics(
        self,
    ) -> None:
        """
        Open Analytics.
        """

        self._open(
            "/analytics",
        )

    def comments(
        self,
    ) -> None:
        """
        Open Comments.
        """

        self._open(
            "/comments",
        )

    def subtitles(
        self,
    ) -> None:
        """
        Open Subtitles.
        """

        self._open(
            "/subtitles",
        )

    def copyright(
        self,
    ) -> None:
        """
        Open Copyright.
        """

        self._open(
            "/copyright",
        )

    def monetization(
        self,
    ) -> None:
        """
        Open Monetization.
        """

        self._open(
            "/monetization",
        )

    def customization(
        self,
    ) -> None:
        """
        Open Customization.
        """

        self._open(
            "/customization",
        )

    def audio_library(
        self,
    ) -> None:
        """
        Open Audio Library.
        """

        self._open(
            "/music",
        )

    def settings(
        self,
    ) -> None:
        """
        Open Settings.
        """

        self._open(
            "/settings",
        )

    def _remember_base_url(
        self,
    ) -> None:
        """
        Remember the Studio base URL.
        """

        url = self._session.driver.current_url

        if "/videos" in url:
            url = url.split("/videos")[0]

        elif "/analytics" in url:
            url = url.split("/analytics")[0]

        elif "/comments" in url:
            url = url.split("/comments")[0]

        elif "/subtitles" in url:
            url = url.split("/subtitles")[0]

        elif "/copyright" in url:
            url = url.split("/copyright")[0]

        elif "/monetization" in url:
            url = url.split("/monetization")[0]

        elif "/customization" in url:
            url = url.split("/customization")[0]

        elif "/music" in url:
            url = url.split("/music")[0]

        elif "/settings" in url:
            url = url.split("/settings")[0]

        self._base_url = url.rstrip("/")

    def _open(
        self,
        path: str,
    ) -> None:
        """
        Open a Studio page.
        """

        if self._base_url is None:
            self.open_studio()

        self._session.driver.get(
            f"{self._base_url}{path}",
        )