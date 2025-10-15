"""
Playwright-specific locator implementation.
Converts Locator value objects to Playwright selector strings.
"""

# pylint: disable=too-many-return-statements,no-else-return

from src.core.locator import Locator, LocatorStrategy


class PlaywrightLocator(Locator):
    """
    Playwright-specific locator implementation.

    Converts framework-agnostic Locator to Playwright's string selector format.

    Example:
        >>> locator = PlaywrightLocator(LocatorStrategy.ID, "username")
        >>> locator.to_native()  # Returns: "#username"

        >>> css_locator = PlaywrightLocator(LocatorStrategy.CSS, ".btn-primary")
        >>> css_locator.to_native()  # Returns: ".btn-primary"

        >>> xpath_locator = PlaywrightLocator(LocatorStrategy.XPATH, "//button")
        >>> xpath_locator.to_native()  # Returns: "xpath=//button"
    """

    def to_native(self) -> str:
        """
        Convert to Playwright native format.

        Returns:
            String selector compatible with Playwright's page.locator()

        Raises:
            ValueError: If strategy is not supported by Playwright

        Example:
            >>> locator = PlaywrightLocator(LocatorStrategy.CSS, ".login-btn")
            >>> locator.to_native()
            ".login-btn"
        """
        strategy = self.strategy
        value = self.value

        # Map strategy to Playwright selector format
        if strategy == LocatorStrategy.ID:
            return f"#{value}"

        elif strategy == LocatorStrategy.NAME:
            return f'[name="{value}"]'

        elif strategy == LocatorStrategy.CSS:
            return value

        elif strategy == LocatorStrategy.XPATH:
            return f"xpath={value}"

        elif strategy == LocatorStrategy.CLASS_NAME:
            return f".{value}"

        elif strategy == LocatorStrategy.TAG_NAME:
            return value

        elif strategy == LocatorStrategy.LINK_TEXT:
            # Playwright uses text= for exact text match
            return f'text="{value}"'

        elif strategy == LocatorStrategy.PARTIAL_LINK_TEXT:
            # Playwright uses text= with regex for partial match
            return f"text=/{value}/"

        else:
            raise ValueError(
                f"Locator strategy {strategy} not supported by Playwright. "
                f"Supported strategies: {[s.value for s in LocatorStrategy]}"
            )
