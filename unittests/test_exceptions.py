"""
Unit tests for custom exception classes.
Tests exception hierarchy and error messages.
"""

import pytest

from utils.exceptions import (
    ConfigurationException,
    ElementNotClickableException,
    ElementNotFoundException,
    FrameworkException,
    InvalidParameterException,
    PageNotLoadedException,
)


class TestFrameworkException:
    """Test suite for FrameworkException base class."""

    def test_framework_exception_is_exception(self):
        """Test that FrameworkException is an Exception."""
        assert issubclass(FrameworkException, Exception)

    def test_framework_exception_can_be_raised(self):
        """Test that FrameworkException can be raised."""
        with pytest.raises(FrameworkException):
            raise FrameworkException("Test error")

    def test_framework_exception_has_message(self):
        """Test that FrameworkException has a message."""
        error = FrameworkException("Test error message")
        assert str(error) == "Test error message"


class TestElementNotFoundException:
    """Test suite for ElementNotFoundException."""

    def test_element_not_found_exception_is_framework_exception(self):
        """Test that ElementNotFoundException is a FrameworkException."""
        assert issubclass(ElementNotFoundException, FrameworkException)

    def test_element_not_found_exception_with_locator(self):
        """Test ElementNotFoundException with locator tuple."""
        locator = ("id", "test-id")
        error = ElementNotFoundException(locator)
        assert "test-id" in str(error)
        assert error.locator == locator

    def test_element_not_found_exception_with_custom_message(self):
        """Test ElementNotFoundException with custom message."""
        locator = ("css", ".test-class")
        custom_msg = "Custom error message"
        error = ElementNotFoundException(locator, custom_msg)
        assert str(error) == custom_msg
        assert error.locator == locator

    def test_element_not_found_exception_default_message(self):
        """Test ElementNotFoundException default message format."""
        locator = ("name", "username")
        error = ElementNotFoundException(locator)
        assert "Element not found" in str(error)
        assert "username" in str(error)


class TestElementNotClickableException:
    """Test suite for ElementNotClickableException."""

    def test_element_not_clickable_exception_is_framework_exception(self):
        """Test that ElementNotClickableException is a FrameworkException."""
        assert issubclass(ElementNotClickableException, FrameworkException)

    def test_element_not_clickable_exception_with_locator(self):
        """Test ElementNotClickableException with locator tuple."""
        locator = ("id", "submit-button")
        error = ElementNotClickableException(locator)
        assert "submit-button" in str(error)
        assert error.locator == locator

    def test_element_not_clickable_exception_default_message(self):
        """Test ElementNotClickableException default message format."""
        locator = ("xpath", "//button[@type='submit']")
        error = ElementNotClickableException(locator)
        assert "not clickable" in str(error)


class TestInvalidParameterException:
    """Test suite for InvalidParameterException."""

    def test_invalid_parameter_exception_is_framework_exception(self):
        """Test that InvalidParameterException is a FrameworkException."""
        assert issubclass(InvalidParameterException, FrameworkException)

    def test_invalid_parameter_exception_with_all_args(self):
        """Test InvalidParameterException with all arguments."""
        error = InvalidParameterException("url", None, "URL cannot be None")
        assert "URL cannot be None" in str(error)
        assert error.parameter_name == "url"
        assert error.value is None

    def test_invalid_parameter_exception_default_message(self):
        """Test InvalidParameterException default message format."""
        error = InvalidParameterException("text", "")
        assert "Invalid parameter" in str(error)
        assert "text" in str(error)


class TestPageNotLoadedException:
    """Test suite for PageNotLoadedException."""

    def test_page_not_loaded_exception_is_framework_exception(self):
        """Test that PageNotLoadedException is a FrameworkException."""
        assert issubclass(PageNotLoadedException, FrameworkException)

    def test_page_not_loaded_exception_with_page_name(self):
        """Test PageNotLoadedException with page name."""
        page_name = "LoginPage"
        error = PageNotLoadedException(page_name)
        assert page_name in str(error)
        assert error.page_name == page_name

    def test_page_not_loaded_exception_default_message(self):
        """Test PageNotLoadedException default message format."""
        page_name = "DashboardPage"
        error = PageNotLoadedException(page_name)
        assert "not load" in str(error).lower()


class TestConfigurationException:
    """Test suite for ConfigurationException."""

    def test_configuration_exception_is_framework_exception(self):
        """Test that ConfigurationException is a FrameworkException."""
        assert issubclass(ConfigurationException, FrameworkException)

    def test_configuration_exception_can_be_raised(self):
        """Test that ConfigurationException can be raised."""
        with pytest.raises(ConfigurationException):
            raise ConfigurationException("Invalid config")

    def test_configuration_exception_has_message(self):
        """Test that ConfigurationException has a message."""
        error = ConfigurationException("BROWSER")
        assert "BROWSER" in str(error)
