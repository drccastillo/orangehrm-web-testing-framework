"""
Unit tests for EnvironmentConfigService.
Validates that the new implementation fulfills the ConfigService protocol
and maintains behavior parity with the original Config class.
"""

from pathlib import Path

import pytest

from src.config.environment_config import EnvironmentConfigService
from src.config.protocols import ConfigService


class TestEnvironmentConfigServiceContract:
    """Test that EnvironmentConfigService implements ConfigService protocol."""

    @pytest.fixture
    def config(self) -> ConfigService:
        """Create config service instance."""
        return EnvironmentConfigService()

    def test_implements_config_service_protocol(self, config):
        """EnvironmentConfigService implements ConfigService protocol."""
        assert isinstance(config, ConfigService)

    def test_has_base_url_property(self, config):
        """Provides base_url property."""
        assert hasattr(config, "base_url")
        url = config.base_url
        assert isinstance(url, str)
        assert len(url) > 0

    def test_has_username_property(self, config):
        """Provides username property."""
        assert hasattr(config, "username")
        assert isinstance(config.username, str)

    def test_has_password_property(self, config):
        """Provides password property."""
        assert hasattr(config, "password")
        assert isinstance(config.password, str)


    def test_has_browser_configuration(self, config):
        """Provides browser configuration properties."""
        assert hasattr(config, "default_browser")
        assert isinstance(config.default_browser, str)

        assert hasattr(config, "headless")
        assert isinstance(config.headless, bool)

    def test_has_timeout_configuration(self, config):
        """Provides timeout configuration properties."""
        assert hasattr(config, "default_timeout")
        assert isinstance(config.default_timeout, int)
        assert config.default_timeout > 0

        assert hasattr(config, "page_load_timeout")
        assert isinstance(config.page_load_timeout, int)

    def test_has_window_configuration(self, config):
        """Provides window configuration properties."""
        assert hasattr(config, "window_width")
        assert isinstance(config.window_width, int)

        assert hasattr(config, "window_height")
        assert isinstance(config.window_height, int)

        assert hasattr(config, "maximize_window")
        assert isinstance(config.maximize_window, bool)

    def test_has_screenshot_configuration(self, config):
        """Provides screenshot configuration properties."""
        assert hasattr(config, "screenshot_on_failure")
        assert isinstance(config.screenshot_on_failure, bool)

        assert hasattr(config, "screenshots_dir")
        assert isinstance(config.screenshots_dir, Path)

    def test_has_reports_directory(self, config):
        """Provides reports directory property."""
        assert hasattr(config, "reports_dir")
        assert isinstance(config.reports_dir, Path)


    def test_has_ensure_directories_method(self, config):
        """Provides ensure_directories method."""
        assert hasattr(config, "ensure_directories")
        assert callable(config.ensure_directories)

        # Should not raise exception
        config.ensure_directories()


class TestEnvironmentConfigServiceBehavior:
    """Test EnvironmentConfigService behavior matches Config class."""

    @pytest.fixture
    def config(self) -> EnvironmentConfigService:
        """Create config service instance."""
        return EnvironmentConfigService()

    def test_loads_from_environment_variables(self, monkeypatch):
        """Config loads values from environment variables."""
        # Set custom environment
        monkeypatch.setenv("URL", "http://test-url.com")
        monkeypatch.setenv("ORANGEHRM_USERNAME", "TestUser")
        monkeypatch.setenv("ORANGEHRM_PASSWORD", "TestPass")
        monkeypatch.setenv("BROWSER", "firefox")
        monkeypatch.setenv("HEADLESS", "true")

        # Create new config (will read new env vars)
        config = EnvironmentConfigService()

        # Verify values loaded
        assert config.base_url == "http://test-url.com"
        assert config.username == "TestUser"
        assert config.password == "TestPass"
        assert config.default_browser == "firefox"
        assert config.headless is True

    def test_provides_defaults_when_env_not_set(self, monkeypatch):
        """Config provides sensible defaults when env vars not set."""
        # Clear environment
        monkeypatch.delenv("URL", raising=False)
        monkeypatch.delenv("BROWSER", raising=False)
        monkeypatch.delenv("DEFAULT_TIMEOUT", raising=False)

        config = EnvironmentConfigService()

        # Should have defaults
        assert "http" in config.base_url
        assert config.default_browser in ["chrome", "firefox", "edge"]
        assert config.default_timeout == 10

    def test_parses_boolean_strings_correctly(self, monkeypatch):
        """Config correctly parses boolean string values."""
        # Test "true"
        monkeypatch.setenv("HEADLESS", "true")
        config = EnvironmentConfigService()
        assert config.headless is True

        # Test "false"
        monkeypatch.setenv("HEADLESS", "false")
        config = EnvironmentConfigService()
        assert config.headless is False

        # Test "True" (capital)
        monkeypatch.setenv("MAXIMIZE_WINDOW", "True")
        config = EnvironmentConfigService()
        assert config.maximize_window is True

    def test_parses_integer_strings_correctly(self, monkeypatch):
        """Config correctly parses integer string values."""
        monkeypatch.setenv("DEFAULT_TIMEOUT", "20")
        monkeypatch.setenv("WINDOW_WIDTH", "1280")

        config = EnvironmentConfigService()

        assert config.default_timeout == 20
        assert config.window_width == 1280


    def test_ensure_directories_creates_paths(self, tmp_path, monkeypatch):
        """ensure_directories creates screenshots and reports directories."""
        # Create config with temporary paths
        monkeypatch.setenv("URL", "http://localhost")
        config = EnvironmentConfigService()

        # Override paths to use tmp_path
        test_screenshots = tmp_path / "screenshots"
        test_reports = tmp_path / "reports"
        config._screenshots_dir = test_screenshots
        config._reports_dir = test_reports

        # Ensure directories don't exist yet
        assert not test_screenshots.exists()
        assert not test_reports.exists()

        # Call ensure_directories
        config.ensure_directories()

        # Verify directories created
        assert test_screenshots.exists()
        assert test_screenshots.is_dir()
        assert test_reports.exists()
        assert test_reports.is_dir()

    def test_config_is_not_singleton(self):
        """Multiple config instances can be created (not Singleton)."""
        config1 = EnvironmentConfigService()
        config2 = EnvironmentConfigService()

        # Different instances
        assert config1 is not config2

        # But same values
        assert config1.base_url == config2.base_url

    def test_config_repr_is_informative(self, config):
        """String representation contains useful info."""
        repr_str = repr(config)
        assert "EnvironmentConfigService" in repr_str
        assert "base_url" in repr_str
        assert "browser" in repr_str


class TestEnvironmentConfigServiceCustomEnvFile:
    """Test custom .env file loading."""

    def test_can_load_from_custom_env_file(self, tmp_path):
        """Config can load from custom .env file path."""
        # Create custom .env file
        custom_env = tmp_path / "custom.env"
        custom_env.write_text(
            "URL=http://custom-environment.com\n"
            "ORANGEHRM_USERNAME=CustomUser\n"
            "ORANGEHRM_PASSWORD=CustomPass\n"
        )

        # Create config with custom path
        config = EnvironmentConfigService(env_path=custom_env)

        # Verify custom values loaded
        assert config.base_url == "http://custom-environment.com"
        assert config.username == "CustomUser"
        assert config.password == "CustomPass"


class TestEnvironmentConfigServiceValidation:
    """Test configuration validation."""

    @pytest.fixture
    def config(self) -> EnvironmentConfigService:
        """Create config service instance."""
        return EnvironmentConfigService()

    def test_timeout_values_are_positive(self, config):
        """All timeout values are positive."""
        assert config.default_timeout > 0
        assert config.page_load_timeout > 0

    def test_window_dimensions_are_positive(self, config):
        """Window dimensions are positive."""
        assert config.window_width > 0
        assert config.window_height > 0

    def test_browser_is_supported(self, config):
        """Browser is one of supported values."""
        assert config.default_browser in ["chrome", "firefox", "edge", "webkit"]

    def test_paths_are_absolute(self, config):
        """Directory paths are absolute."""
        assert config.screenshots_dir.is_absolute()
        assert config.reports_dir.is_absolute()
