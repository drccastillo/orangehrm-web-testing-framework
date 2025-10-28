"""
Login Page Object for Playwright.
Implements page-specific functionality for the OrangeHRM login page.
"""

from playwright.sync_api import Page, expect

from src.pages_playwright.base_page_pw import BasePagePW
from src.pages_playwright.locators.login_locators_pw import LoginLocatorsPW


class LoginPagePW(BasePagePW):
    """
    Page Object Model for the Login Page using Playwright.
    Provides methods to interact with login page elements.
    """

    def __init__(self, page: Page, timeout: int = 10):
        """
        Initialize the Login Page.

        Args:
            page: Playwright Page instance
            timeout: Default timeout for operations in seconds
        """
        super().__init__(page, timeout)
        self.locators = LoginLocatorsPW

    def enter_username(self, username: str) -> "LoginPagePW":
        """
        Enter username into the username field.

        Args:
            username: Username to enter

        Returns:
            Self for method chaining

        Example:
            >>> login_page.enter_username("admin")
        """
        self.fill(self.locators.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPagePW":
        """
        Enter password into the password field.

        Args:
            password: Password to enter

        Returns:
            Self for method chaining

        Example:
            >>> login_page.enter_password("password123")
        """
        self.fill(self.locators.PASSWORD_INPUT, password)
        return self

    def click_login_button(self) -> "LoginPagePW":
        """
        Click the login button.

        Returns:
            Self for method chaining

        Example:
            >>> login_page.click_login_button()
        """
        self.click(self.locators.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str) -> "LoginPagePW":
        """
        Perform complete login operation.
        High-level method that combines username, password, and login.

        Args:
            username: Username to enter
            password: Password to enter

        Returns:
            Self for method chaining

        Example:
            >>> login_page.login("admin", "admin123")
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        return self

    def click_forgot_password(self) -> "LoginPagePW":
        """
        Click the 'Forgot Password' link.

        Returns:
            Self for method chaining
        """
        self.click(self.locators.FORGOT_PASSWORD_LINK)
        return self

    def get_error_message(self) -> str:
        """
        Get the error message displayed on the login page.
        Returns empty string if no error message is visible.

        Returns:
            Error message text, or empty string if not visible

        Example:
            >>> error = login_page.get_error_message()
        """
        try:
            # get_text() already has auto-waiting, no need to check visibility first
            return self.get_text(self.locators.ERROR_MESSAGE)
        except Exception:
            # Element not found or not visible
            return ""

    def is_error_message_displayed(self) -> bool:
        """
        Check if an error message is displayed.

        Returns:
            True if error message is visible, False otherwise

        Example:
            >>> if login_page.is_error_message_displayed():
            ...     print("Login failed")
        """
        return self.is_visible(self.locators.ERROR_MESSAGE)

    def get_page_title_text(self) -> str:
        """
        Get the login page title text.

        Returns:
            Login page title text
        """
        return self.get_text(self.locators.LOGIN_TITLE)

    def is_login_logo_displayed(self) -> bool:
        """
        Check if the login logo is displayed.

        Returns:
            True if logo is visible, False otherwise
        """
        return self.is_visible(self.locators.LOGIN_LOGO)

    def is_username_field_displayed(self) -> bool:
        """
        Check if the username field is displayed.

        Returns:
            True if username field is visible, False otherwise
        """
        return self.is_visible(self.locators.USERNAME_INPUT)

    def is_password_field_displayed(self) -> bool:
        """
        Check if the password field is displayed.

        Returns:
            True if password field is visible, False otherwise
        """
        return self.is_visible(self.locators.PASSWORD_INPUT)

    def is_login_button_displayed(self) -> bool:
        """
        Check if the login button is displayed.

        Returns:
            True if login button is visible, False otherwise
        """
        return self.is_visible(self.locators.LOGIN_BUTTON)

    def is_login_button_enabled(self) -> bool:
        """
        Check if the login button is enabled.

        Returns:
            True if login button is enabled, False otherwise
        """
        return self.is_enabled(self.locators.LOGIN_BUTTON)

    def clear_username(self) -> "LoginPagePW":
        """
        Clear the username field.

        Returns:
            Self for method chaining
        """
        self.clear(self.locators.USERNAME_INPUT)
        return self

    def clear_password(self) -> "LoginPagePW":
        """
        Clear the password field.

        Returns:
            Self for method chaining
        """
        self.clear(self.locators.PASSWORD_INPUT)
        return self

    def clear_form(self) -> "LoginPagePW":
        """
        Clear both username and password fields.

        Returns:
            Self for method chaining
        """
        self.clear_username()
        self.clear_password()
        return self

    def submit_with_enter_key(self) -> "LoginPagePW":
        """
        Submit the login form by pressing Enter key on password field.

        Returns:
            Self for method chaining
        """
        self.press_key(self.locators.PASSWORD_INPUT, "Enter")
        return self

    def get_username_value(self) -> str:
        """
        Get the current value of the username field.

        Returns:
            Username field value
        """
        return self.get_input_value(self.locators.USERNAME_INPUT)

    def get_password_value(self) -> str:
        """
        Get the current value of the password field.

        Returns:
            Password field value
        """
        return self.get_input_value(self.locators.PASSWORD_INPUT)

    def wait_for_login_page_to_load(self) -> "LoginPagePW":
        """
        Wait for the login page to fully load.
        Verifies login button is visible using Playwright's auto-waiting.

        Returns:
            Self for method chaining

        Note:
            navigate_to() already waits for 'domcontentloaded' by default.
            This method adds an extra check that the login button is visible.
        """
        # expect() with auto-waiting - waits until button is visible
        expect(self.page.locator(self.locators.LOGIN_BUTTON)).to_be_visible()
        return self

    def highlight_login_button(self, duration: int = 2) -> "LoginPagePW":
        """
        Highlight the login button for debugging.

        Args:
            duration: Duration in seconds to highlight

        Returns:
            Self for method chaining
        """
        self.highlight_element(self.locators.LOGIN_BUTTON, duration=duration)
        return self
