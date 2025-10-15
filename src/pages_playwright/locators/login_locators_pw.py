"""
Locators for the Login Page using Playwright.
Centralizes all element locators for easier maintenance.

Playwright uses string-based selectors instead of tuples.
"""


class LoginLocatorsPW:
    """Locator constants for the Login Page (Playwright)."""

    # Input fields
    USERNAME_INPUT: str = "input[name='username']"
    PASSWORD_INPUT: str = "input[name='password']"

    # Buttons
    LOGIN_BUTTON: str = "button[type='submit']"

    # Links
    FORGOT_PASSWORD_LINK: str = ".orangehrm-login-forgot-header"

    # Messages and alerts
    ERROR_MESSAGE: str = ".oxd-alert-content-text"

    # Branding elements
    LOGIN_LOGO: str = ".orangehrm-login-branding img"
    LOGIN_TITLE: str = ".orangehrm-login-title"
