"""
Unit tests for common_actions module.

These tests verify the LOGIC of workflow functions, not the UI interactions.
UI interactions are tested by E2E tests.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from shared.workflows.common_actions import navigate_to_module


@pytest.mark.unit
class TestNavigateToModule:
    """
    Unit tests for navigate_to_module function.

    This function has LOGIC (module mapping, validation, case handling)
    that can fail independently of the UI, so it needs unit tests.
    """

    @patch('shared.workflows.common_actions.OrangeHRMNavigation')
    def test_navigate_to_admin_calls_correct_method(self, mock_nav_class):
        """Verify that 'admin' module calls navigate_to_admin()."""
        # Setup
        driver = Mock()
        mock_nav = Mock()
        mock_nav_class.return_value = mock_nav

        # Execute
        navigate_to_module(driver, 'admin')

        # Verify
        mock_nav_class.assert_called_once_with(driver)
        mock_nav.navigate_to_admin.assert_called_once()

    @patch('shared.workflows.common_actions.OrangeHRMNavigation')
    def test_navigate_to_pim_calls_correct_method(self, mock_nav_class):
        """Verify that 'pim' module calls navigate_to_pim()."""
        driver = Mock()
        mock_nav = Mock()
        mock_nav_class.return_value = mock_nav

        navigate_to_module(driver, 'pim')

        mock_nav.navigate_to_pim.assert_called_once()

    @patch('shared.workflows.common_actions.OrangeHRMNavigation')
    def test_navigate_to_leave_calls_correct_method(self, mock_nav_class):
        """Verify that 'leave' module calls navigate_to_leave()."""
        driver = Mock()
        mock_nav = Mock()
        mock_nav_class.return_value = mock_nav

        navigate_to_module(driver, 'leave')

        mock_nav.navigate_to_leave.assert_called_once()

    @patch('shared.workflows.common_actions.OrangeHRMNavigation')
    def test_navigate_to_time_calls_correct_method(self, mock_nav_class):
        """Verify that 'time' module calls navigate_to_time()."""
        driver = Mock()
        mock_nav = Mock()
        mock_nav_class.return_value = mock_nav

        navigate_to_module(driver, 'time')

        mock_nav.navigate_to_time.assert_called_once()

    @patch('shared.workflows.common_actions.OrangeHRMNavigation')
    def test_navigate_to_recruitment_calls_correct_method(self, mock_nav_class):
        """Verify that 'recruitment' module calls navigate_to_recruitment()."""
        driver = Mock()
        mock_nav = Mock()
        mock_nav_class.return_value = mock_nav

        navigate_to_module(driver, 'recruitment')

        mock_nav.navigate_to_recruitment.assert_called_once()

    @patch('shared.workflows.common_actions.OrangeHRMNavigation')
    def test_navigate_to_dashboard_calls_correct_method(self, mock_nav_class):
        """Verify that 'dashboard' module calls navigate_to_dashboard()."""
        driver = Mock()
        mock_nav = Mock()
        mock_nav_class.return_value = mock_nav

        navigate_to_module(driver, 'dashboard')

        mock_nav.navigate_to_dashboard.assert_called_once()

    @patch('shared.workflows.common_actions.OrangeHRMNavigation')
    def test_navigate_with_uppercase_module_name(self, mock_nav_class):
        """Verify that module names are case-insensitive (uppercase)."""
        driver = Mock()
        mock_nav = Mock()
        mock_nav_class.return_value = mock_nav

        navigate_to_module(driver, 'ADMIN')  # Uppercase

        mock_nav.navigate_to_admin.assert_called_once()

    @patch('shared.workflows.common_actions.OrangeHRMNavigation')
    def test_navigate_with_mixed_case_module_name(self, mock_nav_class):
        """Verify that module names are case-insensitive (mixed case)."""
        driver = Mock()
        mock_nav = Mock()
        mock_nav_class.return_value = mock_nav

        navigate_to_module(driver, 'PiM')  # Mixed case

        mock_nav.navigate_to_pim.assert_called_once()

    def test_navigate_with_invalid_module_raises_value_error(self):
        """Verify that invalid module name raises ValueError."""
        driver = Mock()

        with pytest.raises(ValueError, match="Unknown module: invalid"):
            navigate_to_module(driver, 'invalid')

    def test_navigate_with_empty_string_raises_value_error(self):
        """Verify that empty module name raises ValueError."""
        driver = Mock()

        with pytest.raises(ValueError, match="Unknown module: "):
            navigate_to_module(driver, '')

    def test_navigate_with_typo_raises_value_error(self):
        """Verify that typo in module name raises ValueError."""
        driver = Mock()

        # Common typos
        with pytest.raises(ValueError, match="Unknown module: admon"):
            navigate_to_module(driver, 'admon')  # typo of 'admin'

        with pytest.raises(ValueError, match="Unknown module: tim"):
            navigate_to_module(driver, 'tim')  # typo of 'time'

    @patch('shared.workflows.common_actions.OrangeHRMNavigation')
    def test_navigate_creates_navigation_with_driver(self, mock_nav_class):
        """Verify that OrangeHRMNavigation is initialized with the driver."""
        driver = Mock()
        mock_nav = Mock()
        mock_nav_class.return_value = mock_nav

        navigate_to_module(driver, 'admin')

        # Verify Navigation was created with the correct driver
        mock_nav_class.assert_called_once_with(driver)


# Note: quick_login and quick_logout are simple wrappers without logic
# They don't need unit tests because:
# 1. They just delegate to LoginPage.login() and Navigation.logout()
# 2. E2E tests already validate these workflows
# 3. No business logic to test independently
