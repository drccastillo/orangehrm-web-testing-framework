"""
Element Finder Mixin - provides element finding capabilities.
Implements Interface Segregation Principle.
"""
from typing import Tuple, List, TYPE_CHECKING

if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement
    from framework.page.components import ElementFinder


class ElementFinderMixin:
    """
    Mixin for pages that need element finding capabilities.

    Provides methods to find elements on the page.
    Requires the class to have a 'finder' attribute of type ElementFinder.
    """

    finder: 'ElementFinder'  # Type hint for required attribute

    def find_element(self, locator: Tuple[str, str]) -> 'WebElement':
        """
        Find a single element using explicit wait.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            WebElement if found
        """
        return self.finder.find_element(locator)

    def find_elements(self, locator: Tuple[str, str]) -> List['WebElement']:
        """
        Find multiple elements using explicit wait.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            List of WebElements (empty list if none found)
        """
        return self.finder.find_elements(locator)

    def find_clickable_element(self, locator: Tuple[str, str]) -> 'WebElement':
        """
        Find a clickable element using explicit wait.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            WebElement if found and clickable
        """
        return self.finder.find_clickable_element(locator)
