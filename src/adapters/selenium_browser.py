"""
SeleniumBrowserAdapter: Adapter for Selenium WebDriver to BrowserProtocol.

This adapter wraps Selenium WebDriver and provides a unified interface
compatible with BrowserProtocol.
"""

from typing import Any

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.adapters.selenium_element import SeleniumWebElement
from src.core.element_protocol import WebElementProtocol
from src.core.locator import Locator
from utils.exceptions import ElementNotFoundException, InvalidParameterException
from utils.logger import TestLogger


class SeleniumBrowserAdapter:
    """
    Adapter for Selenium WebDriver implementing BrowserProtocol.

    This adapter converts Selenium WebDriver API to the unified BrowserProtocol,
    enabling framework-agnostic test code.

    Design Pattern:
        Adapter Pattern - Wraps Selenium WebDriver to provide BrowserProtocol interface

    Attributes:
        driver: Selenium WebDriver instance
        timeout: Default timeout for operations in seconds
        logger: Logger instance for debugging

    Example:
        >>> from selenium import webdriver
        >>> driver = webdriver.Chrome()
        >>> browser = SeleniumBrowserAdapter(driver, timeout=10)
        >>> browser.navigate("https://example.com")
        >>> element = browser.find_element(username_locator)
    """

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initialize the Selenium browser adapter.

        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout for explicit waits in seconds
        """
        self._driver = driver
        self._timeout = timeout
        self._wait = WebDriverWait(driver, timeout)
        self.logger = TestLogger.get_logger(self.__class__.__name__)

    @property
    def timeout(self) -> int:
        """Get the default timeout in seconds."""
        return self._timeout

    @timeout.setter
    def timeout(self, value: int) -> None:
        """
        Set the default timeout in seconds.

        Args:
            value: Timeout in seconds
        """
        self._timeout = value
        self._wait = WebDriverWait(self._driver, value)

    def navigate(self, url: str) -> None:
        """
        Navigate to the specified URL.

        Args:
            url: Target URL to navigate to

        Raises:
            InvalidParameterException: If URL is None or empty
        """
        if not url or not isinstance(url, str):
            raise InvalidParameterException("url", url, "URL must be a non-empty string")

        self.logger.debug(f"Navigating to: {url}")
        self._driver.get(url)

    def find_element(self, locator: Locator) -> WebElementProtocol:
        """
        Find a single element using explicit wait.

        Args:
            locator: Locator value object

        Returns:
            WebElementProtocol: Wrapped Selenium element

        Raises:
            ElementNotFoundException: If element is not found within timeout
        """
        native_locator = locator.to_native()

        try:
            element = self._wait.until(
                EC.presence_of_element_located(native_locator),
                message=f"Element not found: {locator.description}",
            )
            self.logger.debug(f"Found element: {locator.description}")
            return SeleniumWebElement(element)
        except TimeoutException as e:
            self.logger.error(f"Timeout waiting for element: {locator.description}")
            raise ElementNotFoundException(
                native_locator, f"Timeout waiting for element: {locator.description}"
            ) from e

    def find_elements(self, locator: Locator) -> list[WebElementProtocol]:
        """
        Find all elements matching the locator.

        Args:
            locator: Locator value object

        Returns:
            List of WebElementProtocol objects (empty list if none found)
        """
        native_locator = locator.to_native()

        try:
            elements = self._wait.until(
                EC.presence_of_all_elements_located(native_locator),
                message=f"Elements not found: {locator.description}",
            )
            self.logger.debug(f"Found {len(elements)} elements: {locator.description}")
            return [SeleniumWebElement(elem) for elem in elements]
        except TimeoutException:
            self.logger.debug(f"No elements found: {locator.description}")
            return []

    def execute_script(self, script: str, *args: Any) -> Any:
        """
        Execute JavaScript code in the browser context.

        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script (can be WebElement objects)

        Returns:
            Result of the JavaScript execution

        Raises:
            InvalidParameterException: If script is None or empty
        """
        if not script or not isinstance(script, str):
            raise InvalidParameterException(
                "script", script, "JavaScript code must be a non-empty string"
            )

        # Unwrap SeleniumWebElement objects to native WebElement
        unwrapped_args = []
        for arg in args:
            if isinstance(arg, SeleniumWebElement):
                unwrapped_args.append(arg._element)  # Access internal element
            else:
                unwrapped_args.append(arg)

        return self._driver.execute_script(script, *unwrapped_args)

    def get_current_url(self) -> str:
        """
        Get the current page URL.

        Returns:
            Current URL as string
        """
        return self._driver.current_url

    def get_title(self) -> str:
        """
        Get the current page title.

        Returns:
            Page title as string
        """
        return self._driver.title

    def refresh(self) -> None:
        """Refresh the current page."""
        self.logger.debug("Refreshing page")
        self._driver.refresh()

    def take_screenshot(self, path: str) -> bytes:
        """
        Take a screenshot of the current page.

        Args:
            path: File path to save the screenshot

        Returns:
            Screenshot as bytes
        """
        self.logger.debug(f"Taking screenshot: {path}")
        self._driver.save_screenshot(path)
        return self._driver.get_screenshot_as_png()

    def quit(self) -> None:
        """Close the browser and clean up resources."""
        self.logger.debug("Closing browser")
        self._driver.quit()

    def switch_to_frame(self, locator: Locator) -> None:
        """
        Switch context to an iframe.

        Args:
            locator: Locator for the iframe element
        """
        element = self.find_element(locator)
        # Unwrap SeleniumWebElement to get native WebElement
        # We know find_element returns SeleniumWebElement, so cast it
        assert isinstance(element, SeleniumWebElement)
        native_element = element._element
        self.logger.debug(f"Switching to frame: {locator.description}")
        self._driver.switch_to.frame(native_element)

    def switch_to_default_content(self) -> None:
        """Switch back to the main page content from an iframe."""
        self.logger.debug("Switching to default content")
        self._driver.switch_to.default_content()

    def get_page_source(self) -> str:
        """
        Get the HTML source of the current page.

        Returns:
            HTML source as string
        """
        return self._driver.page_source

    def is_element_clickable(self, locator: Locator) -> bool:
        """
        Check if an element is clickable.

        Args:
            locator: Locator value object

        Returns:
            True if element is clickable, False otherwise
        """
        native_locator = locator.to_native()
        try:
            self._wait.until(EC.element_to_be_clickable(native_locator))
            return True
        except TimeoutException:
            return False

    def is_element_visible(self, locator: Locator) -> bool:
        """
        Check if an element is visible on the page.

        Args:
            locator: Locator value object

        Returns:
            True if element is visible, False otherwise
        """
        native_locator = locator.to_native()
        try:
            self._wait.until(EC.visibility_of_element_located(native_locator))
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator: Locator) -> bool:
        """
        Check if an element is present in the DOM.

        Args:
            locator: Locator value object

        Returns:
            True if element is present, False otherwise
        """
        try:
            self.find_element(locator)
            return True
        except (TimeoutException, NoSuchElementException, ElementNotFoundException):
            return False

    def wait_for_element_to_disappear(self, locator: Locator) -> bool:
        """
        Wait for an element to disappear from the page.

        Args:
            locator: Locator value object

        Returns:
            True if element disappeared, False otherwise
        """
        native_locator = locator.to_native()
        try:
            self._wait.until(EC.invisibility_of_element_located(native_locator))
            return True
        except TimeoutException:
            return False

    def scroll_to_element(self, locator: Locator) -> None:
        """
        Scroll to an element on the page.

        Args:
            locator: Locator value object
        """
        element = self.find_element(locator)
        self.execute_script("arguments[0].scrollIntoView(true);", element)
