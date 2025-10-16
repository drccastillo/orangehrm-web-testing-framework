"""
PlaywrightBrowserAdapter: Adapter for Playwright Page to BrowserProtocol.

This adapter wraps Playwright Page and provides a unified interface
compatible with BrowserProtocol.
"""

from typing import Any

from playwright.sync_api import Page, Playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from src.adapters.playwright_element import PlaywrightWebElement
from src.core.element_protocol import WebElementProtocol
from src.core.browser_protocol import LocatorProtocol
from utils.exceptions import ElementNotFoundException, InvalidParameterException
from utils.logger import TestLogger


class PlaywrightBrowserAdapter:
    """
    Adapter for Playwright Page implementing BrowserProtocol.

    This adapter converts Playwright Page API to the unified BrowserProtocol,
    enabling framework-agnostic test code.

    Design Pattern:
        Adapter Pattern - Wraps Playwright Page to provide BrowserProtocol interface

    Attributes:
        page: Playwright Page instance
        timeout: Default timeout for operations in seconds
        logger: Logger instance for debugging
        playwright: Playwright instance (for cleanup)

    Example:
        >>> from playwright.sync_api import sync_playwright
        >>> pw = sync_playwright().start()
        >>> browser = pw.chromium.launch()
        >>> page = browser.new_page()
        >>> adapter = PlaywrightBrowserAdapter(page, timeout=10, playwright=pw)
        >>> adapter.navigate("https://example.com")
    """

    def __init__(self, page: Page, timeout: int = 10, playwright: Playwright | None = None):
        """
        Initialize the Playwright browser adapter.

        Args:
            page: Playwright Page instance
            timeout: Default timeout for operations in seconds
            playwright: Playwright instance (optional, for proper cleanup)
        """
        self._page = page
        self._playwright = playwright
        self._timeout_seconds = timeout
        self._timeout_ms = timeout * 1000  # Playwright uses milliseconds
        self._page.set_default_timeout(self._timeout_ms)
        self.logger = TestLogger.get_logger(self.__class__.__name__)

    @property
    def timeout(self) -> int:
        """Get the default timeout in seconds."""
        return self._timeout_seconds

    @timeout.setter
    def timeout(self, value: int) -> None:
        """
        Set the default timeout in seconds.

        Args:
            value: Timeout in seconds
        """
        self._timeout_seconds = value
        self._timeout_ms = value * 1000
        self._page.set_default_timeout(self._timeout_ms)

    def navigate(self, url: str) -> None:
        """
        Navigate to the specified URL.

        Args:
            url: Target URL to navigate to

        Raises:
            InvalidParameterException: If URL is None or empty
        """
        if not url or not isinstance(url, str):
            raise InvalidParameterException("url", url, "URL must be a non-empty string")

        self.logger.debug(f"Navigating to: {url}")
        self._page.goto(url)

    def find_element(self, locator: LocatorProtocol) -> WebElementProtocol:
        """
        Find a single element.

        Args:
            locator: LocatorProtocol value object

        Returns:
            WebElementProtocol: Wrapped Playwright locator

        Raises:
            ElementNotFoundException: If element is not found within timeout
        """
        native_selector = locator.to_native()

        try:
            pw_locator = self._page.locator(native_selector)
            # Wait for element to be present (attached to DOM)
            pw_locator.wait_for(state="attached", timeout=self._timeout_ms)
            self.logger.debug(f"Found element: {locator.description}")
            return PlaywrightWebElement(pw_locator)
        except PlaywrightTimeoutError as e:
            self.logger.error(f"Timeout waiting for element: {locator.description}")
            raise ElementNotFoundException(
                ("playwright", native_selector),
                f"Timeout waiting for element: {locator.description}",
            ) from e

    def find_elements(self, locator: LocatorProtocol) -> list[WebElementProtocol]:
        """
        Find all elements matching the locator.

        Args:
            locator: LocatorProtocol value object

        Returns:
            List of WebElementProtocol objects (empty list if none found)
        """
        native_selector = locator.to_native()

        try:
            pw_locator = self._page.locator(native_selector)
            # Get count of elements
            count = pw_locator.count()
            self.logger.debug(f"Found {count} elements: {locator.description}")

            if count == 0:
                return []

            # Return wrapped locators for each element
            return [PlaywrightWebElement(pw_locator.nth(i)) for i in range(count)]
        except Exception:
            self.logger.debug(f"No elements found: {locator.description}")
            return []

    def execute_script(self, script: str, *args: Any) -> Any:
        """
        Execute JavaScript code in the browser context.

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

        return self._page.evaluate(script, *args)

    def get_current_url(self) -> str:
        """
        Get the current page URL.

        Returns:
            Current URL as string
        """
        return self._page.url

    def get_title(self) -> str:
        """
        Get the current page title.

        Returns:
            Page title as string
        """
        return self._page.title()

    def refresh(self) -> None:
        """Refresh the current page."""
        self.logger.debug("Refreshing page")
        self._page.reload()

    def take_screenshot(self, path: str) -> bytes:
        """
        Take a screenshot of the current page.

        Args:
            path: File path to save the screenshot

        Returns:
            Screenshot as bytes
        """
        self.logger.debug(f"Taking screenshot: {path}")
        screenshot_bytes = self._page.screenshot(path=path)
        return screenshot_bytes

    def quit(self) -> None:
        """Close the browser and clean up resources."""
        self.logger.debug("Closing browser")
        # Close the page
        self._page.close()
        # Close the browser context if available
        if self._page.context:
            self._page.context.close()
        # Close the browser if available
        if self._page.context and self._page.context.browser:
            self._page.context.browser.close()
        # Close the Playwright instance if available
        if self._playwright:
            self._playwright.stop()
            self.logger.debug("Playwright instance stopped")

    def switch_to_frame(self, locator: LocatorProtocol) -> None:
        """
        Switch context to an iframe using Playwright's frame_locator.

        Args:
            locator: LocatorProtocol for the iframe element

        Note:
            In Playwright, frame switching is done using frame_locator().
            This method provides protocol compatibility. For actual iframe interaction,
            use page.frame_locator(selector) directly in your test code.
        """
        self.logger.debug(f"Frame context available for: {locator.description}")
        # Playwright uses frame_locator() - frame switching is implicit

    def switch_to_default_content(self) -> None:
        """
        Switch back to the main page content from an iframe.

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
        return self._page.content()

    def is_element_visible(self, locator: LocatorProtocol, timeout: int | None = None) -> bool:
        """
        Check if an element is visible on the page.

        Args:
            locator: LocatorProtocol value object
            timeout: Optional timeout in seconds

        Returns:
            True if element becomes visible within timeout, False otherwise
        """
        native_selector = locator.to_native()
        timeout_ms = (timeout * 1000) if timeout else self._timeout_ms

        try:
            pw_locator = self._page.locator(native_selector)
            pw_locator.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def is_element_hidden(self, locator: LocatorProtocol, timeout: int | None = None) -> bool:
        """
        Check if an element is hidden.

        Args:
            locator: LocatorProtocol value object
            timeout: Optional timeout in seconds

        Returns:
            True if element becomes hidden within timeout, False otherwise
        """
        native_selector = locator.to_native()
        timeout_ms = (timeout * 1000) if timeout else self._timeout_ms

        try:
            pw_locator = self._page.locator(native_selector)
            pw_locator.wait_for(state="hidden", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def is_element_present(self, locator: LocatorProtocol) -> bool:
        """
        Check if an element is present in the DOM.

        Args:
            locator: LocatorProtocol value object

        Returns:
            True if element is present, False otherwise
        """
        try:
            self.find_element(locator)
            return True
        except ElementNotFoundException:
            return False

    def wait_for_element_to_disappear(self, locator: LocatorProtocol) -> bool:
        """
        Wait for an element to disappear from the page.

        Args:
            locator: LocatorProtocol value object

        Returns:
            True if element disappeared, False otherwise
        """
        return self.is_element_hidden(locator)

    def scroll_to_element(self, locator: LocatorProtocol) -> None:
        """
        Scroll to an element on the page.

        Args:
            locator: LocatorProtocol value object
        """
        native_selector = locator.to_native()
        self._page.locator(native_selector).scroll_into_view_if_needed(timeout=self._timeout_ms)
