"""
Element Interactor Mixin - provides element interaction capabilities.
Implements Interface Segregation Principle.
"""
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from framework.page.components import ElementInteractor


class ElementInteractorMixin:
    """
    Mixin for pages that need element interaction capabilities.

    Provides methods to interact with elements (click, type, etc.).
    Requires the class to have an 'interactor' attribute of type ElementInteractor.
    """

    interactor: 'ElementInteractor'  # Type hint for required attribute

    def click(self, locator: Tuple[str, str]) -> None:
        """
        Click on an element after waiting for it to be clickable.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
        """
        return self.interactor.click(locator)

    def send_keys(self, locator: Tuple[str, str], text: str, clear_first: bool = True) -> None:
        """
        Type text into an input field.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            text: Text to type
            clear_first: Whether to clear the field before typing
        """
        return self.interactor.send_keys(locator, text, clear_first)

    def get_text(self, locator: Tuple[str, str]) -> str:
        """
        Get the text content of an element.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            Text content of the element
        """
        return self.interactor.get_text(locator)

    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        """
        Get an attribute value from an element.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            attribute: Name of the attribute

        Returns:
            Value of the attribute
        """
        return self.interactor.get_attribute(locator, attribute)

    def clear(self, locator: Tuple[str, str]) -> None:
        """
        Clear the content of an input field.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
        """
        return self.interactor.clear(locator)

    def submit(self, locator: Tuple[str, str]) -> None:
        """
        Submit a form element.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
        """
        return self.interactor.submit(locator)
