"""
Locators for the Login Page.
Centralizes all element locators for easier maintenance.
"""
from typing import Tuple
from selenium.webdriver.common.by import By


class LoginLocators:
    """Locator constants for the Login Page."""

    # Input fields
    USERNAME_INPUT: Tuple[str, str] = (By.NAME, "username")
    PASSWORD_INPUT: Tuple[str, str] = (By.NAME, "password")

    # Buttons
    LOGIN_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, "button[type='submit']")

    # Links
    FORGOT_PASSWORD_LINK: Tuple[str, str] = (By.CSS_SELECTOR, ".orangehrm-login-forgot-header")

    # Messages and alerts
    ERROR_MESSAGE: Tuple[str, str] = (By.CSS_SELECTOR, ".oxd-alert-content-text")

    # Branding elements
    LOGIN_LOGO: Tuple[str, str] = (By.CSS_SELECTOR, ".orangehrm-login-branding img")
    LOGIN_TITLE: Tuple[str, str] = (By.CSS_SELECTOR, ".orangehrm-login-title")
