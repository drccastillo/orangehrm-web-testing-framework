"""
Test cases for OrangeHRM Login functionality.
Uses LoginPage object model and BasePage functionality.
"""

import allure
import pytest

from src.config.config import Config
from src.pages_selenium.login_page import LoginPage


@allure.feature("Authentication")
@allure.story("User Login")
@pytest.mark.login
@pytest.mark.smoke
class TestLogin:
    """Test suite for login functionality."""

    @allure.title("Successful login with valid credentials")
    @allure.description(
        "Test that a user can successfully log in using valid username and password"
    )
    @allure.severity(allure.severity_level.CRITICAL)
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
        with allure.step("Verify login page is loaded"):
            assert login_page.is_login_page_loaded(), "Login page did not load properly"

        with allure.step(f"Enter username: {Config.USERNAME}"):
            login_page.enter_username(Config.USERNAME)

        with allure.step("Enter password"):
            login_page.enter_password(Config.PASSWORD)

        with allure.step("Click login button"):
            login_page.click_login_button()

        with allure.step("Verify successful redirect to dashboard"):
            current_url = login_page.get_current_url()
            allure.attach(
                current_url, name="Current URL", attachment_type=allure.attachment_type.TEXT
            )
            assert "dashboard" in current_url.lower(), f"Login failed. Current URL: {current_url}"

    @allure.title("Login with invalid credentials shows error message")
    @allure.severity(allure.severity_level.CRITICAL)
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
        with allure.step("Attempt login with invalid credentials"):
            login_page.login("invalid_user", "invalid_password")

        with allure.step("Verify error message is displayed"):
            assert (
                login_page.is_error_message_displayed()
            ), "Error message not displayed for invalid credentials"

        with allure.step("Verify error message content"):
            error_message = login_page.get_error_message()
            allure.attach(
                error_message, name="Error Message", attachment_type=allure.attachment_type.TEXT
            )
            assert len(error_message) > 0, "Error message is empty"

    @allure.title("Login with empty username should fail")
    @allure.severity(allure.severity_level.NORMAL)
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
        with allure.step("Enter password without username"):
            login_page.enter_password(Config.PASSWORD)

        with allure.step("Click login button"):
            login_page.click_login_button()

        with allure.step("Verify still on login page"):
            current_url = login_page.get_current_url()
            allure.attach(
                current_url, name="Current URL", attachment_type=allure.attachment_type.TEXT
            )
            assert (
                "dashboard" not in current_url.lower()
            ), "Login should not succeed with empty username"

    @allure.title("Login with empty password should fail")
    @allure.severity(allure.severity_level.NORMAL)
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
        with allure.step(f"Enter username: {Config.USERNAME}"):
            login_page.enter_username(Config.USERNAME)

        with allure.step("Click login button without password"):
            login_page.click_login_button()

        with allure.step("Verify still on login page"):
            current_url = login_page.get_current_url()
            allure.attach(
                current_url, name="Current URL", attachment_type=allure.attachment_type.TEXT
            )
            assert (
                "dashboard" not in current_url.lower()
            ), "Login should not succeed with empty password"

    @allure.title("Login with valid username but invalid password shows error")
    @allure.severity(allure.severity_level.CRITICAL)
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
        with allure.step("Attempt login with valid username and wrong password"):
            login_page.login(Config.USERNAME, "wrong_password123")

        with allure.step("Verify error message is displayed"):
            assert (
                login_page.is_error_message_displayed()
            ), "Error message not displayed for invalid password"

    @allure.title("All login page elements are visible")
    @allure.severity(allure.severity_level.NORMAL)
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
        with allure.step("Verify username field is visible"):
            assert login_page.is_element_visible(
                login_page.USERNAME_INPUT
            ), "Username field not visible"

        with allure.step("Verify password field is visible"):
            assert login_page.is_element_visible(
                login_page.PASSWORD_INPUT
            ), "Password field not visible"

        with allure.step("Verify login button is visible"):
            assert login_page.is_element_visible(
                login_page.LOGIN_BUTTON
            ), "Login button not visible"

        with allure.step("Verify logo is visible"):
            assert login_page.is_logo_displayed(), "Logo not visible"

    @allure.title("Login with method chaining succeeds")
    @allure.severity(allure.severity_level.NORMAL)
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
        with allure.step("Use method chaining to enter credentials"):
            login_page.enter_username(Config.USERNAME).enter_password(Config.PASSWORD)

        with allure.step("Click login button"):
            login_page.click_login_button()

        with allure.step("Verify successful login"):
            current_url = login_page.get_current_url()
            allure.attach(
                current_url, name="Current URL", attachment_type=allure.attachment_type.TEXT
            )
            assert "dashboard" in current_url.lower(), "Login with method chaining failed"

    @allure.title("Login page has correct title")
    @allure.severity(allure.severity_level.MINOR)
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
        with allure.step("Get page title"):
            page_title = login_page.get_page_title()
            allure.attach(
                page_title, name="Page Title", attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Verify title contains 'OrangeHRM'"):
            assert "OrangeHRM" in page_title, f"Unexpected page title: {page_title}"


@allure.feature("Login Page Interactions")
@pytest.mark.login
class TestLoginPageInteractions:
    """Test suite for login page element interactions."""

    @allure.title("Clear username field")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.skip(
        reason="OrangeHRM uses React-controlled inputs that don't clear with standard .clear() method"
    )
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
        assert (
            username_value == "" or username_value is None
        ), f"Username field was not cleared, value: {username_value}"

    @allure.title("Clear password field")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.skip(
        reason="OrangeHRM uses React-controlled inputs that don't clear with standard .clear() method"
    )
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
        assert (
            password_value == "" or password_value is None
        ), f"Password field was not cleared, value: {password_value}"
