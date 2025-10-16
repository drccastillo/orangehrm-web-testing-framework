"""
Login tests using Playwright.

These tests use the LoginPage class directly since we only use Playwright.

Run tests:
    pytest tests/test_login_unified.py

Run with specific browser:
    pytest tests/test_login_unified.py --browser=firefox
    pytest tests/test_login_unified.py --browser=chromium
"""

import pytest

from src.pages.login_page import LoginPage


@pytest.mark.smoke
def test_valid_login(login_page: LoginPage, config_service):
    """
    Test successful login with valid credentials.

    This test works with ANY framework (Selenium, Playwright, etc.)
    through the LoginPageProtocol interface.

    Args:
        login_page: LoginPage instance (framework-agnostic)
        config_service: Configuration service with test credentials
    """
    # Perform login
    login_page.login(config_service.username, config_service.password)

    # Verify successful login by checking URL
    current_url = login_page.get_current_url()
    assert "dashboard" in current_url, f"Expected dashboard URL, got: {current_url}"


@pytest.mark.smoke
def test_invalid_login(login_page: LoginPage):
    """
    Test login failure with invalid credentials.

    Args:
        login_page: LoginPage instance (framework-agnostic)
    """
    # Attempt login with invalid credentials
    login_page.login("invalid_user", "invalid_password")

    # Verify error message is displayed
    assert login_page.is_error_message_displayed(), "Error message should be displayed"

    # Verify error message text
    error_message = login_page.get_error_message()
    assert "Invalid credentials" in error_message, f"Unexpected error message: {error_message}"


@pytest.mark.smoke
def test_login_page_elements_visible(login_page: LoginPage):
    """
    Test that all login page elements are visible.

    Args:
        login_page: LoginPage instance (framework-agnostic)
    """
    # Verify page is loaded
    assert login_page.is_page_loaded(), "Login page should be fully loaded"

    # Verify key elements are visible
    assert login_page.is_login_logo_visible(), "Login logo should be visible"


@pytest.mark.regression
def test_empty_credentials(login_page: LoginPage):
    """
    Test login attempt with empty credentials.

    Args:
        login_page: LoginPage instance (framework-agnostic)
    """
    # Click login button without entering credentials
    login_page.click_login_button()

    # Should show validation error or remain on login page
    current_url = login_page.get_current_url()
    assert "auth/login" in current_url, "Should remain on login page with empty credentials"


@pytest.mark.regression
def test_empty_username(login_page: LoginPage):
    """
    Test login with empty username.

    Args:
        login_page: LoginPage instance (framework-agnostic)
    """
    # Enter only password
    login_page.enter_password("somepassword")
    login_page.click_login_button()

    # Should remain on login page
    current_url = login_page.get_current_url()
    assert "auth/login" in current_url, "Should remain on login page with empty username"


@pytest.mark.regression
def test_empty_password(login_page: LoginPage):
    """
    Test login with empty password.

    Args:
        login_page: LoginPage instance (framework-agnostic)
    """
    # Enter only username
    login_page.enter_username("someuser")
    login_page.click_login_button()

    # Should remain on login page
    current_url = login_page.get_current_url()
    assert "auth/login" in current_url, "Should remain on login page with empty password"


@pytest.mark.regression
def test_method_chaining(login_page: LoginPage, config_service):
    """
    Test that method chaining works correctly.

    Args:
        login_page: LoginPage instance (framework-agnostic)
        config_service: Configuration service
    """
    # Test method chaining (fluent interface)
    login_page.enter_username(config_service.username).enter_password(
        config_service.password
    ).click_login_button()

    # Verify successful login
    current_url = login_page.get_current_url()
    assert "dashboard" in current_url, "Login with method chaining should succeed"
