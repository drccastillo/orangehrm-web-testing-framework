"""
Playwright locators for the Login Page.

These locators use Playwright selector syntax for modern web automation.
"""

from src.core.playwright_locator import PlaywrightLocator


class LoginLocators:
    """
    Playwright locator value objects for the Login Page.

    These locators use PlaywrightLocator which implements the Locator protocol.
    They use native Playwright selector syntax for optimal performance.

    Benefits:
        - Type safety at creation time
        - Self-documenting with descriptions
        - Native Playwright selectors (no conversion needed)
        - Validation on construction

    Example:
        >>> playwright_browser = PlaywrightBrowserAdapter(page)
        >>> page = LoginPage(playwright_browser)
        >>> page.send_keys(LoginLocators.USERNAME_INPUT, "admin")
        >>> # PlaywrightBrowserAdapter uses the selector directly
    """

    # Input fields
    USERNAME_INPUT = PlaywrightLocator("input[name='username']", "Username input field")

    PASSWORD_INPUT = PlaywrightLocator("input[name='password']", "Password input field")

    # Buttons
    LOGIN_BUTTON = PlaywrightLocator("button[type='submit']", "Login submit button")

    # Messages and alerts
    ERROR_MESSAGE = PlaywrightLocator(".oxd-alert-content-text", "Login error message")

    # Branding elements
    LOGIN_LOGO = PlaywrightLocator(".orangehrm-login-branding img", "OrangeHRM logo")

    LOGIN_TITLE = PlaywrightLocator(".orangehrm-login-title", "Login page title")
