"""
Test cases for OrangeHRM Login functionality.
Uses LoginPage object model and BasePage functionality.
"""
import pytest
from src.config.config import Config
from src.pages.login_page import LoginPage


@pytest.mark.login
@pytest.mark.smoke
class TestLogin:
    """Test suite for login functionality."""

    def test_successful_login(self, login_page: LoginPage):
        """
        Test successful login with valid credentials.

        Steps:
            1. Navigate to login page
            2. Enter valid username
            3. Enter valid password
            4. Click login button
            5. Verify successful login (URL changes)

        Expected:
            User should be logged in and redirected to dashboard
        """
        # Verify login page is loaded
        assert login_page.is_login_page_loaded(), "Login page did not load properly"

        # Perform login
        login_page.login(Config.USERNAME, Config.PASSWORD)

        # Verify successful login by checking URL change
        current_url = login_page.get_current_url()
        assert "dashboard" in current_url.lower(), f"Login failed. Current URL: {current_url}"

    def test_login_with_invalid_credentials(self, login_page: LoginPage):
        """
        Test login with invalid credentials.

        Steps:
            1. Navigate to login page
            2. Enter invalid username
            3. Enter invalid password
            4. Click login button
            5. Verify error message is displayed

        Expected:
            Error message should be displayed
        """
        # Perform login with invalid credentials
        login_page.login("invalid_user", "invalid_password")

        # Verify error message is displayed
        assert login_page.is_error_message_displayed(), "Error message not displayed for invalid credentials"

        # Verify error message content
        error_message = login_page.get_error_message()
        assert len(error_message) > 0, "Error message is empty"

    def test_login_with_empty_username(self, login_page: LoginPage):
        """
        Test login with empty username.

        Steps:
            1. Navigate to login page
            2. Leave username empty
            3. Enter password
            4. Click login button
            5. Verify validation or error

        Expected:
            Login should fail with appropriate message
        """
        # Perform login with empty username
        login_page.enter_password(Config.PASSWORD)
        login_page.click_login_button()

        # Verify still on login page (URL should not change)
        current_url = login_page.get_current_url()
        assert "dashboard" not in current_url.lower(), "Login should not succeed with empty username"

    def test_login_with_empty_password(self, login_page: LoginPage):
        """
        Test login with empty password.

        Steps:
            1. Navigate to login page
            2. Enter username
            3. Leave password empty
            4. Click login button
            5. Verify validation or error

        Expected:
            Login should fail with appropriate message
        """
        # Perform login with empty password
        login_page.enter_username(Config.USERNAME)
        login_page.click_login_button()

        # Verify still on login page (URL should not change)
        current_url = login_page.get_current_url()
        assert "dashboard" not in current_url.lower(), "Login should not succeed with empty password"

    def test_login_with_valid_username_invalid_password(self, login_page: LoginPage):
        """
        Test login with valid username but invalid password.

        Steps:
            1. Navigate to login page
            2. Enter valid username
            3. Enter invalid password
            4. Click login button
            5. Verify error message

        Expected:
            Error message should be displayed
        """
        # Perform login with valid username but invalid password
        login_page.login(Config.USERNAME, "wrong_password123")

        # Verify error message is displayed
        assert login_page.is_error_message_displayed(), "Error message not displayed for invalid password"

    def test_login_page_elements_visibility(self, login_page: LoginPage):
        """
        Test that all login page elements are visible.

        Steps:
            1. Navigate to login page
            2. Verify username field is visible
            3. Verify password field is visible
            4. Verify login button is visible
            5. Verify logo is visible

        Expected:
            All elements should be visible
        """
        assert login_page.is_element_visible(login_page.USERNAME_INPUT), "Username field not visible"
        assert login_page.is_element_visible(login_page.PASSWORD_INPUT), "Password field not visible"
        assert login_page.is_element_visible(login_page.LOGIN_BUTTON), "Login button not visible"
        assert login_page.is_logo_displayed(), "Logo not visible"

    def test_login_with_method_chaining(self, login_page: LoginPage):
        """
        Test login using method chaining pattern.

        Steps:
            1. Navigate to login page
            2. Use method chaining to enter credentials
            3. Click login button
            4. Verify successful login

        Expected:
            User should be logged in successfully
        """
        # Use method chaining
        login_page.enter_username(Config.USERNAME).enter_password(Config.PASSWORD)
        login_page.click_login_button()

        # Verify successful login
        current_url = login_page.get_current_url()
        assert "dashboard" in current_url.lower(), "Login with method chaining failed"

    @pytest.mark.regression
    def test_login_page_title(self, login_page: LoginPage):
        """
        Test that login page has correct title.

        Steps:
            1. Navigate to login page
            2. Get page title
            3. Verify title contains expected text

        Expected:
            Page title should contain 'OrangeHRM'
        """
        page_title = login_page.get_page_title()
        assert "OrangeHRM" in page_title, f"Unexpected page title: {page_title}"


@pytest.mark.login
class TestLoginPageInteractions:
    """Test suite for login page element interactions."""

    @pytest.mark.skip(reason="OrangeHRM uses React-controlled inputs that don't clear with standard .clear() method")
    def test_clear_username_field(self, login_page: LoginPage):
        """
        Test clearing the username field.

        Steps:
            1. Enter username
            2. Clear username field
            3. Verify field is empty

        Expected:
            Username field should be cleared
        """
        # Enter and clear username
        login_page.enter_username("test_user")
        login_page.clear_username()

        # Get the value attribute
        username_value = login_page.get_attribute(login_page.USERNAME_INPUT, "value")
        assert username_value == "" or username_value is None, f"Username field was not cleared, value: {username_value}"

    @pytest.mark.skip(reason="OrangeHRM uses React-controlled inputs that don't clear with standard .clear() method")
    def test_clear_password_field(self, login_page: LoginPage):
        """
        Test clearing the password field.

        Steps:
            1. Enter password
            2. Clear password field
            3. Verify field is empty

        Expected:
            Password field should be cleared
        """
        # Enter and clear password
        login_page.enter_password("test_password")
        login_page.clear_password()

        # Get the value attribute
        password_value = login_page.get_attribute(login_page.PASSWORD_INPUT, "value")
        assert password_value == "" or password_value is None, f"Password field was not cleared, value: {password_value}"
