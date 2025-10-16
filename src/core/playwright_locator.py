"""
Playwright-specific locator implementation.
Uses native Playwright selector strings for optimal performance.
"""


class PlaywrightLocator:
    """
    Playwright locator using native selector strings.

    This simplified locator directly stores Playwright selector strings,
    eliminating the need for conversion and improving performance.

    Attributes:
        selector: Playwright selector string (CSS, XPath, text, etc.)
        description: Human-readable description of the locator

    Example:
        >>> locator = PlaywrightLocator("input[name='username']", "Username input")
        >>> locator.to_native()  # Returns: "input[name='username']"

        >>> xpath_locator = PlaywrightLocator("//button[@id='submit']", "Submit button")
        >>> xpath_locator.to_native()  # Returns: "//button[@id='submit']"
    """

    def __init__(self, selector: str, description: str = ""):
        """
        Initialize Playwright locator with native selector string.

        Args:
            selector: Playwright selector string (CSS, XPath, text=, etc.)
            description: Human-readable description of what this locates

        Raises:
            ValueError: If selector is empty
        """
        if not selector or not isinstance(selector, str):
            raise ValueError("Selector must be a non-empty string")

        self.selector = selector
        self.description = description or f"Playwright selector: {selector}"

    def to_native(self) -> str:
        """
        Return the native Playwright selector string.

        Returns:
            String selector compatible with Playwright's page.locator()

        Example:
            >>> locator = PlaywrightLocator("button.submit")
            >>> locator.to_native()
            "button.submit"
        """
        return self.selector

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"PlaywrightLocator(selector='{self.selector}', description='{self.description}')"

    def __str__(self) -> str:
        """User-friendly string representation."""
        return f"{self.description} ['{self.selector}']"
