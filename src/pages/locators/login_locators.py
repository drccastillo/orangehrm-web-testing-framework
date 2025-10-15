"""
Unified locators for the Login Page.

These locators work with ANY automation framework (Selenium, Playwright, etc.)
through the Locator value object abstraction.
"""

from src.core.locator import LocatorStrategy
from src.core.selenium_locator import SeleniumLocator


class LoginLocators:
    """
    Unified locator value objects for the Login Page.

    These locators use SeleniumLocator which implements the Locator protocol.
    The browser adapters convert them to framework-specific format via to_native().

    Benefits:
        - Type safety at creation time
        - Self-documenting with descriptions
        - Framework-agnostic representation
        - Validation on construction
        - Works with Selenium AND Playwright

    Example (Selenium):
        >>> selenium_browser = SeleniumBrowserAdapter(driver)
        >>> page = LoginPage(selenium_browser)
        >>> page.send_keys(LoginLocators.USERNAME_INPUT, "admin")
        >>> # SeleniumBrowserAdapter calls USERNAME_INPUT.to_native() -> (By.NAME, "username")

    Example (Playwright):
        >>> playwright_browser = PlaywrightBrowserAdapter(page)
        >>> page = LoginPage(playwright_browser)
        >>> page.send_keys(LoginLocators.USERNAME_INPUT, "admin")
        >>> # PlaywrightBrowserAdapter calls USERNAME_INPUT.to_native() -> "input[name='username']"
    """

    # Input fields
    USERNAME_INPUT = SeleniumLocator(LocatorStrategy.NAME, "username", "Username input field")

    PASSWORD_INPUT = SeleniumLocator(LocatorStrategy.NAME, "password", "Password input field")

    # Buttons
    LOGIN_BUTTON = SeleniumLocator(
        LocatorStrategy.CSS, "button[type='submit']", "Login submit button"
    )

    # Links
    FORGOT_PASSWORD_LINK = SeleniumLocator(
        LocatorStrategy.CSS, ".orangehrm-login-forgot-header", "Forgot password link"
    )

    # Messages and alerts
    ERROR_MESSAGE = SeleniumLocator(
        LocatorStrategy.CSS, ".oxd-alert-content-text", "Login error message"
    )

    # Branding elements
    LOGIN_LOGO = SeleniumLocator(
        LocatorStrategy.CSS, ".orangehrm-login-branding img", "OrangeHRM logo"
    )

    LOGIN_TITLE = SeleniumLocator(LocatorStrategy.CSS, ".orangehrm-login-title", "Login page title")
