"""
Page Object protocols for framework-agnostic testing.
Define common interfaces that both Selenium and Playwright implementations must satisfy.
"""

# pylint: disable=unnecessary-ellipsis

from typing import Protocol, runtime_checkable


@runtime_checkable
class PageObjectProtocol(Protocol):
    """
    Base protocol for all page objects.

    This protocol defines the common interface that all page objects must implement,
    regardless of the underlying automation framework (Selenium or Playwright).

    Benefits:
    - Tests can work with any page implementation
    - Type-safe contracts enforced at compile-time
    - Easy to add new automation frameworks
    - Framework-agnostic test code
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


@runtime_checkable
class LoginPageProtocol(PageObjectProtocol, Protocol):
    """
    Protocol for login page objects.

    Extends PageObjectProtocol with login-specific operations.
    Both Selenium and Playwright login pages must implement this interface.

    Example:
        >>> def test_login(login_page: LoginPageProtocol, config: ConfigService):
        ...     login_page.login(config.username, config.password)
        ...     assert "dashboard" in login_page.get_current_url()
    """

    def enter_username(self, username: str) -> "LoginPageProtocol":
        """
        Enter username into the username field.

        Args:
            username: The username to enter

        Returns:
            Self for method chaining

        Example:
            >>> login_page.enter_username("admin").enter_password("pass")
        """
        ...

    def enter_password(self, password: str) -> "LoginPageProtocol":
        """
        Enter password into the password field.

        Args:
            password: The password to enter

        Returns:
            Self for method chaining

        Example:
            >>> login_page.enter_password("admin123")
        """
        ...

    def click_login_button(self) -> None:
        """
        Click the login button to submit credentials.

        Example:
            >>> login_page.click_login_button()
        """
        ...

    def login(self, username: str, password: str) -> None:
        """
        Perform complete login operation.

        Convenience method that combines enter_username, enter_password,
        and click_login_button.

        Args:
            username: The username to login with
            password: The password to login with

        Example:
            >>> login_page.login("admin", "admin123")
        """
        ...

    def get_error_message(self) -> str:
        """
        Get the error message displayed on login failure.

        Returns:
            The error message text

        Example:
            >>> login_page.login("invalid", "invalid")
            >>> error = login_page.get_error_message()
            >>> assert "Invalid credentials" in error
        """
        ...

    def is_error_message_displayed(self) -> bool:
        """
        Check if an error message is displayed.

        Returns:
            True if error message is visible, False otherwise

        Example:
            >>> login_page.login("invalid", "invalid")
            >>> assert login_page.is_error_message_displayed()
        """
        ...

    def is_login_logo_visible(self) -> bool:
        """
        Check if the login logo is visible.

        Returns:
            True if the logo is visible, False otherwise

        Example:
            >>> assert login_page.is_login_logo_visible()
        """
        ...
