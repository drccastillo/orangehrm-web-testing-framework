"""
Selenium-specific locator implementation.
Converts Locator value objects to Selenium (By.X, "value") tuples.
"""

from selenium.webdriver.common.by import By

from src.core.locator import Locator, LocatorStrategy


class SeleniumLocator(Locator):
    """
    Selenium-specific locator implementation.

    Converts framework-agnostic Locator to Selenium's tuple format.

    Example:
        >>> locator = SeleniumLocator(LocatorStrategy.ID, "username")
        >>> locator.to_native()  # Returns: (By.ID, "username")

        >>> css_locator = SeleniumLocator(LocatorStrategy.CSS, ".btn-primary")
        >>> css_locator.to_native()  # Returns: (By.CSS_SELECTOR, ".btn-primary")
    """

    # Mapping from framework-agnostic strategy to Selenium's By class
    STRATEGY_MAP = {
        LocatorStrategy.ID: By.ID,
        LocatorStrategy.NAME: By.NAME,
        LocatorStrategy.CSS: By.CSS_SELECTOR,
        LocatorStrategy.XPATH: By.XPATH,
        LocatorStrategy.CLASS_NAME: By.CLASS_NAME,
        LocatorStrategy.TAG_NAME: By.TAG_NAME,
        LocatorStrategy.LINK_TEXT: By.LINK_TEXT,
        LocatorStrategy.PARTIAL_LINK_TEXT: By.PARTIAL_LINK_TEXT,
    }

    def to_native(self) -> tuple[str, str]:
        """
        Convert to Selenium native format.

        Returns:
            Tuple of (By.STRATEGY, "value") compatible with Selenium WebDriver

        Raises:
            KeyError: If strategy is not supported by Selenium

        Example:
            >>> locator = SeleniumLocator(LocatorStrategy.XPATH, "//button")
            >>> locator.to_native()
            (By.XPATH, "//button")
        """
        by_type = self.STRATEGY_MAP.get(self.strategy)
        if by_type is None:
            raise KeyError(
                f"Locator strategy {self.strategy} not supported by Selenium. "
                f"Supported strategies: {list(self.STRATEGY_MAP.keys())}"
            )
        return (by_type, self.value)

    @classmethod
    def from_tuple(cls, locator_tuple: tuple[str, str], description: str = "") -> "SeleniumLocator":
        """
        Create SeleniumLocator from legacy tuple format.

        Utility method for migrating existing code.

        Args:
            locator_tuple: Legacy (By.X, "value") tuple
            description: Optional description

        Returns:
            SeleniumLocator instance

        Example:
            >>> legacy = (By.ID, "username")
            >>> locator = SeleniumLocator.from_tuple(legacy, "Username field")
        """
        by_strategy, value = locator_tuple

        # Reverse lookup: By.X -> LocatorStrategy
        for strategy, by_const in cls.STRATEGY_MAP.items():
            if by_const == by_strategy:
                return cls(strategy, value, description)

        raise ValueError(f"Unsupported Selenium By strategy: {by_strategy}")
