"""
Unit tests for WebElement adapters.
Tests that adapters correctly implement WebElementProtocol.
"""

import unittest
from unittest.mock import Mock

from src.adapters.playwright_element import PlaywrightWebElement
from src.adapters.selenium_element import SeleniumWebElement
from src.core.element_protocol import WebElementProtocol


class TestSeleniumWebElement(unittest.TestCase):
    """Test suite for SeleniumWebElement adapter."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_element = Mock()
        self.adapter = SeleniumWebElement(self.mock_element)

    def test_implements_protocol(self):
        """Test that SeleniumWebElement implements WebElementProtocol."""
        self.assertIsInstance(self.adapter, WebElementProtocol)

    def test_click_delegates_to_selenium(self):
        """Test that click() delegates to Selenium's click()."""
        self.adapter.click()
        self.mock_element.click.assert_called_once()

    def test_send_keys_delegates_to_selenium(self):
        """Test that send_keys() delegates to Selenium's send_keys()."""
        test_text = "test input"
        self.adapter.send_keys(test_text)
        self.mock_element.send_keys.assert_called_once_with(test_text)

    def test_clear_delegates_to_selenium(self):
        """Test that clear() delegates to Selenium's clear()."""
        self.adapter.clear()
        self.mock_element.clear.assert_called_once()

    def test_get_text_returns_selenium_text(self):
        """Test that get_text() returns Selenium's .text property."""
        expected_text = "Element text"
        self.mock_element.text = expected_text
        result = self.adapter.get_text()
        self.assertEqual(result, expected_text)

    def test_get_attribute_delegates_to_selenium(self):
        """Test that get_attribute() delegates to Selenium's get_attribute()."""
        attr_name = "class"
        expected_value = "btn-primary"
        self.mock_element.get_attribute.return_value = expected_value

        result = self.adapter.get_attribute(attr_name)

        self.mock_element.get_attribute.assert_called_once_with(attr_name)
        self.assertEqual(result, expected_value)

    def test_get_attribute_returns_none_when_not_exists(self):
        """Test that get_attribute() returns None for non-existent attributes."""
        self.mock_element.get_attribute.return_value = None
        result = self.adapter.get_attribute("nonexistent")
        self.assertIsNone(result)

    def test_is_visible_delegates_to_selenium(self):
        """Test that is_visible() delegates to Selenium's is_displayed()."""
        self.mock_element.is_displayed.return_value = True
        result = self.adapter.is_visible()
        self.mock_element.is_displayed.assert_called_once()
        self.assertTrue(result)

    def test_is_visible_returns_false(self):
        """Test that is_visible() returns False when element is not displayed."""
        self.mock_element.is_displayed.return_value = False
        result = self.adapter.is_visible()
        self.assertFalse(result)

    def test_is_enabled_delegates_to_selenium(self):
        """Test that is_enabled() delegates to Selenium's is_enabled()."""
        self.mock_element.is_enabled.return_value = True
        result = self.adapter.is_enabled()
        self.mock_element.is_enabled.assert_called_once()
        self.assertTrue(result)

    def test_is_enabled_returns_false(self):
        """Test that is_enabled() returns False when element is disabled."""
        self.mock_element.is_enabled.return_value = False
        result = self.adapter.is_enabled()
        self.assertFalse(result)

    def test_is_selected_delegates_to_selenium(self):
        """Test that is_selected() delegates to Selenium's is_selected()."""
        self.mock_element.is_selected.return_value = True
        result = self.adapter.is_selected()
        self.mock_element.is_selected.assert_called_once()
        self.assertTrue(result)

    def test_is_selected_returns_false(self):
        """Test that is_selected() returns False when element is not selected."""
        self.mock_element.is_selected.return_value = False
        result = self.adapter.is_selected()
        self.assertFalse(result)

    def test_repr_contains_wrapped_element(self):
        """Test that __repr__() includes the wrapped element."""
        repr_str = repr(self.adapter)
        self.assertIn("SeleniumWebElement", repr_str)
        self.assertIn(str(self.mock_element), repr_str)


class TestPlaywrightWebElement(unittest.TestCase):
    """Test suite for PlaywrightWebElement adapter."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_locator = Mock()
        self.adapter = PlaywrightWebElement(self.mock_locator)

    def test_implements_protocol(self):
        """Test that PlaywrightWebElement implements WebElementProtocol."""
        self.assertIsInstance(self.adapter, WebElementProtocol)

    def test_click_delegates_to_playwright(self):
        """Test that click() delegates to Playwright's click()."""
        self.adapter.click()
        self.mock_locator.click.assert_called_once()

    def test_send_keys_delegates_to_playwright_fill(self):
        """Test that send_keys() delegates to Playwright's fill()."""
        test_text = "test input"
        self.adapter.send_keys(test_text)
        self.mock_locator.fill.assert_called_once_with(test_text)

    def test_clear_delegates_to_playwright(self):
        """Test that clear() delegates to Playwright's clear()."""
        self.adapter.clear()
        self.mock_locator.clear.assert_called_once()

    def test_get_text_returns_playwright_text_content(self):
        """Test that get_text() returns Playwright's text_content()."""
        expected_text = "Element text"
        self.mock_locator.text_content.return_value = expected_text
        result = self.adapter.get_text()
        self.mock_locator.text_content.assert_called_once()
        self.assertEqual(result, expected_text)

    def test_get_text_returns_empty_string_when_none(self):
        """Test that get_text() returns empty string when text_content is None."""
        self.mock_locator.text_content.return_value = None
        result = self.adapter.get_text()
        self.assertEqual(result, "")

    def test_get_attribute_delegates_to_playwright(self):
        """Test that get_attribute() delegates to Playwright's get_attribute()."""
        attr_name = "class"
        expected_value = "btn-primary"
        self.mock_locator.get_attribute.return_value = expected_value

        result = self.adapter.get_attribute(attr_name)

        self.mock_locator.get_attribute.assert_called_once_with(attr_name)
        self.assertEqual(result, expected_value)

    def test_get_attribute_returns_none_when_not_exists(self):
        """Test that get_attribute() returns None for non-existent attributes."""
        self.mock_locator.get_attribute.return_value = None
        result = self.adapter.get_attribute("nonexistent")
        self.assertIsNone(result)

    def test_is_visible_delegates_to_playwright(self):
        """Test that is_visible() delegates to Playwright's is_visible()."""
        self.mock_locator.is_visible.return_value = True
        result = self.adapter.is_visible()
        self.mock_locator.is_visible.assert_called_once()
        self.assertTrue(result)

    def test_is_visible_returns_false(self):
        """Test that is_visible() returns False when element is not visible."""
        self.mock_locator.is_visible.return_value = False
        result = self.adapter.is_visible()
        self.assertFalse(result)

    def test_is_enabled_delegates_to_playwright(self):
        """Test that is_enabled() delegates to Playwright's is_enabled()."""
        self.mock_locator.is_enabled.return_value = True
        result = self.adapter.is_enabled()
        self.mock_locator.is_enabled.assert_called_once()
        self.assertTrue(result)

    def test_is_enabled_returns_false(self):
        """Test that is_enabled() returns False when element is disabled."""
        self.mock_locator.is_enabled.return_value = False
        result = self.adapter.is_enabled()
        self.assertFalse(result)

    def test_is_selected_delegates_to_playwright_is_checked(self):
        """Test that is_selected() delegates to Playwright's is_checked()."""
        self.mock_locator.is_checked.return_value = True
        result = self.adapter.is_selected()
        self.mock_locator.is_checked.assert_called_once()
        self.assertTrue(result)

    def test_is_selected_returns_false(self):
        """Test that is_selected() returns False when element is not checked."""
        self.mock_locator.is_checked.return_value = False
        result = self.adapter.is_selected()
        self.assertFalse(result)

    def test_repr_contains_wrapped_locator(self):
        """Test that __repr__() includes the wrapped locator."""
        repr_str = repr(self.adapter)
        self.assertIn("PlaywrightWebElement", repr_str)
        self.assertIn(str(self.mock_locator), repr_str)


class TestProtocolCompliance(unittest.TestCase):
    """Test suite for protocol compliance verification."""

    def test_selenium_adapter_has_all_protocol_methods(self):
        """Test that SeleniumWebElement has all WebElementProtocol methods."""
        protocol_methods = [
            "click",
            "send_keys",
            "clear",
            "get_text",
            "get_attribute",
            "is_visible",
            "is_enabled",
            "is_selected",
        ]

        mock_element = Mock()
        adapter = SeleniumWebElement(mock_element)

        for method_name in protocol_methods:
            self.assertTrue(
                hasattr(adapter, method_name),
                f"SeleniumWebElement missing method: {method_name}",
            )
            self.assertTrue(
                callable(getattr(adapter, method_name)),
                f"SeleniumWebElement.{method_name} is not callable",
            )

    def test_playwright_adapter_has_all_protocol_methods(self):
        """Test that PlaywrightWebElement has all WebElementProtocol methods."""
        protocol_methods = [
            "click",
            "send_keys",
            "clear",
            "get_text",
            "get_attribute",
            "is_visible",
            "is_enabled",
            "is_selected",
        ]

        mock_locator = Mock()
        adapter = PlaywrightWebElement(mock_locator)

        for method_name in protocol_methods:
            self.assertTrue(
                hasattr(adapter, method_name),
                f"PlaywrightWebElement missing method: {method_name}",
            )
            self.assertTrue(
                callable(getattr(adapter, method_name)),
                f"PlaywrightWebElement.{method_name} is not callable",
            )


if __name__ == "__main__":
    unittest.main()
