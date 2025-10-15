"""
Login Page Object Model for OrangeHRM application.
Contains methods specific to the login page functionality.
"""

from selenium.webdriver.remote.webdriver import WebDriver

from src.pages_selenium.base_page import BasePage
from src.pages_selenium.locators.login_locators import LoginLocators


class LoginPage(BasePage):
    """
    Page Object Model for the OrangeHRM Login Page.
    Inherits common functionality from BasePage.
    """

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initialize the Login Page.

        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout for explicit waits in seconds
        """
        super().__init__(driver, timeout)
        self.locators = LoginLocators

    def enter_username(self, username: str) -> "LoginPage":
        """
        Enter username in the username field.

        Args:
            username: Username to enter

        Returns:
            Self for method chaining
        """
        self.send_keys(self.locators.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """
        Enter password in the password field.

        Args:
            password: Password to enter

        Returns:
            Self for method chaining
        """
        self.send_keys(self.locators.PASSWORD_INPUT, password)
        return self

    def click_login_button(self) -> None:
        """Click the login button to submit credentials."""
        self.click(self.locators.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """
        Perform complete login action.

        Args:
            username: Username to login with
            password: Password to login with
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def get_error_message(self) -> str:
        """
        Get the error message displayed on failed login.

        Returns:
            Error message text
        """
        return self.get_text(self.locators.ERROR_MESSAGE)

    def is_error_message_displayed(self) -> bool:
        """
        Check if error message is displayed.

        Returns:
            True if error message is visible, False otherwise
        """
        return self.is_element_visible(self.locators.ERROR_MESSAGE)

    def click_forgot_password(self) -> None:
        """Click the 'Forgot Password' link."""
        self.click(self.locators.FORGOT_PASSWORD_LINK)

    def is_page_loaded(self) -> bool:
        """
        Verify if the login page is fully loaded.

        Returns:
            True if login page elements are visible, False otherwise
        """
        return (
            self.is_element_visible(self.locators.USERNAME_INPUT)
            and self.is_element_visible(self.locators.PASSWORD_INPUT)
            and self.is_element_visible(self.locators.LOGIN_BUTTON)
        )

    def get_login_title(self) -> str:
        """
        Get the login page title text.

        Returns:
            Login title text
        """
        return self.get_text(self.locators.LOGIN_TITLE)

    def is_login_logo_visible(self) -> bool:
        """
        Check if the OrangeHRM login logo is visible.

        Returns:
            True if logo is visible, False otherwise
        """
        return self.is_element_visible(self.locators.LOGIN_LOGO)

    def is_forgot_password_link_visible(self) -> bool:
        """
        Check if the forgot password link is visible.

        Returns:
            True if the link is visible, False otherwise
        """
        return self.is_element_visible(self.locators.FORGOT_PASSWORD_LINK)

    def clear_username(self) -> "LoginPage":
        """
        Clear the username field.

        Returns:
            Self for method chaining
        """
        username_field = self.find_element(self.locators.USERNAME_INPUT)
        username_field.clear()
        return self

    def clear_password(self) -> "LoginPage":
        """
        Clear the password field.

        Returns:
            Self for method chaining
        """
        password_field = self.find_element(self.locators.PASSWORD_INPUT)
        password_field.clear()
        return self
