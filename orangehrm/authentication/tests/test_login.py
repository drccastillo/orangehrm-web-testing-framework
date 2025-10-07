"""
Login tests for OrangeHRM Authentication feature.

This module contains all test cases related to login functionality.
"""
import pytest
from framework.utils import log_test_step
from orangehrm.authentication.pages import LoginPage


@pytest.mark.authentication
@pytest.mark.smoke
class TestLoginSuccess:
    """Test suite for successful login scenarios."""

    @log_test_step("Test successful login with valid credentials")
    def test_valid_login(self, login_page: LoginPage, valid_user):
        """
        Test successful login with valid credentials.

        Given: User is on login page
        When: User enters valid credentials and clicks login
        Then: User should be redirected to dashboard
        """
        # Verify login page is loaded
        assert login_page.is_login_page_loaded(), "Login page not loaded"

        # Perform login
        login_page.login(valid_user.username, valid_user.password)

        # Verify successful login - redirected to dashboard or index page
        current_url = login_page.get_current_url().lower()
        assert "dashboard" in current_url or "index" in current_url, \
            f"User not redirected to dashboard after login. Current URL: {current_url}"

    @log_test_step("Test login with method chaining")
    def test_login_with_method_chaining(self, login_page: LoginPage, valid_user):
        """
        Test login using method chaining pattern.

        Demonstrates fluent interface usage.
        """
        login_page.enter_username(valid_user.username)\
                  .enter_password(valid_user.password)\
                  .click_login_button()

        assert "dashboard" in login_page.get_current_url().lower()


@pytest.mark.authentication
@pytest.mark.regression
class TestLoginFailure:
    """Test suite for login failure scenarios."""

    def test_invalid_credentials(self, login_page: LoginPage, invalid_user_data):
        """
        Test login with invalid credentials.

        Given: User is on login page
        When: User enters invalid credentials
        Then: Error message should be displayed
        And: User should remain on login page
        """
        login_page.login(invalid_user_data.username, invalid_user_data.password)

        assert login_page.is_error_message_displayed(), \
            "Error message not displayed for invalid credentials"

    def test_empty_username(self, login_page: LoginPage, valid_user):
        """Test login with empty username."""
        login_page.enter_password(valid_user.password)
        login_page.click_login_button()

        current_url = login_page.get_current_url()
        assert "dashboard" not in current_url.lower(), \
            "Should not login with empty username"

    def test_empty_password(self, login_page: LoginPage, valid_user):
        """Test login with empty password."""
        login_page.enter_username(valid_user.username)
        login_page.click_login_button()

        current_url = login_page.get_current_url()
        assert "dashboard" not in current_url.lower(), \
            "Should not login with empty password"

    def test_both_fields_empty(self, login_page: LoginPage):
        """Test login with both fields empty."""
        login_page.click_login_button()

        current_url = login_page.get_current_url()
        assert "dashboard" not in current_url.lower(), \
            "Should not login with empty fields"


@pytest.mark.authentication
class TestLoginUI:
    """Test suite for login UI elements."""

    def test_login_page_elements_visible(self, login_page: LoginPage):
        """
        Test that all login page elements are visible.

        Verifies:
        - Username field is visible
        - Password field is visible
        - Login button is visible
        - Logo is visible
        """
        assert login_page.is_element_visible(login_page.USERNAME_INPUT), \
            "Username field not visible"

        assert login_page.is_element_visible(login_page.PASSWORD_INPUT), \
            "Password field not visible"

        assert login_page.is_element_visible(login_page.LOGIN_BUTTON), \
            "Login button not visible"

        assert login_page.is_logo_displayed(), \
            "Logo not visible"

    def test_login_page_title(self, login_page: LoginPage):
        """Test login page has correct title."""
        page_title = login_page.get_page_title()
        assert "OrangeHRM" in page_title, f"Unexpected page title: {page_title}"
