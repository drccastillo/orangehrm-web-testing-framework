"""
Unit tests for Page Object protocols.
Verify that concrete implementations satisfy protocol contracts.
"""

import unittest
from unittest.mock import Mock

from src.pages.protocols import LoginPageProtocol, PageObjectProtocol
from src.pages_playwright.login_page_pw import LoginPagePW
from src.pages_selenium.login_page import LoginPage


class TestPageObjectProtocolCompliance(unittest.TestCase):
    """Test that page objects implement PageObjectProtocol."""

    def test_selenium_login_page_implements_page_object_protocol(self):
        """Test that Selenium LoginPage implements PageObjectProtocol."""
        mock_driver = Mock()
        page = LoginPage(mock_driver)
        self.assertIsInstance(page, PageObjectProtocol)

    def test_playwright_login_page_implements_page_object_protocol(self):
        """Test that Playwright LoginPagePW implements PageObjectProtocol."""
        mock_page = Mock()
        page = LoginPagePW(mock_page)
        self.assertIsInstance(page, PageObjectProtocol)

    def test_selenium_login_page_has_navigate_to(self):
        """Test that Selenium LoginPage has navigate_to method."""
        mock_driver = Mock()
        page = LoginPage(mock_driver)
        self.assertTrue(hasattr(page, "navigate_to"))
        self.assertTrue(callable(page.navigate_to))

    def test_playwright_login_page_has_navigate_to(self):
        """Test that Playwright LoginPagePW has navigate_to method."""
        mock_page = Mock()
        page = LoginPagePW(mock_page)
        self.assertTrue(hasattr(page, "navigate_to"))
        self.assertTrue(callable(page.navigate_to))

    def test_selenium_login_page_has_get_current_url(self):
        """Test that Selenium LoginPage has get_current_url method."""
        mock_driver = Mock()
        page = LoginPage(mock_driver)
        self.assertTrue(hasattr(page, "get_current_url"))
        self.assertTrue(callable(page.get_current_url))

    def test_playwright_login_page_has_get_current_url(self):
        """Test that Playwright LoginPagePW has get_current_url method."""
        mock_page = Mock()
        page = LoginPagePW(mock_page)
        self.assertTrue(hasattr(page, "get_current_url"))
        self.assertTrue(callable(page.get_current_url))

    def test_selenium_login_page_has_is_page_loaded(self):
        """Test that Selenium LoginPage has is_page_loaded method."""
        mock_driver = Mock()
        page = LoginPage(mock_driver)
        self.assertTrue(hasattr(page, "is_page_loaded"))
        self.assertTrue(callable(page.is_page_loaded))

    def test_playwright_login_page_has_is_page_loaded(self):
        """Test that Playwright LoginPagePW has is_page_loaded method."""
        mock_page = Mock()
        page = LoginPagePW(mock_page)
        self.assertTrue(hasattr(page, "is_page_loaded"))
        self.assertTrue(callable(page.is_page_loaded))


class TestLoginPageProtocolCompliance(unittest.TestCase):
    """Test that login pages implement LoginPageProtocol."""

    def test_selenium_login_page_implements_login_page_protocol(self):
        """Test that Selenium LoginPage implements LoginPageProtocol."""
        mock_driver = Mock()
        page = LoginPage(mock_driver)
        self.assertIsInstance(page, LoginPageProtocol)

    def test_playwright_login_page_implements_login_page_protocol(self):
        """Test that Playwright LoginPagePW implements LoginPageProtocol."""
        mock_page = Mock()
        page = LoginPagePW(mock_page)
        self.assertIsInstance(page, LoginPageProtocol)

    def test_selenium_login_page_has_all_protocol_methods(self):
        """Test that Selenium LoginPage has all LoginPageProtocol methods."""
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
            "is_forgot_password_link_visible",
            "is_login_logo_visible",
        ]

        mock_driver = Mock()
        page = LoginPage(mock_driver)

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

    def test_playwright_login_page_has_all_protocol_methods(self):
        """Test that Playwright LoginPagePW has all LoginPageProtocol methods."""
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
            "is_forgot_password_link_visible",
            "is_login_logo_visible",
        ]

        mock_page = Mock()
        page = LoginPagePW(mock_page)

        for method_name in protocol_methods:
            with self.subTest(method=method_name):
                self.assertTrue(
                    hasattr(page, method_name),
                    f"LoginPagePW missing method: {method_name}",
                )
                self.assertTrue(
                    callable(getattr(page, method_name)),
                    f"LoginPagePW.{method_name} is not callable",
                )

    def test_selenium_login_page_enter_username_returns_self(self):
        """Test that enter_username returns self for chaining."""
        mock_driver = Mock()
        mock_driver.find_element = Mock(return_value=Mock())
        page = LoginPage(mock_driver)

        # Configure mock to avoid actual element operations
        page.find_element = Mock(return_value=Mock())

        result = page.enter_username("test")
        self.assertIsInstance(result, LoginPage)

    def test_playwright_login_page_enter_username_returns_self(self):
        """Test that enter_username returns self for chaining."""
        mock_page = Mock()
        page = LoginPagePW(mock_page)

        # Configure mock
        mock_page.locator = Mock(return_value=Mock())

        result = page.enter_username("test")
        self.assertIsInstance(result, LoginPagePW)

    def test_selenium_login_page_enter_password_returns_self(self):
        """Test that enter_password returns self for chaining."""
        mock_driver = Mock()
        mock_driver.find_element = Mock(return_value=Mock())
        page = LoginPage(mock_driver)

        # Configure mock
        page.find_element = Mock(return_value=Mock())

        result = page.enter_password("test")
        self.assertIsInstance(result, LoginPage)

    def test_playwright_login_page_enter_password_returns_self(self):
        """Test that enter_password returns self for chaining."""
        mock_page = Mock()
        page = LoginPagePW(mock_page)

        # Configure mock
        mock_page.locator = Mock(return_value=Mock())

        result = page.enter_password("test")
        self.assertIsInstance(result, LoginPagePW)


class TestProtocolInheritance(unittest.TestCase):
    """Test that LoginPageProtocol extends PageObjectProtocol."""

    def test_login_page_protocol_extends_page_object_protocol(self):
        """Test that LoginPageProtocol implementations also satisfy PageObjectProtocol."""
        mock_driver = Mock()
        selenium_page = LoginPage(mock_driver)

        # Should be instance of both protocols
        self.assertIsInstance(selenium_page, PageObjectProtocol)
        self.assertIsInstance(selenium_page, LoginPageProtocol)

        mock_page = Mock()
        playwright_page = LoginPagePW(mock_page)

        # Should be instance of both protocols
        self.assertIsInstance(playwright_page, PageObjectProtocol)
        self.assertIsInstance(playwright_page, LoginPageProtocol)


if __name__ == "__main__":
    unittest.main()
