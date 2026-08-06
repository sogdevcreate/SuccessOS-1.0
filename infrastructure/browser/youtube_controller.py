"""
YouTube Controller.

Handles YouTube browser automation.
"""

from __future__ import annotations

import urllib.parse

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from infrastructure.browser.browser_session import BrowserSession


class YouTubeController:
    """
    Provides YouTube automation.
    """

    def __init__(
        self,
        session: BrowserSession,
    ) -> None:
        self._session = session

    def search(
        self,
        query: str,
    ) -> None:
        """
        Search YouTube.
        """

        driver = self._session.driver

        encoded = urllib.parse.quote_plus(
            query,
        )

        driver.get(
            f"https://www.youtube.com/results?search_query={encoded}"
        )

    def play(
        self,
        query: str,
    ) -> None:
        """
        Search YouTube and play the first result.
        """

        self.search(
            query,
        )

        driver = self._session.driver

        try:

            WebDriverWait(
                driver,
                20,
            ).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "a#video-title",
                    )
                )
            )

            video = self._first_video()

            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                video,
            )

            try:
                video.click()

            except StaleElementReferenceException:

                video = self._first_video()

                driver.execute_script(
                    "arguments[0].click();",
                    video,
                )

        except TimeoutException:

            raise RuntimeError(
                "Unable to locate a YouTube video."
            )

    def open_video(
        self,
        video_id: str,
    ) -> None:
        """
        Open a YouTube video.
        """

        self._session.driver.get(
            f"https://www.youtube.com/watch?v={video_id}"
        )

    def open_playlist(
        self,
        playlist_id: str,
    ) -> None:
        """
        Open a YouTube playlist.
        """

        self._session.driver.get(
            f"https://www.youtube.com/playlist?list={playlist_id}"
        )

    def open_channel(
        self,
        channel: str,
    ) -> None:
        """
        Open a YouTube channel.
        """

        self._session.driver.get(
            f"https://www.youtube.com/@{channel}"
        )

    def _first_video(
        self,
    ) -> WebElement:
        """
        Return the first search result.
        """

        driver = self._session.driver

        return driver.find_element(
            By.CSS_SELECTOR,
            "a#video-title",
        )