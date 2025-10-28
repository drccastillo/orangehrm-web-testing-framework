"""
Login tests using Playwright.
Tests the login functionality of OrangeHRM application.
"""

import re

import allure
import pytest
from playwright.sync_api import expect

from src.config.config import Config
from src.pages_playwright.login_page_pw import LoginPagePW
from utils.logger import TestLogger, log_test_step

# Initialize logger
logger = TestLogger.get_logger(__name__)


@allure.feature("Authentication - Playwright")
@allure.story("User Login")
@allure.title("Successful login with valid credentials (Playwright)")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.playwright
@pytest.mark.smoke
@pytest.mark.login
@log_test_step("Test successful login with valid credentials")
def test_login_success_playwright(login_page_pw: LoginPagePW):
    """
    Test successful login with valid credentials.

    Steps:
        1. Navigate to login page (done by fixture)
        2. Enter valid username
        3. Enter valid password
        4. Click login button
        5. Verify redirect to dashboard

    Expected:
        - User should be redirected to dashboard
        - URL should contain 'dashboard'
    """
    with allure.step(f"Perform login with username: {Config.USERNAME}"):
        login_page_pw.login(Config.USERNAME, Config.PASSWORD)

    with allure.step("Verify successful redirect to dashboard"):
        # Using regex pattern with case-insensitive flag
        expect(login_page_pw.page).to_have_url(re.compile(".*dashboard.*", re.IGNORECASE))
        current_url = login_page_pw.page.url
        allure.attach(current_url, name="Current URL", attachment_type=allure.attachment_type.TEXT)


@allure.feature("Authentication - Playwright")
@allure.story("User Login")
@allure.title("Login with invalid credentials shows error (Playwright)")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.playwright
@pytest.mark.smoke
@pytest.mark.login
@log_test_step("Test login with invalid credentials")
def test_login_invalid_credentials_playwright(login_page_pw: LoginPagePW):
    """
    Test login with invalid credentials.

    Steps:
        1. Navigate to login page (done by fixture)
        2. Enter invalid username
        3. Enter invalid password
        4. Click login button
        5. Verify error message is displayed

    Expected:
        - Error message should be displayed
        - User should remain on login page
    """
    with allure.step("Attempt login with invalid credentials"):
        login_page_pw.login("invalid_user", "invalid_password")

    with allure.step("Verify error message is displayed"):
        assert login_page_pw.is_error_message_displayed(), (
            "Error message should be displayed for invalid credentials"
        )

    with allure.step("Verify error message content"):
        error_message = login_page_pw.get_error_message()
        allure.attach(
            error_message, name="Error Message", attachment_type=allure.attachment_type.TEXT
        )
        assert error_message, "Error message text should not be empty"

    with allure.step("Verify still on login page"):
        expect(login_page_pw.page).not_to_have_url(re.compile(".*dashboard.*", re.IGNORECASE))


@allure.feature("Authentication - Playwright")
@allure.story("User Login")
@allure.title("Login with empty username should fail (Playwright)")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.playwright
@pytest.mark.regression
@pytest.mark.login
@log_test_step("Test login with empty username")
def test_login_empty_username_playwright(login_page_pw: LoginPagePW):
    """
    Test login with empty username field.

    Steps:
        1. Navigate to login page (done by fixture)
        2. Leave username field empty
        3. Enter password
        4. Click login button
        5. Verify error or validation message

    Expected:
        - Error message or validation should be displayed
        - User should remain on login page
    """
    with allure.step("Enter password without username"):
        login_page_pw.enter_password(Config.PASSWORD)

    with allure.step("Click login button"):
        login_page_pw.click_login_button()

    with allure.step("Verify still on login page"):
        expect(login_page_pw.page).not_to_have_url(re.compile(".*dashboard.*", re.IGNORECASE))


@allure.feature("Authentication - Playwright")
@allure.story("User Login")
@allure.title("Login with empty password should fail (Playwright)")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.playwright
@pytest.mark.regression
@pytest.mark.login
@log_test_step("Test login with empty password")
def test_login_empty_password_playwright(login_page_pw: LoginPagePW):
    """
    Test login with empty password field.

    Steps:
        1. Navigate to login page (done by fixture)
        2. Enter username
        3. Leave password field empty
        4. Click login button
        5. Verify error or validation message

    Expected:
        - Error message or validation should be displayed
        - User should remain on login page
    """
    with allure.step(f"Enter username: {Config.USERNAME}"):
        login_page_pw.enter_username(Config.USERNAME)

    with allure.step("Click login button without password"):
        login_page_pw.click_login_button()

    with allure.step("Verify still on login page"):
        expect(login_page_pw.page).not_to_have_url(re.compile(".*dashboard.*", re.IGNORECASE))


@allure.feature("Authentication - Playwright")
@allure.story("User Login")
@allure.title("Login with empty fields should fail (Playwright)")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.playwright
@pytest.mark.regression
@pytest.mark.login
@log_test_step("Test login with empty fields")
def test_login_empty_fields_playwright(login_page_pw: LoginPagePW):
    """
    Test login with both username and password fields empty.

    Steps:
        1. Navigate to login page (done by fixture)
        2. Leave both fields empty
        3. Click login button
        4. Verify validation message

    Expected:
        - Validation message should be displayed
        - User should remain on login page
    """
    with allure.step("Click login without entering any credentials"):
        login_page_pw.click_login_button()

    with allure.step("Verify still on login page"):
        expect(login_page_pw.page).not_to_have_url(re.compile(".*dashboard.*", re.IGNORECASE))


@allure.feature("Login Page Elements - Playwright")
@allure.story("Element Visibility")
@allure.title("All login page elements are visible (Playwright)")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.playwright
@pytest.mark.smoke
@pytest.mark.login
@log_test_step("Test login page elements visibility")
def test_login_page_elements_visible_playwright(login_page_pw: LoginPagePW):
    """
    Test that all login page elements are visible.

    Steps:
        1. Navigate to login page (done by fixture)
        2. Verify all elements are visible

    Expected:
        - Username field should be visible
        - Password field should be visible
        - Login button should be visible
        - Logo should be visible (optional)
    """
    with allure.step("Verify username field is visible"):
        assert login_page_pw.is_username_field_displayed(), "Username field should be visible"

    with allure.step("Verify password field is visible"):
        assert login_page_pw.is_password_field_displayed(), "Password field should be visible"

    with allure.step("Verify login button is visible"):
        assert login_page_pw.is_login_button_displayed(), "Login button should be visible"

    with allure.step("Verify login button is enabled"):
        assert login_page_pw.is_login_button_enabled(), "Login button should be enabled"


@allure.feature("Authentication - Playwright")
@allure.story("Method Chaining")
@allure.title("Login with method chaining succeeds (Playwright)")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.playwright
@pytest.mark.regression
@pytest.mark.login
@log_test_step("Test login with method chaining")
def test_login_method_chaining_playwright(login_page_pw: LoginPagePW):
    """
    Test login using method chaining pattern.

    Steps:
        1. Navigate to login page (done by fixture)
        2. Use method chaining to enter credentials and login
        3. Verify successful login

    Expected:
        - Method chaining should work correctly
        - User should be redirected to dashboard
    """
    with allure.step("Use method chaining to enter credentials and login"):
        (
            login_page_pw.enter_username(Config.USERNAME)
            .enter_password(Config.PASSWORD)
            .click_login_button()
        )

    with allure.step("Verify successful login"):
        expect(login_page_pw.page).to_have_url(re.compile(".*dashboard.*", re.IGNORECASE))
        current_url = login_page_pw.page.url
        allure.attach(current_url, name="Current URL", attachment_type=allure.attachment_type.TEXT)


@allure.feature("Authentication - Playwright")
@allure.story("Form Submission")
@allure.title("Login submission with Enter key (Playwright)")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.playwright
@pytest.mark.regression
@pytest.mark.login
@log_test_step("Test login submission with Enter key")
def test_login_submit_with_enter_key_playwright(login_page_pw: LoginPagePW):
    """
    Test login submission using Enter key.

    Steps:
        1. Navigate to login page (done by fixture)
        2. Enter username
        3. Enter password
        4. Press Enter key to submit
        5. Verify successful login

    Expected:
        - Form should be submitted with Enter key
        - User should be redirected to dashboard

    Note:
        This test is skipped because OrangeHRM's login form does not respond
        to Enter key submission. This is a known behavior of the application.
    """
    with allure.step("Enter credentials"):
        login_page_pw.enter_username(Config.USERNAME)
        login_page_pw.enter_password(Config.PASSWORD)

    with allure.step("Submit with Enter key"):
        login_page_pw.submit_with_enter_key()

    with allure.step("Verify successful login"):
        expect(login_page_pw.page).to_have_url(re.compile(".*dashboard.*", re.IGNORECASE))
        current_url = login_page_pw.page.url
        allure.attach(current_url, name="Current URL", attachment_type=allure.attachment_type.TEXT)


@allure.feature("Login Page Elements - Playwright")
@allure.story("Form Manipulation")
@allure.title("Clear login form (Playwright)")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.playwright
@pytest.mark.regression
@pytest.mark.login
@log_test_step("Test clearing login form")
def test_clear_login_form_playwright(login_page_pw: LoginPagePW):
    """
    Test clearing the login form.

    Steps:
        1. Navigate to login page (done by fixture)
        2. Enter username and password
        3. Clear the form
        4. Verify fields are empty

    Expected:
        - Both fields should be cleared
        - Fields should accept new input

    Note:
        This test is skipped because OrangeHRM automatically clears username
        fields when invalid usernames are entered. This is application behavior.
    """
    with allure.step("Enter test credentials"):
        login_page_pw.enter_username("test_user")
        login_page_pw.enter_password("test_password")

    with allure.step("Verify data is present"):
        username_value = login_page_pw.get_username_value()

        # If the field is empty, it's application behavior (auto-clear)
        # Try with a valid user that the app accepts
        if not username_value:
            login_page_pw.enter_username(Config.USERNAME)
            username_value = login_page_pw.get_username_value()

        allure.attach(
            username_value, name="Username Value", attachment_type=allure.attachment_type.TEXT
        )
        assert username_value, "Username field should contain entered value"

    with allure.step("Clear the form"):
        login_page_pw.clear_form()

    with allure.step("Verify fields are empty"):
        username_after_clear = login_page_pw.get_username_value()
        password_after_clear = login_page_pw.get_password_value()

        allure.attach(
            f"Username: '{username_after_clear}', Password: '{password_after_clear}'",
            name="Fields After Clear",
            attachment_type=allure.attachment_type.TEXT,
        )

        assert username_after_clear == "", "Username field should be empty after clearing"
        assert password_after_clear == "", "Password field should be empty after clearing"
