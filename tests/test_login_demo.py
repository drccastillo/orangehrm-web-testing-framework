"""
Demo tests showing Playwright's native highlight() functionality.

These tests demonstrate how to use Playwright's built-in highlight() method
for visual debugging during test development, while maintaining the Page Object
Model pattern.

IMPORTANT:
- highlight() is for debugging only
- Remove or skip these tests before committing to production
- Use --headed flag to see the highlights visually

Run demo:
    pytest tests/test_login_demo.py --headed
    pytest tests/test_login_demo.py::test_login_with_highlight_demo --headed -s
"""

import time

import pytest

from src.pages.login_page import LoginPage
from utils.logger import TestLogger

# Initialize logger for this module
logger = TestLogger.get_logger(__name__)


# @pytest.mark.skip(reason="Demo test with highlight - for development/debugging only")
@pytest.mark.smoke
def test_login_with_highlight_demo(login_page: LoginPage, config_service):
    """
    Demo: Login test with visual highlighting for debugging.

    This test shows how to use Playwright's native highlight() during development
    to visually identify which elements are being interacted with.

    Steps:
    1. Highlight username field, then enter username
    2. Highlight password field, then enter password
    3. Highlight login button, then click it
    4. Verify successful login

    Usage:
        pytest tests/test_login_demo.py::test_login_with_highlight_demo --headed -s

    Args:
        login_page: LoginPage instance
        config_service: Configuration service with credentials
    """
    logger.info("Starting login demo with visual highlights")

    # Step 1: Highlight and enter username
    username_field = login_page.locators.USERNAME_INPUT(login_page.page)
    username_field.highlight()
    time.sleep(1)  # Pause to see highlight

    login_page.enter_username(config_service.username)
    logger.debug(f"Entered username: {config_service.username}")

    # Step 2: Highlight and enter password
    password_field = login_page.locators.PASSWORD_INPUT(login_page.page)
    password_field.highlight()
    time.sleep(1)

    login_page.enter_password(config_service.password)
    logger.debug("Entered password")

    # Step 3: Highlight and click login button
    login_button = login_page.locators.LOGIN_BUTTON(login_page.page)
    login_button.highlight()
    time.sleep(1)

    login_page.click_login_button()
    logger.debug("Clicked login button")

    # Step 4: Verify successful login
    current_url = login_page.get_current_url()
    assert "dashboard" in current_url, f"Expected dashboard URL, got: {current_url}"
    logger.info("Login demo completed successfully - redirected to dashboard")


# @pytest.mark.skip(reason="Demo test with highlight - for development/debugging only")
@pytest.mark.smoke
def test_invalid_login_with_highlight(login_page: LoginPage):
    """
    Demo: Invalid login attempt with visual highlighting.

    Shows how to use highlight() when debugging error scenarios.

    Usage:
        pytest tests/test_login_demo.py::test_invalid_login_with_highlight --headed -s

    Args:
        login_page: LoginPage instance
    """
    logger.info("Starting invalid login demo with visual highlights")

    # Highlight and enter invalid username
    login_page.locators.USERNAME_INPUT(login_page.page).highlight()
    time.sleep(0.5)
    login_page.enter_username("invalid_user")

    # Highlight and enter invalid password
    login_page.locators.PASSWORD_INPUT(login_page.page).highlight()
    time.sleep(0.5)
    login_page.enter_password("invalid_password")

    # Highlight and click login button
    login_page.locators.LOGIN_BUTTON(login_page.page).highlight()
    time.sleep(0.5)
    login_page.click_login_button()

    # Highlight error message
    time.sleep(1)  # Wait for error to appear
    error_locator = login_page.locators.ERROR_MESSAGE(login_page.page)
    error_locator.highlight()
    time.sleep(1)

    # Verify error is displayed
    assert login_page.is_error_message_displayed(), "Error message should be visible"
    error_text = login_page.get_error_message()
    logger.info(f"Invalid login handled correctly - error message: '{error_text}'")


# @pytest.mark.skip(reason="Demo test with highlight - for development/debugging only")
@pytest.mark.regression
def test_method_chaining_with_highlight(login_page: LoginPage, config_service):
    """
    Demo: Method chaining with selective highlighting.

    Shows how to combine fluent API with strategic highlights for debugging.

    Usage:
        pytest tests/test_login_demo.py::test_method_chaining_with_highlight --headed -s

    Args:
        login_page: LoginPage instance
        config_service: Configuration service
    """
    logger.info("Starting method chaining demo with selective highlights")

    # Highlight the elements we're about to interact with
    login_page.locators.USERNAME_INPUT(login_page.page).highlight()
    time.sleep(0.5)

    login_page.locators.PASSWORD_INPUT(login_page.page).highlight()
    time.sleep(0.5)

    login_page.locators.LOGIN_BUTTON(login_page.page).highlight()
    time.sleep(0.5)

    # Execute with method chaining
    logger.debug("Executing login with method chaining")
    login_page.enter_username(config_service.username).enter_password(
        config_service.password
    ).click_login_button()

    # Verify
    current_url = login_page.get_current_url()
    assert "dashboard" in current_url, "Login with method chaining should succeed"
    logger.info("Method chaining demo completed successfully")
