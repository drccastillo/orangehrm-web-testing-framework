"""
Leave List Page Object Model for OrangeHRM application.

This page inherits from LeaveBasePage and adds Leave List specific functionality.
"""

# pylint: disable=import-error  # src module is in project root
from playwright.sync_api import Locator, Page

from src.ui.pages.leave.leave_base_page import LeaveBasePage


class LeaveListPage(LeaveBasePage):
    """
    Page Object Model for the OrangeHRM Leave List Page.

    Inherits Leave module top bar navigation from LeaveBasePage.
    This page adds Leave List specific elements and functionality.

    Attributes:
        page_title: Leave page heading

    Example:
        >>> from playwright.sync_api import sync_playwright
        >>> with sync_playwright() as p:
        ...     browser = p.chromium.launch()
        ...     page = browser.new_page()
        ...     leave_list_page = LeaveListPage(page, timeout=10)
        ...     # Navigate to Leave module using NavigationHeader
        ...     leave_list_page.nav_header.navigate_to_leave()
        ...     # Leave List specific functionality here
    """

    def __init__(self, page: Page, timeout: int = 10):
        """
        Initialize the Leave List Page.

        Args:
            page: Playwright Page instance
            timeout: Default timeout for operations in seconds
        """
        super().__init__(page, timeout)

        # Page-specific elements for Leave List
        self.page_title: Locator = page.get_by_role("heading", name="Leave", exact=True)
