"""
Factory for creating Locator value objects from legacy formats.
Facilitates migration from primitive tuples/strings to rich domain objects.
"""

from src.core.locator import Locator
from src.core.playwright_locator import PlaywrightLocator
from src.core.selenium_locator import SeleniumLocator


class LocatorFactory:
    """
    Factory for creating appropriate Locator instances.

    Provides utility methods to convert legacy locator formats
    (tuples, strings) into new Locator value objects.

    Example:
        >>> # From Selenium tuple
        >>> from selenium.webdriver.common.by import By
        >>> locator = LocatorFactory.create_selenium((By.ID, "username"))

        >>> # From Playwright string
        >>> locator = LocatorFactory.create_playwright("#username")

        >>> # Auto-detect framework
        >>> locator = LocatorFactory.auto_create((By.ID, "btn"), "selenium")
    """

    @staticmethod
    def create_selenium(
        locator: tuple[str, str] | SeleniumLocator, description: str = ""
    ) -> SeleniumLocator:
        """
        Create SeleniumLocator from tuple or existing SeleniumLocator.

        Args:
            locator: Either (By.X, "value") tuple or SeleniumLocator instance
            description: Optional description

        Returns:
            SeleniumLocator instance

        Example:
            >>> from selenium.webdriver.common.by import By
            >>> locator = LocatorFactory.create_selenium((By.ID, "login-btn"), "Login button")
        """
        if isinstance(locator, SeleniumLocator):
            return locator

        if isinstance(locator, tuple) and len(locator) == 2:
            return SeleniumLocator.from_tuple(locator, description)

        raise TypeError(
            f"Expected tuple or SeleniumLocator, got {type(locator)}. Use format: (By.X, 'value')"
        )

    @staticmethod
    def create_playwright(
        locator: str | PlaywrightLocator, description: str = ""
    ) -> PlaywrightLocator:
        """
        Create PlaywrightLocator from string or existing PlaywrightLocator.

        Args:
            locator: Either string selector or PlaywrightLocator instance
            description: Optional description

        Returns:
            PlaywrightLocator instance

        Example:
            >>> locator = LocatorFactory.create_playwright("#login-btn", "Login button")
        """
        if isinstance(locator, PlaywrightLocator):
            return locator

        if isinstance(locator, str):
            return PlaywrightLocator.from_string(locator, description)

        raise TypeError(
            f"Expected str or PlaywrightLocator, got {type(locator)}. "
            f"Use format: '#id' or '.class' or 'css selector'"
        )

    @staticmethod
    def auto_create(
        locator: tuple[str, str] | str | Locator, framework: str, description: str = ""
    ) -> Locator:
        """
        Auto-detect and create appropriate Locator based on framework.

        Args:
            locator: Legacy locator (tuple for Selenium, string for Playwright) or Locator instance
            framework: "selenium" or "playwright"
            description: Optional description

        Returns:
            Appropriate Locator subclass

        Raises:
            ValueError: If framework is unknown

        Example:
            >>> from selenium.webdriver.common.by import By
            >>> locator = LocatorFactory.auto_create((By.ID, "btn"), "selenium", "Button")
            >>> # Returns SeleniumLocator

            >>> locator = LocatorFactory.auto_create("#btn", "playwright", "Button")
            >>> # Returns PlaywrightLocator
        """
        # Already a Locator object
        if isinstance(locator, Locator):
            return locator

        framework_lower = framework.lower()

        if framework_lower == "selenium":
            # Type narrowing: Selenium needs tuple, not string
            if isinstance(locator, str):
                raise TypeError(f"Selenium locators must be tuples, not strings: {locator}")
            return LocatorFactory.create_selenium(locator, description)

        if framework_lower == "playwright":
            # Type narrowing: Playwright needs string, not tuple
            if isinstance(locator, tuple):
                raise TypeError(f"Playwright locators must be strings, not tuples: {locator}")
            return LocatorFactory.create_playwright(locator, description)

        raise ValueError(
            f"Unknown framework: {framework}. Supported frameworks: 'selenium', 'playwright'"
        )
