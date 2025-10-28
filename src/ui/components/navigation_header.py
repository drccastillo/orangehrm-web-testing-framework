"""
NavigationHeader Component - Global navigation menu for OrangeHRM application.

This component encapsulates the main navigation menu that appears on all pages
after login, providing access to different modules (Admin, PIM, Leave, etc.)
and user account actions (logout, change password, etc.).

Design Pattern:
    - Component-Based Abstraction: Reusable across all authenticated pages
    - Composition over Inheritance: Injected into page objects
    - Single Responsibility: Only handles global navigation
    - Navigation methods return page objects for fluent interface
"""

# pylint: disable=import-error  # utils module is in project root
from typing import TYPE_CHECKING

from playwright.sync_api import Locator, Page

from utils.logger import TestLogger

# Type hints only - avoid circular imports
if TYPE_CHECKING:
    from src.ui.pages.leave.list.leave_list_page import LeaveListPage


class NavigationHeader:
    """
    Global navigation header component for OrangeHRM.

    This component appears on all pages after successful login and provides
    navigation to different modules and user account management.

    Key Features:
        - Main menu navigation (Admin, PIM, Leave, Time, etc.)
        - User dropdown actions (Logout, Change Password, About)
        - Cross-module navigation support
        - Consistent across all authenticated pages

    Attributes:
        page: Playwright Page instance
        logger: Logger instance for this component

        # Main Menu Items
        admin_menu: Admin module link
        pim_menu: PIM (Personal Information Management) module link
        leave_menu: Leave management module link
        time_menu: Time tracking module link
        recruitment_menu: Recruitment module link
        my_info_menu: My Info module link
        performance_menu: Performance management module link
        dashboard_menu: Dashboard link
        directory_menu: Directory module link
        maintenance_menu: Maintenance module link
        buzz_menu: Buzz (social) module link

        # User Dropdown
        user_dropdown: User dropdown button
        change_password_link: Link to change password
        about_link: About application link
        support_link: Support link
        logout_link: Logout link

    Example:
        >>> # In a page object
        >>> class DashboardPage(BasePage):
        ...     def __init__(self, page: Page):
        ...         super().__init__(page)
        ...         self.nav_header = NavigationHeader(page)
        ...
        ...     def go_to_leave(self):
        ...         self.nav_header.navigate_to_leave()

        >>> # In tests
        >>> dashboard_page.nav_header.navigate_to_leave()
        >>> # Now on Leave module
        >>> leave_page.nav_header.logout()
        >>> # Logged out

    Note:
        This component uses direct Playwright locators without inheriting from
        BasePage to keep it lightweight and focused on navigation only.
    """

    def __init__(self, page: Page):
        """
        Initialize the Navigation Header component.

        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.logger = TestLogger.get_logger(self.__class__.__name__)

        # Main Menu Navigation Items
        # Using role-based locators for accessibility and reliability
        self.admin_menu: Locator = page.get_by_role("link", name="Admin", exact=True)
        self.pim_menu: Locator = page.get_by_role("link", name="PIM", exact=True)
        self.leave_menu: Locator = page.get_by_role("link", name="Leave", exact=True)
        self.time_menu: Locator = page.get_by_role("link", name="Time", exact=True)
        self.recruitment_menu: Locator = page.get_by_role("link", name="Recruitment", exact=True)
        self.my_info_menu: Locator = page.get_by_role("link", name="My Info", exact=True)
        self.performance_menu: Locator = page.get_by_role("link", name="Performance", exact=True)
        self.dashboard_menu: Locator = page.get_by_role("link", name="Dashboard", exact=True)
        self.directory_menu: Locator = page.get_by_role("link", name="Directory", exact=True)
        self.maintenance_menu: Locator = page.get_by_role("link", name="Maintenance", exact=True)
        self.claim_menu: Locator = page.get_by_role("link", name="Claim", exact=True)
        self.buzz_menu: Locator = page.get_by_role("link", name="Buzz", exact=True)

        # User Dropdown and Actions
        # Note: These locators may need adjustment based on actual OrangeHRM HTML
        self.user_dropdown: Locator = page.locator(".oxd-userdropdown-tab")
        self.change_password_link: Locator = page.get_by_role("menuitem", name="Change Password")
        self.about_link: Locator = page.get_by_role("menuitem", name="About")
        self.support_link: Locator = page.get_by_role("menuitem", name="Support")
        self.logout_link: Locator = page.get_by_role("menuitem", name="Logout")

    # Main Module Navigation Methods

    def navigate_to_admin(self) -> None:
        """
        Navigate to Admin module.

        The Admin module provides access to user management, job management,
        organization settings, and qualifications.

        Example:
            >>> nav_header.navigate_to_admin()
            >>> # Now on Admin module
        """
        self.logger.info("Navigating to Admin module")
        self.admin_menu.click()

    def navigate_to_pim(self) -> None:
        """
        Navigate to PIM (Personal Information Management) module.

        The PIM module handles employee records, reports, and employee management.

        Example:
            >>> nav_header.navigate_to_pim()
            >>> # Now on PIM module
        """
        self.logger.info("Navigating to PIM module")
        self.pim_menu.click()

    def navigate_to_leave(self) -> "LeaveListPage":
        """
        Navigate to Leave module and return LeaveListPage instance.

        The Leave module handles leave requests, entitlements, and leave configuration.

        Returns:
            LeaveListPage: Leave List page object ready for interaction

        Example:
            >>> leave_page = nav_header.navigate_to_leave()
            >>> leave_page.search_leave(...)  # Can immediately use the page
        """
        # Import here to avoid circular dependency
        from src.ui.pages.leave.list.leave_list_page import LeaveListPage

        self.logger.info("Navigating to Leave module")
        self.leave_menu.click()

        # Wait for navigation and create page object
        self.page.wait_for_load_state("networkidle")

        # Create and return page object
        return LeaveListPage(self.page, timeout=10)

    def navigate_to_time(self) -> None:
        """
        Navigate to Time module.

        The Time module handles timesheets, attendance, and time tracking.

        Example:
            >>> nav_header.navigate_to_time()
            >>> # Now on Time module
        """
        self.logger.info("Navigating to Time module")
        self.time_menu.click()

    def navigate_to_recruitment(self) -> None:
        """
        Navigate to Recruitment module.

        The Recruitment module handles job vacancies, candidates, and hiring workflow.

        Example:
            >>> nav_header.navigate_to_recruitment()
            >>> # Now on Recruitment module
        """
        self.logger.info("Navigating to Recruitment module")
        self.recruitment_menu.click()

    def navigate_to_my_info(self) -> None:
        """
        Navigate to My Info module.

        The My Info module shows the current user's personal information.

        Example:
            >>> nav_header.navigate_to_my_info()
            >>> # Now on My Info page
        """
        self.logger.info("Navigating to My Info module")
        self.my_info_menu.click()

    def navigate_to_performance(self) -> None:
        """
        Navigate to Performance module.

        The Performance module handles performance reviews, KPIs, and tracking.

        Example:
            >>> nav_header.navigate_to_performance()
            >>> # Now on Performance module
        """
        self.logger.info("Navigating to Performance module")
        self.performance_menu.click()

    def navigate_to_dashboard(self) -> None:
        """
        Navigate to Dashboard.

        The Dashboard is the home page showing widgets and quick links.

        Example:
            >>> nav_header.navigate_to_dashboard()
            >>> # Now on Dashboard
        """
        self.logger.info("Navigating to Dashboard")
        self.dashboard_menu.click()

    def navigate_to_directory(self) -> None:
        """
        Navigate to Directory module.

        The Directory shows employee listings and search.

        Example:
            >>> nav_header.navigate_to_directory()
            >>> # Now on Directory
        """
        self.logger.info("Navigating to Directory module")
        self.directory_menu.click()

    def navigate_to_maintenance(self) -> None:
        """
        Navigate to Maintenance module.

        The Maintenance module provides database backup, cleanup, and admin tools.

        Example:
            >>> nav_header.navigate_to_maintenance()
            >>> # Now on Maintenance module
        """
        self.logger.info("Navigating to Maintenance module")
        self.maintenance_menu.click()

    def navigate_to_buzz(self) -> None:
        """
        Navigate to Buzz module.

        Buzz is the social/communication module for internal posts and updates.

        Example:
            >>> nav_header.navigate_to_buzz()
            >>> # Now on Buzz module
        """
        self.logger.info("Navigating to Buzz module")
        self.buzz_menu.click()

    # User Dropdown Actions

    def open_user_dropdown(self) -> None:
        """
        Open the user dropdown menu.

        This dropdown contains user account actions like logout, change password.

        Example:
            >>> nav_header.open_user_dropdown()
            >>> # Dropdown is now open
        """
        self.logger.debug("Opening user dropdown")
        self.user_dropdown.click()

    def logout(self) -> None:
        """
        Logout from the application.

        Opens user dropdown and clicks logout link.

        Example:
            >>> nav_header.logout()
            >>> # User is logged out, redirected to login page
        """
        self.logger.info("Logging out")
        self.open_user_dropdown()
        self.logout_link.click()

    def navigate_to_change_password(self) -> None:
        """
        Navigate to Change Password page.

        Opens user dropdown and clicks change password link.

        Example:
            >>> nav_header.change_password()
            >>> # Now on Change Password page
        """
        self.logger.info("Navigating to Change Password")
        self.open_user_dropdown()
        self.change_password_link.click()

    def open_about(self) -> None:
        """
        Open About dialog.

        Opens user dropdown and clicks about link to show application info.

        Example:
            >>> nav_header.open_about()
            >>> # About dialog is displayed
        """
        self.logger.info("Opening About dialog")
        self.open_user_dropdown()
        self.about_link.click()

    def navigate_to_support(self) -> None:
        """
        Open Support page/link.

        Opens user dropdown and clicks support link.

        Example:
            >>> nav_header.open_support()
            >>> # Support page/dialog is displayed
        """
        self.logger.info("Opening Support")
        self.open_user_dropdown()
        self.support_link.click()

    # Helper Methods

    def is_menu_visible(self, menu_name: str) -> bool:
        """
        Check if a specific menu item is visible.

        Args:
            menu_name: Name of the menu (e.g., "Admin", "PIM", "Leave")

        Returns:
            True if menu is visible, False otherwise

        Example:
            >>> if nav_header.is_menu_visible("Leave"):
            ...     print("User has access to Leave module")
        """
        menu_mapping = {
            "Admin": self.admin_menu,
            "PIM": self.pim_menu,
            "Leave": self.leave_menu,
            "Time": self.time_menu,
            "Recruitment": self.recruitment_menu,
            "My Info": self.my_info_menu,
            "Performance": self.performance_menu,
            "Dashboard": self.dashboard_menu,
            "Directory": self.directory_menu,
            "Maintenance": self.maintenance_menu,
            "Buzz": self.buzz_menu,
        }

        menu = menu_mapping.get(menu_name)
        if menu:
            return menu.is_visible()
        return False

    def get_visible_menus(self) -> list[str]:
        """
        Get list of all visible menu items.

        Returns:
            List of menu names that are currently visible

        Example:
            >>> visible = nav_header.get_visible_menus()
            >>> print(f"User has access to: {', '.join(visible)}")
        """
        all_menus = [
            "Admin",
            "PIM",
            "Leave",
            "Time",
            "Recruitment",
            "My Info",
            "Performance",
            "Dashboard",
            "Directory",
            "Maintenance",
            "Buzz",
        ]

        visible_menus = [menu for menu in all_menus if self.is_menu_visible(menu)]
        return visible_menus
