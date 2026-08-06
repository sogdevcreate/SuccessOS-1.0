"""
Browser Interaction.

Provides Selenium browser interaction.
"""

from __future__ import annotations

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from infrastructure.browser.browser_session import BrowserSession
from infrastructure.browser.element_finder import ElementFinder
from services.browser_interaction_service import (
    BrowserInteractionService,
)


class BrowserInteraction(BrowserInteractionService):
    """
    Selenium implementation of browser interaction.
    """

    def __init__(
        self,
        session: BrowserSession,
    ) -> None:
        self._session = session
        self._finder = ElementFinder(session)

    def click(
        self,
        selector: str,
    ) -> None:
        """
        Click an element.
        """

        element = self._finder.find(selector)
        element.click()

    def type(
        self,
        selector: str,
        text: str,
    ) -> None:
        """
        Type into an element.
        """

        element = self._finder.find(selector)
        element.clear()
        element.send_keys(text)

    def press(
        self,
        key: str,
    ) -> None:
        """
        Press a keyboard key.
        """

        self._session.driver.switch_to.active_element.send_keys(
            getattr(
                Keys,
                key.upper(),
            )
        )

    def wait_for(
        self,
        selector: str,
        timeout: int = 10,
    ) -> None:
        """
        Wait for an element.
        """

        self._finder.find(
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

        self._session.driver.execute_script(
            "window.scrollBy(0, arguments[0]);",
            pixels,
        )

    def select(
        self,
        selector: str,
        value: str,
    ) -> None:
        """
        Select an option.
        """

        Select(
            self._finder.find(selector)
        ).select_by_visible_text(
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

        self._finder.find(
            selector,
        ).send_keys(
            path,
        )

    def screenshot(
        self,
        path: str,
    ) -> None:
        """
        Save a screenshot.
        """

        self._session.driver.save_screenshot(
            path,
        )