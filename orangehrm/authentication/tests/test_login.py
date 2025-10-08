"""
Login tests for OrangeHRM Authentication feature.

This module contains all test cases related to login functionality.
"""
import pytest
import allure
from orangehrm.authentication.pages import LoginPage


@pytest.mark.authentication
@pytest.mark.smoke
@allure.feature("Authentication")
@allure.story("Login Success")
class TestLoginSuccess:
    """Test suite for successful login scenarios."""

    @allure.title("Test successful login with valid credentials")
    @allure.description("Verify that user can login successfully with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "positive")
    def test_valid_login(self, login_page: LoginPage, valid_user):
        """
        Test successful login with valid credentials.

        Given: User is on login page
        When: User enters valid credentials and clicks login
        Then: User should be redirected to dashboard
        """
        # Steps are automatically reported from LoginPage methods
        assert login_page.is_login_page_loaded(), "Login page not loaded"

        login_page.login(valid_user.username, valid_user.password)

        current_url = login_page.get_current_url().lower()
        allure.attach(current_url, "Current URL", allure.attachment_type.TEXT)
        assert "dashboard" in current_url or "index" in current_url, \
            f"User not redirected to dashboard after login. Current URL: {current_url}"

    @allure.title("Test login with method chaining")
    @allure.description("Verify login using method chaining pattern")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("positive", "pattern")
    def test_login_with_method_chaining(self, login_page: LoginPage, valid_user):
        """
        Test login using method chaining pattern.

        Demonstrates fluent interface usage.
        """
        # Each method in the chain reports its own step
        login_page.enter_username(valid_user.username)\
                  .enter_password(valid_user.password)\
                  .click_login_button()

        assert "dashboard" in login_page.get_current_url().lower()


@pytest.mark.authentication
@pytest.mark.regression
@allure.feature("Authentication")
@allure.story("Login Failure")
class TestLoginFailure:
    """Test suite for login failure scenarios."""

    @allure.title("Test login with invalid credentials")
    @allure.description("Verify error message is displayed for invalid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("negative", "validation")
    def test_invalid_credentials(self, login_page: LoginPage, invalid_user_data):
        """
        Test login with invalid credentials.

        Given: User is on login page
        When: User enters invalid credentials
        Then: Error message should be displayed
        And: User should remain on login page
        """
        # Steps automatically reported from LoginPage methods
        login_page.login(invalid_user_data.username, invalid_user_data.password)

        assert login_page.is_error_message_displayed(), \
            "Error message not displayed for invalid credentials"

    @allure.title("Test login with empty username")
    @allure.description("Verify that login fails when username field is empty")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "validation")
    def test_empty_username(self, login_page: LoginPage, valid_user):
        """Test login with empty username."""
        # Steps automatically reported from LoginPage methods
        login_page.enter_password(valid_user.password)
        login_page.click_login_button()

        current_url = login_page.get_current_url()
        allure.attach(current_url, "Current URL", allure.attachment_type.TEXT)
        assert "dashboard" not in current_url.lower(), \
            "Should not login with empty username"

    @allure.title("Test login with empty password")
    @allure.description("Verify that login fails when password field is empty")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "validation")
    def test_empty_password(self, login_page: LoginPage, valid_user):
        """Test login with empty password."""
        # Steps automatically reported from LoginPage methods
        login_page.enter_username(valid_user.username)
        login_page.click_login_button()

        current_url = login_page.get_current_url()
        allure.attach(current_url, "Current URL", allure.attachment_type.TEXT)
        assert "dashboard" not in current_url.lower(), \
            "Should not login with empty password"

    @allure.title("Test login with both fields empty")
    @allure.description("Verify that login fails when both username and password are empty")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("negative", "validation", "boundary")
    def test_both_fields_empty(self, login_page: LoginPage):
        """Test login with both fields empty."""
        # Step automatically reported from LoginPage method
        login_page.click_login_button()

        current_url = login_page.get_current_url()
        allure.attach(current_url, "Current URL", allure.attachment_type.TEXT)
        assert "dashboard" not in current_url.lower(), \
            "Should not login with empty fields"


@pytest.mark.authentication
@allure.feature("Authentication")
@allure.story("Login UI")
class TestLoginUI:
    """Test suite for login UI elements."""

    @allure.title("Test login page elements are visible")
    @allure.description("Verify all login page elements are visible")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("ui", "validation")
    def test_login_page_elements_visible(self, login_page: LoginPage):
        """
        Test that all login page elements are visible.

        Verifies:
        - Username field is visible
        - Password field is visible
        - Login button is visible
        - Logo is visible
        """
        # Steps automatically reported from LoginPage methods
        assert login_page.is_username_field_visible(), "Username field not visible"
        assert login_page.is_password_field_visible(), "Password field not visible"
        assert login_page.is_login_button_visible(), "Login button not visible"
        assert login_page.is_logo_displayed(), "Logo not visible"

    @allure.title("Test login page title")
    @allure.description("Verify login page has correct title")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("ui", "validation")
    def test_login_page_title(self, login_page: LoginPage):
        """Test login page has correct title."""
        page_title = login_page.get_page_title()
        allure.attach(page_title, "Page Title", allure.attachment_type.TEXT)
        assert "OrangeHRM" in page_title, f"Unexpected page title: {page_title}"
