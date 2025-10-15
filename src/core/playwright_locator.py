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

    @classmethod
    def from_string(cls, selector: str, description: str = "") -> "PlaywrightLocator":
        """
        Create PlaywrightLocator from legacy string selector.

        Utility method for migrating existing code.

        Args:
            selector: Legacy string selector (e.g., "#username", ".btn")
            description: Optional description

        Returns:
            PlaywrightLocator instance

        Example:
            >>> legacy = "#username"
            >>> locator = PlaywrightLocator.from_string(legacy, "Username field")
        """
        # Detect strategy from selector format
        if selector.startswith("#"):
            return cls(LocatorStrategy.ID, selector[1:], description)

        elif selector.startswith("."):
            return cls(LocatorStrategy.CLASS_NAME, selector[1:], description)

        elif selector.startswith("xpath="):
            return cls(LocatorStrategy.XPATH, selector[6:], description)

        elif selector.startswith("[name="):
            # Extract name value: [name="username"] -> username
            name_value = selector.split('"')[1]
            return cls(LocatorStrategy.NAME, name_value, description)

        elif selector.startswith("text="):
            # Handle both exact and partial text
            text_value = selector[5:].strip('"').strip("/")
            return cls(LocatorStrategy.LINK_TEXT, text_value, description)

        else:
            # Default to CSS selector
            return cls(LocatorStrategy.CSS, selector, description)
