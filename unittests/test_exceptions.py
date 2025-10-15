"""
Unit tests for custom exception classes.
Tests exception hierarchy and error messages.
"""

import unittest

from selenium.webdriver.common.by import By

from utils.exceptions import (
    ConfigurationException,
    ElementNotClickableException,
    ElementNotFoundException,
    FrameworkException,
    InvalidParameterException,
    PageNotLoadedException,
)


class TestFrameworkException(unittest.TestCase):
    """Test suite for FrameworkException base class."""

    def test_framework_exception_is_exception(self):
        """Test that FrameworkException is an Exception."""
        self.assertTrue(issubclass(FrameworkException, Exception))

    def test_framework_exception_can_be_raised(self):
        """Test that FrameworkException can be raised."""
        with self.assertRaises(FrameworkException):
            raise FrameworkException("Test error")

    def test_framework_exception_has_message(self):
        """Test that FrameworkException has a message."""
        error = FrameworkException("Test error message")
        self.assertEqual(str(error), "Test error message")


class TestElementNotFoundException(unittest.TestCase):
    """Test suite for ElementNotFoundException."""

    def test_element_not_found_exception_is_framework_exception(self):
        """Test that ElementNotFoundException is a FrameworkException."""
        self.assertTrue(issubclass(ElementNotFoundException, FrameworkException))

    def test_element_not_found_exception_with_locator(self):
        """Test ElementNotFoundException with locator tuple."""
        locator = (By.ID, "test-id")
        error = ElementNotFoundException(locator)
        self.assertIn("test-id", str(error))
        self.assertEqual(error.locator, locator)

    def test_element_not_found_exception_with_custom_message(self):
        """Test ElementNotFoundException with custom message."""
        locator = (By.CSS_SELECTOR, ".test-class")
        custom_msg = "Custom error message"
        error = ElementNotFoundException(locator, custom_msg)
        self.assertEqual(str(error), custom_msg)
        self.assertEqual(error.locator, locator)

    def test_element_not_found_exception_default_message(self):
        """Test ElementNotFoundException default message format."""
        locator = (By.NAME, "username")
        error = ElementNotFoundException(locator)
        self.assertIn("Element not found", str(error))
        self.assertIn("username", str(error))


class TestElementNotClickableException(unittest.TestCase):
    """Test suite for ElementNotClickableException."""

    def test_element_not_clickable_exception_is_framework_exception(self):
        """Test that ElementNotClickableException is a FrameworkException."""
        self.assertTrue(issubclass(ElementNotClickableException, FrameworkException))

    def test_element_not_clickable_exception_with_locator(self):
        """Test ElementNotClickableException with locator tuple."""
        locator = (By.ID, "submit-button")
        error = ElementNotClickableException(locator)
        self.assertIn("submit-button", str(error))
        self.assertEqual(error.locator, locator)

    def test_element_not_clickable_exception_default_message(self):
        """Test ElementNotClickableException default message format."""
        locator = (By.XPATH, "//button[@type='submit']")
        error = ElementNotClickableException(locator)
        self.assertIn("not clickable", str(error))


class TestInvalidParameterException(unittest.TestCase):
    """Test suite for InvalidParameterException."""

    def test_invalid_parameter_exception_is_framework_exception(self):
        """Test that InvalidParameterException is a FrameworkException."""
        self.assertTrue(issubclass(InvalidParameterException, FrameworkException))

    def test_invalid_parameter_exception_with_all_args(self):
        """Test InvalidParameterException with all arguments."""
        error = InvalidParameterException("url", None, "URL cannot be None")
        self.assertIn("URL cannot be None", str(error))
        self.assertEqual(error.parameter_name, "url")
        self.assertIsNone(error.value)

    def test_invalid_parameter_exception_default_message(self):
        """Test InvalidParameterException default message format."""
        error = InvalidParameterException("text", "")
        self.assertIn("Invalid parameter", str(error))
        self.assertIn("text", str(error))


class TestPageNotLoadedException(unittest.TestCase):
    """Test suite for PageNotLoadedException."""

    def test_page_not_loaded_exception_is_framework_exception(self):
        """Test that PageNotLoadedException is a FrameworkException."""
        self.assertTrue(issubclass(PageNotLoadedException, FrameworkException))

    def test_page_not_loaded_exception_with_page_name(self):
        """Test PageNotLoadedException with page name."""
        page_name = "LoginPage"
        error = PageNotLoadedException(page_name)
        self.assertIn(page_name, str(error))
        self.assertEqual(error.page_name, page_name)

    def test_page_not_loaded_exception_default_message(self):
        """Test PageNotLoadedException default message format."""
        page_name = "DashboardPage"
        error = PageNotLoadedException(page_name)
        self.assertIn("not load", str(error).lower())


class TestConfigurationException(unittest.TestCase):
    """Test suite for ConfigurationException."""

    def test_configuration_exception_is_framework_exception(self):
        """Test that ConfigurationException is a FrameworkException."""
        self.assertTrue(issubclass(ConfigurationException, FrameworkException))

    def test_configuration_exception_can_be_raised(self):
        """Test that ConfigurationException can be raised."""
        with self.assertRaises(ConfigurationException):
            raise ConfigurationException("Invalid config")

    def test_configuration_exception_has_message(self):
        """Test that ConfigurationException has a message."""
        error = ConfigurationException("BROWSER")
        self.assertIn("BROWSER", str(error))


if __name__ == "__main__":
    unittest.main()
