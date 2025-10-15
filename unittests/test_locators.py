"""
Unit tests for page locators.
Tests that locators are properly defined and formatted.
"""

import unittest

from selenium.webdriver.common.by import By

from src.pages_selenium.locators.login_locators import LoginLocators


class TestLoginLocators(unittest.TestCase):
    """Test suite for LoginLocators class."""

    def test_username_input_locator_is_tuple(self):
        """Test that USERNAME_INPUT is a tuple."""
        self.assertIsInstance(LoginLocators.USERNAME_INPUT, tuple)

    def test_username_input_locator_has_correct_format(self):
        """Test that USERNAME_INPUT has correct format (By strategy, value)."""
        self.assertEqual(len(LoginLocators.USERNAME_INPUT), 2)
        self.assertEqual(LoginLocators.USERNAME_INPUT[0], By.NAME)
        self.assertIsInstance(LoginLocators.USERNAME_INPUT[1], str)

    def test_password_input_locator_is_tuple(self):
        """Test that PASSWORD_INPUT is a tuple."""
        self.assertIsInstance(LoginLocators.PASSWORD_INPUT, tuple)

    def test_password_input_locator_has_correct_format(self):
        """Test that PASSWORD_INPUT has correct format (By strategy, value)."""
        self.assertEqual(len(LoginLocators.PASSWORD_INPUT), 2)
        self.assertEqual(LoginLocators.PASSWORD_INPUT[0], By.NAME)
        self.assertIsInstance(LoginLocators.PASSWORD_INPUT[1], str)

    def test_login_button_locator_is_tuple(self):
        """Test that LOGIN_BUTTON is a tuple."""
        self.assertIsInstance(LoginLocators.LOGIN_BUTTON, tuple)

    def test_login_button_locator_has_correct_format(self):
        """Test that LOGIN_BUTTON has correct format (By strategy, value)."""
        self.assertEqual(len(LoginLocators.LOGIN_BUTTON), 2)
        self.assertEqual(LoginLocators.LOGIN_BUTTON[0], By.CSS_SELECTOR)
        self.assertIsInstance(LoginLocators.LOGIN_BUTTON[1], str)

    def test_error_message_locator_is_tuple(self):
        """Test that ERROR_MESSAGE is a tuple."""
        self.assertIsInstance(LoginLocators.ERROR_MESSAGE, tuple)

    def test_error_message_locator_has_correct_format(self):
        """Test that ERROR_MESSAGE has correct format (By strategy, value)."""
        self.assertEqual(len(LoginLocators.ERROR_MESSAGE), 2)
        self.assertEqual(LoginLocators.ERROR_MESSAGE[0], By.CSS_SELECTOR)
        self.assertIsInstance(LoginLocators.ERROR_MESSAGE[1], str)

    def test_forgot_password_link_locator_exists(self):
        """Test that FORGOT_PASSWORD_LINK locator exists."""
        self.assertTrue(hasattr(LoginLocators, "FORGOT_PASSWORD_LINK"))
        self.assertIsInstance(LoginLocators.FORGOT_PASSWORD_LINK, tuple)

    def test_login_logo_locator_exists(self):
        """Test that LOGIN_LOGO locator exists."""
        self.assertTrue(hasattr(LoginLocators, "LOGIN_LOGO"))
        self.assertIsInstance(LoginLocators.LOGIN_LOGO, tuple)

    def test_all_locators_use_valid_by_strategies(self):
        """Test that all locators use valid By strategies."""
        valid_strategies = [
            By.ID,
            By.NAME,
            By.CLASS_NAME,
            By.TAG_NAME,
            By.LINK_TEXT,
            By.PARTIAL_LINK_TEXT,
            By.CSS_SELECTOR,
            By.XPATH,
        ]

        locators = [
            LoginLocators.USERNAME_INPUT,
            LoginLocators.PASSWORD_INPUT,
            LoginLocators.LOGIN_BUTTON,
            LoginLocators.ERROR_MESSAGE,
            LoginLocators.FORGOT_PASSWORD_LINK,
            LoginLocators.LOGIN_LOGO,
        ]

        for locator in locators:
            self.assertIn(
                locator[0], valid_strategies, f"Invalid By strategy for locator: {locator}"
            )

    def test_all_locators_have_non_empty_values(self):
        """Test that all locators have non-empty selector values."""
        locators = [
            LoginLocators.USERNAME_INPUT,
            LoginLocators.PASSWORD_INPUT,
            LoginLocators.LOGIN_BUTTON,
            LoginLocators.ERROR_MESSAGE,
            LoginLocators.FORGOT_PASSWORD_LINK,
            LoginLocators.LOGIN_LOGO,
        ]

        for locator in locators:
            self.assertIsNotNone(locator[1], f"Locator value is None: {locator}")
            self.assertGreater(len(locator[1]), 0, f"Locator value is empty: {locator}")


if __name__ == "__main__":
    unittest.main()
