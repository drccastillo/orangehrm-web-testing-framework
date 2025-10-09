"""
Element interaction component - responsible for interacting with web elements.
Single Responsibility: Perform actions on elements (click, type, get text, etc.)
"""
from typing import Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException
from framework.utils.logger import TestLogger
from framework.utils.exceptions import ElementNotClickableException, InvalidParameterException
from .element_finder import ElementFinder


class ElementInteractor:
    """
    Component responsible for interacting with web elements.

    Single Responsibility: Perform user actions on elements.
    Depends on ElementFinder for locating elements.
    """

    def __init__(self, driver: WebDriver, timeout: int):
        """
        Initialize the element interactor.

        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout for explicit waits
        """
        self.driver = driver
        self.timeout = timeout
        self.finder = ElementFinder(driver, timeout)
        self.logger = TestLogger.get_logger(self.__class__.__name__)

    def click(self, locator: Tuple[str, str]) -> None:
        """
        Click on an element after waiting for it to be clickable.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Raises:
            InvalidParameterException: If locator is None or invalid
            ElementNotClickableException: If element is not clickable

        Example:
            >>> interactor.click((By.ID, "submit-button"))
        """
        self.logger.debug(f"Clicking element: {locator}")
        try:
            element = self.finder.find_clickable_element(locator)
            element.click()
            self.logger.debug(f"Clicked element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to click element: {locator}")
            raise ElementNotClickableException(locator) from e

    def send_keys(self, locator: Tuple[str, str], text: str, clear_first: bool = True) -> None:
        """
        Type text into an input field.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            text: Text to type
            clear_first: Whether to clear the field before typing

        Raises:
            InvalidParameterException: If text is None or empty
            ElementNotFoundException: If element is not found

        Example:
            >>> interactor.send_keys((By.ID, "username"), "admin")
        """
        if text is None or (isinstance(text, str) and not text.strip()):
            raise InvalidParameterException("text", text, "Text cannot be None or empty")

        self.logger.debug(f"Sending keys to element: {locator}")
        element = self.finder.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        self.logger.debug(f"Sent keys to element: {locator}")

    def get_text(self, locator: Tuple[str, str]) -> str:
        """
        Get the text content of an element.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")

        Returns:
            Text content of the element

        Example:
            >>> error_text = interactor.get_text((By.CSS_SELECTOR, ".error-message"))
        """
        element = self.finder.find_element(locator)
        return element.text

    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        """
        Get an attribute value from an element.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            attribute: Name of the attribute

        Returns:
            Value of the attribute

        Raises:
            InvalidParameterException: If attribute is None or empty
        """
        if not attribute or not isinstance(attribute, str):
            raise InvalidParameterException(
                "attribute",
                attribute,
                "Attribute name must be a non-empty string"
            )

        element = self.finder.find_element(locator)
        return element.get_attribute(attribute)

    def clear(self, locator: Tuple[str, str]) -> None:
        """
        Clear the content of an input field.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
        """
        self.logger.debug(f"Clearing element: {locator}")
        element = self.finder.find_element(locator)
        element.clear()
        self.logger.debug(f"Cleared element: {locator}")

    def submit(self, locator: Tuple[str, str]) -> None:
        """
        Submit a form element.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
        """
        self.logger.debug(f"Submitting form element: {locator}")
        element = self.finder.find_element(locator)
        element.submit()
        self.logger.debug(f"Submitted form element: {locator}")
