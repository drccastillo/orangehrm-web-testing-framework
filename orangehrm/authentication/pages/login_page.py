"""
Login Page Object Model for OrangeHRM application.
Contains methods specific to the login page functionality.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from framework.page import BasePage
from orangehrm.authentication.pages.locators import LoginLocators


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

    # Expose locators as properties for backward compatibility
    @property
    def USERNAME_INPUT(self):
        return self.locators.USERNAME_INPUT

    @property
    def PASSWORD_INPUT(self):
        return self.locators.PASSWORD_INPUT

    @property
    def LOGIN_BUTTON(self):
        return self.locators.LOGIN_BUTTON

    @property
    def ERROR_MESSAGE(self):
        return self.locators.ERROR_MESSAGE

    @property
    def FORGOT_PASSWORD_LINK(self):
        return self.locators.FORGOT_PASSWORD_LINK

    @property
    def LOGIN_LOGO(self):
        return self.locators.LOGIN_LOGO

    @property
    def LOGIN_TITLE(self):
        return self.locators.LOGIN_TITLE

    def enter_username(self, username: str) -> 'LoginPage':
        """
        Enter username in the username field.

        Args:
            username: Username to enter

        Returns:
            Self for method chaining
        """
        self.send_keys(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> 'LoginPage':
        """
        Enter password in the password field.

        Args:
            password: Password to enter

        Returns:
            Self for method chaining
        """
        self.send_keys(self.PASSWORD_INPUT, password)
        return self

    def click_login_button(self) -> 'LoginPage':
        """
        Click the login button to submit credentials.

        Returns:
            Self for method chaining
        """
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str) -> None:
        """
        Perform complete login action.

        Args:
            username: Username to login with
            password: Password to login with
        """
        self.logger.info(f"Attempting login with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        self.logger.info("Login action completed")

    def get_error_message(self) -> str:
        """
        Get the error message displayed on failed login.

        Returns:
            Error message text
        """
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_message_displayed(self) -> bool:
        """
        Check if error message is displayed.

        Returns:
            True if error message is visible, False otherwise
        """
        return self.is_element_visible(self.ERROR_MESSAGE)

    def click_forgot_password(self) -> None:
        """Click the 'Forgot Password' link."""
        self.click(self.FORGOT_PASSWORD_LINK)

    def is_login_page_loaded(self) -> bool:
        """
        Verify if the login page is fully loaded.

        Returns:
            True if login page elements are visible, False otherwise
        """
        self.logger.debug("Checking if login page is loaded")
        is_loaded = (
            self.is_element_visible(self.USERNAME_INPUT) and
            self.is_element_visible(self.PASSWORD_INPUT) and
            self.is_element_visible(self.LOGIN_BUTTON)
        )
        self.logger.debug(f"Login page loaded: {is_loaded}")
        return is_loaded

    def get_login_title(self) -> str:
        """
        Get the login page title text.

        Returns:
            Login title text
        """
        return self.get_text(self.LOGIN_TITLE)

    def is_logo_displayed(self) -> bool:
        """
        Check if the OrangeHRM logo is displayed.

        Returns:
            True if logo is visible, False otherwise
        """
        return self.is_element_visible(self.LOGIN_LOGO)

    def clear_username(self) -> 'LoginPage':
        """
        Clear the username field.

        Returns:
            Self for method chaining
        """
        username_field = self.find_element(self.USERNAME_INPUT)
        username_field.clear()
        return self

    def clear_password(self) -> 'LoginPage':
        """
        Clear the password field.

        Returns:
            Self for method chaining
        """
        password_field = self.find_element(self.PASSWORD_INPUT)
        password_field.clear()
        return self
