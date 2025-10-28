"""
Simplified BasePage using Playwright Page directly.

This BasePage works exclusively with Playwright, eliminating unnecessary
adapter layers and providing direct access to Playwright's powerful API.

Design Pattern:
    - Single Responsibility: Interaction methods only
    - YAGNI Principle: Only what we need, no over-engineering
    - Leverages Playwright auto-waiting (no manual waits needed)
    - All locators are Playwright Locator instances
    - Direct Playwright API: Use locator.highlight() for debugging
    - Composition: NavigationHeader component for global navigation
"""

# pylint: disable=import-error  # utils and src modules are in project root
from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from src.ui.components.navigation_header import NavigationHeader
from utils.exceptions import ElementNotClickableException, InvalidParameterException
from utils.logger import TestLogger


class BasePage:
    """
    Simplified base class for all page objects using Playwright directly.

    This BasePage uses Playwright Page directly, eliminating adapter overhead
    and leveraging Playwright's built-in auto-waiting capabilities.

    All locators should be Playwright Locator instances created in page object __init__.
    No need for manual waits - Playwright auto-waits for actionability.

    Attributes:
        page: Playwright Page instance
        timeout: Default timeout for operations in seconds
        timeout_ms: Timeout in milliseconds (Playwright format)
        logger: Logger instance for this page
        nav_header: NavigationHeader component for global navigation (all pages)

    Example:
        >>> class LoginPage(BasePage):
        ...     def __init__(self, page: Page, timeout: int = 10):
        ...         super().__init__(page, timeout)
        ...         # Define locators using Playwright functional locators
        ...         self.username_input = page.get_by_placeholder("Username")
        ...         self.password_input = page.get_by_placeholder("Password")
        ...         self.login_button = page.get_by_role("button", name="Login")
        ...
        ...     def login(self, username: str, password: str):
        ...         self.send_keys(self.username_input, username)
        ...         self.send_keys(self.password_input, password)
        ...         self.click(self.login_button)

        >>> # Using NavigationHeader component (after login)
        >>> class DashboardPage(BasePage):
        ...     def go_to_leave(self):
        ...         self.nav_header.navigate_to_leave()  # Global navigation
    """

    def __init__(self, page: Page, timeout: int = 10):
        """
        Initialize the base page.

        Args:
            page: Playwright Page instance
            timeout: Default timeout for operations in seconds (default: 10)
        """
        self.page = page
        self.timeout = timeout
        self.timeout_ms = timeout * 1000  # Playwright uses milliseconds
        self.page.set_default_timeout(self.timeout_ms)
        self.logger = TestLogger.get_logger(self.__class__.__name__)

        # Global navigation component (available on all pages)
        # Note: LoginPage won't use this, but having it doesn't cause issues
        self.nav_header = NavigationHeader(page)

    def click(self, locator: Locator) -> None:
        """
        Click on an element.

        Playwright auto-waits for the element to be visible, enabled, and stable.

        Args:
            locator: Playwright Locator instance

        Raises:
            ElementNotClickableException: If element is not clickable within timeout

        Example:
            >>> # In your page object
            >>> self.login_button = page.get_by_role("button", name="Login")
            >>> self.click(self.login_button)
        """
        try:
            locator.click()
            self.logger.debug(f"Clicked element: {locator}")
        except PlaywrightTimeoutError as e:
            self.logger.error(f"Failed to click element: {locator}")
            raise ElementNotClickableException(str(locator)) from e

    def send_keys(self, locator: Locator, text: str, clear_first: bool = True) -> None:
        """
        Type text into an input field.

        Playwright auto-waits for the element to be editable.

        Args:
            locator: Playwright Locator instance
            text: Text to type
            clear_first: Whether to clear the field before typing (default: True)

        Raises:
            InvalidParameterException: If text is None or empty

        Example:
            >>> # In your page object
            >>> self.username_input = page.get_by_placeholder("Username")
            >>> self.send_keys(self.username_input, "admin")
        """
        if text is None or (isinstance(text, str) and not text.strip()):
            raise InvalidParameterException("text", text, "Text cannot be None or empty")

        if clear_first:
            locator.clear()
        locator.fill(text)
        self.logger.debug(f"Sent keys to element: {locator}")

    def get_text(self, locator: Locator) -> str:
        """
        Get the inner text content of an element.

        Args:
            locator: Playwright Locator instance

        Returns:
            Text content of the element

        Example:
            >>> # In your page object
            >>> self.welcome_message = page.get_by_role("heading")
            >>> text = self.get_text(self.welcome_message)
            >>> assert text == "Welcome"
        """
        text = locator.inner_text()
        self.logger.debug(f"Got text from element: {locator} -> {text}")
        return text

    def get_attribute(self, locator: Locator, attribute_name: str) -> str | None:
        """
        Get an attribute value from an element.

        Args:
            locator: Playwright Locator instance
            attribute_name: Name of the attribute (e.g., 'href', 'class', 'data-id')

        Returns:
            Attribute value or None if not found

        Example:
            >>> # Get href from a link
            >>> link = page.get_by_role("link", name="Documentation")
            >>> href = self.get_attribute(link, "href")
            >>> print(f"Link points to: {href}")
        """
        value = locator.get_attribute(attribute_name)
        self.logger.debug(f"Got attribute '{attribute_name}' from {locator} -> {value}")
        return value

    def get_value(self, locator: Locator) -> str:
        """
        Get the value of an input element.

        Args:
            locator: Playwright Locator instance (must be an input element)

        Returns:
            Current value of the input field

        Example:
            >>> # Get current value of username input
            >>> value = self.get_value(self.username_input)
            >>> assert value == "admin"
        """
        value = locator.input_value()
        self.logger.debug(f"Got value from input: {locator} -> {value}")
        return value

    def is_visible(self, locator: Locator) -> bool:
        """
        Check if an element is visible on the page.

        Args:
            locator: Playwright Locator instance

        Returns:
            True if visible, False otherwise

        Example:
            >>> if self.is_visible(self.error_message):
            ...     print("Error message is displayed")
        """
        return locator.is_visible()

    def is_enabled(self, locator: Locator) -> bool:
        """
        Check if an element is enabled (not disabled).

        Args:
            locator: Playwright Locator instance

        Returns:
            True if enabled, False otherwise

        Example:
            >>> if not self.is_enabled(self.submit_button):
            ...     print("Submit button is disabled")
        """
        return locator.is_enabled()

    def is_hidden(self, locator: Locator) -> bool:
        """
        Check if an element is hidden.

        Args:
            locator: Playwright Locator instance

        Returns:
            True if hidden, False otherwise
        """
        return locator.is_hidden()

    def count_elements(self, locator: Locator) -> int:
        """
        Count the number of elements matching the locator.

        Args:
            locator: Playwright Locator instance

        Returns:
            Number of matching elements

        Example:
            >>> # Count number of rows in a table
            >>> rows = page.locator(".table-row")
            >>> count = self.count_elements(rows)
            >>> print(f"Found {count} rows")
        """
        count = locator.count()
        self.logger.debug(f"Counted {count} elements for: {locator}")
        return count

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

    def scroll_to_element(self, locator: Locator) -> None:
        """
        Scroll to an element on the page.

        Playwright automatically scrolls elements into view before interaction,
        so this method is rarely needed. Use it only for explicit scroll requirements.

        Args:
            locator: Playwright Locator instance

        Example:
            >>> # Scroll to footer before taking screenshot
            >>> footer = page.get_by_role("contentinfo")
            >>> self.scroll_to_element(footer)
        """
        locator.scroll_into_view_if_needed(timeout=self.timeout_ms)
        self.logger.debug(f"Scrolled to element: {locator}")

    def take_screenshot(self, path: str) -> bytes:
        """
        Take a screenshot of the current page.

        Args:
            path: File path to save the screenshot

        Returns:
            Screenshot as bytes

        Example:
            >>> self.take_screenshot("screenshots/failure.png")
        """
        self.logger.info(f"Taking screenshot: {path}")
        screenshot_bytes = self.page.screenshot(path=path)
        return screenshot_bytes

    def get_page_source(self) -> str:
        """
        Get the HTML source of the current page.

        Returns:
            HTML source as string

        Example:
            >>> html = self.get_page_source()
            >>> assert "<title>Dashboard</title>" in html
        """
        return self.page.content()

    def select_option(
        self,
        locator: Locator,
        value: str | None = None,
        label: str | None = None,
        index: int | None = None,
    ) -> None:
        """
        Select an option from a dropdown (<select> element).

        Args:
            locator: Playwright Locator for the <select> element
            value: Option value to select (e.g., value="USA")
            label: Option label to select (e.g., "United States")
            index: Option index to select (0-based)

        Raises:
            InvalidParameterException: If none of value, label, or index is provided

        Example:
            >>> # Select by value
            >>> country_dropdown = page.get_by_label("Country")
            >>> self.select_option(country_dropdown, value="USA")

            >>> # Select by visible label
            >>> self.select_option(country_dropdown, label="United States")

            >>> # Select by index
            >>> self.select_option(country_dropdown, index=0)
        """
        if value:
            locator.select_option(value=value)
            self.logger.debug(f"Selected option by value: {value}")
        elif label:
            locator.select_option(label=label)
            self.logger.debug(f"Selected option by label: {label}")
        elif index is not None:
            locator.select_option(index=index)
            self.logger.debug(f"Selected option by index: {index}")
        else:
            raise InvalidParameterException(
                "value/label/index",
                None,
                "Must provide either value, label, or index",
            )

    def press_key(self, locator: Locator, key: str) -> None:
        """
        Press a keyboard key on an element.

        Args:
            locator: Playwright Locator instance
            key: Key to press (e.g., 'Enter', 'Tab', 'Escape', 'ArrowDown')

        Example:
            >>> # Press Enter after typing
            >>> self.send_keys(self.search_input, "test")
            >>> self.press_key(self.search_input, "Enter")

            >>> # Navigate with Tab
            >>> self.press_key(self.username_input, "Tab")
        """
        locator.press(key)
        self.logger.debug(f"Pressed key '{key}' on element: {locator}")

    def double_click(self, locator: Locator) -> None:
        """
        Double-click an element.

        Args:
            locator: Playwright Locator instance

        Example:
            >>> # Double-click to select text
            >>> self.double_click(self.text_field)
        """
        locator.dblclick()
        self.logger.debug(f"Double-clicked element: {locator}")

    def hover(self, locator: Locator) -> None:
        """
        Hover over an element.

        Args:
            locator: Playwright Locator instance

        Example:
            >>> # Hover to reveal dropdown menu
            >>> self.hover(self.menu_item)
        """
        locator.hover()
        self.logger.debug(f"Hovered over element: {locator}")

    def wait_for_url(self, url_pattern: str, timeout: int | None = None) -> None:
        """
        Wait for the page URL to match a pattern.

        Args:
            url_pattern: URL pattern (can be string or regex)
            timeout: Optional timeout in seconds (uses default if None)

        Example:
            >>> # Wait for navigation to dashboard
            >>> self.click(self.login_button)
            >>> self.wait_for_url("**/dashboard")
        """
        timeout_ms = (timeout or self.timeout) * 1000
        self.page.wait_for_url(url_pattern, timeout=timeout_ms)
        self.logger.debug(f"URL matched pattern: {url_pattern}")

    def get_page(self) -> Page:
        """
        Get the underlying Playwright Page instance for advanced operations.

        Use this when you need direct access to Playwright features not wrapped
        by BasePage methods (e.g., frame_locator, request interception, etc.).

        Returns:
            Playwright Page instance

        Example:
            >>> # Access frames directly
            >>> frame = self.get_page().frame_locator("#myframe")
            >>> frame.locator("button").click()

            >>> # Use expect assertions
            >>> from playwright.sync_api import expect
            >>> expect(self.get_page().locator(".title")).to_be_visible()
        """
        return self.page
