"""
Element Finder.

Finds browser elements using human-friendly names.
"""

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from infrastructure.browser.browser_session import BrowserSession


class ElementFinder:
    """
    Resolves natural element names into Selenium elements.
    """

    def __init__(
        self,
        session: BrowserSession,
    ) -> None:
        self._session = session

    def find(
        self,
        target: str,
        timeout: int = 10,
    ) -> WebElement:
        """
        Find an element using several strategies.
        """

        driver = self._session.driver

        strategies = [

            (By.ID, target),

            (By.NAME, target),

            (
                By.CSS_SELECTOR,
                f'[aria-label="{target}"]',
            ),

            (
                By.CSS_SELECTOR,
                f'[placeholder="{target}"]',
            ),

            (
                By.CSS_SELECTOR,
                f'[title="{target}"]',
            ),

            (
                By.CSS_SELECTOR,
                f'[data-testid="{target}"]',
            ),

            (
                By.XPATH,
                f'//*[normalize-space(text())="{target}"]',
            ),

            (
                By.XPATH,
                f'//*[contains(normalize-space(text()), "{target}")]',
            ),

            (
                By.XPATH,
                f'//*[@role="{target}"]',
            ),
        ]

        last_exception = None

        for by, value in strategies:

            try:

                return WebDriverWait(
                    driver,
                    timeout,
                ).until(
                    EC.presence_of_element_located(
                        (
                            by,
                            value,
                        )
                    )
                )

            except Exception as ex:
                last_exception = ex

        raise last_exception