"""
Login test suite with Playwright assertions and Gherkin-style documentation.

All tests follow AAA (Arrange-Act-Assert) pattern using Playwright's native
expect() assertions for auto-waiting and better error messages.

Run tests:
    pytest tests/test_login.py -v

Run with specific browser:
    pytest tests/test_login.py --browser=firefox
    pytest tests/test_login.py --browser=chromium
"""

import re

import pytest
from playwright.sync_api import expect

from src.pages.login_page import LoginPage


@pytest.mark.smoke
def test_valid_login(login_page: LoginPage, config_service):
    """
    Verify user can login successfully with valid credentials.

    Scenario:
        Given: User is on the login page
        When: User enters valid username and password
        And: User clicks the login button
        Then: User should be redirected to the dashboard page

    Args:
        login_page: LoginPage instance (already navigated to login page)
        config_service: Configuration service with valid test credentials
    """
    # Arrange
    valid_username = config_service.username
    valid_password = config_service.password

    # Act
    login_page.login(valid_username, valid_password)

    # Assert - Playwright assertions with auto-waiting
    expect(login_page.page).to_have_url(re.compile(r"dashboard"), timeout=10000)


@pytest.mark.smoke
def test_invalid_login(login_page: LoginPage):
    """
    Verify error message is displayed when login fails with invalid credentials.

    Scenario:
        Given: User is on the login page
        When: User enters invalid username and password
        And: User clicks the login button
        Then: Error message should be visible
        And: Error message should contain "Invalid credentials"

    Args:
        login_page: LoginPage instance
    """
    # Arrange
    invalid_username = "invalid_user"
    invalid_password = "invalid_password"

    # Act
    login_page.login(invalid_username, invalid_password)

    # Assert - Playwright assertions
    error_locator = login_page.locators.ERROR_MESSAGE(login_page.page)
    expect(error_locator).to_be_visible(timeout=5000)
    expect(error_locator).to_contain_text("Invalid credentials")


@pytest.mark.smoke
def test_login_page_elements_visible(login_page: LoginPage):
    """
    Verify all critical login page elements are visible on page load.

    Scenario:
        Given: User is on the login page
        When: Page finishes loading
        Then: Username field should be visible
        And: Password field should be visible
        And: Login button should be visible
        And: Login logo should be visible

    Args:
        login_page: LoginPage instance
    """
    # Arrange
    # (Fixture already navigated to login page)

    # Act
    # (Page load happens automatically)

    # Assert - Verify all key elements are visible
    expect(login_page.locators.USERNAME_INPUT(login_page.page)).to_be_visible()
    expect(login_page.locators.PASSWORD_INPUT(login_page.page)).to_be_visible()
    expect(login_page.locators.LOGIN_BUTTON(login_page.page)).to_be_visible()
    expect(login_page.locators.LOGIN_LOGO(login_page.page)).to_be_visible()


@pytest.mark.regression
def test_empty_credentials(login_page: LoginPage):
    """
    Verify user cannot login with empty username and password.

    Scenario:
        Given: User is on the login page
        When: User clicks login button without entering credentials
        Then: User should remain on the login page
        And: URL should still contain "auth/login"

    Args:
        login_page: LoginPage instance
    """
    # Arrange
    # (No credentials to enter)

    # Act
    login_page.click_login_button()

    # Assert - Should remain on login page
    expect(login_page.page).to_have_url(re.compile(r"auth/login"), timeout=5000)


@pytest.mark.regression
def test_empty_username(login_page: LoginPage):
    """
    Verify user cannot login with empty username.

    Scenario:
        Given: User is on the login page
        When: User enters only password (no username)
        And: User clicks the login button
        Then: User should remain on the login page

    Args:
        login_page: LoginPage instance
    """
    # Arrange
    password_only = "somepassword"

    # Act
    login_page.enter_password(password_only)
    login_page.click_login_button()

    # Assert - Should remain on login page
    expect(login_page.page).to_have_url(re.compile(r"auth/login"), timeout=5000)


@pytest.mark.regression
def test_empty_password(login_page: LoginPage):
    """
    Verify user cannot login with empty password.

    Scenario:
        Given: User is on the login page
        When: User enters only username (no password)
        And: User clicks the login button
        Then: User should remain on the login page

    Args:
        login_page: LoginPage instance
    """
    # Arrange
    username_only = "someuser"

    # Act
    login_page.enter_username(username_only)
    login_page.click_login_button()

    # Assert - Should remain on login page
    expect(login_page.page).to_have_url(re.compile(r"auth/login"), timeout=5000)


@pytest.mark.regression
def test_method_chaining(login_page: LoginPage, config_service):
    """
    Verify fluent API (method chaining) works correctly for login flow.

    Scenario:
        Given: User is on the login page
        When: User chains enter_username, enter_password, and click_login methods
        Then: User should be redirected to dashboard (login successful)

    Args:
        login_page: LoginPage instance
        config_service: Configuration service with valid credentials
    """
    # Arrange
    username = config_service.username
    password = config_service.password

    # Act - Test method chaining (fluent interface)
    login_page.enter_username(username).enter_password(password).click_login_button()

    # Assert - Login should succeed with method chaining
    expect(login_page.page).to_have_url(re.compile(r"dashboard"), timeout=10000)
