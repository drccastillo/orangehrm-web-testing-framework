"""
Element Highlighter for visual debugging.
Extracted from BasePage following Single Responsibility Principle.
"""

import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.constants.visual_debugging import (
    BLINK_DELAY_SECONDS,
    DEFAULT_BLINK_COLOR,
    DEFAULT_BLINK_TIMES,
    DEFAULT_BORDER_WIDTH,
    DEFAULT_HIGHLIGHT_COLOR,
    DEFAULT_HIGHLIGHT_DURATION,
)


class ElementHighlighter:
    """
    Handles visual debugging operations for web elements.

    Responsibilities:
    - Highlight elements with borders and colors
    - Blink elements for attention
    - Manage visual debugging styling

    This class follows SRP by focusing solely on visual debugging,
    extracted from the God Class BasePage.
    """

    def __init__(self, driver: WebDriver):
        """
        Initialize the element highlighter.

        Args:
            driver: Selenium WebDriver instance for JavaScript execution
        """
        self.driver = driver

    def highlight_element(
        self,
        element: WebElement,
        duration: int | None = None,
        color: str | None = None,
        border: str | None = None,
    ) -> None:
        """
        Highlight an element on the page for visual debugging.

        Args:
            element: WebElement to highlight
            duration: Duration to highlight in seconds (default: 2)
            color: Border color for highlighting (default: "red")
            border: Border style (default: "3px solid")

        Example:
            >>> highlighter.highlight_element(element, duration=3, color="blue")
        """
        duration = duration or DEFAULT_HIGHLIGHT_DURATION
        color = color or DEFAULT_HIGHLIGHT_COLOR
        border = border or f"{DEFAULT_BORDER_WIDTH} solid"

        original_style = element.get_attribute("style")

        # Apply highlight style
        highlight_style = f"{original_style}; border: {border} {color} !important;"
        self._set_element_style(element, highlight_style)

        time.sleep(duration)

        # Restore original style
        self._set_element_style(element, original_style or "")

    def blink_element(
        self, element: WebElement, times: int | None = None, color: str | None = None
    ) -> None:
        """
        Blink an element multiple times for visual debugging.

        Args:
            element: WebElement to blink
            times: Number of times to blink (default: 3)
            color: Border color for blinking (default: "red")

        Example:
            >>> highlighter.blink_element(element, times=5, color="green")
        """
        times = times or DEFAULT_BLINK_TIMES
        color = color or DEFAULT_BLINK_COLOR

        original_style = element.get_attribute("style")

        for _ in range(times):
            # Highlight on
            highlight_style = (
                f"{original_style}; "
                f"border: {DEFAULT_BORDER_WIDTH} solid {color} !important; "
                f"background-color: yellow !important;"
            )
            self._set_element_style(element, highlight_style)
            time.sleep(BLINK_DELAY_SECONDS)

            # Highlight off
            self._set_element_style(element, original_style or "")
            time.sleep(BLINK_DELAY_SECONDS)

    def _set_element_style(self, element: WebElement, style: str) -> None:
        """
        Private helper method to set element style.

        Args:
            element: WebElement to modify
            style: CSS style string to apply
        """
        self.driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);", element, style
        )
