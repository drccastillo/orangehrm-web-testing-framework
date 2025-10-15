"""
Unit tests for Leave Page protocols with unified architecture.
Verify that unified implementations satisfy protocol contracts.
"""

import unittest
from unittest.mock import Mock

from src.pages.leave_page import LeavePage
from src.pages.protocols import LeavePageProtocol, PageObjectProtocol


class TestUnifiedLeavePageProtocolCompliance(unittest.TestCase):
    """Test that unified leave page implements LeavePageProtocol."""

    def test_unified_leave_page_implements_page_object_protocol(self):
        """Test that unified LeavePage implements PageObjectProtocol."""
        mock_browser = Mock()
        page = LeavePage(mock_browser)
        self.assertIsInstance(page, PageObjectProtocol)

    def test_unified_leave_page_implements_leave_page_protocol(self):
        """Test that unified LeavePage implements LeavePageProtocol."""
        mock_browser = Mock()
        page = LeavePage(mock_browser)
        self.assertIsInstance(page, LeavePageProtocol)

    def test_unified_leave_page_has_navigate_to(self):
        """Test that unified LeavePage has navigate_to method."""
        mock_browser = Mock()
        page = LeavePage(mock_browser)
        self.assertTrue(hasattr(page, "navigate_to"))
        self.assertTrue(callable(page.navigate_to))

    def test_unified_leave_page_has_get_current_url(self):
        """Test that unified LeavePage has get_current_url method."""
        mock_browser = Mock()
        page = LeavePage(mock_browser)
        self.assertTrue(hasattr(page, "get_current_url"))
        self.assertTrue(callable(page.get_current_url))

    def test_unified_leave_page_has_is_page_loaded(self):
        """Test that unified LeavePage has is_page_loaded method."""
        mock_browser = Mock()
        page = LeavePage(mock_browser)
        self.assertTrue(hasattr(page, "is_page_loaded"))
        self.assertTrue(callable(page.is_page_loaded))


class TestUnifiedLeavePageMethods(unittest.TestCase):
    """Test that unified leave page has all LeavePageProtocol methods."""

    def test_unified_leave_page_has_all_protocol_methods(self):
        """Test that unified LeavePage has all LeavePageProtocol methods."""
        protocol_methods = [
            # PageObjectProtocol methods
            "navigate_to",
            "get_current_url",
            "is_page_loaded",
            # LeavePageProtocol methods
            "navigate_to_apply_leave",
            "navigate_to_leave_list",
            "navigate_to_my_leave",
            "is_apply_button_visible",
            "is_leave_list_button_visible",
            "apply_leave",
            "search_leave",
            "get_leave_count",
            "is_success_message_displayed",
            "is_no_records_message_displayed",
        ]

        mock_browser = Mock()
        page = LeavePage(mock_browser)

        for method_name in protocol_methods:
            with self.subTest(method=method_name):
                self.assertTrue(
                    hasattr(page, method_name),
                    f"LeavePage missing method: {method_name}",
                )
                self.assertTrue(
                    callable(getattr(page, method_name)),
                    f"LeavePage.{method_name} is not callable",
                )


class TestUnifiedProtocolInheritance(unittest.TestCase):
    """Test that LeavePageProtocol extends PageObjectProtocol."""

    def test_leave_page_protocol_extends_page_object_protocol(self):
        """Test that unified LeavePage satisfies both protocols."""
        mock_browser = Mock()
        page = LeavePage(mock_browser)

        # Should be instance of both protocols
        self.assertIsInstance(page, PageObjectProtocol)
        self.assertIsInstance(page, LeavePageProtocol)


if __name__ == "__main__":
    unittest.main()
