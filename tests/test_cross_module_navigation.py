"""
Test suite for cross-module navigation workflows.

This module tests navigation workflows that span multiple modules,
verifying that users can navigate seamlessly across different areas
of the OrangeHRM application using the NavigationHeader component.

Test Categories:
    - Sequential Navigation: Navigate through multiple modules in sequence
    - Round-Trip Navigation: Navigate away and back to verify state
    - Common User Workflows: Simulate real user navigation patterns
    - Navigation Performance: Verify navigation doesn't cause delays or errors
"""

# pylint: disable=import-error  # src and utils modules are in project root
import re

import pytest
from playwright.sync_api import expect


@pytest.mark.navigation
@pytest.mark.integration
@pytest.mark.cross_module
class TestSequentialNavigation:
    """Test sequential navigation through multiple modules."""

    def test_navigate_through_all_main_modules(self, dashboard_page):
        """
        Test navigation through all main modules sequentially.

        Simulates a user exploring different modules in the application,
        verifying that each navigation works correctly.
        """
        nav = dashboard_page.nav_header

        # Start on Leave module (from fixture)
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )

        # Navigate to Leave
        nav.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"leave", re.IGNORECASE),
            timeout=5000,
        )
        expect(nav.dashboard_menu).to_be_visible()

        # Navigate to Admin
        nav.navigate_to_admin()
        expect(dashboard_page.page).to_have_url(re.compile(r"admin", re.IGNORECASE), timeout=5000)
        expect(nav.admin_menu).to_be_visible()

        # Navigate to PIM
        nav.navigate_to_pim()
        expect(dashboard_page.page).to_have_url(re.compile(r"pim", re.IGNORECASE), timeout=5000)
        expect(nav.pim_menu).to_be_visible()

        # Navigate to Time
        nav.navigate_to_time()
        expect(dashboard_page.page).to_have_url(re.compile(r"time", re.IGNORECASE), timeout=5000)
        expect(nav.time_menu).to_be_visible()

        # Navigate to Recruitment
        nav.navigate_to_recruitment()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"recruitment", re.IGNORECASE),
            timeout=5000,
        )
        expect(nav.recruitment_menu).to_be_visible()

        # Navigate back to Dashboard
        nav.navigate_to_dashboard()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )
        expect(nav.dashboard_menu).to_be_visible()

    def test_navigate_admin_to_pim_workflow(self, dashboard_page):
        """
        Test Admin to PIM navigation workflow.

        Common workflow: Admin creates user, then views in PIM.
        """
        nav = dashboard_page.nav_header

        # Navigate to Admin
        nav.navigate_to_admin()
        expect(dashboard_page.page).to_have_url(re.compile(r"admin", re.IGNORECASE), timeout=5000)

        # Navigate to PIM
        nav.navigate_to_pim()
        expect(dashboard_page.page).to_have_url(re.compile(r"pim", re.IGNORECASE), timeout=5000)

        # Verify navigation header still works
        expect(nav.admin_menu).to_be_visible()
        expect(nav.pim_menu).to_be_visible()

    def test_navigate_pim_to_leave_workflow(self, dashboard_page):
        """
        Test PIM to Leave navigation workflow.

        Common workflow: View employee in PIM, then assign leave.
        """
        nav = dashboard_page.nav_header

        # Navigate to PIM
        nav.navigate_to_pim()
        expect(dashboard_page.page).to_have_url(re.compile(r"pim", re.IGNORECASE), timeout=5000)

        # Navigate to Leave
        nav.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=5000)

        # Verify navigation header still works
        expect(nav.pim_menu).to_be_visible()
        expect(nav.leave_menu).to_be_visible()

    def test_navigate_leave_to_time_workflow(self, dashboard_page):
        """
        Test Leave to Time navigation workflow.

        Common workflow: Check leave balance, then view timesheets.
        """
        nav = dashboard_page.nav_header

        # Start on Dashboard (from fixture)
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )

        # Navigate to Time
        nav.navigate_to_time()
        expect(dashboard_page.page).to_have_url(re.compile(r"time", re.IGNORECASE), timeout=5000)

        # Verify navigation header still works
        expect(nav.leave_menu).to_be_visible()
        expect(nav.time_menu).to_be_visible()

    def test_navigate_recruitment_to_performance_workflow(self, dashboard_page):
        """
        Test Recruitment to Performance navigation workflow.

        Common workflow: Recruit employee, then manage performance.
        """
        nav = dashboard_page.nav_header

        # Navigate to Recruitment
        nav.navigate_to_recruitment()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"recruitment", re.IGNORECASE),
            timeout=5000,
        )

        # Navigate to Performance
        nav.navigate_to_performance()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"performance", re.IGNORECASE),
            timeout=5000,
        )

        # Verify navigation header still works
        expect(nav.recruitment_menu).to_be_visible()
        expect(nav.performance_menu).to_be_visible()


@pytest.mark.navigation
@pytest.mark.integration
@pytest.mark.cross_module
class TestRoundTripNavigation:
    """Test round-trip navigation (navigate away and back)."""

    def test_leave_to_dashboard_and_back(self, dashboard_page):
        """
        Test navigating from Leave to Dashboard and back.

        Verifies that returning to Leave module after visiting Dashboard
        works correctly.
        """
        nav = dashboard_page.nav_header

        # Start on Leave
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )

        # Navigate to Leave
        nav.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"leave", re.IGNORECASE),
            timeout=5000,
        )

        # Navigate back to Dashboard
        nav.navigate_to_dashboard()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )

    def test_multiple_round_trips(self, dashboard_page):
        """
        Test multiple round trips between modules.

        Verifies that navigating back and forth multiple times
        works correctly without errors.
        """
        nav = dashboard_page.nav_header

        # Round trip 1: Leave -> Dashboard -> Leave
        nav.navigate_to_dashboard()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )
        nav.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=5000)

        # Round trip 2: Leave -> PIM -> Leave
        nav.navigate_to_pim()
        expect(dashboard_page.page).to_have_url(re.compile(r"pim", re.IGNORECASE), timeout=5000)
        nav.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=5000)

        # Round trip 3: Leave -> Time -> Leave
        nav.navigate_to_time()
        expect(dashboard_page.page).to_have_url(re.compile(r"time", re.IGNORECASE), timeout=5000)
        nav.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=5000)

        # Verify navigation still works after multiple round trips
        expect(nav.leave_menu).to_be_visible()

    def test_round_trip_with_user_dropdown(self, dashboard_page):
        """
        Test round trip navigation with user dropdown interaction.

        Verifies that user dropdown works correctly after navigating
        between modules.
        """
        nav = dashboard_page.nav_header

        # Navigate to Dashboard
        nav.navigate_to_dashboard()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )

        # Open user dropdown
        nav.open_user_dropdown()
        expect(nav.logout_link).to_be_visible(timeout=5000)

        # Navigate to PIM
        nav.navigate_to_pim()
        expect(dashboard_page.page).to_have_url(re.compile(r"pim", re.IGNORECASE), timeout=5000)

        # Open user dropdown again
        nav.open_user_dropdown()
        expect(nav.logout_link).to_be_visible(timeout=5000)

        # Navigate back to Leave
        nav.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=5000)

        # Verify user dropdown still works
        nav.open_user_dropdown()
        expect(nav.logout_link).to_be_visible(timeout=5000)


@pytest.mark.navigation
@pytest.mark.integration
@pytest.mark.cross_module
class TestCommonUserWorkflows:
    """Test common user workflows that span multiple modules."""

    def test_hr_manager_workflow(self, dashboard_page):
        """
        Test typical HR Manager workflow.

        Workflow:
        1. Check dashboard for quick stats
        2. View employees in PIM
        3. Check leave requests
        4. Review recruitment pipeline
        """
        nav = dashboard_page.nav_header

        # Step 1: Check dashboard
        nav.navigate_to_dashboard()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )

        # Step 2: View employees
        nav.navigate_to_pim()
        expect(dashboard_page.page).to_have_url(re.compile(r"pim", re.IGNORECASE), timeout=5000)

        # Step 3: Check leave requests
        nav.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=5000)

        # Step 4: Review recruitment
        nav.navigate_to_recruitment()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"recruitment", re.IGNORECASE),
            timeout=5000,
        )

        # Verify all navigations successful
        expect(nav.recruitment_menu).to_be_visible()

    def test_employee_self_service_workflow(self, dashboard_page):
        """
        Test typical employee self-service workflow.

        Workflow:
        1. View dashboard
        2. Update personal info (My Info)
        3. Apply for leave
        4. Submit timesheet
        """
        nav = dashboard_page.nav_header

        # Step 1: Dashboard
        nav.navigate_to_dashboard()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )

        # Step 2: My Info
        nav.navigate_to_my_info()
        dashboard_page.get_current_url().lower()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"(pim|myinfo)", re.IGNORECASE),
            timeout=5000,
        )

        # Step 3: Apply for leave
        nav.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=5000)

        # Step 4: Timesheet
        nav.navigate_to_time()
        expect(dashboard_page.page).to_have_url(re.compile(r"time", re.IGNORECASE), timeout=5000)

        # Verify all navigations successful
        expect(nav.time_menu).to_be_visible()

    def test_admin_configuration_workflow(self, dashboard_page):
        """
        Test admin configuration workflow.

        Workflow:
        1. Access admin panel
        2. Configure system settings
        3. Return to dashboard
        4. Verify changes (navigate to relevant module)
        """
        nav = dashboard_page.nav_header

        # Step 1: Admin panel
        nav.navigate_to_admin()
        expect(dashboard_page.page).to_have_url(re.compile(r"admin", re.IGNORECASE), timeout=5000)

        # Step 2: Access maintenance (system settings)
        nav.navigate_to_maintenance()
        dashboard_page.get_current_url().lower()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"(maintenance|admin)", re.IGNORECASE),
            timeout=5000,
        )

    def test_performance_review_workflow(self, dashboard_page):
        """
        Test performance review workflow.

        Workflow:
        1. View employee in PIM
        2. Check employee performance
        3. Review attendance (Time)
        4. Check leave history
        """
        nav = dashboard_page.nav_header

        # Step 1: View employee
        nav.navigate_to_pim()
        expect(dashboard_page.page).to_have_url(re.compile(r"pim", re.IGNORECASE), timeout=5000)

        # Step 2: Performance review
        nav.navigate_to_performance()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"performance", re.IGNORECASE),
            timeout=5000,
        )

        # Step 3: Check attendance
        nav.navigate_to_time()
        expect(dashboard_page.page).to_have_url(re.compile(r"time", re.IGNORECASE), timeout=5000)

        # Step 4: Leave history
        nav.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=5000)

        # Verify all navigations successful
        expect(nav.leave_menu).to_be_visible()


@pytest.mark.navigation
@pytest.mark.integration
@pytest.mark.cross_module
class TestNavigationConsistency:
    """Test navigation consistency across modules."""

    def test_navigation_header_consistent_across_modules(self, dashboard_page):
        """
        Test that navigation header remains consistent across all modules.

        Verifies that the same navigation options are available regardless
        of which module the user is currently viewing.
        """
        nav = dashboard_page.nav_header
        modules_to_test = [
            ("dashboard", nav.navigate_to_dashboard),
            ("admin", nav.navigate_to_admin),
            ("pim", nav.navigate_to_pim),
            ("leave", nav.navigate_to_leave),
            ("time", nav.navigate_to_time),
        ]

        for expected_path, navigate_method in modules_to_test:
            # Navigate to module
            navigate_method()
            expect(dashboard_page.page).to_have_url(
                re.compile(expected_path, re.IGNORECASE),
                timeout=5000,
            )

            # Verify all main menu items are still visible
            expect(nav.admin_menu).to_be_visible()
            expect(nav.pim_menu).to_be_visible()
            expect(nav.leave_menu).to_be_visible()
            expect(nav.time_menu).to_be_visible()
            expect(nav.dashboard_menu).to_be_visible()

            # Verify user dropdown is still accessible
            expect(nav.user_dropdown).to_be_visible()

    def test_navigation_state_independent(self, dashboard_page):
        """
        Test that navigation doesn't depend on previous navigation state.

        Verifies that each navigation action works independently,
        regardless of navigation history.
        """
        nav = dashboard_page.nav_header

        # Random navigation sequence
        nav.navigate_to_dashboard()
        nav.navigate_to_recruitment()
        nav.navigate_to_admin()
        nav.navigate_to_leave()

        # Each subsequent navigation should work independently
        nav.navigate_to_pim()
        expect(dashboard_page.page).to_have_url(re.compile(r"pim", re.IGNORECASE), timeout=5000)

        nav.navigate_to_time()
        expect(dashboard_page.page).to_have_url(re.compile(r"time", re.IGNORECASE), timeout=5000)

        nav.navigate_to_performance()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"performance", re.IGNORECASE),
            timeout=5000,
        )

        # Verify navigation still functional
        expect(nav.performance_menu).to_be_visible()

    def test_url_changes_reflect_navigation(self, dashboard_page):
        """
        Test that URL changes correctly reflect navigation actions.

        Verifies that each navigation action results in a unique URL
        corresponding to the target module.
        """
        nav = dashboard_page.nav_header
        visited_urls = []

        # Navigate through modules and collect URLs
        modules = [
            (nav.navigate_to_dashboard, "dashboard"),
            (nav.navigate_to_admin, "admin"),
            (nav.navigate_to_pim, "pim"),
            (nav.navigate_to_leave, "leave"),
            (nav.navigate_to_time, "time"),
        ]

        for navigate_method, expected_path in modules:
            navigate_method()
            # Verify URL contains expected path
            expect(dashboard_page.page).to_have_url(
                re.compile(expected_path, re.IGNORECASE),
                timeout=5000,
            )
            # Collect URL for uniqueness check
            visited_urls.append(dashboard_page.get_current_url())

        # Verify all URLs are unique (except possible duplicate for default landing)
        # At least 4 of 5 should be unique
        unique_urls = set(visited_urls)
        if len(unique_urls) < 4:
            raise AssertionError(
                f"Expected at least 4 unique URLs, got {len(unique_urls)}: {unique_urls}",
            )


@pytest.mark.navigation
@pytest.mark.integration
@pytest.mark.cross_module
@pytest.mark.smoke
class TestCrossModuleNavigationSmoke:
    """Smoke tests for critical cross-module navigation workflows."""

    def test_smoke_basic_cross_module_navigation(self, dashboard_page):
        """
        Smoke test: Basic cross-module navigation works.

        Critical test to ensure users can navigate between modules.
        """
        nav = dashboard_page.nav_header

        # Navigate from Leave to Dashboard
        nav.navigate_to_dashboard()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )

        # Navigate to PIM
        nav.navigate_to_pim()
        expect(dashboard_page.page).to_have_url(re.compile(r"pim", re.IGNORECASE), timeout=5000)

        # Navigate back to Leave
        nav.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=5000)

    def test_smoke_navigation_header_persistent(self, dashboard_page):
        """
        Smoke test: Navigation header persists across modules.

        Critical test to ensure navigation header doesn't disappear.
        """
        nav = dashboard_page.nav_header

        # Navigate through multiple modules
        for navigate_method in [
            nav.navigate_to_dashboard,
            nav.navigate_to_admin,
            nav.navigate_to_pim,
            nav.navigate_to_leave,
        ]:
            navigate_method()
            # Verify navigation header still visible
            expect(nav.dashboard_menu).to_be_visible()
            expect(nav.user_dropdown).to_be_visible()

    def test_smoke_round_trip_navigation(self, dashboard_page):
        """
        Smoke test: Round-trip navigation works.

        Critical test to ensure users can navigate away and return.
        """
        nav = dashboard_page.nav_header

        # Navigate away from Leave
        nav.navigate_to_dashboard()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )

        # Navigate back to Leave
        nav.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=5000)

        # Verify navigation still works
        expect(nav.leave_menu).to_be_visible()


@pytest.mark.navigation
@pytest.mark.integration
@pytest.mark.cross_module
@pytest.mark.performance
class TestNavigationPerformance:
    """Test navigation performance and reliability."""

    def test_rapid_sequential_navigation(self, dashboard_page):
        """
        Test rapid sequential navigation doesn't cause errors.

        Verifies that navigating quickly between modules doesn't
        cause race conditions or errors.
        """
        nav = dashboard_page.nav_header

        # Rapid navigation sequence
        nav.navigate_to_dashboard()
        nav.navigate_to_admin()
        nav.navigate_to_pim()
        nav.navigate_to_leave()
        nav.navigate_to_time()
        nav.navigate_to_dashboard()

        # Verify final navigation successful
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )
        expect(nav.dashboard_menu).to_be_visible()

    def test_navigation_after_page_interaction(self, dashboard_page):
        """
        Test navigation works after page interactions.

        Verifies that performing actions on a page doesn't break
        subsequent navigation.
        """
        nav = dashboard_page.nav_header

        # Perform some interaction (open user dropdown)
        nav.open_user_dropdown()
        expect(nav.logout_link).to_be_visible(timeout=5000)

        # Navigate to another module
        nav.navigate_to_dashboard()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )

        # Verify navigation still works
        nav.navigate_to_pim()
        expect(dashboard_page.page).to_have_url(re.compile(r"pim", re.IGNORECASE), timeout=5000)

    def test_navigation_with_page_refresh(self, dashboard_page):
        """
        Test navigation works correctly after page refresh.

        Verifies that refreshing the page doesn't break navigation.
        """
        nav = dashboard_page.nav_header

        # Navigate to Dashboard
        nav.navigate_to_dashboard()
        expect(dashboard_page.page).to_have_url(
            re.compile(r"dashboard", re.IGNORECASE),
            timeout=5000,
        )

        # Refresh page
        dashboard_page.page.reload()

        # Verify navigation header still works after refresh
        expect(nav.dashboard_menu).to_be_visible()

        # Navigate to another module
        nav.navigate_to_leave()
        expect(dashboard_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE), timeout=5000)
