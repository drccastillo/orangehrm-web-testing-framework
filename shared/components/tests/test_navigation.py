"""
Unit tests for OrangeHRMNavigation.navigate_to_module() method.

These tests verify the LOGIC of navigate_to_module(), not the UI interactions.
UI interactions are tested by E2E tests.

Migrated from: shared/workflows/unittests/test_common_actions.py
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from shared.components.navigation import OrangeHRMNavigation


@pytest.mark.unit
class TestNavigateToModule:
    """
    Unit tests for OrangeHRMNavigation.navigate_to_module() method.

    This method has LOGIC (module mapping, validation, case handling)
    that can fail independently of the UI, so it needs unit tests.
    """

    def test_navigate_to_admin_calls_correct_method(self):
        """Verify that 'admin' module calls navigate_to_admin()."""
        # Setup
        driver = Mock()
        nav = OrangeHRMNavigation(driver)
        nav.navigate_to_admin = Mock(return_value=nav)

        # Execute
        result = nav.navigate_to_module('admin')

        # Verify
        nav.navigate_to_admin.assert_called_once()
        assert result is nav  # Method chaining

    def test_navigate_to_pim_calls_correct_method(self):
        """Verify that 'pim' module calls navigate_to_pim()."""
        driver = Mock()
        nav = OrangeHRMNavigation(driver)
        nav.navigate_to_pim = Mock(return_value=nav)

        result = nav.navigate_to_module('pim')

        nav.navigate_to_pim.assert_called_once()
        assert result is nav

    def test_navigate_to_leave_calls_correct_method(self):
        """Verify that 'leave' module calls navigate_to_leave()."""
        driver = Mock()
        nav = OrangeHRMNavigation(driver)
        nav.navigate_to_leave = Mock(return_value=nav)

        result = nav.navigate_to_module('leave')

        nav.navigate_to_leave.assert_called_once()
        assert result is nav

    def test_navigate_to_time_calls_correct_method(self):
        """Verify that 'time' module calls navigate_to_time()."""
        driver = Mock()
        nav = OrangeHRMNavigation(driver)
        nav.navigate_to_time = Mock(return_value=nav)

        result = nav.navigate_to_module('time')

        nav.navigate_to_time.assert_called_once()
        assert result is nav

    def test_navigate_to_recruitment_calls_correct_method(self):
        """Verify that 'recruitment' module calls navigate_to_recruitment()."""
        driver = Mock()
        nav = OrangeHRMNavigation(driver)
        nav.navigate_to_recruitment = Mock(return_value=nav)

        result = nav.navigate_to_module('recruitment')

        nav.navigate_to_recruitment.assert_called_once()
        assert result is nav

    def test_navigate_to_dashboard_calls_correct_method(self):
        """Verify that 'dashboard' module calls navigate_to_dashboard()."""
        driver = Mock()
        nav = OrangeHRMNavigation(driver)
        nav.navigate_to_dashboard = Mock(return_value=nav)

        result = nav.navigate_to_module('dashboard')

        nav.navigate_to_dashboard.assert_called_once()
        assert result is nav

    def test_navigate_with_uppercase_module_name(self):
        """Verify that module names are case-insensitive (uppercase)."""
        driver = Mock()
        nav = OrangeHRMNavigation(driver)
        nav.navigate_to_admin = Mock(return_value=nav)

        nav.navigate_to_module('ADMIN')  # Uppercase

        nav.navigate_to_admin.assert_called_once()

    def test_navigate_with_mixed_case_module_name(self):
        """Verify that module names are case-insensitive (mixed case)."""
        driver = Mock()
        nav = OrangeHRMNavigation(driver)
        nav.navigate_to_pim = Mock(return_value=nav)

        nav.navigate_to_module('PiM')  # Mixed case

        nav.navigate_to_pim.assert_called_once()

    def test_navigate_with_invalid_module_raises_value_error(self):
        """Verify that invalid module name raises ValueError."""
        driver = Mock()
        nav = OrangeHRMNavigation(driver)

        with pytest.raises(ValueError, match="Unknown module: invalid"):
            nav.navigate_to_module('invalid')

    def test_navigate_with_empty_string_raises_value_error(self):
        """Verify that empty module name raises ValueError."""
        driver = Mock()
        nav = OrangeHRMNavigation(driver)

        with pytest.raises(ValueError, match="Unknown module: "):
            nav.navigate_to_module('')

    def test_navigate_with_typo_raises_value_error(self):
        """Verify that typo in module name raises ValueError."""
        driver = Mock()
        nav = OrangeHRMNavigation(driver)

        # Common typos
        with pytest.raises(ValueError, match="Unknown module: admon"):
            nav.navigate_to_module('admon')  # typo of 'admin'

        with pytest.raises(ValueError, match="Unknown module: tim"):
            nav.navigate_to_module('tim')  # typo of 'time'

    def test_navigate_method_chaining(self):
        """Verify that navigate_to_module() supports method chaining."""
        driver = Mock()
        nav = OrangeHRMNavigation(driver)
        nav.navigate_to_admin = Mock(return_value=nav)
        nav.logout = Mock()

        # Method chaining
        nav.navigate_to_module('admin').logout()

        nav.navigate_to_admin.assert_called_once()
        nav.logout.assert_called_once()

    def test_navigate_returns_self_for_chaining(self):
        """Verify that navigate_to_module() returns self."""
        driver = Mock()
        nav = OrangeHRMNavigation(driver)
        nav.navigate_to_dashboard = Mock(return_value=nav)

        result = nav.navigate_to_module('dashboard')

        assert result is nav


@pytest.mark.parametrize("module_name,expected_method", [
    ('admin', 'navigate_to_admin'),
    ('pim', 'navigate_to_pim'),
    ('leave', 'navigate_to_leave'),
    ('time', 'navigate_to_time'),
    ('recruitment', 'navigate_to_recruitment'),
    ('dashboard', 'navigate_to_dashboard'),
])
def test_navigate_to_module_parametrized(module_name, expected_method):
    """Parametrized test for all valid modules."""
    driver = Mock()
    nav = OrangeHRMNavigation(driver)

    # Mock the expected method
    setattr(nav, expected_method, Mock(return_value=nav))

    # Execute
    nav.navigate_to_module(module_name)

    # Verify the correct method was called
    getattr(nav, expected_method).assert_called_once()
