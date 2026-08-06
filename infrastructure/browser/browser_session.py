"""
Browser Session.

Owns and manages the Selenium Edge browser session.
"""

from __future__ import annotations

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchWindowException,
    WebDriverException,
)
from selenium.webdriver.edge.options import Options

from infrastructure.browser.edge_launcher import EdgeLauncher


class BrowserSession:
    """
    Manages a persistent Microsoft Edge session.
    """

    def __init__(self) -> None:
        self._driver: webdriver.Edge | None = None
        self._current_handle: str | None = None

    @property
    def driver(
        self,
    ) -> webdriver.Edge:
        """
        Return the active Edge driver.

        Creates a new session if necessary.
        """

        if self._driver is None:
            self._driver = self._create_driver()
            self._remember_current_handle()
            return self._driver

        try:
            _ = self._driver.current_url

        except WebDriverException:

            try:
                self._driver.quit()

            except Exception:
                pass

            self._driver = self._create_driver()
            self._remember_current_handle()

        self._restore_handle()

        return self._driver

    @property
    def current_handle(
        self,
    ) -> str | None:
        """
        Return the active window handle.
        """

        return self._current_handle

    def remember_current_tab(
        self,
    ) -> None:
        """
        Remember the active browser tab.
        """

        self._remember_current_handle()

    def switch_to(
        self,
        index: int,
    ) -> None:
        """
        Switch to a browser tab.

        Index is zero-based.
        """

        driver = self.driver

        handles = driver.window_handles

        if index < 0:
            raise IndexError(
                "Invalid browser tab."
            )

        if index >= len(handles):
            raise IndexError(
                "Invalid browser tab."
            )

        driver.switch_to.window(
            handles[index],
        )

        self._remember_current_handle()

    def current_index(
        self,
    ) -> int:
        """
        Return the current browser tab index.
        """

        driver = self.driver

        self._restore_handle()

        return driver.window_handles.index(
            self._current_handle,
        )

    def close_current_tab(
        self,
    ) -> None:
        """
        Close the active browser tab.
        """

        driver = self.driver

        driver.close()

        handles = driver.window_handles

        if not handles:

            self.close()

            return

        driver.switch_to.window(
            handles[-1],
        )

        self._remember_current_handle()

    def close(
        self,
    ) -> None:
        """
        Close the browser session.
        """

        if self._driver is None:
            return

        try:
            self._driver.quit()

        finally:
            self._driver = None
            self._current_handle = None

    def _restore_handle(
        self,
    ) -> None:
        """
        Restore the remembered browser tab.
        """

        driver = self._driver

        if driver is None:
            return

        handles = driver.window_handles

        if not handles:
            return

        if self._current_handle not in handles:
            self._current_handle = handles[-1]

        try:

            driver.switch_to.window(
                self._current_handle,
            )

        except NoSuchWindowException:

            self._current_handle = handles[-1]

            driver.switch_to.window(
                self._current_handle,
            )

    def _remember_current_handle(
        self,
    ) -> None:
        """
        Store the active browser tab.
        """

        driver = self._driver

        if driver is None:
            return

        self._current_handle = (
            driver.current_window_handle
        )

    def _create_driver(
        self,
    ) -> webdriver.Edge:
        """
        Create or attach to the SuccessOS Edge session.
        """

        launcher = EdgeLauncher()
        launcher.start()

        options = Options()

        options.add_experimental_option(
            "debuggerAddress",
            "127.0.0.1:9222",
        )

        driver = webdriver.Edge(
            options=options,
        )

        return driver