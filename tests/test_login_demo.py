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


@pytest.mark.skip(reason="Demo test with highlight - for development/debugging only")
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
    print("\n🔍 Starting login demo with highlights...")

    # Step 1: Highlight and enter username
    print("  → Highlighting username field...")
    username_field = login_page.locators.USERNAME_INPUT(login_page.page)
    username_field.highlight()
    time.sleep(1)  # Pause to see highlight

    login_page.enter_username(config_service.username)
    print(f"  ✓ Entered username: {config_service.username}")

    # Step 2: Highlight and enter password
    print("  → Highlighting password field...")
    password_field = login_page.locators.PASSWORD_INPUT(login_page.page)
    password_field.highlight()
    time.sleep(1)

    login_page.enter_password(config_service.password)
    print("  ✓ Entered password")

    # Step 3: Highlight and click login button
    print("  → Highlighting login button...")
    login_button = login_page.locators.LOGIN_BUTTON(login_page.page)
    login_button.highlight()
    time.sleep(1)

    login_page.click_login_button()
    print("  ✓ Clicked login button")

    # Step 4: Verify successful login
    current_url = login_page.get_current_url()
    assert "dashboard" in current_url, f"Expected dashboard URL, got: {current_url}"
    print("✅ Login successful - redirected to dashboard\n")


@pytest.mark.skip(reason="Demo test with highlight - for development/debugging only")
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
    print("\n🔍 Starting invalid login demo with highlights...")

    # Highlight username field
    print("  → Highlighting username field...")
    login_page.locators.USERNAME_INPUT(login_page.page).highlight()
    time.sleep(0.5)
    login_page.enter_username("invalid_user")

    # Highlight password field
    print("  → Highlighting password field...")
    login_page.locators.PASSWORD_INPUT(login_page.page).highlight()
    time.sleep(0.5)
    login_page.enter_password("invalid_password")

    # Highlight login button
    print("  → Highlighting login button...")
    login_page.locators.LOGIN_BUTTON(login_page.page).highlight()
    time.sleep(0.5)
    login_page.click_login_button()

    # Highlight error message
    print("  → Highlighting error message...")
    time.sleep(1)  # Wait for error to appear
    error_locator = login_page.locators.ERROR_MESSAGE(login_page.page)
    error_locator.highlight()
    time.sleep(1)

    # Verify error is displayed
    assert login_page.is_error_message_displayed(), "Error message should be visible"
    error_text = login_page.get_error_message()
    print(f"  ✓ Error message displayed: '{error_text}'")
    print("✅ Invalid login handled correctly\n")


@pytest.mark.skip(reason="Demo test with highlight - for development/debugging only")
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
    print("\n🔍 Starting method chaining demo with selective highlights...")

    # Highlight the flow we're about to execute
    print("  → Highlighting username field...")
    login_page.locators.USERNAME_INPUT(login_page.page).highlight()
    time.sleep(0.5)

    print("  → Highlighting password field...")
    login_page.locators.PASSWORD_INPUT(login_page.page).highlight()
    time.sleep(0.5)

    print("  → Highlighting login button...")
    login_page.locators.LOGIN_BUTTON(login_page.page).highlight()
    time.sleep(0.5)

    # Now execute with method chaining
    print("  → Executing method chaining...")
    login_page.enter_username(config_service.username).enter_password(
        config_service.password
    ).click_login_button()

    # Verify
    current_url = login_page.get_current_url()
    assert "dashboard" in current_url, "Login with method chaining should succeed"
    print("✅ Method chaining with highlights successful\n")


# Regular test without highlight for comparison
@pytest.mark.smoke
def test_login_without_highlight(login_page: LoginPage, config_service):
    """
    Regular production test WITHOUT highlight() - for comparison.

    This is how tests should look in production (clean, fast, no debugging code).
    Compare this with the demo tests above to see the difference.

    Args:
        login_page: LoginPage instance
        config_service: Configuration service
    """
    # Standard test - no highlights, no delays, production-ready
    login_page.login(config_service.username, config_service.password)

    current_url = login_page.get_current_url()
    assert "dashboard" in current_url, f"Expected dashboard URL, got: {current_url}"
