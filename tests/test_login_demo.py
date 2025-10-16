"""
Demo test showing Playwright's native highlight() functionality.

This test demonstrates how to use Playwright's built-in highlight() method
for visual debugging during test development.

Note: highlight() is for debugging only. Remove or comment out before committing.
"""

import time

import pytest

from src.config.protocols import ConfigService
from src.pages.login_page import LoginPage


@pytest.mark.smoke
def test_login_with_highlight_demo(login_page: LoginPage, config_service: ConfigService):
    """
    Demo test showing Playwright's native highlight() for visual debugging.

    This test demonstrates:
    1. Using locator.highlight() to visually identify elements
    2. Slowing down execution to see highlights
    3. Debugging test steps visually

    WARNING: Remove highlight() calls before committing to production!

    Args:
        login_page: LoginPage instance
        config_service: Configuration service with credentials
    """
    # Get the locators (they return Playwright Locator objects)
    username_locator = login_page.locators.USERNAME_INPUT(login_page.page)
    password_locator = login_page.locators.PASSWORD_INPUT(login_page.page)
    login_button = login_page.locators.LOGIN_BUTTON(login_page.page)

    # Highlight username field (Playwright's native method)
    print("\n🔍 Highlighting username field...")
    username_locator.highlight()
    time.sleep(1)  # Pause to see the highlight

    # Enter username
    login_page.enter_username(config_service.username)
    time.sleep(0.5)

    # Highlight password field
    print("🔍 Highlighting password field...")
    password_locator.highlight()
    time.sleep(1)

    # Enter password
    login_page.enter_password(config_service.password)
    time.sleep(0.5)

    # Highlight login button
    print("🔍 Highlighting login button...")
    login_button.highlight()
    time.sleep(1)

    # Click login
    login_page.click_login_button()

    # Verify successful login
    assert "dashboard" in login_page.get_current_url(), "Should redirect to dashboard"
    print("✅ Login successful!\n")


@pytest.mark.smoke
def test_login_highlight_alternative(login_page: LoginPage, config_service: ConfigService):
    """
    Alternative demo: Highlight elements inline during actions.

    This shows a more compact way to use highlight() during development.

    Args:
        login_page: LoginPage instance
        config_service: Configuration service
    """
    # Highlight and interact in one flow
    print("\n🔍 Demo: Inline highlighting...")

    # Username
    username_loc = login_page.locators.USERNAME_INPUT(login_page.page)
    username_loc.highlight()
    username_loc.fill(config_service.username)
    time.sleep(0.5)

    # Password
    password_loc = login_page.locators.PASSWORD_INPUT(login_page.page)
    password_loc.highlight()
    password_loc.fill(config_service.password)
    time.sleep(0.5)

    # Login button
    button_loc = login_page.locators.LOGIN_BUTTON(login_page.page)
    button_loc.highlight()
    button_loc.click()

    # Verify
    assert "dashboard" in login_page.get_current_url()
    print("✅ Alternative method works!\n")


@pytest.mark.smoke
def test_login_without_highlight(login_page: LoginPage, config_service: ConfigService):
    """
    Normal test WITHOUT highlight - this is production-ready.

    Compare this with the demo tests above to see the difference.

    Args:
        login_page: LoginPage instance
        config_service: Configuration service
    """
    # Normal test - no highlight, fast execution
    login_page.login(config_service.username, config_service.password)
    assert "dashboard" in login_page.get_current_url()
