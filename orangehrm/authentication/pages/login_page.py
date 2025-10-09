"""
Login Page Object Model using Mixins pattern (ISP).
Clean architecture - uses ONLY Mixins, NO BasePage inheritance.
"""
import allure
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver

# Import only the mixins we need
from framework.page.mixins import (
    ElementFinderMixin,
    ElementInteractorMixin,
    ElementValidatorMixin,
    NavigationMixin,
)

# Import components
from framework.page.components import (
    ElementFinder,
    ElementInteractor,
    ElementValidator,
    NavigationHelper,
)

# Import config and locators
from framework.config.interface import ConfigInterface
from framework.config.settings import Config
from framework.utils.logger import TestLogger
from orangehrm.authentication.pages.locators import LoginLocators as Locators


class LoginPage(
    ElementFinderMixin,
    ElementInteractorMixin,
    ElementValidatorMixin,
    NavigationMixin,
):
    """
    Login Page using Mixins pattern (NEW CLEAN ARCHITECTURE).

    Uses ONLY Mixins - NO BasePage inheritance.
    Follows Interface Segregation Principle (ISP).

    Mixins included:
    - ElementFinderMixin: Finding elements
    - ElementInteractorMixin: Clicking, typing, etc.
    - ElementValidatorMixin: Checking visibility, presence
    - NavigationMixin: URL navigation

    Note: VisualDebugMixin and JavaScriptMixin NOT included (not needed).
    """

    def __init__(
        self,
        driver: WebDriver,
        timeout: int = 10,
        config: Optional[ConfigInterface] = None
    ):
        """
        Initialize Login Page with only required components.

        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout for waits
            config: Configuration instance (defaults to Config class)
        """
        # Store essentials
        self.driver = driver
        self.timeout = timeout
        self.config = config if config is not None else Config()
        self.logger = TestLogger.get_logger(self.__class__.__name__)

        # Initialize ONLY the components we need (Composition)
        self.finder = ElementFinder(driver, timeout)
        self.interactor = ElementInteractor(driver, timeout)
        self.validator = ElementValidator(driver, timeout)
        self.navigation = NavigationHelper(driver)

        # Note: No VisualDebugger, no JavaScriptExecutor
        # This is ISP - only include what you need!

    @allure.step("Enter username: {username}")
    def enter_username(self, username: str) -> 'LoginPage':
        """
        Enter username in the username field.

        Args:
            username: Username to enter

        Returns:
            Self for method chaining
        """
        self.send_keys(Locators.USERNAME_INPUT, username)
        return self

    @allure.step("Enter password")
    def enter_password(self, password: str) -> 'LoginPage':
        """
        Enter password in the password field.

        Args:
            password: Password to enter

        Returns:
            Self for method chaining
        """
        self.send_keys(Locators.PASSWORD_INPUT, password)
        return self

    @allure.step("Click login button")
    def click_login_button(self) -> 'LoginPage':
        """
        Click the login button to submit credentials.

        Returns:
            Self for method chaining
        """
        self.click(Locators.LOGIN_BUTTON)
        return self

    @allure.step("Login with username: {username}")
    def login(self, username: str, password: str) -> 'LoginPage':
        """
        Perform complete login action.

        Args:
            username: Username to login with
            password: Password to login with

        Returns:
            Self for method chaining
        """
        self.logger.info(f"Attempting login with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        self.logger.info("Login action completed")
        return self

    @allure.step("Get error message text")
    def get_error_message(self) -> str:
        """
        Get the error message displayed on failed login.

        Returns:
            Error message text
        """
        return self.get_text(Locators.ERROR_MESSAGE)

    @allure.step("Check if error message is displayed")
    def is_error_message_displayed(self) -> bool:
        """
        Check if error message is displayed.

        Returns:
            True if error message is visible, False otherwise
        """
        return self.is_element_visible(Locators.ERROR_MESSAGE)

    def click_forgot_password(self) -> 'LoginPage':
        """
        Click the 'Forgot Password' link.

        Returns:
            Self for method chaining
        """
        self.click(Locators.FORGOT_PASSWORD_LINK)
        return self

    @allure.step("Verify login page is loaded")
    def is_login_page_loaded(self) -> bool:
        """
        Verify if the login page is fully loaded.

        Returns:
            True if login page elements are visible, False otherwise
        """
        self.logger.debug("Checking if login page is loaded")
        is_loaded = (
            self.is_element_visible(Locators.USERNAME_INPUT) and
            self.is_element_visible(Locators.PASSWORD_INPUT) and
            self.is_element_visible(Locators.LOGIN_BUTTON)
        )
        self.logger.debug(f"Login page loaded: {is_loaded}")
        return is_loaded

    def get_login_title(self) -> str:
        """
        Get the login page title text.

        Returns:
            Login title text
        """
        return self.get_text(Locators.LOGIN_TITLE)

    @allure.step("Check if logo is displayed")
    def is_logo_displayed(self) -> bool:
        """
        Check if the OrangeHRM logo is displayed.

        Returns:
            True if logo is visible, False otherwise
        """
        return self.is_element_visible(Locators.LOGIN_LOGO)

    @allure.step("Verify username field is visible")
    def is_username_field_visible(self) -> bool:
        """
        Check if the username input field is visible.

        Returns:
            True if username field is visible, False otherwise
        """
        return self.is_element_visible(Locators.USERNAME_INPUT)

    @allure.step("Verify password field is visible")
    def is_password_field_visible(self) -> bool:
        """
        Check if the password input field is visible.

        Returns:
            True if password field is visible, False otherwise
        """
        return self.is_element_visible(Locators.PASSWORD_INPUT)

    @allure.step("Verify login button is visible")
    def is_login_button_visible(self) -> bool:
        """
        Check if the login button is visible.

        Returns:
            True if login button is visible, False otherwise
        """
        return self.is_element_visible(Locators.LOGIN_BUTTON)

    def clear_username(self) -> 'LoginPage':
        """
        Clear the username field.

        Returns:
            Self for method chaining
        """
        username_field = self.find_element(Locators.USERNAME_INPUT)
        username_field.clear()
        return self

    def clear_password(self) -> 'LoginPage':
        """
        Clear the password field.

        Returns:
            Self for method chaining
        """
        password_field = self.find_element(Locators.PASSWORD_INPUT)
        password_field.clear()
        return self

    @allure.step("Navigate to login page")
    def navigate_to_login(self) -> 'LoginPage':
        """
        Navigate to login page using injected config.

        Returns:
            Self for method chaining
        """
        self.navigate_to(self.config.base_url)
        return self
