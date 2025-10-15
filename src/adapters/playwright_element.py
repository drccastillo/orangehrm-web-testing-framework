"""
Playwright Locator adapter implementing WebElementProtocol.
Bridges Playwright-specific Locator to framework-agnostic protocol.
"""

from typing import TYPE_CHECKING

from playwright.sync_api import Locator

if TYPE_CHECKING:
    from src.core.element_protocol import WebElementProtocol


class PlaywrightWebElement:
    """
    Adapter for Playwright Locator to WebElementProtocol.

    Wraps Playwright's Locator and exposes framework-agnostic interface.

    Example:
        >>> from playwright.sync_api import sync_playwright
        >>> with sync_playwright() as p:
        ...     browser = p.chromium.launch()
        ...     page = browser.new_page()
        ...     raw_locator = page.locator("#username")
        ...     element = PlaywrightWebElement(raw_locator)
        ...     element.send_keys("admin")  # Uses protocol interface
        ...     element.click()

    Benefits:
    - Framework-agnostic operations
    - Easier testing with mocks
    - Prepares for unified BasePage in Phase 3
    """

    def __init__(self, locator: Locator):
        """
        Initialize Playwright element adapter.

        Args:
            locator: Native Playwright Locator instance
        """
        self._locator = locator

    def click(self) -> None:
        """
        Click the element.

        Uses Playwright's native click() method.
        """
        self._locator.click()

    def send_keys(self, text: str) -> None:
        """
        Type text into element.

        Args:
            text: Text to type

        Note:
            Uses Playwright's fill() which clears the field first.
            For append behavior, use type() instead (not in protocol).
        """
        self._locator.fill(text)

    def clear(self) -> None:
        """
        Clear element content.

        Uses Playwright's native clear() method for input fields.
        """
        self._locator.clear()

    def get_text(self) -> str:
        """
        Get element text content.

        Returns:
            Visible text content (Playwright's text_content())
        """
        return self._locator.text_content() or ""

    def get_attribute(self, name: str) -> str | None:
        """
        Get element attribute value.

        Args:
            name: Attribute name (e.g., "value", "href", "class")

        Returns:
            Attribute value or None if attribute doesn't exist
        """
        return self._locator.get_attribute(name)

    def is_visible(self) -> bool:
        """
        Check if element is visible.

        Returns:
            True if element is displayed, False otherwise
        """
        return self._locator.is_visible()

    def is_enabled(self) -> bool:
        """
        Check if element is enabled.

        Returns:
            True if element is enabled (not disabled), False otherwise
        """
        return self._locator.is_enabled()

    def is_selected(self) -> bool:
        """
        Check if element is selected.

        Returns:
            True if element is checked (checkboxes/radio), False otherwise

        Note:
            Playwright uses is_checked() for this operation.
        """
        return self._locator.is_checked()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"PlaywrightWebElement({self._locator})"


# Type check: Verify that PlaywrightWebElement implements WebElementProtocol
def _verify_protocol_implementation(locator: Locator) -> None:
    """Compile-time check that adapter implements protocol."""
    _: WebElementProtocol = PlaywrightWebElement(locator)


# This will cause mypy/pyright to error if protocol not fully implemented
