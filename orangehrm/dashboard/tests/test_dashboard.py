"""
Dashboard page tests using NEW clean architecture.
Tests validate dashboard functionality with Mixins-based page objects.
"""
import pytest
import allure
from orangehrm.dashboard.pages import DashboardPage


@allure.feature("Dashboard")
@allure.story("Dashboard Navigation")
class TestDashboardNavigation:
    """Test dashboard navigation and page loading."""

    @pytest.mark.smoke
    @allure.title("Verify dashboard page loads successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_dashboard_loads(self, dashboard_page: DashboardPage):
        """Test that dashboard page loads after login."""
        assert dashboard_page.is_dashboard_loaded(), "Dashboard should be loaded"

    @pytest.mark.regression
    @allure.title("Verify dashboard URL is correct")
    def test_dashboard_url(self, dashboard_page: DashboardPage):
        """Test that dashboard URL is correct."""
        current_url = dashboard_page.get_current_url()
        assert "dashboard/index" in current_url, f"Expected dashboard URL, got: {current_url}"


@allure.feature("Dashboard")
@allure.story("Dashboard UI Elements")
class TestDashboardUI:
    """Test dashboard UI elements visibility."""

    @pytest.mark.smoke
    @allure.title("Verify dashboard title is visible")
    def test_dashboard_title_visible(self, dashboard_page: DashboardPage):
        """Test that dashboard title is visible."""
        title = dashboard_page.get_dashboard_title()
        assert title == "Dashboard", f"Expected 'Dashboard', got: {title}"

    @pytest.mark.smoke
    @allure.title("Verify user dropdown is visible")
    def test_user_dropdown_visible(self, dashboard_page: DashboardPage):
        """Test that user dropdown is visible."""
        user_name = dashboard_page.get_user_name()
        assert user_name, "User name should be visible in dropdown"

    @pytest.mark.regression
    @allure.title("Verify Quick Launch is visible")
    def test_quick_launch_visible(self, dashboard_page: DashboardPage):
        """Test that Quick Launch section is visible."""
        assert dashboard_page.is_quick_launch_visible(), "Quick Launch should be visible"


@allure.feature("Dashboard")
@allure.story("Dashboard Widgets")
class TestDashboardWidgets:
    """Test dashboard widgets."""

    @pytest.mark.regression
    @allure.title("Verify Time at Work widget is visible")
    def test_time_at_work_widget(self, dashboard_page: DashboardPage):
        """Test that Time at Work widget is visible."""
        assert dashboard_page.is_time_at_work_widget_visible(), "Time at Work widget should be visible"

    @pytest.mark.regression
    @allure.title("Verify My Actions widget is visible")
    def test_my_actions_widget(self, dashboard_page: DashboardPage):
        """Test that My Actions widget is visible."""
        assert dashboard_page.is_my_actions_widget_visible(), "My Actions widget should be visible"

    @pytest.mark.regression
    @allure.title("Verify Quick Launch widget is visible")
    def test_quick_launch_widget(self, dashboard_page: DashboardPage):
        """Test that Quick Launch widget is visible."""
        assert dashboard_page.is_quick_launch_widget_visible(), "Quick Launch widget should be visible"


@allure.feature("Dashboard")
@allure.story("Method Chaining")
class TestDashboardMethodChaining:
    """Test method chaining in dashboard page."""

    @pytest.mark.smoke
    @allure.title("Test method chaining with user dropdown")
    def test_method_chaining(self, dashboard_page: DashboardPage):
        """Test that method chaining works correctly."""
        # This should not raise any errors
        dashboard_page.click_user_dropdown()

        # Verify dropdown is still functional
        assert dashboard_page.is_dashboard_loaded(), "Dashboard should still be loaded after clicking dropdown"
