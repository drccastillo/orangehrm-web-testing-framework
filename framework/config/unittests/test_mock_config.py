"""
Unit tests for MockConfig class.
"""
import pytest
from pathlib import Path
from framework.config import MockConfig, ConfigInterface


class TestMockConfig:
    """Test suite for MockConfig class."""

    def test_mock_config_implements_config_interface(self):
        """Test that MockConfig implements ConfigInterface."""
        config = MockConfig()
        assert isinstance(config, ConfigInterface)

    def test_mock_config_default_values(self):
        """Test MockConfig with default values."""
        config = MockConfig()

        assert config.base_url == "http://localhost:8080"
        assert config.username == "test_user"
        assert config.password == "test_password"
        assert config.selenium_grid_url == "http://localhost:4444"
        assert config.default_browser == "chrome"
        assert config.headless is True
        assert config.default_timeout == 10
        assert config.page_load_timeout == 30
        assert config.implicit_wait == 0
        assert config.window_width == 1920
        assert config.window_height == 1080
        assert config.maximize_window is False
        assert config.screenshot_on_failure is False

    def test_mock_config_custom_values(self):
        """Test MockConfig with custom values."""
        config = MockConfig(
            base_url="http://example.com",
            username="custom_user",
            password="custom_pass",
            default_browser="firefox",
            headless=False,
            default_timeout=20,
        )

        assert config.base_url == "http://example.com"
        assert config.username == "custom_user"
        assert config.password == "custom_pass"
        assert config.default_browser == "firefox"
        assert config.headless is False
        assert config.default_timeout == 20

    def test_mock_config_get_selenium_grid_url(self):
        """Test get_selenium_grid_url method."""
        config = MockConfig(selenium_grid_url="http://grid.example.com:4444")
        grid_url = config.get_selenium_grid_url()

        assert grid_url == "http://grid.example.com:4444/wd/hub"

    def test_mock_config_get_selenium_grid_url_with_browser(self):
        """Test get_selenium_grid_url with browser parameter."""
        config = MockConfig()
        grid_url = config.get_selenium_grid_url(browser="firefox")

        assert grid_url == "http://localhost:4444/wd/hub"

    def test_mock_config_validate_success(self):
        """Test validate method with valid configuration."""
        config = MockConfig()
        config.validate()  # Should not raise

    def test_mock_config_validate_missing_base_url(self):
        """Test validate fails when base_url is empty."""
        config = MockConfig(base_url="")

        with pytest.raises(ValueError) as exc_info:
            config.validate()

        assert "base_url is required" in str(exc_info.value)

    def test_mock_config_validate_missing_username(self):
        """Test validate fails when username is empty."""
        config = MockConfig(username="")

        with pytest.raises(ValueError) as exc_info:
            config.validate()

        assert "username is required" in str(exc_info.value)

    def test_mock_config_validate_invalid_timeout(self):
        """Test validate fails when timeout is negative."""
        config = MockConfig(default_timeout=-1)

        with pytest.raises(ValueError) as exc_info:
            config.validate()

        assert "default_timeout must be positive" in str(exc_info.value)

    def test_mock_config_validate_invalid_browser(self):
        """Test validate fails when browser is invalid."""
        config = MockConfig(default_browser="safari")

        with pytest.raises(ValueError) as exc_info:
            config.validate()

        assert "default_browser must be one of" in str(exc_info.value)

    def test_mock_config_directories_properties(self):
        """Test directory properties."""
        config = MockConfig()

        assert isinstance(config.screenshots_dir, Path)
        assert isinstance(config.reports_dir, Path)
        assert isinstance(config.allure_results_dir, Path)
        assert isinstance(config.allure_report_dir, Path)

    def test_mock_config_custom_directories(self):
        """Test MockConfig with custom directories."""
        screenshots = Path("/custom/screenshots")
        reports = Path("/custom/reports")

        config = MockConfig(
            screenshots_dir=screenshots,
            reports_dir=reports,
        )

        assert config.screenshots_dir == screenshots
        assert config.reports_dir == reports

    def test_mock_config_ensure_directories(self, tmp_path):
        """Test ensure_directories creates directories."""
        screenshots = tmp_path / "screenshots"
        reports = tmp_path / "reports"
        allure_results = reports / "allure-results"
        allure_report = reports / "allure-report"

        config = MockConfig(
            screenshots_dir=screenshots,
            reports_dir=reports,
            allure_results_dir=allure_results,
            allure_report_dir=allure_report,
        )

        # Directories shouldn't exist yet
        assert not screenshots.exists()
        assert not reports.exists()

        # Create directories
        config.ensure_directories()

        # Directories should now exist
        assert screenshots.exists()
        assert reports.exists()
        assert allure_results.exists()
        assert allure_report.exists()

    def test_mock_config_for_different_browsers(self):
        """Test creating MockConfig instances for different browsers."""
        chrome_config = MockConfig(default_browser="chrome")
        firefox_config = MockConfig(default_browser="firefox")
        edge_config = MockConfig(default_browser="edge")

        assert chrome_config.default_browser == "chrome"
        assert firefox_config.default_browser == "firefox"
        assert edge_config.default_browser == "edge"

    def test_mock_config_headless_mode(self):
        """Test MockConfig headless mode configurations."""
        headless_config = MockConfig(headless=True)
        headed_config = MockConfig(headless=False)

        assert headless_config.headless is True
        assert headed_config.headless is False
