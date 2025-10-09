"""
Element Validator Mixin - provides element validation capabilities.
Implements Interface Segregation Principle.
"""
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from framework.page.components import ElementValidator


class ElementValidatorMixin:
    """
    Mixin for pages that need element validation capabilities.

    Provides methods to validate element states.
    Requires the class to have a 'validator' attribute of type ElementValidator.
    """

    validator: 'ElementValidator'  # Type hint for required attribute

    def is_element_visible(self, locator: Tuple[str, str]) -> bool:
        """
        Check if an element is visible on the page.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element is visible, False otherwise
        """
        return self.validator.is_element_visible(locator)

    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """
        Check if an element is present in the DOM.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element is present, False otherwise
        """
        return self.validator.is_element_present(locator)

    def is_element_clickable(self, locator: Tuple[str, str]) -> bool:
        """
        Check if an element is clickable.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element is clickable, False otherwise
        """
        return self.validator.is_element_clickable(locator)

    def is_element_selected(self, locator: Tuple[str, str]) -> bool:
        """
        Check if an element is selected (for checkboxes/radio buttons).

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element is selected, False otherwise
        """
        return self.validator.is_element_selected(locator)

    def is_element_enabled(self, locator: Tuple[str, str]) -> bool:
        """
        Check if an element is enabled.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element is enabled, False otherwise
        """
        return self.validator.is_element_enabled(locator)

    def wait_for_element_to_disappear(self, locator: Tuple[str, str]) -> bool:
        """
        Wait for an element to disappear from the page.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element disappeared, False otherwise
        """
        return self.validator.wait_for_element_to_disappear(locator)

    def wait_for_element_to_be_visible(self, locator: Tuple[str, str]) -> bool:
        """
        Wait for an element to become visible.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element became visible, False otherwise
        """
        return self.validator.wait_for_element_to_be_visible(locator)

    def wait_for_text_to_be_present(self, locator: Tuple[str, str], text: str) -> bool:
        """
        Wait for specific text to be present in an element.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            text: Text to wait for

        Returns:
            True if text is present, False otherwise
        """
        return self.validator.wait_for_text_to_be_present(locator, text)
