"""
Windows Browser Service.

Windows implementation of the BrowserService contract.
"""

from __future__ import annotations

from infrastructure.browser.browser_interaction import (
    BrowserInteraction,
)
from infrastructure.browser.browser_policy_manager import (
    BrowserPolicyManager,
)
from infrastructure.browser.browser_session import BrowserSession
from infrastructure.browser.browser_tab_manager import (
    BrowserTabManager,
)
from infrastructure.browser.youtube_controller import (
    YouTubeController,
)
from infrastructure.browser.youtube_studio_controller import (
    YouTubeStudioController,
)
from services.browser_service import BrowserService


class WindowsBrowserService(BrowserService):
    """
    Windows implementation of browser automation.
    """

    def __init__(
        self,
        policy_manager: BrowserPolicyManager | None = None,
    ) -> None:
        self._policy = policy_manager or BrowserPolicyManager(
            allowed_domains=("youtube.com",),
        )
        self._session = BrowserSession()

        self._tabs = BrowserTabManager(
            self._session,
        )

        self._interaction = BrowserInteraction(
            self._session,
        )

        self._youtube = YouTubeController(
            self._session,
        )

        self._studio = YouTubeStudioController(
            self._session,
        )

    #
    # Navigation
    #

    def open_url(
        self,
        url: str,
    ) -> None:
        """
        Open a URL.
        """

        driver = self._session.driver

        driver.get(self._policy.authorize_navigation(url))

        self._session.remember_current_tab()

    def open_tab(
        self,
        url: str,
    ) -> None:
        """
        Open a URL in a new tab.
        """

        driver = self._session.driver

        driver.switch_to.new_window(
            "tab",
        )

        driver.get(self._policy.authorize_navigation(url))

        self._session.remember_current_tab()

    def close_tab(
        self,
    ) -> None:
        """
        Close the current tab.
        """

        self._tabs.close_tab(
            self._tabs.current_tab() + 1,
        )

    def refresh_page(
        self,
    ) -> None:
        """
        Refresh the current page.
        """

        driver = self._session.driver
        self._policy.authorize_navigation(driver.current_url)
        driver.refresh()

    def go_back(
        self,
    ) -> None:
        """
        Navigate back.
        """

        self._session.driver.back()

    def go_forward(
        self,
    ) -> None:
        """
        Navigate forward.
        """

        self._session.driver.forward()

    #
    # Tabs
    #

    def list_tabs(
        self,
    ) -> list[str]:
        """
        Return all open tab titles.
        """

        return self._tabs.list_tabs()

    def current_tab(
        self,
    ) -> int:
        """
        Return the current tab index.
        """

        return self._tabs.current_tab()

    def switch_tab(
        self,
        index: int,
    ) -> None:
        """
        Switch to a browser tab.
        """

        self._tabs.switch_tab(
            index,
        )

    def page_title(
        self,
    ) -> str:
        """
        Return the current page title.
        """

        return self._tabs.page_title()

    #
    # Interaction
    #

    def click(
        self,
        selector: str,
    ) -> None:
        """
        Click an element.
        """

        self._interaction.click(
            selector,
        )

    def type(
        self,
        selector: str,
        text: str,
    ) -> None:
        """
        Type into an element.
        """

        self._policy.authorize_form_submission((text,))
        self._interaction.type(
            selector,
            text,
        )

    def press(
        self,
        key: str,
    ) -> None:
        """
        Press a keyboard key.
        """

        self._interaction.press(
            key,
        )

    def wait_for(
        self,
        selector: str,
        timeout: int = 10,
    ) -> None:
        """
        Wait for an element.
        """

        self._interaction.wait_for(
            selector,
            timeout,
        )

    def scroll(
        self,
        pixels: int,
    ) -> None:
        """
        Scroll the page.
        """

        self._interaction.scroll(
            pixels,
        )

    def select(
        self,
        selector: str,
        value: str,
    ) -> None:
        """
        Select a dropdown option.
        """

        self._interaction.select(
            selector,
            value,
        )

    def upload_file(
        self,
        selector: str,
        path: str,
    ) -> None:
        """
        Upload a file.
        """

        self._policy.authorize_upload(path)
        self._interaction.upload_file(
            selector,
            path,
        )

    def screenshot(
        self,
        path: str,
    ) -> None:
        """
        Save a screenshot.
        """

        self._interaction.screenshot(
            path,
        )

    #
    # YouTube
    #

    def youtube_search(
        self,
        query: str,
    ) -> None:
        """
        Search YouTube.
        """

        self._policy.authorize_navigation("https://www.youtube.com/")
        self._youtube.search(
            query,
        )

        self._session.remember_current_tab()

    def youtube_play(
        self,
        query: str,
    ) -> None:
        """
        Play the first matching YouTube video.
        """

        self._policy.authorize_navigation("https://www.youtube.com/")
        self._youtube.play(
            query,
        )

        self._session.remember_current_tab()

    def youtube_video(
        self,
        video_id: str,
    ) -> None:
        """
        Open a YouTube video.
        """

        self._policy.authorize_navigation("https://www.youtube.com/")
        self._youtube.open_video(
            video_id,
        )

        self._session.remember_current_tab()

    def youtube_playlist(
        self,
        playlist_id: str,
    ) -> None:
        """
        Open a YouTube playlist.
        """

        self._policy.authorize_navigation("https://www.youtube.com/")
        self._youtube.open_playlist(
            playlist_id,
        )

        self._session.remember_current_tab()

    def youtube_channel(
        self,
        channel: str,
    ) -> None:
        """
        Open a YouTube channel.
        """

        self._policy.authorize_navigation("https://www.youtube.com/")
        self._youtube.open_channel(
            channel,
        )

        self._session.remember_current_tab()

    #
    # YouTube Studio
    #

    def studio_open(self) -> None:
        self._policy.authorize_navigation("https://studio.youtube.com/")
        self._studio.open_studio()

    def studio_dashboard(self) -> None:
        self._policy.authorize_navigation("https://studio.youtube.com/")
        self._studio.dashboard()

    def studio_content(self) -> None:
        self._policy.authorize_navigation("https://studio.youtube.com/")
        self._studio.content()

    def studio_analytics(self) -> None:
        self._policy.authorize_navigation("https://studio.youtube.com/")
        self._studio.analytics()

    def studio_comments(self) -> None:
        self._policy.authorize_navigation("https://studio.youtube.com/")
        self._studio.comments()

    def studio_copyright(self) -> None:
        self._policy.authorize_navigation("https://studio.youtube.com/")
        self._studio.copyright()

    def studio_monetization(self) -> None:
        self._policy.authorize_navigation("https://studio.youtube.com/")
        self._studio.monetization()

    def studio_settings(self) -> None:
        self._policy.authorize_navigation("https://studio.youtube.com/")
        self._studio.settings()

