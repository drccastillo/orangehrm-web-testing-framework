"""
Base Page class implementing common functionality for all page objects.
Follows the Page Object Model design pattern.
"""

from typing import Any

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.element_highlighter import ElementHighlighter
from utils.exceptions import (
    ElementNotClickableException,
    ElementNotFoundException,
    InvalidParameterException,
)
from utils.logger import TestLogger


class BasePage:
    """
    Base class for all page objects.
    Provides common methods for interacting with web elements.
    """

    def __init__(
        self,
        driver: WebDriver,
        timeout: int = 10,
        highlighter: ElementHighlighter | None = None,
    ):
        """
        Initialize the base page.

        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout for explicit waits in seconds
            highlighter: Optional ElementHighlighter for visual debugging
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        self.logger = TestLogger.get_logger(self.__class__.__name__)
        self.highlighter = highlighter or ElementHighlighter(driver)

    def find_element(self, locator: tuple[str, str]) -> WebElement:
        """
        Find a single element using explicit wait.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            WebElement if found

        Raises:
            InvalidParameterException: If locator is None or invalid
            ElementNotFoundException: If element is not found within timeout
        """
        if not locator or not isinstance(locator, tuple) or len(locator) != 2:
            raise InvalidParameterException(
                "locator", locator, "Locator must be a tuple of (By.STRATEGY, 'value')"
            )

        try:
            element = self.wait.until(
                EC.presence_of_element_located(locator), message=f"Element not found: {locator}"
            )
            return element
        except TimeoutException as e:
            self.logger.error(f"Timeout waiting for element: {locator}")
            raise ElementNotFoundException(
                locator, f"Timeout waiting for element: {locator}"
            ) from e

    def find_elements(self, locator: tuple[str, str]) -> list[WebElement]:
        """
        Find multiple elements using explicit wait.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            List of WebElements (empty list if none found)

        Raises:
            InvalidParameterException: If locator is None or invalid
        """
        if not locator or not isinstance(locator, tuple) or len(locator) != 2:
            raise InvalidParameterException(
                "locator", locator, "Locator must be a tuple of (By.STRATEGY, 'value')"
            )

        try:
            elements = self.wait.until(
                EC.presence_of_all_elements_located(locator),
                message=f"Elements not found: {locator}",
            )
            return elements
        except TimeoutException:
            return []

    def click(self, locator: tuple[str, str]) -> None:
        """
        Click on an element after waiting for it to be clickable.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Raises:
            InvalidParameterException: If locator is None or invalid
            ElementNotClickableException: If element is not clickable

        Example:
            >>> page.click((By.ID, "submit-button"))
        """
        if not locator or not isinstance(locator, tuple) or len(locator) != 2:
            raise InvalidParameterException(
                "locator", locator, "Locator must be a tuple of (By.STRATEGY, 'value')"
            )

        try:
            element = self.wait.until(
                EC.element_to_be_clickable(locator), message=f"Element not clickable: {locator}"
            )
            element.click()
        except TimeoutException as e:
            self.logger.error(f"Element not clickable: {locator}")
            raise ElementNotClickableException(locator) from e

    def send_keys(self, locator: tuple[str, str], text: str, clear_first: bool = True) -> None:
        """
        Type text into an input field.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            text: Text to type
            clear_first: Whether to clear the field before typing

        Raises:
            InvalidParameterException: If text is None or empty
            ElementNotFoundException: If element is not found

        Example:
            >>> page.send_keys(page.USERNAME_INPUT, "admin")
        """
        if text is None or (isinstance(text, str) and not text.strip()):
            raise InvalidParameterException("text", text, "Text cannot be None or empty")

        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple[str, str]) -> str:
        """
        Get the text content of an element.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            Text content of the element

        Example:
            >>> error_text = page.get_text((By.CSS_SELECTOR, ".error-message"))
        """
        element = self.find_element(locator)
        return element.text

    def get_attribute(self, locator: tuple[str, str], attribute: str) -> str:
        """
        Get an attribute value from an element.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            attribute: Name of the attribute

        Returns:
            Value of the attribute

        Raises:
            InvalidParameterException: If attribute is None or empty
        """
        if not attribute or not isinstance(attribute, str):
            raise InvalidParameterException(
                "attribute", attribute, "Attribute name must be a non-empty string"
            )

        element = self.find_element(locator)
        return element.get_attribute(attribute)

    def is_element_visible(self, locator: tuple[str, str]) -> bool:
        """
        Check if an element is visible on the page.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element is visible, False otherwise

        Example:
            >>> if page.is_element_visible((By.ID, "error-message")):
            ...     print("Error displayed")
        """
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator: tuple[str, str]) -> bool:
        """
        Check if an element is present in the DOM.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element is present, False otherwise
        """
        try:
            self.find_element(locator)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_element_to_disappear(self, locator: tuple[str, str]) -> bool:
        """
        Wait for an element to disappear from the page.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element disappeared, False otherwise
        """
        try:
            self.wait.until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def get_current_url(self) -> str:
        """
        Get the current URL of the page.

        Returns:
            Current URL as string
        """
        return self.driver.current_url

    def get_page_title(self) -> str:
        """
        Get the title of the current page.

        Returns:
            Page title as string
        """
        return self.driver.title

    def refresh_page(self) -> None:
        """Refresh the current page."""
        self.driver.refresh()

    def navigate_to(self, url: str) -> None:
        """
        Navigate to a specific URL.

        Args:
            url: URL to navigate to

        Raises:
            InvalidParameterException: If URL is None or empty

        Example:
            >>> page.navigate_to("https://example.com")
        """
        if not url or not isinstance(url, str):
            raise InvalidParameterException("url", url, "URL must be a non-empty string")

        self.driver.get(url)

    def switch_to_frame(self, locator: tuple[str, str]) -> None:
        """
        Switch to an iframe.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
        """
        frame = self.find_element(locator)
        self.driver.switch_to.frame(frame)

    def switch_to_default_content(self) -> None:
        """Switch back to the main content from an iframe."""
        self.driver.switch_to.default_content()

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
                "script", script, "JavaScript code must be a non-empty string"
            )

        return self.driver.execute_script(script, *args)

    def scroll_to_element(self, locator: tuple[str, str]) -> None:
        """
        Scroll to an element on the page.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
        """
        element = self.find_element(locator)
        self.execute_script("arguments[0].scrollIntoView(true);", element)

    def highlight_element(
        self,
        locator: tuple[str, str],
        duration: int | None = None,
        color: str | None = None,
        border: str | None = None,
    ) -> None:
        """
        Highlight an element on the page for visual debugging.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            duration: Duration to highlight in seconds (default: 2)
            color: Border color for highlighting (default: "red")
            border: Border style (default: "3px solid")

        Example:
            >>> page.highlight_element(page.LOGIN_BUTTON, duration=3, color="blue")
        """
        element = self.find_element(locator)
        self.highlighter.highlight_element(element, duration=duration, color=color, border=border)

    def blink_element(
        self, locator: tuple[str, str], times: int | None = None, color: str | None = None
    ) -> None:
        """
        Blink an element multiple times for visual debugging.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            times: Number of times to blink (default: 3)
            color: Border color for blinking (default: "red")

        Example:
            >>> page.blink_element(page.SUBMIT_BUTTON, times=5, color="green")
        """
        element = self.find_element(locator)
        self.highlighter.blink_element(element, times=times, color=color)
