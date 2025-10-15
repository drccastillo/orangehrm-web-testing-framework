"""
Unified leave tests that work with ANY automation framework.

These tests use the unified page objects and work with both Selenium and Playwright
through the BrowserProtocol interface.

Run with Selenium (default):
    URL="http://orangehrm_app/web/index.php" pytest tests/test_leave_unified.py --framework=selenium -p no:playwright

Run with Playwright:
    pytest tests/test_leave_unified.py --framework=playwright -p no:playwright

Run with specific browser:
    pytest tests/test_leave_unified.py --browser=firefox
    pytest tests/test_leave_unified.py --framework=playwright --browser=chromium
"""

import pytest

from src.pages.protocols import LeavePageProtocol


@pytest.mark.smoke
def test_leave_page_loads(leave_page: LeavePageProtocol):
    """
    Test that leave page loads successfully after navigation.

    This test works with ANY framework (Selenium, Playwright, etc.)
    through the LeavePageProtocol interface.

    Args:
        leave_page: LeavePage instance (framework-agnostic)
    """
    # Verify leave page is loaded
    assert leave_page.is_page_loaded(), "Leave page should be fully loaded"


@pytest.mark.smoke
def test_leave_menu_buttons_visible(leave_page: LeavePageProtocol):
    """
    Test that leave menu buttons are visible.

    Args:
        leave_page: LeavePage instance (framework-agnostic)
    """
    # Verify key navigation buttons are visible
    assert leave_page.is_apply_button_visible(), "Apply button should be visible"
    assert leave_page.is_leave_list_button_visible(), "Leave List button should be visible"
    assert leave_page.is_my_leave_button_visible(), "My Leave button should be visible"


@pytest.mark.smoke
def test_navigate_to_leave_list(leave_page: LeavePageProtocol):
    """
    Test navigation to Leave List page.

    Args:
        leave_page: LeavePage instance (framework-agnostic)
    """
    # Navigate to Leave List
    leave_page.navigate_to_leave_list()

    # Verify URL changed
    current_url = leave_page.get_current_url()
    assert "leave/viewLeaveList" in current_url or "leave/list" in current_url, (
        f"Should navigate to leave list page, got: {current_url}"
    )


@pytest.mark.smoke
def test_navigate_to_my_leave(leave_page: LeavePageProtocol):
    """
    Test navigation to My Leave page.

    Args:
        leave_page: LeavePage instance (framework-agnostic)
    """
    # Navigate to My Leave
    leave_page.navigate_to_my_leave()

    # Verify URL contains leave (might be SPA with # navigation)
    current_url = leave_page.get_current_url()
    assert "leave" in current_url.lower(), f"Should navigate to leave page, got: {current_url}"


@pytest.mark.regression
def test_navigate_to_apply_leave(leave_page: LeavePageProtocol):
    """
    Test navigation to Apply Leave page.

    Args:
        leave_page: LeavePage instance (framework-agnostic)
    """
    # Navigate to Apply Leave
    leave_page.navigate_to_apply_leave()

    # Verify URL contains leave (might be SPA with # navigation)
    current_url = leave_page.get_current_url()
    assert "leave" in current_url.lower(), f"Should navigate to leave page, got: {current_url}"


@pytest.mark.regression
def test_leave_list_table_visible(leave_page: LeavePageProtocol):
    """
    Test that leave list table is visible after navigation.

    Args:
        leave_page: LeavePage instance (framework-agnostic)
    """
    # Navigate to Leave List
    leave_page.navigate_to_leave_list()

    # Verify table is visible or no records message is shown
    is_table_visible = leave_page.is_leave_list_table_visible()
    is_no_records = leave_page.is_no_records_message_displayed()

    assert is_table_visible or is_no_records, (
        "Either leave list table or 'No Records' message should be displayed"
    )


@pytest.mark.regression
def test_get_leave_count(leave_page: LeavePageProtocol):
    """
    Test getting leave count from leave list.

    Args:
        leave_page: LeavePage instance (framework-agnostic)
    """
    # Navigate to Leave List
    leave_page.navigate_to_leave_list()

    # Get leave count (could be 0 if no leaves exist)
    count = leave_page.get_leave_count()

    # Verify count is non-negative
    assert count >= 0, f"Leave count should be non-negative, got: {count}"


@pytest.mark.regression
def test_search_leave_reset(leave_page: LeavePageProtocol):
    """
    Test search functionality with reset.

    Args:
        leave_page: LeavePage instance (framework-agnostic)
    """
    # Navigate to Leave List
    leave_page.navigate_to_leave_list()

    # Perform a search (even if fields are empty, this tests the functionality)
    leave_page.search_leave()

    # Get count after search
    leave_page.get_leave_count()

    # Reset search
    leave_page.reset_search()

    # Verify page still loads after reset
    assert leave_page.is_page_loaded(), "Page should be loaded after reset"


@pytest.mark.smoke
def test_url_contains_leave(leave_page: LeavePageProtocol):
    """
    Test that current URL contains 'leave' after navigation.

    Args:
        leave_page: LeavePage instance (framework-agnostic)
    """
    current_url = leave_page.get_current_url()
    assert "leave" in current_url.lower(), f"URL should contain 'leave', got: {current_url}"
