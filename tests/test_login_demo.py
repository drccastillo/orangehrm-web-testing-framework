"""
Demo tests showing Playwright's native highlight() and expect() functionality.

These tests demonstrate how to use Playwright's built-in methods for visual
debugging during test development, while maintaining the Page Object Model
pattern and using Playwright assertions.

IMPORTANT:
- highlight() is for debugging only
- These tests are for development/learning purposes
- Use --headed flag to see the highlights visually

Run demo:
    pytest tests/test_login_demo.py --headed
    pytest tests/test_login_demo.py::test_login_with_highlight_demo --headed -s
"""

import re
import time

import pytest
from playwright.sync_api import expect

from src.ui.pages.login.login_page import LoginPage
from utils.logger import TestLogger

# Initialize logger for this module
logger = TestLogger.get_logger(__name__)


# @pytest.mark.skip(reason="Demo test with highlight - for development/debugging only")
def test_login_with_highlight_demo(login_page: LoginPage, config_service):
    """
    Demo: Login test with visual highlighting for debugging.

    This test shows how to use Playwright's native highlight() during development
    to visually identify which elements are being interacted with.

    Scenario:
        Given: User is on the login page
        When: User enters valid credentials with visual highlights
        Then: User should be redirected to dashboard

    Args:
        login_page: LoginPage instance
        config_service: Configuration service with credentials
    """
    logger.info("Starting login demo with visual highlights")

    # Arrange
    username = config_service.username
    password = config_service.password

    # Act - Step 1: Highlight and enter username
    login_page.username_input.highlight()
    time.sleep(1)  # Pause to see highlight

    login_page.enter_username(username)
    logger.debug(f"Entered username: {username}")

    # Act - Step 2: Highlight and enter password
    login_page.password_input.highlight()
    time.sleep(1)

    login_page.enter_password(password)
    logger.debug("Entered password")

    # Act - Step 3: Highlight and click login button
    login_page.login_button.highlight()
    time.sleep(1)

    login_page.click_login_button()
    logger.debug("Clicked login button")

    # Assert - Playwright expect with auto-waiting
    expect(login_page.page).to_have_url(re.compile(r"dashboard"), timeout=10000)
    logger.info("Login demo completed successfully - redirected to dashboard")


# @pytest.mark.skip(reason="Demo test with highlight - for development/debugging only")
def test_invalid_login_with_highlight(login_page: LoginPage):
    """
    Demo: Invalid login attempt with visual highlighting.

    Shows how to use highlight() when debugging error scenarios.

    Scenario:
        Given: User is on the login page
        When: User enters invalid credentials with highlights
        Then: Error message should be visible and highlighted

    Args:
        login_page: LoginPage instance
    """
    logger.info("Starting invalid login demo with visual highlights")

    # Arrange
    invalid_username = "invalid_user"
    invalid_password = "invalid_password"

    # Act - Highlight and enter invalid username
    login_page.username_input.highlight()
    time.sleep(0.5)
    login_page.enter_username(invalid_username)

    # Act - Highlight and enter invalid password
    login_page.password_input.highlight()
    time.sleep(0.5)
    login_page.enter_password(invalid_password)

    # Act - Highlight and click login button
    login_page.login_button.highlight()
    time.sleep(0.5)
    login_page.click_login_button()

    # Assert - Highlight and verify error message
    time.sleep(1)  # Wait for error to appear
    login_page.error_message.highlight()
    time.sleep(1)

    # Use Playwright expect for assertions
    expect(login_page.error_message).to_be_visible(timeout=5000)
    expect(login_page.error_message).to_contain_text("Invalid credentials")

    logger.info("Invalid login handled correctly - error message displayed")


# @pytest.mark.skip(reason="Demo test with highlight - for development/debugging only")
def test_method_chaining_with_highlight(login_page: LoginPage, config_service):
    """
    Demo: Method chaining with selective highlighting.

    Shows how to combine fluent API with strategic highlights for debugging.

    Scenario:
        Given: User is on the login page
        When: User previews elements with highlights
        And: User executes login with method chaining
        Then: Login should succeed

    Args:
        login_page: LoginPage instance
        config_service: Configuration service
    """
    logger.info("Starting method chaining demo with selective highlights")

    # Arrange
    username = config_service.username
    password = config_service.password

    # Act - Highlight the elements we're about to interact with
    login_page.username_input.highlight()
    time.sleep(0.5)

    login_page.password_input.highlight()
    time.sleep(0.5)

    login_page.login_button.highlight()
    time.sleep(0.5)

    # Act - Execute with method chaining
    logger.debug("Executing login with method chaining")
    login_page.enter_username(username).enter_password(password).click_login_button()

    # Assert - Playwright expect
    expect(login_page.page).to_have_url(re.compile(r"dashboard"), timeout=10000)
    logger.info("Method chaining demo completed successfully")
