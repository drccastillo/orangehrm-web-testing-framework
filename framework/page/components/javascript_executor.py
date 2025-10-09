"""
JavaScript executor component - responsible for executing JavaScript on the page.
Single Responsibility: Execute JavaScript code and perform script-based operations.
"""
from typing import Tuple, Any
from selenium.webdriver.remote.webdriver import WebDriver
from framework.utils.logger import TestLogger
from framework.utils.exceptions import InvalidParameterException
from .element_finder import ElementFinder


class JavaScriptExecutor:
    """
    Component responsible for executing JavaScript code.

    Single Responsibility: Execute JavaScript and perform script-based operations.
    """

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initialize the JavaScript executor.

        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout for operations
        """
        self.driver = driver
        self.timeout = timeout
        self.finder = ElementFinder(driver, timeout)
        self.logger = TestLogger.get_logger(self.__class__.__name__)

    def execute_script(self, script: str, *args) -> Any:
        """
        Execute JavaScript code.

        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script

        Returns:
            Result of the JavaScript execution

        Raises:
            InvalidParameterException: If script is None or empty
        """
        if not script or not isinstance(script, str):
            raise InvalidParameterException(
                "script",
                script,
                "JavaScript code must be a non-empty string"
            )

        self.logger.debug(f"Executing JavaScript: {script[:50]}...")
        result = self.driver.execute_script(script, *args)
        self.logger.debug("JavaScript execution completed")
        return result

    def execute_async_script(self, script: str, *args) -> Any:
        """
        Execute asynchronous JavaScript code.

        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script

        Returns:
            Result of the JavaScript execution
        """
        if not script or not isinstance(script, str):
            raise InvalidParameterException(
                "script",
                script,
                "JavaScript code must be a non-empty string"
            )

        self.logger.debug(f"Executing async JavaScript: {script[:50]}...")
        result = self.driver.execute_async_script(script, *args)
        self.logger.debug("Async JavaScript execution completed")
        return result

    def scroll_to_element(self, locator: Tuple[str, str]) -> None:
        """
        Scroll to an element on the page.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
        """
        self.logger.debug(f"Scrolling to element: {locator}")
        element = self.finder.find_element(locator)
        self.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.debug(f"Scrolled to element: {locator}")

    def scroll_to_top(self) -> None:
        """Scroll to the top of the page."""
        self.logger.debug("Scrolling to top of page")
        self.execute_script("window.scrollTo(0, 0);")
        self.logger.debug("Scrolled to top")

    def scroll_to_bottom(self) -> None:
        """Scroll to the bottom of the page."""
        self.logger.debug("Scrolling to bottom of page")
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.logger.debug("Scrolled to bottom")

    def scroll_by_pixels(self, x: int, y: int) -> None:
        """
        Scroll by specific pixel amount.

        Args:
            x: Horizontal scroll amount
            y: Vertical scroll amount
        """
        self.logger.debug(f"Scrolling by pixels: x={x}, y={y}")
        self.execute_script(f"window.scrollBy({x}, {y});")
        self.logger.debug("Scroll completed")

    def click_element_via_js(self, locator: Tuple[str, str]) -> None:
        """
        Click an element using JavaScript (useful for hidden/obscured elements).

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
        """
        self.logger.debug(f"Clicking element via JavaScript: {locator}")
        element = self.finder.find_element(locator)
        self.execute_script("arguments[0].click();", element)
        self.logger.debug(f"Clicked element via JavaScript: {locator}")

    def set_element_value(self, locator: Tuple[str, str], value: str) -> None:
        """
        Set an element's value using JavaScript.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            value: Value to set
        """
        self.logger.debug(f"Setting element value via JavaScript: {locator}")
        element = self.finder.find_element(locator)
        self.execute_script(f"arguments[0].value = '{value}';", element)
        self.logger.debug(f"Set element value: {locator}")

    def get_element_property(self, locator: Tuple[str, str], property_name: str) -> Any:
        """
        Get an element's property using JavaScript.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            property_name: Name of the property

        Returns:
            Value of the property
        """
        element = self.finder.find_element(locator)
        return self.execute_script(f"return arguments[0].{property_name};", element)

    def remove_element_attribute(self, locator: Tuple[str, str], attribute: str) -> None:
        """
        Remove an attribute from an element.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            attribute: Attribute name to remove
        """
        self.logger.debug(f"Removing attribute '{attribute}' from element: {locator}")
        element = self.finder.find_element(locator)
        self.execute_script(f"arguments[0].removeAttribute('{attribute}');", element)
        self.logger.debug(f"Removed attribute '{attribute}' from element: {locator}")

    def set_element_attribute(self, locator: Tuple[str, str], attribute: str, value: str) -> None:
        """
        Set an attribute on an element.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            attribute: Attribute name
            value: Attribute value
        """
        self.logger.debug(f"Setting attribute '{attribute}' on element: {locator}")
        element = self.finder.find_element(locator)
        self.execute_script(f"arguments[0].setAttribute('{attribute}', '{value}');", element)
        self.logger.debug(f"Set attribute '{attribute}' on element: {locator}")
