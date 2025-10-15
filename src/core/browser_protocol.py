"""
BrowserProtocol: Unified interface for browser automation frameworks.

This protocol defines a common interface that both Selenium and Playwright
adapters must implement, enabling framework-agnostic test code.
"""
# pylint: disable=unnecessary-ellipsis  # Ellipsis required in Protocol definitions

from typing import Any, Protocol, runtime_checkable

from src.core.element_protocol import WebElementProtocol
from src.core.locator import Locator


@runtime_checkable
class BrowserProtocol(Protocol):
    """
    Protocol defining the interface for browser automation.

    This protocol provides a unified API that works with any automation framework
    (Selenium, Playwright, etc.) through the Adapter pattern.

    Design Pattern:
        - Protocol Pattern: Structural typing without inheritance
        - Adapter Pattern: Converts framework-specific APIs to common interface

    Example:
        >>> # Works with any browser implementation
        >>> def test_login(browser: BrowserProtocol):
        ...     browser.navigate("https://example.com")
        ...     element = browser.find_element(username_locator)
        ...     element.send_keys("admin")
    """

    def navigate(self, url: str) -> None:
        """
        Navigate to the specified URL.

        Args:
            url: Target URL to navigate to

        Raises:
            InvalidParameterException: If URL is None or empty

        Example:
            >>> browser.navigate("https://example.com")
        """
        ...

    def find_element(self, locator: Locator) -> WebElementProtocol:
        """
        Find a single element on the page.

        Args:
            locator: Locator value object (framework-agnostic)

        Returns:
            WebElementProtocol: Wrapped element that implements the protocol

        Raises:
            ElementNotFoundException: If element is not found within timeout

        Example:
            >>> element = browser.find_element(username_locator)
            >>> element.send_keys("admin")
        """
        ...

    def find_elements(self, locator: Locator) -> list[WebElementProtocol]:
        """
        Find all elements matching the locator.

        Args:
            locator: Locator value object

        Returns:
            List of WebElementProtocol objects (empty list if none found)

        Example:
            >>> buttons = browser.find_elements(button_locator)
            >>> for button in buttons:
            ...     print(button.get_text())
        """
        ...

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

        Example:
            >>> result = browser.execute_script("return document.title")
            >>> browser.execute_script("arguments[0].scrollIntoView();", element)
        """
        ...

    def get_current_url(self) -> str:
        """
        Get the current page URL.

        Returns:
            Current URL as string

        Example:
            >>> url = browser.get_current_url()
            >>> assert "dashboard" in url
        """
        ...

    def get_title(self) -> str:
        """
        Get the current page title.

        Returns:
            Page title as string

        Example:
            >>> title = browser.get_title()
            >>> assert "Dashboard" in title
        """
        ...

    def refresh(self) -> None:
        """
        Refresh the current page.

        Example:
            >>> browser.refresh()
        """
        ...

    def take_screenshot(self, path: str) -> bytes:
        """
        Take a screenshot of the current page.

        Args:
            path: File path to save the screenshot

        Returns:
            Screenshot as bytes

        Example:
            >>> browser.take_screenshot("screenshots/error.png")
        """
        ...

    def quit(self) -> None:
        """
        Close the browser and clean up resources.

        Example:
            >>> browser.quit()

        Note:
            This should be called in test teardown to ensure proper cleanup.
        """
        ...

    def switch_to_frame(self, locator: Locator) -> None:
        """
        Switch context to an iframe.

        Args:
            locator: Locator for the iframe element

        Example:
            >>> browser.switch_to_frame(iframe_locator)
            >>> # Now interacting with iframe content
        """
        ...

    def switch_to_default_content(self) -> None:
        """
        Switch back to the main page content from an iframe.

        Example:
            >>> browser.switch_to_frame(iframe_locator)
            >>> # ... interact with iframe ...
            >>> browser.switch_to_default_content()
        """
        ...

    def get_page_source(self) -> str:
        """
        Get the HTML source of the current page.

        Returns:
            HTML source as string

        Example:
            >>> source = browser.get_page_source()
            >>> assert "<html" in source
        """
        ...

    @property
    def timeout(self) -> int:
        """
        Get the default timeout for operations.

        Returns:
            Timeout in seconds
        """
        ...

    @timeout.setter
    def timeout(self, value: int) -> None:
        """
        Set the default timeout for operations.

        Args:
            value: Timeout in seconds
        """
        ...
