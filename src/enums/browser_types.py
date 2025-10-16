"""
Browser types enum for type-safe browser selection.

Replaces hardcoded string comparisons with type-safe Enum (Phase 2 refactor).
"""

from enum import Enum


class BrowserType(str, Enum):
    """
    Supported browser types for Playwright automation.

    This Enum provides type safety and eliminates hardcoded string comparisons.

    Example:
        >>> browser_type = BrowserType.CHROME
        >>> assert browser_type == "chrome"
        >>> assert browser_type.value == "chrome"
    """

    CHROME = "chrome"
    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    EDGE = "edge"
    WEBKIT = "webkit"

    @classmethod
    def from_string(cls, value: str) -> "BrowserType":
        """
        Convert string to BrowserType enum (case-insensitive).

        Args:
            value: Browser name as string

        Returns:
            BrowserType enum value

        Raises:
            ValueError: If browser type is not supported

        Example:
            >>> BrowserType.from_string("Chrome")
            <BrowserType.CHROME: 'chrome'>
        """
        try:
            return cls(value.lower())
        except ValueError as e:
            supported = ", ".join(b.value for b in cls)
            raise ValueError(
                f"Unsupported browser: {value}. Supported browsers: {supported}"
            ) from e
