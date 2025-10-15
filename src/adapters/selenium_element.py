"""
Selenium WebElement adapter implementing WebElementProtocol.
Bridges Selenium-specific WebElement to framework-agnostic protocol.
"""

from typing import TYPE_CHECKING

from selenium.webdriver.remote.webelement import WebElement

if TYPE_CHECKING:
    from src.core.element_protocol import WebElementProtocol


class SeleniumWebElement:
    """
    Adapter for Selenium WebElement to WebElementProtocol.

    Wraps Selenium's WebElement and exposes framework-agnostic interface.

    Example:
        >>> from selenium import webdriver
        >>> driver = webdriver.Chrome()
        >>> raw_element = driver.find_element(By.ID, "username")
        >>> element = SeleniumWebElement(raw_element)
        >>> element.send_keys("admin")  # Uses protocol interface
        >>> element.click()

    Benefits:
    - Framework-agnostic operations
    - Easier testing with mocks
    - Prepares for unified BasePage in Phase 3
    """

    def __init__(self, element: WebElement):
        """
        Initialize Selenium element adapter.

        Args:
            element: Native Selenium WebElement instance
        """
        self._element = element

    def click(self) -> None:
        """
        Click the element.

        Uses Selenium's native click() method.
        """
        self._element.click()

    def send_keys(self, text: str) -> None:
        """
        Type text into element.

        Args:
            text: Text to type

        Note:
            Does NOT clear the field first. Use clear() before if needed.
        """
        self._element.send_keys(text)

    def clear(self) -> None:
        """
        Clear element content.

        Uses Selenium's native clear() method for input fields.
        """
        self._element.clear()

    def get_text(self) -> str:
        """
        Get element text content.

        Returns:
            Visible text content (Selenium's .text property)
        """
        return self._element.text

    def get_attribute(self, name: str) -> str | None:
        """
        Get element attribute value.

        Args:
            name: Attribute name (e.g., "value", "href", "class")

        Returns:
            Attribute value or None if attribute doesn't exist
        """
        return self._element.get_attribute(name)

    def is_visible(self) -> bool:
        """
        Check if element is visible.

        Returns:
            True if element is displayed, False otherwise
        """
        return self._element.is_displayed()

    def is_enabled(self) -> bool:
        """
        Check if element is enabled.

        Returns:
            True if element is enabled (not disabled), False otherwise
        """
        return self._element.is_enabled()

    def is_selected(self) -> bool:
        """
        Check if element is selected.

        Returns:
            True if element is selected (checkboxes/radio), False otherwise
        """
        return self._element.is_selected()

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"SeleniumWebElement({self._element})"


# Type check: Verify that SeleniumWebElement implements WebElementProtocol
def _verify_protocol_implementation(element: WebElement) -> None:
    """Compile-time check that adapter implements protocol."""
    _: WebElementProtocol = SeleniumWebElement(element)


# This will cause mypy/pyright to error if protocol not fully implemented
