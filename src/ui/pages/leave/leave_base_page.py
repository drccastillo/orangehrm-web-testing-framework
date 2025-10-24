"""
LeaveBasePage - Base page for all Leave module pages.

This base page contains the shared Leave module top bar with navigation tabs
and dropdown menus that appear on all pages within the Leave module.

Design Pattern:
    - Inheritance hierarchy: BasePage → LeaveBasePage → Specific Leave Pages
    - DRY Principle: Top bar locators and navigation defined once
    - All Leave module pages inherit from this base

Pages that inherit from LeaveBasePage:
    - LeaveListPage
    - ApplyLeavePage
    - MyLeavePage
    - AssignLeavePage
    - AddEntitlementsPage
    - EmployeeEntitlementsPage
    - MyEntitlementsPage
    - WorkWeekPage
    - HolidaysPage
    - LeavePeriodPage
    - LeaveTypesPage
    - LeaveEntitlementsAndUsageReportPage
    - MyLeaveEntitlementsAndUsageReportPage
"""

# pylint: disable=import-error  # src module is in project root
from typing import TYPE_CHECKING

from playwright.sync_api import Locator, Page

from src.ui.pages.base_page import BasePage

# Avoid circular imports - only import for type hints
if TYPE_CHECKING:
    from src.ui.pages.leave.apply.apply_leave_page import ApplyLeavePage
    from src.ui.pages.leave.assign.assign_leave import AssignLeavePage
    from src.ui.pages.leave.configure.holidays_page import HolidaysPage
    from src.ui.pages.leave.configure.leave_period_page import LeavePeriodPage
    from src.ui.pages.leave.configure.work_week_page import WorkWeekPage
    from src.ui.pages.leave.entitlements.add_entitlements_page import (
        AddEntitlementsPage,
    )
    from src.ui.pages.leave.list.leave_list_page import LeaveListPage
    from src.ui.pages.leave.my_leave.my_leave_page import MyLeavePage
    from src.ui.pages.leave.reports.leave_entitlements_and_usage_report_page import (
        LeaveEntitlementsAndUsageReportPage,
    )
    from src.ui.pages.leave.reports.my_leave_entitlements_and_usage_report import (
        MyLeaveEntitlementsAndUsageReportPage,
    )


class LeaveBasePage(BasePage):
    """
    Base page for all Leave module pages with shared top bar navigation.

    This class encapsulates the Leave module's top bar that appears on all
    Leave pages, including:
    - Direct tabs: Apply, My Leave, Leave List, Assign Leave
    - Dropdown menus: Entitlements, Reports, Configure

    All specific Leave pages should inherit from this base to gain access
    to the shared navigation without code duplication.

    Attributes:
        # Inherited from BasePage:
        nav_header: NavigationHeader component for global navigation

        # Leave Module Top Bar - Direct Tabs:
        apply_leave_tab: Apply tab in Leave top bar
        my_leave_tab: My Leave tab in Leave top bar
        leave_list_tab: Leave List tab in Leave top bar
        assign_leave_tab: Assign Leave tab in Leave top bar

        # Leave Module Top Bar - Entitlements Dropdown:
        entitlements_tab: Entitlements dropdown in Leave top bar
        add_entitlements_menu_item: Add Entitlements menu item
        employee_entitlements_menu_item: Employee Entitlements menu item
        my_entitlements_menu_item: My Entitlements menu item

        # Leave Module Top Bar - Reports Dropdown:
        reports_tab: Reports dropdown in Leave top bar
        entitlements_usage_report_menu_item: Leave Entitlements and Usage Report
        my_entitlements_usage_report_menu_item: My Leave Entitlements Report

        # Leave Module Top Bar - Configure Dropdown:
        configure_tab: Configure dropdown in Leave top bar
        leave_period_menu_item: Leave Period menu item
        leave_types_menu_item: Leave Types menu item
        work_week_menu_item: Work Week menu item
        holidays_menu_item: Holidays menu item

    Example:
        >>> from playwright.sync_api import sync_playwright
        >>> with sync_playwright() as p:
        ...     browser = p.chromium.launch()
        ...     page = browser.new_page()
        ...     leave_page = LeaveBasePage(page, timeout=10)
        ...     # Navigate to Leave module using global navigation
        ...     leave_page.nav_header.navigate_to_leave()
        ...     # Now on Leave module - top bar is available
        ...     leave_page.navigate_to_apply_leave()  # Navigate to Apply Leave page
    """

    def __init__(self, page: Page, timeout: int = 10):
        """
        Initialize the Leave Base Page.

        Args:
            page: Playwright Page instance
            timeout: Default timeout for operations in seconds

        Note:
            Global navigation (navigate to Leave module) is available via
            self.nav_header.navigate_to_leave() (inherited from BasePage)
        """
        super().__init__(page, timeout)

        # Leave Top Bar - Direct Tabs
        self.apply_leave_tab: Locator = page.get_by_role("link", name="Apply", exact=True)
        self.my_leave_tab: Locator = page.get_by_role("link", name="My Leave", exact=True)
        self.leave_list_tab: Locator = page.get_by_role("link", name="Leave List", exact=True)
        self.assign_leave_tab: Locator = page.get_by_role("link", name="Assign Leave", exact=True)

        # Leave Top Bar - Entitlements Dropdown
        self.entitlements_tab: Locator = page.get_by_text("Entitlements", exact=True)
        self.add_entitlements_menu_item: Locator = page.get_by_role(
            "menuitem",
            name="Add Entitlements",
            exact=True,
        )
        self.employee_entitlements_menu_item: Locator = page.get_by_role(
            "menuitem",
            name="Employee Entitlements",
            exact=True,
        )
        self.my_entitlements_menu_item: Locator = page.get_by_role(
            "menuitem",
            name="My Entitlements",
            exact=True,
        )

        # Leave Top Bar - Reports Dropdown
        self.reports_tab: Locator = page.get_by_text("Reports", exact=True)
        self.entitlements_usage_report_menu_item: Locator = page.get_by_role(
            "menuitem",
            name="Leave Entitlements and Usage Report",
            exact=True,
        )
        self.my_entitlements_usage_report_menu_item: Locator = page.get_by_role(
            "menuitem",
            name="My Leave Entitlements and Usage Report",
            exact=True,
        )

        # Leave Top Bar - Configure Dropdown
        # Note: Configure tab is in the Leave module topbar, same level as Entitlements/Reports
        self.configure_tab: Locator = page.locator(
            "li.oxd-topbar-body-nav-tab:has-text('Configure')",
        )
        self.leave_period_menu_item: Locator = page.get_by_role(
            "menuitem",
            name="Leave Period",
            exact=True,
        )
        self.leave_types_menu_item: Locator = page.get_by_role(
            "menuitem",
            name="Leave Types",
            exact=True,
        )
        self.work_week_menu_item: Locator = page.get_by_role(
            "menuitem",
            name="Work Week",
            exact=True,
        )
        self.holidays_menu_item: Locator = page.get_by_role("menuitem", name="Holidays", exact=True)

    # Direct Tab Navigation

    def navigate_to_apply_leave(self) -> "ApplyLeavePage":
        """
        Navigate to Apply Leave page.

        Clicks the Apply tab in the Leave top bar.

        Returns:
            ApplyLeavePage instance for method chaining

        Example:
            >>> apply_page = leave_page.navigate_to_apply_leave()
            >>> apply_page.fill_leave_form(...)
        """
        self.logger.info("Navigating to Apply Leave")
        self.click(self.apply_leave_tab)
        # Import here to avoid circular dependency
        from src.ui.pages.leave.apply.apply_leave_page import ApplyLeavePage

        return ApplyLeavePage(self.page, self.timeout)

    def navigate_to_my_leave(self) -> "MyLeavePage":
        """
        Navigate to My Leave page.

        Clicks the My Leave tab in the Leave top bar.

        Returns:
            MyLeavePage instance for method chaining

        Example:
            >>> my_leave_page = leave_page.navigate_to_my_leave()
            >>> my_leave_page.view_my_leave_history()
        """
        self.logger.info("Navigating to My Leave")
        self.click(self.my_leave_tab)
        # Import here to avoid circular dependency
        from src.ui.pages.leave.my_leave.my_leave_page import MyLeavePage

        return MyLeavePage(self.page, self.timeout)

    def navigate_to_leave_list(self) -> "LeaveListPage":
        """
        Navigate to Leave List page.

        Clicks the Leave List tab in the Leave top bar.

        Returns:
            LeaveListPage instance for method chaining

        Example:
            >>> leave_list_page = leave_page.navigate_to_leave_list()
            >>> leave_list_page.search_leave_by_date(...)
        """
        self.logger.info("Navigating to Leave List")
        self.click(self.leave_list_tab)
        # Import here to avoid circular dependency
        from src.ui.pages.leave.list.leave_list_page import LeaveListPage

        return LeaveListPage(self.page, self.timeout)

    def navigate_to_assign_leave(self) -> "AssignLeavePage":
        """
        Navigate to Assign Leave page.

        Clicks the Assign Leave tab in the Leave top bar.

        Returns:
            AssignLeavePage instance for method chaining

        Example:
            >>> assign_page = leave_page.navigate_to_assign_leave()
            >>> assign_page.assign_leave_to_employee(...)
        """
        self.logger.info("Navigating to Assign Leave")
        self.click(self.assign_leave_tab)
        # Import here to avoid circular dependency
        from src.ui.pages.leave.assign.assign_leave import AssignLeavePage

        return AssignLeavePage(self.page, self.timeout)

    # Entitlements Dropdown Navigation

    def navigate_to_add_entitlements(self) -> "AddEntitlementsPage":
        """
        Navigate to Add Entitlements page.

        Opens Entitlements dropdown and clicks Add Entitlements menu item.

        Returns:
            AddEntitlementsPage instance for method chaining

        Example:
            >>> entitlements_page = leave_page.navigate_to_add_entitlements()
            >>> entitlements_page.add_leave_entitlement(...)
        """
        self.logger.info("Navigating to Add Entitlements")
        self.click(self.entitlements_tab)
        self.click(self.add_entitlements_menu_item)
        # Import here to avoid circular dependency
        from src.ui.pages.leave.entitlements.add_entitlements_page import (
            AddEntitlementsPage,
        )

        return AddEntitlementsPage(self.page, self.timeout)

    def navigate_to_employee_entitlements(self) -> "LeaveBasePage":
        """
        Navigate to Employee Entitlements page.

        Opens Entitlements dropdown and clicks Employee Entitlements menu item.

        Returns:
            Self for method chaining (page not yet implemented)

        Note:
            EmployeeEntitlementsPage not yet implemented - returns LeaveBasePage

        Example:
            >>> leave_page.navigate_to_employee_entitlements()
        """
        self.logger.info("Navigating to Employee Entitlements")
        self.click(self.entitlements_tab)
        self.click(self.employee_entitlements_menu_item)
        # TODO: Return EmployeeEntitlementsPage when implemented
        return self

    def navigate_to_my_entitlements(self) -> "LeaveBasePage":
        """
        Navigate to My Entitlements page.

        Opens Entitlements dropdown and clicks My Entitlements menu item.

        Returns:
            Self for method chaining (page not yet implemented)

        Note:
            MyEntitlementsPage not yet implemented - returns LeaveBasePage

        Example:
            >>> leave_page.navigate_to_my_entitlements()
        """
        self.logger.info("Navigating to My Entitlements")
        self.click(self.entitlements_tab)
        self.click(self.my_entitlements_menu_item)
        # TODO: Return MyEntitlementsPage when implemented
        return self

    # Reports Dropdown Navigation

    def navigate_to_entitlements_usage_report(self) -> "LeaveEntitlementsAndUsageReportPage":
        """
        Navigate to Leave Entitlements and Usage Report page.

        Opens Reports dropdown and clicks Leave Entitlements and Usage Report.

        Returns:
            LeaveEntitlementsAndUsageReportPage instance for method chaining

        Example:
            >>> report_page = leave_page.navigate_to_entitlements_usage_report()
            >>> report_page.generate_report(...)
        """
        self.logger.info("Navigating to Leave Entitlements and Usage Report")
        self.click(self.reports_tab)
        self.click(self.entitlements_usage_report_menu_item)
        # Import here to avoid circular dependency
        from src.ui.pages.leave.reports.leave_entitlements_and_usage_report_page import (
            LeaveEntitlementsAndUsageReportPage,
        )

        return LeaveEntitlementsAndUsageReportPage(self.page, self.timeout)

    def navigate_to_my_entitlements_usage_report(
        self,
    ) -> "MyLeaveEntitlementsAndUsageReportPage":
        """
        Navigate to My Leave Entitlements and Usage Report page.

        Opens Reports dropdown and clicks My Leave Entitlements and Usage Report.

        Returns:
            MyLeaveEntitlementsAndUsageReportPage instance for method chaining

        Example:
            >>> my_report_page = leave_page.navigate_to_my_entitlements_usage_report()
            >>> my_report_page.view_my_usage(...)
        """
        self.logger.info("Navigating to My Leave Entitlements and Usage Report")
        self.click(self.reports_tab)
        self.click(self.my_entitlements_usage_report_menu_item)
        # Import here to avoid circular dependency
        from src.ui.pages.leave.reports.my_leave_entitlements_and_usage_report import (
            MyLeaveEntitlementsAndUsageReportPage,
        )

        return MyLeaveEntitlementsAndUsageReportPage(self.page, self.timeout)

    # Configure Dropdown Navigation

    def navigate_to_leave_period(self) -> "LeavePeriodPage":
        """
        Navigate to Leave Period configuration page.

        Opens Configure dropdown and clicks Leave Period menu item.

        Returns:
            LeavePeriodPage instance for method chaining

        Example:
            >>> leave_period_page = leave_page.navigate_to_leave_period()
            >>> leave_period_page.configure_leave_period("January", "01")
            >>> leave_period_page.save()

        Note:
            This method navigates directly via URL to avoid Configure dropdown issues.
            The dropdown has locator complexities, so direct URL navigation is more reliable.
        """
        from src.ui.pages.leave.configure.leave_period_page import LeavePeriodPage

        self.logger.info("Navigating to Leave Period")

        # Navigate directly to Leave Period URL (avoiding Configure dropdown issues)
        # Extract base URL from current URL
        current_url = self.page.url
        base_url = current_url.split("/web/")[0] if "/web/" in current_url else current_url
        leave_period_url = f"{base_url}/web/index.php/leave/defineLeavePeriod"

        # Navigate to Leave Period page
        self.page.goto(leave_period_url, wait_until="networkidle")

        # Create and return page object
        return LeavePeriodPage(self.page, self.timeout)

    def navigate_to_leave_types(self) -> "LeaveBasePage":
        """
        Navigate to Leave Types configuration page.

        Opens Configure dropdown and clicks Leave Types menu item.

        Returns:
            Self for method chaining (page not yet implemented)

        Note:
            LeaveTypesPage not yet implemented - returns LeaveBasePage

        Example:
            >>> leave_page.navigate_to_leave_types()
        """
        self.logger.info("Navigating to Leave Types")
        self.click(self.configure_tab)
        self.click(self.leave_types_menu_item)
        # TODO: Return LeaveTypesPage when implemented
        return self

    def navigate_to_work_week(self) -> "WorkWeekPage":
        """
        Navigate to Work Week configuration page.

        Opens Configure dropdown and clicks Work Week menu item.

        Returns:
            WorkWeekPage instance for method chaining

        Example:
            >>> work_week_page = leave_page.navigate_to_work_week()
            >>> work_week_page.configure_work_days(...)
        """
        self.logger.info("Navigating to Work Week")
        self.click(self.configure_tab)
        self.click(self.work_week_menu_item)
        # Import here to avoid circular dependency
        from src.ui.pages.leave.configure.work_week_page import WorkWeekPage

        return WorkWeekPage(self.page, self.timeout)

    def navigate_to_holidays(self) -> "HolidaysPage":
        """
        Navigate to Holidays configuration page.

        Opens Configure dropdown and clicks Holidays menu item.

        Returns:
            HolidaysPage instance for method chaining

        Example:
            >>> holidays_page = leave_page.navigate_to_holidays()
            >>> holidays_page.add_holiday(...)
        """
        self.logger.info("Navigating to Holidays")
        self.click(self.configure_tab)
        self.click(self.holidays_menu_item)
        # Import here to avoid circular dependency
        from src.ui.pages.leave.configure.holidays_page import HolidaysPage

        return HolidaysPage(self.page, self.timeout)
