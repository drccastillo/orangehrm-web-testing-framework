"""
Visual debugger component - responsible for visual debugging of elements.
Single Responsibility: Highlight and blink elements for debugging purposes.
"""
import time
from typing import Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from framework.utils.logger import TestLogger
from framework.config.defaults import FrameworkDefaults
from .element_finder import ElementFinder
from .javascript_executor import JavaScriptExecutor


class VisualDebugger:
    """
    Component responsible for visual debugging operations.

    Single Responsibility: Provide visual feedback for debugging (highlight, blink).
    """

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initialize the visual debugger.

        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout for operations
        """
        self.driver = driver
        self.timeout = timeout
        self.finder = ElementFinder(driver, timeout)
        self.js_executor = JavaScriptExecutor(driver, timeout)
        self.logger = TestLogger.get_logger(self.__class__.__name__)

        # Constants from FrameworkDefaults
        self.BLINK_DELAY_SECONDS = FrameworkDefaults.DEFAULT_BLINK_DELAY_SECONDS
        self.DEFAULT_BORDER_WIDTH = FrameworkDefaults.DEFAULT_BORDER_WIDTH
        self.DEFAULT_HIGHLIGHT_COLOR = FrameworkDefaults.DEFAULT_HIGHLIGHT_COLOR
        self.DEFAULT_BLINK_COLOR = FrameworkDefaults.DEFAULT_BLINK_COLOR
        self.DEFAULT_BLINK_TIMES = FrameworkDefaults.DEFAULT_BLINK_TIMES
        self.DEFAULT_HIGHLIGHT_DURATION = FrameworkDefaults.DEFAULT_HIGHLIGHT_DURATION

    def highlight_element(
        self,
        locator: Tuple[str, str],
        duration: int = None,
        color: str = None,
        border: str = None
    ) -> None:
        """
        Highlight an element on the page for visual debugging.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            duration: Duration to highlight in seconds (default: 2)
            color: Border color for highlighting (default: "red")
            border: Border style (default: "3px solid")

        Example:
            >>> debugger.highlight_element((By.ID, "login-button"), duration=3, color="blue")
        """
        duration = duration or self.DEFAULT_HIGHLIGHT_DURATION
        color = color or self.DEFAULT_HIGHLIGHT_COLOR
        border = border or f"{self.DEFAULT_BORDER_WIDTH} solid"

        element = self.finder.find_element(locator)
        original_style = element.get_attribute('style')

        # Apply highlight style
        highlight_style = f"{original_style}; border: {border} {color} !important;"
        self._set_element_style(element, highlight_style)

        self.logger.debug(f"Highlighting element: {locator} for {duration}s")
        time.sleep(duration)

        # Restore original style
        self._set_element_style(element, original_style or '')
        self.logger.debug(f"Highlight removed from element: {locator}")

    def blink_element(
        self,
        locator: Tuple[str, str],
        times: int = None,
        color: str = None
    ) -> None:
        """
        Blink an element multiple times for visual debugging.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            times: Number of times to blink (default: 3)
            color: Border color for blinking (default: "red")

        Example:
            >>> debugger.blink_element((By.ID, "submit-button"), times=5, color="green")
        """
        times = times or self.DEFAULT_BLINK_TIMES
        color = color or self.DEFAULT_BLINK_COLOR

        element = self.finder.find_element(locator)
        original_style = element.get_attribute('style')

        self.logger.debug(f"Blinking element: {locator} {times} times")

        for _ in range(times):
            # Highlight on
            highlight_style = (
                f"{original_style}; "
                f"border: {self.DEFAULT_BORDER_WIDTH} solid {color} !important; "
                f"background-color: yellow !important;"
            )
            self._set_element_style(element, highlight_style)
            time.sleep(self.BLINK_DELAY_SECONDS)

            # Highlight off
            self._set_element_style(element, original_style or '')
            time.sleep(self.BLINK_DELAY_SECONDS)

        self.logger.debug(f"Blink completed for element: {locator}")

    def highlight_multiple_elements(
        self,
        locators: list,
        duration: int = None,
        color: str = None
    ) -> None:
        """
        Highlight multiple elements simultaneously.

        Args:
            locators: List of locator tuples
            duration: Duration to highlight in seconds
            color: Border color for highlighting
        """
        duration = duration or self.DEFAULT_HIGHLIGHT_DURATION
        color = color or self.DEFAULT_HIGHLIGHT_COLOR

        self.logger.debug(f"Highlighting {len(locators)} elements")

        elements_and_styles = []
        for locator in locators:
            element = self.finder.find_element(locator)
            original_style = element.get_attribute('style')
            elements_and_styles.append((element, original_style))

            # Apply highlight
            highlight_style = f"{original_style}; border: {self.DEFAULT_BORDER_WIDTH} solid {color} !important;"
            self._set_element_style(element, highlight_style)

        time.sleep(duration)

        # Restore all original styles
        for element, original_style in elements_and_styles:
            self._set_element_style(element, original_style or '')

        self.logger.debug("Highlight removed from all elements")

    def flash_background(self, locator: Tuple[str, str], color: str = "yellow", times: int = 3) -> None:
        """
        Flash the background color of an element.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            color: Background color to flash
            times: Number of times to flash
        """
        element = self.finder.find_element(locator)
        original_style = element.get_attribute('style')

        self.logger.debug(f"Flashing background of element: {locator}")

        for _ in range(times):
            # Flash on
            flash_style = f"{original_style}; background-color: {color} !important;"
            self._set_element_style(element, flash_style)
            time.sleep(self.BLINK_DELAY_SECONDS)

            # Flash off
            self._set_element_style(element, original_style or '')
            time.sleep(self.BLINK_DELAY_SECONDS)

        self.logger.debug("Background flash completed")

    def outline_element(self, locator: Tuple[str, str], color: str = "red", width: str = "3px") -> None:
        """
        Add a permanent outline to an element (until page refresh).

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            color: Outline color
            width: Outline width
        """
        element = self.finder.find_element(locator)
        self.js_executor.execute_script(
            f"arguments[0].style.outline = '{width} solid {color}';",
            element
        )
        self.logger.debug(f"Outlined element: {locator}")

    def _set_element_style(self, element: WebElement, style: str) -> None:
        """
        Private helper method to set element style.

        Args:
            element: WebElement to modify
            style: CSS style string to apply
        """
        self.js_executor.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);",
            element,
            style
        )
