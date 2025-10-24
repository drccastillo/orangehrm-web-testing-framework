"""
Simplified Login Page Object Model for OrangeHRM application.

This LoginPage uses Playwright Page directly, eliminating adapter overhead.
"""

# pylint: disable=import-error  # src module is in project root
from playwright.sync_api import Locator, Page

from src.ui.pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object Model for the OrangeHRM Login Page using Playwright.

    Benefits:
        - Direct access to Playwright API
        - No adapter overhead
        - Simpler, more maintainable code
        - Full power of Playwright features
        - Encapsulated locators within the page object

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

        # Input fields - using placeholder text (user-facing)
        self.username_input: Locator = page.get_by_placeholder("Username")
        self.password_input: Locator = page.get_by_placeholder("Password")

        # Buttons - using role (accessibility-first)
        self.login_button: Locator = page.get_by_role("button", name="Login")

        # Messages and alerts - using text
        self.error_message: Locator = page.get_by_text("Invalid credentials")

        # Branding elements
        self.login_branding: Locator = page.get_by_alt_text("company-branding")
        # Multiple logos exist; use .last to get the visible one (first is hidden)
        self.login_logo: Locator = page.get_by_alt_text("orangehrm-logo").last
        self.login_title: Locator = page.get_by_role("heading", name="Login")
        self.forgot_password_link: Locator = page.get_by_text("Forgot your password?")
        self.login_footer: Locator = page.get_by_text("OrangeHRM OS")
        self.copyright_text: Locator = page.get_by_text("© 2005 - 2025 OrangeHRM, Inc")

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
        self.send_keys(self.username_input, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """
        Enter password in the password field.

        Args:
            password: Password to enter

        Returns:
            Self for method chaining
        """
        self.send_keys(self.password_input, password)
        return self

    def click_login_button(self) -> None:
        """Click the login button to submit credentials."""
        self.click(self.login_button)

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

    def clear_username(self) -> "LoginPage":
        """
        Clear the username field.

        Returns:
            Self for method chaining

        Example:
            >>> login_page.enter_username("wrong").clear_username().enter_username("correct")
        """
        self.username_input.clear()
        return self

    def clear_password(self) -> "LoginPage":
        """
        Clear the password field.

        Returns:
            Self for method chaining

        Example:
            >>> login_page.enter_password("wrong").clear_password().enter_password("correct")
        """
        self.password_input.clear()
        return self
