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


@runtime_checkable
class LeavePageProtocol(PageObjectProtocol, Protocol):
    """
    Protocol for leave page objects.

    Extends PageObjectProtocol with leave-specific operations.
    Both Selenium and Playwright leave pages must implement this interface.

    Example:
        >>> def test_apply_leave(leave_page: LeavePageProtocol):
        ...     leave_page.navigate_to_apply_leave()
        ...     assert leave_page.is_apply_form_visible()
    """

    def navigate_to_apply_leave(self) -> None:
        """
        Navigate to Apply Leave page.

        Example:
            >>> leave_page.navigate_to_apply_leave()
        """
        ...

    def navigate_to_leave_list(self) -> None:
        """
        Navigate to Leave List page.

        Example:
            >>> leave_page.navigate_to_leave_list()
        """
        ...

    def navigate_to_my_leave(self) -> None:
        """
        Navigate to My Leave page.

        Example:
            >>> leave_page.navigate_to_my_leave()
        """
        ...

    def is_apply_button_visible(self) -> bool:
        """
        Check if the Apply button is visible.

        Returns:
            True if Apply button is visible, False otherwise

        Example:
            >>> assert leave_page.is_apply_button_visible()
        """
        ...

    def is_leave_list_button_visible(self) -> bool:
        """
        Check if the Leave List button is visible.

        Returns:
            True if Leave List button is visible, False otherwise

        Example:
            >>> assert leave_page.is_leave_list_button_visible()
        """
        ...

    def is_my_leave_button_visible(self) -> bool:
        """
        Check if the My Leave button is visible.

        Returns:
            True if My Leave button is visible, False otherwise

        Example:
            >>> assert leave_page.is_my_leave_button_visible()
        """
        ...

    def is_leave_list_table_visible(self) -> bool:
        """
        Check if the leave list table is visible.

        Returns:
            True if table is visible, False otherwise

        Example:
            >>> leave_page.navigate_to_leave_list()
            >>> assert leave_page.is_leave_list_table_visible()
        """
        ...

    def apply_leave(
        self, leave_type: str, from_date: str, to_date: str, comments: str = ""
    ) -> None:
        """
        Apply for leave with specified details.

        Args:
            leave_type: Type of leave to apply for
            from_date: Start date of leave (format: YYYY-MM-DD)
            to_date: End date of leave (format: YYYY-MM-DD)
            comments: Optional comments for leave request

        Example:
            >>> leave_page.apply_leave("CAN - FMLA", "2025-01-15", "2025-01-17", "Family emergency")
        """
        ...

    def search_leave(self, employee_name: str = "", status: str = "") -> None:
        """
        Search for leave records with filters.

        Args:
            employee_name: Employee name to filter (optional)
            status: Leave status to filter (optional)

        Example:
            >>> leave_page.search_leave(employee_name="John Doe", status="Pending")
        """
        ...

    def reset_search(self) -> None:
        """
        Reset all search filters.

        Example:
            >>> leave_page.search_leave(employee_name="John Doe")
            >>> leave_page.reset_search()
        """
        ...

    def get_leave_count(self) -> int:
        """
        Get the count of leave records displayed.

        Returns:
            Number of leave records in the list

        Example:
            >>> count = leave_page.get_leave_count()
            >>> assert count > 0
        """
        ...

    def is_success_message_displayed(self) -> bool:
        """
        Check if success message is displayed.

        Returns:
            True if success message is visible, False otherwise

        Example:
            >>> leave_page.apply_leave("CAN - FMLA", "2025-01-15", "2025-01-17")
            >>> assert leave_page.is_success_message_displayed()
        """
        ...

    def is_no_records_message_displayed(self) -> bool:
        """
        Check if 'No Records Found' message is displayed.

        Returns:
            True if no records message is visible, False otherwise

        Example:
            >>> leave_page.search_leave(employee_name="NonExistentUser")
            >>> assert leave_page.is_no_records_message_displayed()
        """
        ...
