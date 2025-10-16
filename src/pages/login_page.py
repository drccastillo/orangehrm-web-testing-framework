"""
Simplified Login Page Object Model for OrangeHRM application.

This LoginPage uses Playwright Page directly, eliminating adapter overhead.
"""

from playwright.sync_api import Page

from src.pages.base_page import BasePage
from src.pages.locators.login_locators import LoginLocators


class LoginPage(BasePage):
    """
    Page Object Model for the OrangeHRM Login Page using Playwright.

    Benefits:
        - Direct access to Playwright API
        - No adapter overhead
        - Simpler, more maintainable code
        - Full power of Playwright features

    Example:
        >>> from playwright.sync_api import sync_playwright
        >>> with sync_playwright() as p:
        ...     browser = p.chromium.launch()
        ...     page = browser.new_page()
        ...     login_page = LoginPage(page, timeout=10)
        ...     login_page.login("Admin", "admin123")
    """

    def __init__(self, page: Page, timeout: int = 10):
        """
        Initialize the Login Page.

        Args:
            page: Playwright Page instance
            timeout: Default timeout for operations in seconds
        """
        super().__init__(page, timeout)
        self.locators = LoginLocators

    def enter_username(self, username: str) -> "LoginPage":
        """
        Enter username in the username field.

        Args:
            username: Username to enter

        Returns:
            Self for method chaining

        Example:
            >>> login_page.enter_username("Admin").enter_password("pass").click_login_button()
        """
        # Use functional locator (callable)
        self.send_keys(self.locators.USERNAME_INPUT(self.page), username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """
        Enter password in the password field.

        Args:
            password: Password to enter

        Returns:
            Self for method chaining
        """
        self.send_keys(self.locators.PASSWORD_INPUT(self.page), password)
        return self

    def click_login_button(self) -> None:
        """Click the login button to submit credentials."""
        self.click(self.locators.LOGIN_BUTTON(self.page))

    def login(self, username: str, password: str) -> None:
        """
        Perform complete login action.

        This is the main method for logging into the application.
        It combines entering username, password, and clicking login button.

        Args:
            username: Username to login with
            password: Password to login with

        Example:
            >>> login_page.login("Admin", "admin123")
            >>> assert "dashboard" in login_page.get_current_url()
        """
        self.logger.info(f"Logging in with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def get_error_message(self) -> str:
        """
        Get the error message displayed on failed login.

        Returns:
            Error message text

        Example:
            >>> login_page.login("invalid", "invalid")
            >>> error = login_page.get_error_message()
            >>> assert "Invalid credentials" in error
        """
        return self.get_text(self.locators.ERROR_MESSAGE(self.page))

    def is_error_message_displayed(self) -> bool:
        """
        Check if error message is displayed.

        Returns:
            True if error message is visible, False otherwise

        Example:
            >>> login_page.login("invalid", "invalid")
            >>> assert login_page.is_error_message_displayed()
        """
        return self.is_element_visible(self.locators.ERROR_MESSAGE(self.page))

    def is_page_loaded(self) -> bool:
        """
        Verify if the login page is fully loaded.

        Checks that all critical elements are visible:
            - Username input field
            - Password input field
            - Login button

        Returns:
            True if login page elements are visible, False otherwise

        Example:
            >>> login_page.navigate_to("https://example.com/login")
            >>> assert login_page.is_page_loaded()
        """
        return (
            self.is_element_visible(self.locators.USERNAME_INPUT(self.page))
            and self.is_element_visible(self.locators.PASSWORD_INPUT(self.page))
            and self.is_element_visible(self.locators.LOGIN_BUTTON(self.page))
        )

    def get_login_title(self) -> str:
        """
        Get the login page title text.

        Returns:
            Login title text

        Example:
            >>> title = login_page.get_login_title()
            >>> assert "Login" in title
        """
        return self.get_text(self.locators.LOGIN_TITLE(self.page))

    def is_login_logo_visible(self) -> bool:
        """
        Check if the OrangeHRM login logo is visible.

        Returns:
            True if logo is visible, False otherwise

        Example:
            >>> assert login_page.is_login_logo_visible()
        """
        return self.is_element_visible(self.locators.LOGIN_LOGO(self.page))

    def clear_username(self) -> "LoginPage":
        """
        Clear the username field.

        Returns:
            Self for method chaining

        Example:
            >>> login_page.enter_username("wrong").clear_username().enter_username("correct")
        """
        username_field = self.find_element(self.locators.USERNAME_INPUT(self.page))
        username_field.clear()
        return self

    def clear_password(self) -> "LoginPage":
        """
        Clear the password field.

        Returns:
            Self for method chaining

        Example:
            >>> login_page.enter_password("wrong").clear_password().enter_password("correct")
        """
        password_field = self.find_element(self.locators.PASSWORD_INPUT(self.page))
        password_field.clear()
        return self
