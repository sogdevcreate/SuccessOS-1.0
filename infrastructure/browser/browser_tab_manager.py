"""
Browser Tab Manager.
"""

from __future__ import annotations

from infrastructure.browser.browser_session import BrowserSession
from services.browser_tab_service import BrowserTabService


class BrowserTabManager(BrowserTabService):
    """
    Selenium implementation of browser tab management.
    """

    def __init__(
        self,
        session: BrowserSession,
    ) -> None:
        self._session = session

    def list_tabs(
        self,
    ) -> list[str]:
        """
        Return the titles of all open tabs.
        """

        driver = self._session.driver

        current = self._session.current_index()

        titles: list[str] = []

        for index in range(
            len(driver.window_handles),
        ):

            self._session.switch_to(
                index,
            )

            title = driver.title.strip()

            if not title:
                title = "New tab"

            titles.append(
                title,
            )

        self._session.switch_to(
            current,
        )

        return titles

    def current_tab(
        self,
    ) -> int:
        """
        Return the current tab index.
        """

        return self._session.current_index()

    def switch_tab(
        self,
        index: int,
    ) -> None:
        """
        Switch to a browser tab.

        Public API uses one-based indexing.
        """

        self._session.switch_to(
            index - 1,
        )

    def close_tab(
        self,
        index: int,
    ) -> None:
        """
        Close a browser tab.

        Public API uses one-based indexing.
        """

        current = self.current_tab()

        self.switch_tab(
            index,
        )

        self._session.close_current_tab()

        remaining = len(
            self._session.driver.window_handles,
        )

        if remaining == 0:
            return

        if current >= remaining:
            current = remaining - 1

        self._session.switch_to(
            current,
        )

    def page_title(
        self,
    ) -> str:
        """
        Return the current page title.
        """

        return self._session.driver.title