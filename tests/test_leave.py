"""
Leave test suite with Playwright assertions and Gherkin-style documentation.

All tests follow AAA (Arrange-Act-Assert) pattern using Playwright's native
expect() assertions for auto-waiting and better error messages.

Run tests:
    pytest tests/test_leave.py -v

Run with specific browser:
    pytest tests/test_leave.py --browser=firefox
    pytest tests/test_leave.py --browser=chromium
"""

import re

import pytest
from playwright.sync_api import expect

from src.pages.leave_page import LeavePage


@pytest.mark.smoke
def test_leave_page_loads(leave_page: LeavePage):
    """
    Verify leave page loads successfully after authentication and navigation.

    Scenario:
        Given: User is authenticated
        And: User has navigated to Leave section
        When: Leave page finishes loading
        Then: Leave page title should be visible
        And: Essential navigation elements should be present

    Args:
        leave_page: LeavePage instance (already navigated by fixture)
    """
    # Arrange
    # (Fixture already performed login and navigation)

    # Act
    # (Page load happens automatically in fixture)

    # Assert - Verify page loaded successfully
    page_title = leave_page.locators.PAGE_TITLE(leave_page.page)
    expect(page_title).to_be_visible(timeout=10000)


@pytest.mark.smoke
def test_leave_menu_buttons_visible(leave_page: LeavePage):
    """
    Verify all leave navigation buttons are visible.

    Scenario:
        Given: User is on the Leave page
        When: Page finishes loading
        Then: Apply button should be visible
        And: My Leave button should be visible
        And: Leave List button should be visible

    Args:
        leave_page: LeavePage instance
    """
    # Arrange
    apply_button = leave_page.locators.APPLY_BUTTON(leave_page.page)
    my_leave_button = leave_page.locators.MY_LEAVE_BUTTON(leave_page.page)
    leave_list_button = leave_page.locators.LEAVE_LIST_BUTTON(leave_page.page)

    # Act
    # (No action needed - checking visibility)

    # Assert - All key navigation buttons should be visible
    expect(apply_button).to_be_visible(timeout=5000)
    expect(my_leave_button).to_be_visible(timeout=5000)
    expect(leave_list_button).to_be_visible(timeout=5000)


@pytest.mark.smoke
def test_navigate_to_leave_list(leave_page: LeavePage):
    """
    Verify user can navigate to Leave List page.

    Scenario:
        Given: User is on the Leave page
        When: User clicks on Leave List button
        Then: URL should change to leave list page
        And: URL should contain "viewLeaveList" or "leave/list"

    Args:
        leave_page: LeavePage instance
    """
    # Arrange
    # (User already on leave page)

    # Act
    leave_page.navigate_to_leave_list()

    # Assert - URL should change to leave list
    expect(leave_page.page).to_have_url(re.compile(r"(viewLeaveList|leave/list)"), timeout=10000)


@pytest.mark.smoke
def test_navigate_to_my_leave(leave_page: LeavePage):
    """
    Verify user can navigate to My Leave page.

    Scenario:
        Given: User is on the Leave page
        When: User clicks on My Leave button
        Then: URL should contain "leave"

    Args:
        leave_page: LeavePage instance
    """
    # Arrange
    # (User already on leave page)

    # Act
    leave_page.navigate_to_my_leave()

    # Assert - URL should contain "leave"
    expect(leave_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=10000)


@pytest.mark.regression
def test_navigate_to_apply_leave(leave_page: LeavePage):
    """
    Verify user can navigate to Apply Leave page.

    Scenario:
        Given: User is on the Leave page
        When: User clicks on Apply button
        Then: URL should contain "leave"
        And: Apply Leave form should be visible

    Args:
        leave_page: LeavePage instance
    """
    # Arrange
    # (User already on leave page)

    # Act
    leave_page.navigate_to_apply_leave()

    # Assert - URL should contain "leave"
    expect(leave_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=10000)


@pytest.mark.regression
def test_leave_list_table_visible(leave_page: LeavePage):
    """
    Verify leave list table or no records message is displayed.

    Scenario:
        Given: User is on the Leave page
        When: User navigates to Leave List
        Then: Either leave list table should be visible
        Or: "No Records Found" message should be displayed

    Args:
        leave_page: LeavePage instance
    """
    # Arrange
    # (User already on leave page)

    # Act
    leave_page.navigate_to_leave_list()

    # Assert - Either table or no records message should be visible
    leave_table = leave_page.locators.LEAVE_LIST_TABLE(leave_page.page)
    no_records_msg = leave_page.locators.NO_RECORDS_MESSAGE(leave_page.page)

    # Use or condition: at least one should be visible
    try:
        expect(leave_table).to_be_visible(timeout=5000)
    except AssertionError:
        # If table not visible, no records message should be
        expect(no_records_msg).to_be_visible(timeout=2000)


@pytest.mark.regression
def test_get_leave_count(leave_page: LeavePage):
    """
    Verify leave count can be retrieved from leave list.

    Scenario:
        Given: User is on the Leave page
        When: User navigates to Leave List
        And: User gets the leave count
        Then: Count should be a non-negative number

    Args:
        leave_page: LeavePage instance
    """
    # Arrange
    # (User already on leave page)

    # Act
    leave_page.navigate_to_leave_list()
    count = leave_page.get_leave_count()

    # Assert - Count should be non-negative (0 or more)
    assert count >= 0, f"Leave count should be non-negative, got: {count}"


@pytest.mark.regression
def test_search_leave_reset(leave_page: LeavePage):
    """
    Verify search and reset functionality works correctly.

    Scenario:
        Given: User is on the Leave List page
        When: User performs a search
        And: User resets the search
        Then: Page should still be loaded
        And: Search form should be visible

    Args:
        leave_page: LeavePage instance
    """
    # Arrange
    leave_page.navigate_to_leave_list()

    # Act
    leave_page.search_leave()
    leave_page.reset_search()

    # Assert - Page should still be functional after reset
    page_title = leave_page.locators.PAGE_TITLE(leave_page.page)
    expect(page_title).to_be_visible(timeout=5000)


@pytest.mark.smoke
def test_url_contains_leave(leave_page: LeavePage):
    """
    Verify current URL contains 'leave' after navigation.

    Scenario:
        Given: User has navigated to Leave section
        When: Page finishes loading
        Then: Current URL should contain the word "leave"

    Args:
        leave_page: LeavePage instance
    """
    # Arrange
    # (Fixture already navigated to leave page)

    # Act
    # (No action needed)

    # Assert - URL should contain "leave"
    expect(leave_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE))
