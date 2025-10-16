"""
Base protocol for Page Object Model.

Since we only use Playwright (no Selenium), we don't need specific protocols
for each page. This base protocol provides type safety for common operations.

YAGNI Principle: Only LoginPageProtocol and LeavePageProtocol were removed
because we only have one implementation (Playwright). If we ever need multiple
implementations, we can add them back.
"""

# pylint: disable=unnecessary-ellipsis

from typing import Protocol, runtime_checkable


@runtime_checkable
class PageObjectProtocol(Protocol):
    """
    Base protocol for all page objects.

    This protocol defines the common interface that all page objects must implement.
    All page classes (LoginPage, LeavePage, etc.) inherit from BasePage which
    implements this protocol.

    Benefits:
    - Type-safe contracts enforced at compile-time
    - Clean separation between tests and implementation
    - Easy to mock for testing
    - Documents the expected interface

    Example:
        >>> def test_navigation(page: PageObjectProtocol):
        ...     page.navigate_to("https://example.com")
        ...     assert page.is_page_loaded()
    """

    def navigate_to(self, url: str) -> None:
        """
        Navigate to the specified URL.

        Args:
            url: The URL to navigate to

        Example:
            >>> page.navigate_to("https://example.com/login")
        """
        ...

    def get_current_url(self) -> str:
        """
        Get the current page URL.

        Returns:
            The current URL as a string

        Example:
            >>> current_url = page.get_current_url()
            >>> assert "dashboard" in current_url
        """
        ...

    def is_page_loaded(self) -> bool:
        """
        Check if the page is fully loaded.

        Returns:
            True if the page is loaded, False otherwise

        Example:
            >>> page.navigate_to("https://example.com")
            >>> assert page.is_page_loaded()
        """
        ...
