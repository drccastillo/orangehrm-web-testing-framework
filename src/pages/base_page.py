"""
Unified BasePage for all page objects.

This BasePage works with ANY automation framework (Selenium, Playwright, etc.)
through the BrowserProtocol interface, eliminating code duplication.

Design Pattern:
    - Single Responsibility: Interaction methods only
    - Adapter Pattern: Works with any browser via BrowserProtocol
    - Composition: Uses ElementHighlighter for visual debugging
"""

from typing import Any

from src.core.browser_protocol import BrowserProtocol
from src.core.element_protocol import WebElementProtocol
from src.core.locator import Locator
from src.utils.element_highlighter import ElementHighlighter
from utils.exceptions import (
    ElementNotClickableException,
    ElementNotFoundException,
    InvalidParameterException,
)
from utils.logger import TestLogger


class BasePage:
    """
    Unified base class for all page objects.

    This BasePage works with ANY automation framework through BrowserProtocol.
    Eliminates 90% duplication between Selenium and Playwright implementations.

    Attributes:
        browser: Browser adapter implementing BrowserProtocol
        timeout: Default timeout for operations in seconds
        highlighter: ElementHighlighter for visual debugging
        logger: Logger instance

    Example:
        >>> # Works with Selenium
        >>> selenium_browser = SeleniumBrowserAdapter(driver)
        >>> page = LoginPage(selenium_browser)
        >>> page.login("admin", "pass")

        >>> # Works with Playwright
        >>> playwright_browser = PlaywrightBrowserAdapter(page)
        >>> page = LoginPage(playwright_browser)
        >>> page.login("admin", "pass")
    """

    def __init__(
        self,
        browser: BrowserProtocol,
        timeout: int = 10,
        highlighter: ElementHighlighter | None = None,
    ):
        """
        Initialize the base page.

        Args:
            browser: Browser adapter implementing BrowserProtocol
            timeout: Default timeout for operations in seconds
            highlighter: Optional ElementHighlighter for visual debugging
        """
        self.browser = browser
        self.timeout = timeout
        self.logger = TestLogger.get_logger(self.__class__.__name__)
        # Highlighter will be initialized when needed (lazy loading)
        self._highlighter = highlighter

    @property
    def highlighter(self) -> ElementHighlighter:
        """Get or create ElementHighlighter (lazy loading)."""
        if self._highlighter is None:
            # Create highlighter based on browser type
            # ElementHighlighter will need to be updated to work with BrowserProtocol
            # For now, we'll create a placeholder
            self._highlighter = ElementHighlighter(self.browser)  # type: ignore[arg-type]
        return self._highlighter

    @highlighter.setter
    def highlighter(self, value: ElementHighlighter | None) -> None:
        """Set the highlighter."""
        self._highlighter = value

    def find_element(self, locator: Locator) -> WebElementProtocol:
        """
        Find a single element.

        Args:
            locator: Locator value object

        Returns:
            WebElementProtocol: Element that implements the protocol

        Raises:
            ElementNotFoundException: If element is not found within timeout

        Example:
            >>> element = page.find_element(username_locator)
            >>> element.send_keys("admin")
        """
        try:
            element = self.browser.find_element(locator)
            self.logger.debug(f"Found element: {locator.description}")
            return element
        except ElementNotFoundException:
            self.logger.error(f"Element not found: {locator.description}")
            raise

    def find_elements(self, locator: Locator) -> list[WebElementProtocol]:
        """
        Find all elements matching the locator.

        Args:
            locator: Locator value object

        Returns:
            List of WebElementProtocol objects (empty list if none found)

        Example:
            >>> buttons = page.find_elements(button_locator)
            >>> for button in buttons:
            ...     print(button.get_text())
        """
        elements = self.browser.find_elements(locator)
        self.logger.debug(f"Found {len(elements)} elements: {locator.description}")
        return elements

    def click(self, locator: Locator) -> None:
        """
        Click on an element.

        Args:
            locator: Locator value object

        Raises:
            ElementNotFoundException: If element is not found
            ElementNotClickableException: If element is not clickable

        Example:
            >>> page.click(LoginLocators.SUBMIT_BUTTON)
        """
        try:
            element = self.find_element(locator)
            element.click()
            self.logger.debug(f"Clicked element: {locator.description}")
        except Exception as e:
            self.logger.error(f"Failed to click element: {locator.description}")
            raise ElementNotClickableException(locator.to_native()) from e

    def send_keys(self, locator: Locator, text: str, clear_first: bool = True) -> None:
        """
        Type text into an input field.

        Args:
            locator: Locator value object
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
        self.logger.debug(f"Sent keys to element: {locator.description}")

    def get_text(self, locator: Locator) -> str:
        """
        Get the text content of an element.

        Args:
            locator: Locator value object

        Returns:
            Text content of the element

        Example:
            >>> error_text = page.get_text(LoginLocators.ERROR_MESSAGE)
        """
        element = self.find_element(locator)
        text = element.get_text()
        self.logger.debug(f"Got text from element: {locator.description} -> '{text}'")
        return text

    def get_attribute(self, locator: Locator, attribute: str) -> str | None:
        """
        Get an attribute value from an element.

        Args:
            locator: Locator value object
            attribute: Name of the attribute

        Returns:
            Value of the attribute or None

        Raises:
            InvalidParameterException: If attribute is None or empty
        """
        if not attribute or not isinstance(attribute, str):
            raise InvalidParameterException(
                "attribute", attribute, "Attribute name must be a non-empty string"
            )

        element = self.find_element(locator)
        value = element.get_attribute(attribute)
        self.logger.debug(f"Got attribute '{attribute}' from {locator.description} -> '{value}'")
        return value

    def is_element_visible(self, locator: Locator) -> bool:
        """
        Check if an element is visible on the page.

        Args:
            locator: Locator value object

        Returns:
            True if element is visible, False otherwise

        Example:
            >>> if page.is_element_visible(LoginLocators.ERROR_MESSAGE):
            ...     print("Error displayed")
        """
        try:
            element = self.find_element(locator)
            is_visible = element.is_visible()
            self.logger.debug(f"Element visible check: {locator.description} -> {is_visible}")
            return is_visible
        except ElementNotFoundException:
            return False

    def is_element_present(self, locator: Locator) -> bool:
        """
        Check if an element is present in the DOM.

        Args:
            locator: Locator value object

        Returns:
            True if element is present, False otherwise
        """
        try:
            self.find_element(locator)
            self.logger.debug(f"Element present: {locator.description}")
            return True
        except ElementNotFoundException:
            self.logger.debug(f"Element not present: {locator.description}")
            return False

    def get_current_url(self) -> str:
        """
        Get the current URL of the page.

        Returns:
            Current URL as string
        """
        return self.browser.get_current_url()

    def get_page_title(self) -> str:
        """
        Get the title of the current page.

        Returns:
            Page title as string
        """
        return self.browser.get_title()

    def refresh_page(self) -> None:
        """Refresh the current page."""
        self.logger.debug("Refreshing page")
        self.browser.refresh()

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

        self.logger.info(f"Navigating to: {url}")
        self.browser.navigate(url)

    def execute_script(self, script: str, *args: Any) -> Any:
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

        return self.browser.execute_script(script, *args)

    def scroll_to_element(self, locator: Locator) -> None:
        """
        Scroll to an element on the page.

        Args:
            locator: Locator value object
        """
        element = self.find_element(locator)
        self.execute_script("arguments[0].scrollIntoView(true);", element)
        self.logger.debug(f"Scrolled to element: {locator.description}")

    def take_screenshot(self, path: str) -> bytes:
        """
        Take a screenshot of the current page.

        Args:
            path: File path to save the screenshot

        Returns:
            Screenshot as bytes
        """
        self.logger.info(f"Taking screenshot: {path}")
        return self.browser.take_screenshot(path)

    def switch_to_frame(self, locator: Locator) -> None:
        """
        Switch context to an iframe.

        Args:
            locator: Locator for the iframe element
        """
        self.logger.debug(f"Switching to frame: {locator.description}")
        self.browser.switch_to_frame(locator)

    def switch_to_default_content(self) -> None:
        """Switch back to the main content from an iframe."""
        self.logger.debug("Switching to default content")
        self.browser.switch_to_default_content()

    def get_page_source(self) -> str:
        """
        Get the HTML source of the current page.

        Returns:
            HTML source as string
        """
        return self.browser.get_page_source()
