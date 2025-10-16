"""
BrowserProtocol: Unified interface for browser automation frameworks.

This protocol defines a common interface that both Selenium and Playwright
adapters must implement, enabling framework-agnostic test code.
"""
# pylint: disable=unnecessary-ellipsis  # Ellipsis required in Protocol definitions

from typing import Any, Protocol, runtime_checkable

from src.core.element_protocol import WebElementProtocol


@runtime_checkable
class LocatorProtocol(Protocol):
    """
    Protocol for locator objects.

    Any class that has a to_native() method returning a string
    and a description attribute can be used as a locator.
    """

    description: str

    def to_native(self) -> str:
        """
        Convert locator to native format.

        Returns:
            Native selector string
        """
        ...


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

    def find_element(self, locator: LocatorProtocol) -> WebElementProtocol:
        """
        Find a single element on the page.

        Args:
            locator: LocatorProtocol value object (framework-agnostic)

        Returns:
            WebElementProtocol: Wrapped element that implements the protocol

        Raises:
            ElementNotFoundException: If element is not found within timeout

        Example:
            >>> element = browser.find_element(username_locator)
            >>> element.send_keys("admin")
        """
        ...

    def find_elements(self, locator: LocatorProtocol) -> list[WebElementProtocol]:
        """
        Find all elements matching the locator.

        Args:
            locator: LocatorProtocol value object

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

    def switch_to_frame(self, locator: LocatorProtocol) -> None:
        """
        Switch context to an iframe.

        Args:
            locator: LocatorProtocol for the iframe element

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

    def is_element_visible(self, locator: LocatorProtocol, timeout: int | None = None) -> bool:
        """
        Check if an element is visible on the page.

        Args:
            locator: LocatorProtocol value object
            timeout: Optional timeout in seconds (uses default if not specified)

        Returns:
            True if element becomes visible within timeout, False otherwise

        Example:
            >>> if browser.is_element_visible(error_message_locator):
            ...     print("Error message is displayed")
        """
        ...

    def is_element_hidden(self, locator: LocatorProtocol, timeout: int | None = None) -> bool:
        """
        Check if an element is hidden (not visible) on the page.

        Args:
            locator: LocatorProtocol value object
            timeout: Optional timeout in seconds (uses default if not specified)

        Returns:
            True if element becomes hidden within timeout, False otherwise

        Example:
            >>> if browser.is_element_hidden(spinner_locator):
            ...     print("Loading spinner has disappeared")
        """
        ...

    def is_element_present(self, locator: LocatorProtocol) -> bool:
        """
        Check if an element is present in the DOM (regardless of visibility).

        Args:
            locator: LocatorProtocol value object

        Returns:
            True if element is present in DOM, False otherwise

        Example:
            >>> if browser.is_element_present(submit_button_locator):
            ...     print("Submit button exists in DOM")
        """
        ...

    def wait_for_element_to_disappear(self, locator: LocatorProtocol) -> bool:
        """
        Wait for an element to disappear from the page.

        Args:
            locator: LocatorProtocol value object

        Returns:
            True if element disappeared within timeout, False otherwise

        Example:
            >>> browser.wait_for_element_to_disappear(loading_spinner_locator)
        """
        ...

    def scroll_to_element(self, locator: LocatorProtocol) -> None:
        """
        Scroll to bring an element into view.

        Args:
            locator: LocatorProtocol value object

        Example:
            >>> browser.scroll_to_element(footer_locator)
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
