"""
Locators for the Login Page using value objects (Phase 2.1).
Replaces primitive tuples with rich SeleniumLocator objects.
"""

from src.core.locator import LocatorStrategy
from src.core.selenium_locator import SeleniumLocator


class LoginLocators:
    """
    Locator value objects for the Login Page.

    Uses SeleniumLocator instead of primitive tuples for:
    - Type safety
    - Self-documentation
    - Framework-agnostic representation
    - Validation at creation time

    Example:
        >>> LoginLocators.USERNAME_INPUT
        SeleniumLocator(Username input field)

        >>> LoginLocators.USERNAME_INPUT.to_native()
        (By.NAME, "username")
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
        LocatorStrategy.CSS,
        ".orangehrm-login-forgot-header",
        "Forgot password link",
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
