"""
Element validation component - responsible for validating element states.
Single Responsibility: Check element visibility, presence, and state using wait strategies.
"""
from typing import Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from framework.utils.logger import TestLogger
from framework.page.strategies.wait_strategy import (
    VisibilityWaitStrategy,
    ClickableWaitStrategy,
    InvisibilityWaitStrategy,
    TextPresentWaitStrategy,
)
from .element_finder import ElementFinder


class ElementValidator:
    """
    Component responsible for validating element states.

    Single Responsibility: Verify element visibility, presence, and conditions.
    """

    def __init__(self, driver: WebDriver, timeout: int):
        """
        Initialize the element validator.

        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout for explicit waits
        """
        self.driver = driver
        self.timeout = timeout
        self.finder = ElementFinder(driver, timeout)
        self.logger = TestLogger.get_logger(self.__class__.__name__)

    def is_element_visible(self, locator: Tuple[str, str]) -> bool:
        """
        Check if an element is visible on the page using VisibilityWaitStrategy.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element is visible, False otherwise

        Example:
            >>> if validator.is_element_visible((By.ID, "error-message")):
            ...     print("Error displayed")
        """
        try:
            self.logger.debug(f"Checking if element is visible: {locator}")
            strategy = VisibilityWaitStrategy()
            strategy.wait_for(self.driver, locator, self.timeout)
            self.logger.debug(f"Element is visible: {locator}")
            return True
        except TimeoutException:
            self.logger.debug(f"Element is not visible: {locator}")
            return False

    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """
        Check if an element is present in the DOM.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element is present, False otherwise
        """
        try:
            self.finder.find_element(locator)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_clickable(self, locator: Tuple[str, str]) -> bool:
        """
        Check if an element is clickable using ClickableWaitStrategy.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element is clickable, False otherwise
        """
        try:
            self.logger.debug(f"Checking if element is clickable: {locator}")
            strategy = ClickableWaitStrategy()
            strategy.wait_for(self.driver, locator, self.timeout)
            self.logger.debug(f"Element is clickable: {locator}")
            return True
        except TimeoutException:
            self.logger.debug(f"Element is not clickable: {locator}")
            return False

    def is_element_selected(self, locator: Tuple[str, str]) -> bool:
        """
        Check if an element is selected (for checkboxes/radio buttons).

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element is selected, False otherwise
        """
        element = self.finder.find_element(locator)
        return element.is_selected()

    def is_element_enabled(self, locator: Tuple[str, str]) -> bool:
        """
        Check if an element is enabled.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element is enabled, False otherwise
        """
        element = self.finder.find_element(locator)
        return element.is_enabled()

    def wait_for_element_to_disappear(self, locator: Tuple[str, str]) -> bool:
        """
        Wait for an element to disappear from the page using InvisibilityWaitStrategy.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element disappeared, False otherwise
        """
        try:
            self.logger.debug(f"Waiting for element to disappear: {locator}")
            strategy = InvisibilityWaitStrategy()
            strategy.wait_for(self.driver, locator, self.timeout)
            self.logger.debug(f"Element disappeared: {locator}")
            return True
        except TimeoutException:
            self.logger.debug(f"Element did not disappear: {locator}")
            return False

    def wait_for_element_to_be_visible(self, locator: Tuple[str, str]) -> bool:
        """
        Wait for an element to become visible using VisibilityWaitStrategy.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            True if element became visible, False otherwise
        """
        try:
            self.logger.debug(f"Waiting for element to become visible: {locator}")
            strategy = VisibilityWaitStrategy()
            strategy.wait_for(self.driver, locator, self.timeout)
            self.logger.debug(f"Element is now visible: {locator}")
            return True
        except TimeoutException:
            self.logger.debug(f"Element did not become visible: {locator}")
            return False

    def wait_for_text_to_be_present(self, locator: Tuple[str, str], text: str) -> bool:
        """
        Wait for specific text to be present in an element using TextPresentWaitStrategy.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            text: Text to wait for

        Returns:
            True if text is present, False otherwise
        """
        try:
            self.logger.debug(f"Waiting for text '{text}' in element: {locator}")
            strategy = TextPresentWaitStrategy(text)
            strategy.wait_for(self.driver, locator, self.timeout)
            self.logger.debug(f"Text '{text}' is present in element: {locator}")
            return True
        except TimeoutException:
            self.logger.debug(f"Text '{text}' not present in element: {locator}")
            return False
