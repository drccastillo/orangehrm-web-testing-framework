"""
Simplified BasePage using Playwright Page directly.

This BasePage works exclusively with Playwright, eliminating unnecessary
adapter layers and providing direct access to Playwright's powerful API.

Design Pattern:
    - Single Responsibility: Interaction methods only
    - YAGNI Principle: No adapters, only what we need
    - Supports Playwright functional locators (get_by_role, get_by_label, etc.)
    - Direct Playwright API: Use locator.highlight() for debugging
"""

# pylint: disable=import-error  # utils module is in project root

from collections.abc import Callable
from typing import Any

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from utils.exceptions import (
    ElementNotClickableException,
    InvalidParameterException,
)
from utils.logger import TestLogger

# Type alias for locator flexibility
# Supports: Playwright Locator, string selector, or callable that returns Locator
LocatorType = Locator | str | Callable[[Page], Locator]


class BasePage:
    """
    Simplified base class for all page objects using Playwright directly.

    This BasePage uses Playwright Page directly, eliminating adapter overhead
    and providing access to the full Playwright API.

    Attributes:
        page: Playwright Page instance
        timeout: Default timeout for operations in seconds
        logger: Logger instance

    Example:
        >>> from playwright.sync_api import sync_playwright
        >>> with sync_playwright() as p:
        ...     browser = p.chromium.launch()
        ...     page = browser.new_page()
        ...     login_page = LoginPage(page, timeout=10)
        ...     login_page.login("admin", "pass")
    """

    def __init__(self, page: Page, timeout: int = 10):
        """
        Initialize the base page.

        Args:
            page: Playwright Page instance
            timeout: Default timeout for operations in seconds
        """
        self.page = page
        self.timeout = timeout
        self.timeout_ms = timeout * 1000  # Playwright uses milliseconds
        self.page.set_default_timeout(self.timeout_ms)
        self.logger = TestLogger.get_logger(self.__class__.__name__)

    def _resolve_locator(self, locator: LocatorType) -> Locator:
        """
        Resolve various locator types to a Playwright Locator.

        Supports:
            - Playwright Locator (returned as-is)
            - String selector (converted via page.locator())
            - Callable (executed with page to get Locator)

        Args:
            locator: Locator in any supported format

        Returns:
            Playwright Locator instance

        Example:
            >>> # String selector
            >>> loc = self._resolve_locator("button.submit")

            >>> # Callable (functional locator)
            >>> loc = self._resolve_locator(lambda page: page.get_by_role("button", name="Submit"))

            >>> # Already a Locator
            >>> existing_loc = page.locator("input")
            >>> loc = self._resolve_locator(existing_loc)
        """
        if isinstance(locator, Locator):
            # Already a Playwright Locator
            return locator
        if callable(locator):
            # Functional locator (e.g., lambda page: page.get_by_role(...))
            return locator(self.page)
        if isinstance(locator, str):
            # String selector (CSS, XPath, etc.)
            return self.page.locator(locator)
        raise InvalidParameterException(
            "locator",
            locator,
            "Locator must be a Playwright Locator, string selector, or callable",
        )

    def find_elements(self, locator: LocatorType) -> list[Locator]:
        """
        Find all elements matching the locator.

        Args:
            locator: Locator in any supported format

        Returns:
            List of Playwright Locator instances (empty list if none found)

        Example:
            >>> buttons = page.find_elements(lambda p: p.get_by_role("button"))
            >>> for button in buttons:
            ...     print(button.inner_text())
        """
        try:
            pw_locator = self._resolve_locator(locator)
            count = pw_locator.count()
            self.logger.debug(f"Found {count} elements: {locator}")

            if count == 0:
                return []

            return [pw_locator.nth(i) for i in range(count)]
        except Exception as e:
            self.logger.debug(f"No elements found: {locator} - {e}")
            return []

    def click(self, locator: LocatorType) -> None:
        """
        Click on an element.

        Args:
            locator: Locator in any supported format

        Raises:
            ElementNotFoundException: If element is not found
            ElementNotClickableException: If element is not clickable

        Example:
            >>> # Functional locator (recommended)
            >>> page.click(lambda p: p.get_by_role("button", name="Submit"))

            >>> # String selector
            >>> page.click("button[type='submit']")
        """
        try:
            pw_locator = self._resolve_locator(locator)
            pw_locator.click()
            self.logger.debug(f"Clicked element: {locator}")
        except PlaywrightTimeoutError as e:
            self.logger.error(f"Failed to click element: {locator}")
            raise ElementNotClickableException(str(locator)) from e

    def send_keys(self, locator: LocatorType, text: str, clear_first: bool = True) -> None:
        """
        Type text into an input field.

        Args:
            locator: Locator in any supported format
            text: Text to type
            clear_first: Whether to clear the field before typing

        Raises:
            InvalidParameterException: If text is None or empty
            ElementNotFoundException: If element is not found

        Example:
            >>> # Functional locator (recommended)
            >>> page.send_keys(lambda p: p.get_by_placeholder("Username"), "admin")

            >>> # String selector
            >>> page.send_keys("input[name='username']", "admin")
        """
        if text is None or (isinstance(text, str) and not text.strip()):
            raise InvalidParameterException("text", text, "Text cannot be None or empty")

        pw_locator = self._resolve_locator(locator)
        if clear_first:
            pw_locator.clear()
        pw_locator.fill(text)
        self.logger.debug(f"Sent keys to element: {locator}")

    def get_current_url(self) -> str:
        """
        Get the current URL of the page.

        Returns:
            Current URL as string
        """
        return self.page.url

    def get_page_title(self) -> str:
        """
        Get the title of the current page.

        Returns:
            Page title as string
        """
        return self.page.title()

    def refresh_page(self) -> None:
        """Refresh the current page."""
        self.logger.debug("Refreshing page")
        self.page.reload()

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
        self.page.goto(url)

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

        # Playwright's evaluate expects function format
        # Convert simple script to function if needed
        if not script.strip().startswith("(") and not script.strip().startswith("function"):
            # Wrap in function if it's a simple expression
            if "return" not in script:
                script = f"() => {{ return {script} }}"
            else:
                script = f"() => {{ {script} }}"

        return self.page.evaluate(script, *args)

    def scroll_to_element(self, locator: LocatorType) -> None:
        """
        Scroll to an element on the page.

        Args:
            locator: Locator in any supported format (Locator, str, or callable)
        """
        pw_locator = self._resolve_locator(locator)
        pw_locator.scroll_into_view_if_needed(timeout=self.timeout_ms)
        self.logger.debug(f"Scrolled to element: {locator}")

    def take_screenshot(self, path: str) -> bytes:
        """
        Take a screenshot of the current page.

        Args:
            path: File path to save the screenshot

        Returns:
            Screenshot as bytes
        """
        self.logger.info(f"Taking screenshot: {path}")
        screenshot_bytes = self.page.screenshot(path=path)
        return screenshot_bytes

    def switch_to_frame(self, locator: LocatorType) -> None:
        """
        Switch context to an iframe (note: Playwright uses frame_locator).

        Args:
            locator: Locator for the iframe element

        Note:
            In Playwright, frame switching is done using frame_locator().
            This method provides compatibility. For actual iframe interaction,
            use page.frame_locator(selector) directly in your test code.
        """
        self.logger.debug(f"Frame context available for: {locator}")
        # Playwright uses frame_locator() - frame switching is implicit

    def switch_to_default_content(self) -> None:
        """
        Switch back to the main content from an iframe.

        Note:
            In Playwright, switching back is implicit when using page.locator().
        """
        self.logger.debug("Switched to default content (implicit in Playwright)")

    def get_page_source(self) -> str:
        """
        Get the HTML source of the current page.

        Returns:
            HTML source as string
        """
        return self.page.content()
