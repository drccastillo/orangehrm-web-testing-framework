"""
Base Page class for Playwright implementing common functionality for all page objects.
Follows the Page Object Model design pattern.
"""

import time
from typing import Any

from playwright.sync_api import Locator, Page, expect

from utils.exceptions import (
    ElementNotClickableException,
    ElementNotFoundException,
    InvalidParameterException,
)
from utils.logger import TestLogger


class BasePagePW:
    """
    Base class for all Playwright page objects.
    Provides common methods for interacting with web elements using Playwright.
    """

    # Constants for visual debugging
    BLINK_DELAY_SECONDS = 0.2
    DEFAULT_BORDER_WIDTH = "3px"
    DEFAULT_HIGHLIGHT_COLOR = "red"
    DEFAULT_BLINK_COLOR = "red"
    DEFAULT_BLINK_TIMES = 3
    DEFAULT_HIGHLIGHT_DURATION = 2

    def __init__(self, page: Page, timeout: int = 10):
        """
        Initialize the base page.

        Args:
            page: Playwright Page instance
            timeout: Default timeout for operations in seconds
        """
        self.page = page
        self.timeout = timeout * 1000  # Playwright uses milliseconds
        self.page.set_default_timeout(self.timeout)
        self.logger = TestLogger.get_logger(self.__class__.__name__)

    def get_locator(self, locator: str) -> Locator:
        """
        Get a Playwright Locator object.

        Args:
            locator: String selector (CSS, XPath, text, etc.)

        Returns:
            Playwright Locator object

        Raises:
            InvalidParameterException: If locator is None or invalid
        """
        if not locator or not isinstance(locator, str):
            raise InvalidParameterException(
                "locator", locator, "Locator must be a non-empty string"
            )

        return self.page.locator(locator)

    def click(self, locator: str, force: bool = False) -> None:
        """
        Click on an element.
        Playwright auto-waits for element to be clickable.

        Args:
            locator: String selector
            force: Force click even if element is not ready (default: False)

        Raises:
            InvalidParameterException: If locator is None or invalid
            ElementNotClickableException: If element is not clickable

        Example:
            >>> page.click("button[type='submit']")
        """
        if not locator or not isinstance(locator, str):
            raise InvalidParameterException(
                "locator", locator, "Locator must be a non-empty string"
            )

        try:
            self.page.locator(locator).click(force=force, timeout=self.timeout)
        except Exception as e:
            self.logger.error(f"Element not clickable: {locator}")
            raise ElementNotClickableException(("playwright", locator)) from e

    def fill(self, locator: str, text: str, clear_first: bool = True) -> None:
        """
        Fill text into an input field.
        Playwright's fill() automatically clears the field first.

        Args:
            locator: String selector
            text: Text to type (can be empty string for validation testing)
            clear_first: Whether to clear the field before typing (default: True)

        Raises:
            InvalidParameterException: If text is None
            ElementNotFoundException: If element is not found

        Example:
            >>> page.fill("input[name='username']", "admin")
            >>> page.fill("input[name='username']", "")  # Valid: for testing empty field validation
        """
        if text is None:
            raise InvalidParameterException("text", text, "Text cannot be None")

        try:
            if clear_first:
                self.page.locator(locator).fill(text, timeout=self.timeout)
            else:
                self.page.locator(locator).press_sequentially(text, timeout=self.timeout)
        except Exception as e:
            self.logger.error(f"Failed to fill element: {locator}")
            raise ElementNotFoundException(
                ("playwright", locator), f"Element not found: {locator}"
            ) from e

    def clear(self, locator: str) -> None:
        """
        Clear an input field.
        Uses keyboard shortcuts (Ctrl+A + Backspace) for reliable clearing.

        Args:
            locator: String selector

        Example:
            >>> page.clear("input[name='username']")

        Note:
            This method uses keyboard shortcuts instead of Playwright's clear() method
            because some applications (like OrangeHRM) have JavaScript that prevents
            the default clear behavior.
        """
        try:
            element = self.page.locator(locator)
            # Click to focus the element
            element.click(timeout=self.timeout)
            # Select all and delete using keyboard shortcuts
            self.page.keyboard.press("Control+A")
            self.page.keyboard.press("Backspace")
        except Exception as e:
            self.logger.error(f"Failed to clear element: {locator}")
            raise ElementNotFoundException(
                ("playwright", locator), f"Element not found: {locator}"
            ) from e

    def type(self, locator: str, text: str, delay: int = 0) -> None:
        """
        Type text into an input field with optional delay between keystrokes.
        Uses Playwright's modern press_sequentially() API.

        Args:
            locator: String selector
            text: Text to type
            delay: Delay between keystrokes in milliseconds (default: 0)

        Raises:
            InvalidParameterException: If text is None

        Example:
            >>> page.type("input[name='search']", "playwright", delay=100)

        Note:
            This method uses press_sequentially() which is the modern Playwright API.
            For simple text input without delays, use fill() instead (faster).
        """
        if text is None:
            raise InvalidParameterException("text", text, "Text cannot be None")

        self.page.locator(locator).press_sequentially(text, delay=delay, timeout=self.timeout)

    def get_text(self, locator: str) -> str:
        """
        Get the text content of an element.

        Args:
            locator: String selector

        Returns:
            Text content of the element

        Example:
            >>> error_text = page.get_text(".error-message")
        """
        try:
            text = self.page.locator(locator).text_content(timeout=self.timeout)
            return text or ""
        except Exception as e:
            self.logger.error(f"Failed to get text from element: {locator}")
            raise ElementNotFoundException(
                ("playwright", locator), f"Element not found: {locator}"
            ) from e

    def get_inner_text(self, locator: str) -> str:
        """
        Get the inner text of an element (visible text only).

        Args:
            locator: String selector

        Returns:
            Inner text of the element
        """
        return self.page.locator(locator).inner_text(timeout=self.timeout)

    def get_attribute(self, locator: str, attribute: str) -> str | None:
        """
        Get an attribute value from an element.

        Args:
            locator: String selector
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

        return self.page.locator(locator).get_attribute(attribute, timeout=self.timeout)

    def get_input_value(self, locator: str) -> str:
        """
        Get the current value of an input field.
        This method correctly retrieves the value property (not attribute) of input elements.

        Args:
            locator: String selector

        Returns:
            Value of the input field (empty string if no value)

        Example:
            >>> username_value = page.get_input_value("input[name='username']")

        Note:
            For input fields, use this method instead of get_attribute('value').
            Input values are stored as JavaScript properties, not HTML attributes.
        """
        return self.page.locator(locator).input_value(timeout=self.timeout)

    def is_visible(self, locator: str, timeout: int | None = None) -> bool:
        """
        Check if an element is visible on the page.
        Uses Playwright's wait_for with state='visible' for auto-waiting.

        Args:
            locator: String selector
            timeout: Optional timeout in milliseconds

        Returns:
            True if element becomes visible within timeout, False otherwise

        Example:
            >>> if page.is_visible(".error-message"):
            ...     print("Error displayed")

        Note:
            This method uses Playwright's wait_for with auto-waiting.
            It will wait up to `timeout` ms for the element to become visible.
        """
        try:
            timeout_ms = timeout if timeout else self.timeout
            # Use wait_for with state='visible' for proper auto-waiting
            self.page.locator(locator).wait_for(state="visible", timeout=timeout_ms)
            return True
        except Exception:
            # Element not found or timeout
            return False

    def is_hidden(self, locator: str, timeout: int | None = None) -> bool:
        """
        Check if an element is hidden.
        Uses Playwright's wait_for with state='hidden' for auto-waiting.

        Args:
            locator: String selector
            timeout: Optional timeout in milliseconds

        Returns:
            True if element becomes hidden within timeout, False otherwise

        Note:
            This method uses Playwright's wait_for with auto-waiting.
            It will wait up to `timeout` ms for the element to become hidden.
        """
        try:
            timeout_ms = timeout if timeout else self.timeout
            # Use wait_for with state='hidden' for proper auto-waiting
            self.page.locator(locator).wait_for(state="hidden", timeout=timeout_ms)
            return True
        except Exception:
            # Element not found or timeout
            return False

    def is_enabled(self, locator: str) -> bool:
        """
        Check if an element is enabled.

        Args:
            locator: String selector

        Returns:
            True if element is enabled, False otherwise
        """
        return self.page.locator(locator).is_enabled(timeout=self.timeout)

    def is_disabled(self, locator: str) -> bool:
        """
        Check if an element is disabled.

        Args:
            locator: String selector

        Returns:
            True if element is disabled, False otherwise
        """
        return self.page.locator(locator).is_disabled(timeout=self.timeout)

    def navigate_to(self, url: str) -> None:
        """
        Navigate to a specific URL.
        Relies on Playwright's auto-waiting for subsequent element interactions.

        Args:
            url: URL to navigate to

        Raises:
            InvalidParameterException: If URL is None or empty

        Example:
            >>> page.navigate_to("https://example.com")
            >>> # Playwright auto-waits on next action
            >>> page.click("button")  # auto-waits for button to be ready

        Note:
            This uses Playwright's default wait_until="load" behavior.
            After navigation, use expect() or element actions which have built-in auto-waiting.
            Avoid using wait_until="networkidle" - instead wait for specific elements.
        """
        if not url or not isinstance(url, str):
            raise InvalidParameterException("url", url, "URL must be a non-empty string")

        self.page.goto(url)

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

        return self.page.evaluate(script, *args)

    def scroll_to_element(self, locator: str) -> None:
        """
        Scroll to an element on the page.

        Args:
            locator: String selector
        """
        self.page.locator(locator).scroll_into_view_if_needed(timeout=self.timeout)

    def screenshot(self, path: str, full_page: bool = False) -> bytes:
        """
        Take a screenshot of the page or element.

        Args:
            path: File path to save screenshot
            full_page: Capture full scrollable page (default: False)

        Returns:
            Screenshot bytes
        """
        return self.page.screenshot(path=path, full_page=full_page)

    def highlight_element(
        self, locator: str, duration: int = None, color: str = None, border: str = None
    ) -> None:
        """
        Highlight an element on the page for visual debugging.

        Args:
            locator: String selector
            duration: Duration to highlight in seconds (default: 2)
            color: Border color for highlighting (default: "red")
            border: Border style (default: "3px solid")

        Example:
            >>> page.highlight_element("button[type='submit']", duration=3, color="blue")
        """
        duration = duration or self.DEFAULT_HIGHLIGHT_DURATION
        color = color or self.DEFAULT_HIGHLIGHT_COLOR
        border = border or f"{self.DEFAULT_BORDER_WIDTH} solid"

        element = self.page.locator(locator)

        # Get original style
        original_style = element.get_attribute("style") or ""

        # Apply highlight style
        highlight_style = f"{original_style}; border: {border} {color} !important;"
        element.evaluate(f"element => element.setAttribute('style', '{highlight_style}')")

        time.sleep(duration)

        # Restore original style
        element.evaluate(f"element => element.setAttribute('style', '{original_style}')")

    def blink_element(self, locator: str, times: int = None, color: str = None) -> None:
        """
        Blink an element multiple times for visual debugging.

        Args:
            locator: String selector
            times: Number of times to blink (default: 3)
            color: Border color for blinking (default: "red")

        Example:
            >>> page.blink_element("button[type='submit']", times=5, color="green")
        """
        times = times or self.DEFAULT_BLINK_TIMES
        color = color or self.DEFAULT_BLINK_COLOR

        element = self.page.locator(locator)
        original_style = element.get_attribute("style") or ""

        for _ in range(times):
            # Highlight on
            highlight_style = (
                f"{original_style}; "
                f"border: {self.DEFAULT_BORDER_WIDTH} solid {color} !important; "
                f"background-color: yellow !important;"
            )
            element.evaluate(f"element => element.setAttribute('style', '{highlight_style}')")
            time.sleep(self.BLINK_DELAY_SECONDS)

            # Highlight off
            element.evaluate(f"element => element.setAttribute('style', '{original_style}')")
            time.sleep(self.BLINK_DELAY_SECONDS)

    def expect_element(self, locator: str):
        """
        Get Playwright's expect assertions for an element.

        Args:
            locator: String selector

        Returns:
            Playwright expect object for assertions

        Example:
            >>> page.expect_element("h1").to_be_visible()
            >>> page.expect_element(".error").to_contain_text("Invalid")
        """
        return expect(self.page.locator(locator))

    def press_key(self, locator: str, key: str) -> None:
        """
        Press a key on an element.

        Args:
            locator: String selector
            key: Key to press (e.g., "Enter", "Escape", "Tab")

        Example:
            >>> page.press_key("input[name='search']", "Enter")
        """
        self.page.locator(locator).press(key, timeout=self.timeout)

    def select_option(
        self,
        locator: str,
        value: str | None = None,
        label: str | None = None,
        index: int | None = None,
    ) -> None:
        """
        Select an option in a dropdown.

        Args:
            locator: String selector for the select element
            value: Option value to select
            label: Option label to select
            index: Option index to select

        Raises:
            InvalidParameterException: If no selection parameter is provided

        Example:
            >>> page.select_option("select#country", value="US")
            >>> page.select_option("select#country", label="United States")
            >>> page.select_option("select#country", index=0)
        """
        if value is not None:
            self.page.locator(locator).select_option(value=value, timeout=self.timeout)
        elif label is not None:
            self.page.locator(locator).select_option(label=label, timeout=self.timeout)
        elif index is not None:
            self.page.locator(locator).select_option(index=index, timeout=self.timeout)
        else:
            raise InvalidParameterException(
                "select_option",
                None,
                "At least one of 'value', 'label', or 'index' must be provided",
            )

    def check(self, locator: str) -> None:
        """
        Check a checkbox or radio button.

        Args:
            locator: String selector
        """
        self.page.locator(locator).check(timeout=self.timeout)

    def uncheck(self, locator: str) -> None:
        """
        Uncheck a checkbox.

        Args:
            locator: String selector
        """
        self.page.locator(locator).uncheck(timeout=self.timeout)

    def is_checked(self, locator: str) -> bool:
        """
        Check if a checkbox or radio button is checked.

        Args:
            locator: String selector

        Returns:
            True if checked, False otherwise
        """
        return self.page.locator(locator).is_checked(timeout=self.timeout)

    def get_current_url(self) -> str:
        """
        Get the current page URL.

        Returns:
            Current page URL as string

        Example:
            >>> current_url = page.get_current_url()
            >>> assert "dashboard" in current_url
        """
        return self.page.url
