"""
Protocol for web element abstraction across automation frameworks.
Enables framework-agnostic element interactions.
"""

# pylint: disable=unnecessary-ellipsis

from typing import Protocol, runtime_checkable


@runtime_checkable
class WebElementProtocol(Protocol):
    """
    Protocol for interacting with web elements across frameworks.

    This protocol defines a common interface that both Selenium WebElement
    and Playwright Locator can implement via adapter classes.

    Benefits:
    - Framework-agnostic element operations
    - Enables unified BasePage in Phase 3
    - Easy to add new frameworks
    - Type-safe element interactions
    """

    def click(self) -> None:
        """
        Click the element.

        Raises:
            ElementNotClickableException: If element cannot be clicked
        """
        ...

    def send_keys(self, text: str) -> None:
        """
        Type text into element.

        Args:
            text: Text to type

        Raises:
            InvalidParameterException: If text is empty
            ElementNotFoundException: If element not found
        """
        ...

    def clear(self) -> None:
        """
        Clear element content.

        Used for input fields before typing new text.
        """
        ...

    def get_text(self) -> str:
        """
        Get element text content.

        Returns:
            Visible text content of the element
        """
        ...

    def get_attribute(self, name: str) -> str | None:
        """
        Get element attribute value.

        Args:
            name: Attribute name (e.g., "value", "href", "class")

        Returns:
            Attribute value or None if attribute doesn't exist
        """
        ...

    def is_visible(self) -> bool:
        """
        Check if element is visible on page.

        Returns:
            True if element is visible, False otherwise
        """
        ...

    def is_enabled(self) -> bool:
        """
        Check if element is enabled (not disabled).

        Returns:
            True if element is enabled, False otherwise
        """
        ...

    def is_selected(self) -> bool:
        """
        Check if element is selected (for checkboxes/radio buttons).

        Returns:
            True if element is selected, False otherwise
        """
        ...
