"""
Unit tests for Page Object protocols with unified architecture.
Verify that unified implementations satisfy protocol contracts.
"""

import unittest
from unittest.mock import Mock

from src.pages.login_page import LoginPage
from src.pages.protocols import LoginPageProtocol, PageObjectProtocol


class TestUnifiedPageObjectProtocolCompliance(unittest.TestCase):
    """Test that unified page objects implement PageObjectProtocol."""

    def test_unified_login_page_implements_page_object_protocol(self):
        """Test that unified LoginPage implements PageObjectProtocol."""
        mock_browser = Mock()
        page = LoginPage(mock_browser)
        self.assertIsInstance(page, PageObjectProtocol)

    def test_unified_login_page_has_navigate_to(self):
        """Test that unified LoginPage has navigate_to method."""
        mock_browser = Mock()
        page = LoginPage(mock_browser)
        self.assertTrue(hasattr(page, "navigate_to"))
        self.assertTrue(callable(page.navigate_to))

    def test_unified_login_page_has_get_current_url(self):
        """Test that unified LoginPage has get_current_url method."""
        mock_browser = Mock()
        page = LoginPage(mock_browser)
        self.assertTrue(hasattr(page, "get_current_url"))
        self.assertTrue(callable(page.get_current_url))

    def test_unified_login_page_has_is_page_loaded(self):
        """Test that unified LoginPage has is_page_loaded method."""
        mock_browser = Mock()
        page = LoginPage(mock_browser)
        self.assertTrue(hasattr(page, "is_page_loaded"))
        self.assertTrue(callable(page.is_page_loaded))


class TestUnifiedLoginPageProtocolCompliance(unittest.TestCase):
    """Test that unified login page implements LoginPageProtocol."""

    def test_unified_login_page_implements_login_page_protocol(self):
        """Test that unified LoginPage implements LoginPageProtocol."""
        mock_browser = Mock()
        page = LoginPage(mock_browser)
        self.assertIsInstance(page, LoginPageProtocol)

    def test_unified_login_page_has_all_protocol_methods(self):
        """Test that unified LoginPage has all LoginPageProtocol methods."""
        protocol_methods = [
            # PageObjectProtocol methods
            "navigate_to",
            "get_current_url",
            "is_page_loaded",
            # LoginPageProtocol methods
            "enter_username",
            "enter_password",
            "click_login_button",
            "login",
            "get_error_message",
            "is_error_message_displayed",
            "is_login_logo_visible",
        ]

        mock_browser = Mock()
        page = LoginPage(mock_browser)

        for method_name in protocol_methods:
            with self.subTest(method=method_name):
                self.assertTrue(
                    hasattr(page, method_name),
                    f"LoginPage missing method: {method_name}",
                )
                self.assertTrue(
                    callable(getattr(page, method_name)),
                    f"LoginPage.{method_name} is not callable",
                )

    def test_unified_login_page_enter_username_returns_self(self):
        """Test that enter_username returns self for method chaining."""
        mock_browser = Mock()
        page = LoginPage(mock_browser)

        # Configure mock to avoid actual element operations
        mock_element = Mock()
        page.find_element = Mock(return_value=mock_element)

        result = page.enter_username("test")
        self.assertIsInstance(result, LoginPage)

    def test_unified_login_page_enter_password_returns_self(self):
        """Test that enter_password returns self for method chaining."""
        mock_browser = Mock()
        page = LoginPage(mock_browser)

        # Configure mock to avoid actual element operations
        mock_element = Mock()
        page.find_element = Mock(return_value=mock_element)

        result = page.enter_password("test")
        self.assertIsInstance(result, LoginPage)


class TestUnifiedProtocolInheritance(unittest.TestCase):
    """Test that LoginPageProtocol extends PageObjectProtocol."""

    def test_login_page_protocol_extends_page_object_protocol(self):
        """Test that unified LoginPage satisfies both protocols."""
        mock_browser = Mock()
        page = LoginPage(mock_browser)

        # Should be instance of both protocols
        self.assertIsInstance(page, PageObjectProtocol)
        self.assertIsInstance(page, LoginPageProtocol)


if __name__ == "__main__":
    unittest.main()
