"""
Element finding component - responsible for locating elements on the page.
Single Responsibility: Find elements using Chain of Responsibility wait strategies.
"""
from typing import Tuple, List, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from framework.utils.logger import TestLogger
from framework.utils.exceptions import ElementNotFoundException, InvalidParameterException
from framework.page.strategies.wait_strategy import (
    WaitStrategy,
    create_default_wait_chain,
    PresenceWaitStrategy,
    ClickableWaitStrategy,
    PresenceOfAllWaitStrategy,
)


class ElementFinder:
    """
    Component responsible for finding web elements.

    Single Responsibility: Locate elements using various strategies with explicit waits.
    """

    def __init__(self, driver: WebDriver, timeout: int, wait_strategy: Optional[WaitStrategy] = None):
        """
        Initialize the element finder.

        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout for explicit waits
            wait_strategy: Optional custom wait strategy chain (uses default if not provided)
        """
        self.driver = driver
        self.timeout = timeout
        self.wait_strategy = wait_strategy or create_default_wait_chain()
        self.logger = TestLogger.get_logger(self.__class__.__name__)

    def _validate_locator(self, locator: Tuple[str, str]) -> None:
        """
        Validate that locator is properly formatted.

        Args:
            locator: Tuple to validate

        Raises:
            InvalidParameterException: If locator is None or invalid format
        """
        if not locator or not isinstance(locator, tuple) or len(locator) != 2:
            raise InvalidParameterException(
                "locator",
                locator,
                "Locator must be a tuple of (By.STRATEGY, 'value')"
            )

    def find_element(self, locator: Tuple[str, str], custom_strategy: Optional[WaitStrategy] = None) -> WebElement:
        """
        Find a single element using Chain of Responsibility wait strategy.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            custom_strategy: Optional custom wait strategy (uses default chain if not provided)

        Returns:
            WebElement if found

        Raises:
            InvalidParameterException: If locator is None or invalid
            ElementNotFoundException: If element is not found within timeout
        """
        self._validate_locator(locator)

        try:
            self.logger.debug(f"Finding element with wait chain: {locator}")
            strategy = custom_strategy or self.wait_strategy
            element = strategy.wait_for(self.driver, locator, self.timeout)
            self.logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException as e:
            self.logger.error(f"Timeout waiting for element with all strategies: {locator}")
            raise ElementNotFoundException(locator, f"Timeout waiting for element: {locator}") from e

    def find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """
        Find multiple elements using PresenceOfAllWaitStrategy.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            List of WebElements (empty list if none found)

        Raises:
            InvalidParameterException: If locator is None or invalid
        """
        self._validate_locator(locator)

        try:
            self.logger.debug(f"Finding multiple elements: {locator}")
            strategy = PresenceOfAllWaitStrategy()
            elements = strategy.wait_for(self.driver, locator, self.timeout)
            self.logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            self.logger.debug(f"No elements found: {locator}")
            return []

    def find_clickable_element(self, locator: Tuple[str, str]) -> WebElement:
        """
        Find a clickable element using ClickableWaitStrategy.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            WebElement if found and clickable

        Raises:
            InvalidParameterException: If locator is None or invalid
            ElementNotFoundException: If element is not clickable within timeout
        """
        self._validate_locator(locator)

        try:
            self.logger.debug(f"Finding clickable element: {locator}")
            strategy = ClickableWaitStrategy()
            element = strategy.wait_for(self.driver, locator, self.timeout)
            self.logger.debug(f"Clickable element found: {locator}")
            return element
        except TimeoutException as e:
            self.logger.error(f"Element not clickable: {locator}")
            raise ElementNotFoundException(locator, f"Element not clickable: {locator}") from e
