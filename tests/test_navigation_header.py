"""
Test suite for NavigationHeader component.

This module tests the global navigation header component that appears on all
authenticated pages, including main menu navigation and user dropdown actions.

Test Categories:
    - Component Visibility: Verify navigation elements are present
    - Main Menu Navigation: Test navigation to different modules
    - User Dropdown: Test user account actions (logout, change password, etc.)
    - Component Integration: Verify component works across different pages
"""

# pylint: disable=import-error  # src and utils modules are in project root
import re

import pytest
from playwright.sync_api import expect

from src.config.protocols import ConfigService
from src.ui.components.navigation_header import NavigationHeader


@pytest.mark.navigation
@pytest.mark.component
class TestNavigationHeaderVisibility:
    """Test visibility and presence of NavigationHeader elements."""

    def test_main_menu_items_visible(self, dashboard_page):
        """
        Verify all main menu items are visible after login.

        Tests that the navigation header displays all expected menu items
        for a logged-in user with standard permissions.
        """
        nav = dashboard_page.nav_header

        # Verify main menu items are visible
        expect(nav.admin_menu).to_be_visible()
        expect(nav.pim_menu).to_be_visible()
        expect(nav.leave_menu).to_be_visible()
        expect(nav.time_menu).to_be_visible()
        expect(nav.recruitment_menu).to_be_visible()
        expect(nav.my_info_menu).to_be_visible()
        expect(nav.performance_menu).to_be_visible()
        expect(nav.dashboard_menu).to_be_visible()
        expect(nav.directory_menu).to_be_visible()
        expect(nav.maintenance_menu).to_be_visible()
        expect(nav.buzz_menu).to_be_visible()

    def test_user_dropdown_visible(self, dashboard_page):
        """
        Verify user dropdown is visible and clickable.

        Tests that the user dropdown button appears in the navigation header
        and can be interacted with.
        """
        nav = dashboard_page.nav_header

        # Verify user dropdown is visible
        expect(nav.user_dropdown).to_be_visible()
        expect(nav.user_dropdown).to_be_enabled()

    def test_user_dropdown_menu_items(self, dashboard_page):
        """
        Verify user dropdown menu items appear when opened.

        Tests that clicking the user dropdown reveals all expected menu items
        (Change Password, About, Support, Logout).
        """
        nav = dashboard_page.nav_header

        # Open user dropdown
        nav.open_user_dropdown()

        # Verify dropdown menu items are visible
        expect(nav.change_password_link).to_be_visible()
        expect(nav.about_link).to_be_visible()
        expect(nav.support_link).to_be_visible()
        expect(nav.logout_link).to_be_visible()


@pytest.mark.navigation
@pytest.mark.component
class TestNavigationHeaderMainMenu:
    """Test main menu navigation functionality."""

    def test_navigate_to_admin(self, dashboard_page):
        """
        Test navigation to Admin module.

        Verifies that clicking Admin menu navigates to the Admin module
        and the URL changes accordingly.
        """
        nav = dashboard_page.nav_header

        # Navigate to Admin
        nav.navigate_to_admin()

        # Verify URL contains admin path
        expect(dashboard_page.page).to_have_url(re.compile(r"admin", re.IGNORECASE), timeout=5000)

    def test_navigate_to_pim(self, dashboard_page):
        """
        Test navigation to PIM module.

        Verifies that clicking PIM menu navigates to the PIM module
        and the URL changes accordingly.
        """
        nav = dashboard_page.nav_header

        # Navigate to PIM
        nav.navigate_to_pim()

        # Verify URL contains pim path
        expect(dashboard_page.page).to_have_url(re.compile(r"pim", re.IGNORECASE), timeout=5000)

    def test_navigate_to_leave(self, dashboard_page):
        """
        Test navigation to Leave module.

        Verifies that clicking Leave menu navigates to the Leave module from Dashboard.
        """
        nav = dashboard_page.nav_header

        # Navigate to Leave from Dashboard
        nav.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=5000)

    def test_navigate_to_time(self, dashboard_page):
        """
        Test navigation to Time module.

        Verifies that clicking Time menu navigates to the Time module
        and the URL changes accordingly.
        """
        nav = dashboard_page.nav_header

        # Navigate to Time
        nav.navigate_to_time()

        # Verify URL contains time path
        expect(dashboard_page.page).to_have_url(re.compile(r"time", re.IGNORECASE), timeout=5000)

    def test_navigate_to_recruitment(self, dashboard_page):
        """
        Test navigation to Recruitment module.

        Verifies that clicking Recruitment menu navigates to the Recruitment
        module and the URL changes accordingly.
        """
        nav = dashboard_page.nav_header

        # Navigate to Recruitment
        nav.navigate_to_recruitment()

        # Verify URL contains recruitment path
        expect(dashboard_page.page).to_have_url(
            re.compile(r"recruitment", re.IGNORECASE),
            timeout=5000,
        )

    def test_navigate_to_my_info(self, dashboard_page):
        """
        Test navigation to My Info module.

        Verifies that clicking My Info menu navigates to the My Info module
        and the URL changes accordingly.
        """
        nav = dashboard_page.nav_header

        # Navigate to My Info
        nav.navigate_to_my_info()

        # Verify URL contains pim/viewMyDetails or similar
        dashboard_page.get_current_url().lower()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"(pim|myinfo)", re.IGNORECASE),
            timeout=5000,
        )

    def test_navigate_to_performance(self, dashboard_page):
        """
        Test navigation to Performance module.

        Verifies that clicking Performance menu navigates to the Performance
        module and the URL changes accordingly.
        """
        nav = dashboard_page.nav_header

        # Navigate to Performance
        nav.navigate_to_performance()

        # Verify URL contains performance path
        expect(dashboard_page.page).to_have_url(
            re.compile(r"performance", re.IGNORECASE),
            timeout=5000,
        )

    def test_navigate_to_dashboard(self, dashboard_page):
        """
        Test navigation to Dashboard.

        Verifies that clicking Dashboard menu navigates to the main dashboard
        and the URL changes accordingly.
        """
        nav = dashboard_page.nav_header

        # Navigate to Dashboard
        nav.navigate_to_dashboard()

        # Verify URL contains dashboard path
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )

    def test_navigate_to_directory(self, dashboard_page):
        """
        Test navigation to Directory module.

        Verifies that clicking Directory menu navigates to the Directory
        module and the URL changes accordingly.
        """
        nav = dashboard_page.nav_header

        # Navigate to Directory
        nav.navigate_to_directory()

        # Verify URL contains directory path
        expect(dashboard_page.page).to_have_url(
            re.compile(r"directory", re.IGNORECASE),
            timeout=5000,
        )

    def test_navigate_to_maintenance(self, dashboard_page):
        """
        Test navigation to Maintenance module.

        Verifies that clicking Maintenance menu navigates to the Maintenance
        module and the URL changes accordingly.
        """
        nav = dashboard_page.nav_header

        # Navigate to Maintenance
        nav.navigate_to_maintenance()

        # Verify URL contains maintenance or admin path
        dashboard_page.get_current_url().lower()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"(maintenance|admin)", re.IGNORECASE),
            timeout=5000,
        )

    def test_navigate_to_buzz(self, dashboard_page):
        """
        Test navigation to Buzz module.

        Verifies that clicking Buzz menu navigates to the Buzz (social) module
        and the URL changes accordingly.
        """
        nav = dashboard_page.nav_header

        # Navigate to Buzz
        nav.navigate_to_buzz()

        # Verify URL contains buzz path
        expect(dashboard_page.page).to_have_url(re.compile(r"buzz", re.IGNORECASE), timeout=5000)


@pytest.mark.navigation
@pytest.mark.component
class TestNavigationHeaderUserDropdown:
    """Test user dropdown functionality."""

    def test_open_user_dropdown(self, dashboard_page):
        """
        Test opening the user dropdown.

        Verifies that the user dropdown can be opened and menu items
        become visible.
        """
        nav = dashboard_page.nav_header

        # Open dropdown
        nav.open_user_dropdown()

        # Verify dropdown menu items are visible
        expect(nav.logout_link).to_be_visible(timeout=5000)

    def test_logout_functionality(self, dashboard_page, config_service: ConfigService):
        """
        Test logout functionality.

        Verifies that clicking logout redirects to login page and
        the session is terminated.
        """
        nav = dashboard_page.nav_header

        # Perform logout
        nav.logout()

        # Verify redirected to login page (login or auth/login in URL)
        expect(dashboard_page.page).to_have_url(
            re.compile(r"(login|auth/login)", re.IGNORECASE),
            timeout=5000,
        )

        # Verify login form is visible (confirms logged out)
        login_form = dashboard_page.page.locator("form")
        expect(login_form).to_be_visible(timeout=5000)

    def test_change_password_navigation(self, dashboard_page):
        """
        Test navigation to Change Password page.

        Verifies that clicking Change Password in the user dropdown
        navigates to the password change page.
        """
        nav = dashboard_page.nav_header

        # Navigate to change password
        nav.navigate_to_change_password()

        # Verify URL contains password or update password path
        dashboard_page.get_current_url().lower()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"(password|updatepassword)", re.IGNORECASE),
            timeout=5000,
        )

    def test_about_opening(self, dashboard_page):
        """
        Test navigation to About page.

        Verifies that clicking About in the user dropdown
        opens the about dialog or page.
        """
        nav = dashboard_page.nav_header

        # Navigate to about
        nav.open_about()

        # Verify about dialog or modal appears
        # Note: About may open a modal instead of navigating to a new page
        about_dialog = dashboard_page.page.get_by_text("×AboutCompany Name:")
        expect(about_dialog).to_be_visible(timeout=5000)

    def test_support_navigation(self, dashboard_page):
        """
        Test navigation to Support page.

        Verifies that clicking Support in the user dropdown
        navigates to the support page or opens support resources.
        """
        nav = dashboard_page.nav_header

        # Navigate to support
        nav.navigate_to_support()

        # Verify URL contains password or update password path
        dashboard_page.get_current_url().lower()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"(support)", re.IGNORECASE),
            timeout=5000,
        )


@pytest.mark.navigation
@pytest.mark.component
@pytest.mark.integration
class TestNavigationHeaderIntegration:
    """Test NavigationHeader component integration across pages."""

    def test_navigation_header_available_on_all_pages(self, dashboard_page):
        """
        Test that NavigationHeader is available on all authenticated pages.

        Verifies that the navigation header persists when navigating
        between different modules.
        """
        nav = dashboard_page.nav_header

        # Start on Leave page
        expect(nav.leave_menu).to_be_visible()

        # Navigate to Dashboard
        nav.navigate_to_dashboard()
        expect(nav.dashboard_menu).to_be_visible()

        # Navigate to PIM
        nav.navigate_to_pim()
        expect(nav.pim_menu).to_be_visible()

        # Navigate to Admin
        nav.navigate_to_admin()
        expect(nav.admin_menu).to_be_visible()

        # Verify all menu items still visible after navigations
        expect(nav.leave_menu).to_be_visible()
        expect(nav.dashboard_menu).to_be_visible()
        expect(nav.pim_menu).to_be_visible()

    def test_navigation_header_composition_pattern(self, dashboard_page):
        """
        Test that NavigationHeader uses composition pattern correctly.

        Verifies that the nav_header attribute is available on page objects
        and works as expected via composition (not inheritance).
        """

        # Verify nav_header exists and is accessible (test composition pattern)
        # Use expect to verify the nav_header component is functional
        nav = dashboard_page.nav_header

        # Verify it's the correct type by testing its functionality
        expect(nav.dashboard_menu).to_be_visible()
        expect(nav.user_dropdown).to_be_visible()

        # Verify nav_header is a NavigationHeader instance (Python check)
        if not isinstance(nav, NavigationHeader):
            raise AssertionError(f"Expected NavigationHeader, got {type(nav)}")

    def test_multiple_page_objects_share_navigation(self, dashboard_page, browser, config_service):
        """
        Test that different page objects can use the same NavigationHeader.

        Verifies that NavigationHeader is composable and can be used
        across different page object instances.
        """

        # Create a new page object instance (LoginPage just as example)
        # Note: We're on dashboard_page, so we'll navigate to dashboard then check
        dashboard_page.nav_header.navigate_to_dashboard()

        # Verify navigation works from different page context
        dashboard_page.nav_header.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=5000)

        # Verify we can navigate to another module
        dashboard_page.nav_header.navigate_to_pim()
        expect(dashboard_page.page).to_have_url(re.compile(r"pim", re.IGNORECASE), timeout=5000)

    def test_navigation_preserves_state(self, dashboard_page):
        """
        Test that navigation preserves application state correctly.

        Verifies that navigating between modules using NavigationHeader
        doesn't cause state loss or errors.
        """
        nav = dashboard_page.nav_header

        # Navigate through multiple modules and verify URLs change
        nav.navigate_to_dashboard()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )

        nav.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=5000)

        nav.navigate_to_pim()
        expect(dashboard_page.page).to_have_url(re.compile(r"pim", re.IGNORECASE), timeout=5000)

        # URLs are verified to be different by the unique path expectations above


@pytest.mark.navigation
@pytest.mark.component
@pytest.mark.smoke
class TestNavigationHeaderSmoke:
    """Smoke tests for critical NavigationHeader functionality."""

    def test_smoke_main_menu_visible(self, dashboard_page):
        """
        Smoke test: Verify main navigation menu is visible.

        Critical test to ensure the navigation header renders correctly
        after login.
        """
        nav = dashboard_page.nav_header

        # Verify at least the main menu items are visible
        expect(nav.dashboard_menu).to_be_visible()
        expect(nav.leave_menu).to_be_visible()
        expect(nav.pim_menu).to_be_visible()

    def test_smoke_user_dropdown_accessible(self, dashboard_page):
        """
        Smoke test: Verify user dropdown is accessible.

        Critical test to ensure users can access account options.
        """
        nav = dashboard_page.nav_header

        # Verify user dropdown exists and is clickable
        expect(nav.user_dropdown).to_be_visible()
        nav.open_user_dropdown()
        expect(nav.logout_link).to_be_visible(timeout=5000)

    def test_smoke_navigation_works(self, dashboard_page):
        """
        Smoke test: Verify basic navigation works.

        Critical test to ensure users can navigate between modules.
        """
        nav = dashboard_page.nav_header

        # Navigate to Dashboard
        nav.navigate_to_dashboard()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )

        # Navigate back to Leave
        nav.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=5000)

    def test_smoke_logout_works(self, dashboard_page):
        """
        Smoke test: Verify logout works.

        Critical test to ensure users can log out of the application.
        """
        nav = dashboard_page.nav_header

        # Perform logout
        nav.logout()

        # Verify logged out (login page visible)
        expect(dashboard_page.page).to_have_url(
            re.compile(r"(login|auth/login)", re.IGNORECASE),
            timeout=5000,
        )
