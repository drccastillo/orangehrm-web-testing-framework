"""
Unit tests for Playwright browser adapter and factory.

Tests BrowserProtocol implementation (Playwright adapter)
and BrowserFactory functionality.
"""

from unittest.mock import Mock

import pytest

from src.adapters.playwright_browser import PlaywrightBrowserAdapter
from src.core.browser_protocol import BrowserProtocol
from src.factories.browser_factory import BrowserFactory
from utils.exceptions import InvalidParameterException


class TestPlaywrightBrowserAdapter:
    """Tests for PlaywrightBrowserAdapter."""

    @pytest.fixture
    def mock_page(self):
        """Create a mock Playwright Page."""
        page = Mock()
        page.url = "https://example.com"
        page.title.return_value = "Example Page"
        page.content.return_value = "<html></html>"
        page.context = None  # No context for simple tests
        return page

    @pytest.fixture
    def adapter(self, mock_page):
        """Create PlaywrightBrowserAdapter with mock page."""
        return PlaywrightBrowserAdapter(mock_page, timeout=10)

    def test_implements_browser_protocol(self, adapter):
        """Test that adapter implements BrowserProtocol."""
        assert isinstance(adapter, BrowserProtocol)

    def test_timeout_property(self, adapter):
        """Test timeout getter and setter."""
        assert adapter.timeout == 10

        adapter.timeout = 15
        assert adapter.timeout == 15

    def test_navigate_valid_url(self, adapter, mock_page):
        """Test navigating to a valid URL."""
        adapter.navigate("https://example.com")
        mock_page.goto.assert_called_once_with("https://example.com")

    def test_navigate_invalid_url_raises_exception(self, adapter):
        """Test navigating with invalid URL raises exception."""
        with pytest.raises(InvalidParameterException):
            adapter.navigate("")

        with pytest.raises(InvalidParameterException):
            adapter.navigate(None)

    def test_get_current_url(self, adapter):
        """Test getting current URL."""
        assert adapter.get_current_url() == "https://example.com"

    def test_get_title(self, adapter, mock_page):
        """Test getting page title."""
        assert adapter.get_title() == "Example Page"

    def test_refresh(self, adapter, mock_page):
        """Test page refresh."""
        adapter.refresh()
        mock_page.reload.assert_called_once()

    def test_get_page_source(self, adapter, mock_page):
        """Test getting page source."""
        assert adapter.get_page_source() == "<html></html>"

    def test_execute_script_valid(self, adapter, mock_page):
        """Test executing JavaScript."""
        mock_page.evaluate.return_value = "result"

        result = adapter.execute_script("document.title")
        assert result == "result"
        mock_page.evaluate.assert_called_once()

    def test_execute_script_invalid_raises_exception(self, adapter):
        """Test executing invalid script raises exception."""
        with pytest.raises(InvalidParameterException):
            adapter.execute_script("")

        with pytest.raises(InvalidParameterException):
            adapter.execute_script(None)

    def test_take_screenshot(self, adapter, mock_page):
        """Test taking screenshot."""
        mock_page.screenshot.return_value = b"screenshot_data"

        result = adapter.take_screenshot("test.png")
        assert result == b"screenshot_data"
        mock_page.screenshot.assert_called_once_with(path="test.png")

    def test_quit(self, adapter, mock_page):
        """Test browser quit."""
        adapter.quit()
        mock_page.close.assert_called_once()


class TestBrowserFactory:
    """Tests for BrowserFactory."""

    def test_get_supported_browsers(self):
        """Test getting list of supported browsers."""
        browsers = BrowserFactory.get_supported_browsers()
        assert "chrome" in browsers
        assert "firefox" in browsers
        assert "edge" in browsers

    def test_is_browser_supported(self):
        """Test checking if browser is supported."""
        assert BrowserFactory.is_browser_supported("chrome")
        assert BrowserFactory.is_browser_supported("firefox")
        assert BrowserFactory.is_browser_supported("edge")
        assert not BrowserFactory.is_browser_supported("safari")


class TestBrowserProtocolCompliance:
    """Tests to verify protocol compliance."""

    def test_playwright_adapter_has_all_protocol_methods(self):
        """Test PlaywrightBrowserAdapter has all BrowserProtocol methods."""
        required_methods = [
            "navigate",
            "find_element",
            "find_elements",
            "execute_script",
            "get_current_url",
            "get_title",
            "refresh",
            "take_screenshot",
            "quit",
            "switch_to_frame",
            "switch_to_default_content",
            "get_page_source",
            "timeout",
            "is_element_visible",
            "is_element_hidden",
            "is_element_present",
            "wait_for_element_to_disappear",
            "scroll_to_element",
        ]

        mock_page = Mock()
        mock_page.url = "https://example.com"
        adapter = PlaywrightBrowserAdapter(mock_page)

        for method in required_methods:
            assert hasattr(adapter, method), f"Missing method: {method}"
