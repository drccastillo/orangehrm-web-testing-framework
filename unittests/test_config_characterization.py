"""
Characterization tests for Config class.
These tests lock down current behavior before refactoring to ConfigService.

Purpose: Ensure Config behavior remains unchanged during Singleton → DI refactor.
"""

from pathlib import Path

import pytest

from src.config.config import Config


class TestConfigCharacterization:
    """
    Characterization tests to capture current Config behavior.
    These tests document how Config currently works.
    """

    def test_config_has_base_url(self):
        """Config provides BASE_URL attribute."""
        assert hasattr(Config, "BASE_URL")
        assert isinstance(Config.BASE_URL, str)
        assert len(Config.BASE_URL) > 0

    def test_config_has_username(self):
        """Config provides USERNAME attribute."""
        assert hasattr(Config, "USERNAME")
        assert isinstance(Config.USERNAME, str)

    def test_config_has_password(self):
        """Config provides PASSWORD attribute."""
        assert hasattr(Config, "PASSWORD")
        assert isinstance(Config.PASSWORD, str)

    def test_config_has_selenium_grid_url(self):
        """Config provides SELENIUM_GRID_URL attribute."""
        assert hasattr(Config, "SELENIUM_GRID_URL")
        assert isinstance(Config.SELENIUM_GRID_URL, str)

    def test_config_has_default_browser(self):
        """Config provides DEFAULT_BROWSER attribute."""
        assert hasattr(Config, "DEFAULT_BROWSER")
        assert isinstance(Config.DEFAULT_BROWSER, str)

    def test_config_has_headless_mode(self):
        """Config provides HEADLESS attribute."""
        assert hasattr(Config, "HEADLESS")
        assert isinstance(Config.HEADLESS, bool)

    def test_config_has_timeout_settings(self):
        """Config provides timeout settings."""
        assert hasattr(Config, "DEFAULT_TIMEOUT")
        assert isinstance(Config.DEFAULT_TIMEOUT, int)
        assert Config.DEFAULT_TIMEOUT > 0

        assert hasattr(Config, "PAGE_LOAD_TIMEOUT")
        assert isinstance(Config.PAGE_LOAD_TIMEOUT, int)
        assert Config.PAGE_LOAD_TIMEOUT > 0

        assert hasattr(Config, "IMPLICIT_WAIT")
        assert isinstance(Config.IMPLICIT_WAIT, int)
        assert Config.IMPLICIT_WAIT >= 0

    def test_config_has_window_settings(self):
        """Config provides window configuration."""
        assert hasattr(Config, "WINDOW_WIDTH")
        assert isinstance(Config.WINDOW_WIDTH, int)
        assert Config.WINDOW_WIDTH > 0

        assert hasattr(Config, "WINDOW_HEIGHT")
        assert isinstance(Config.WINDOW_HEIGHT, int)
        assert Config.WINDOW_HEIGHT > 0

        assert hasattr(Config, "MAXIMIZE_WINDOW")
        assert isinstance(Config.MAXIMIZE_WINDOW, bool)

    def test_config_has_screenshot_settings(self):
        """Config provides screenshot configuration."""
        assert hasattr(Config, "SCREENSHOT_ON_FAILURE")
        assert isinstance(Config.SCREENSHOT_ON_FAILURE, bool)

        assert hasattr(Config, "SCREENSHOTS_DIR")
        assert isinstance(Config.SCREENSHOTS_DIR, Path)

    def test_config_has_reports_directory(self):
        """Config provides reports directory."""
        assert hasattr(Config, "REPORTS_DIR")
        assert isinstance(Config.REPORTS_DIR, Path)

    def test_get_selenium_grid_url_returns_string(self):
        """get_selenium_grid_url() returns properly formatted URL."""
        url = Config.get_selenium_grid_url()
        assert isinstance(url, str)
        assert url.endswith("/wd/hub")
        assert "http" in url

    def test_get_selenium_grid_url_with_browser_parameter(self):
        """get_selenium_grid_url() accepts browser parameter (though not currently used)."""
        url = Config.get_selenium_grid_url(browser="chrome")
        assert isinstance(url, str)
        assert url.endswith("/wd/hub")

    def test_ensure_directories_creates_paths(self, tmp_path, monkeypatch):
        """ensure_directories() creates necessary directories."""
        # Use temporary directory for test
        test_screenshots = tmp_path / "screenshots"
        test_reports = tmp_path / "reports"

        # Monkey-patch Config paths
        monkeypatch.setattr(Config, "SCREENSHOTS_DIR", test_screenshots)
        monkeypatch.setattr(Config, "REPORTS_DIR", test_reports)

        # Call ensure_directories
        Config.ensure_directories()

        # Verify directories were created
        assert test_screenshots.exists()
        assert test_screenshots.is_dir()
        assert test_reports.exists()
        assert test_reports.is_dir()

    def test_config_loads_from_environment(self, monkeypatch):
        """Config reads from environment variables."""
        # Set custom environment variable
        monkeypatch.setenv("URL", "http://custom-url.com")
        monkeypatch.setenv("ORANGEHRM_USERNAME", "TestUser")
        monkeypatch.setenv("ORANGEHRM_PASSWORD", "TestPass123")

        # Reload config module to pick up new env vars
        import importlib

        from src.config import config as config_module

        importlib.reload(config_module)

        # Verify Config loaded new values
        assert config_module.Config.BASE_URL == "http://custom-url.com"
        assert config_module.Config.USERNAME == "TestUser"
        assert config_module.Config.PASSWORD == "TestPass123"

    def test_config_uses_defaults_when_env_not_set(self, monkeypatch):
        """Config provides sensible defaults when env vars not set."""
        # Remove environment variables
        monkeypatch.delenv("URL", raising=False)
        monkeypatch.delenv("BROWSER", raising=False)
        monkeypatch.delenv("HEADLESS", raising=False)

        # Reload config
        import importlib

        from src.config import config as config_module

        importlib.reload(config_module)

        # Verify defaults are used
        assert "http" in config_module.Config.BASE_URL
        assert config_module.Config.DEFAULT_BROWSER in ["chrome", "firefox", "edge"]
        assert isinstance(config_module.Config.HEADLESS, bool)

    def test_config_parses_boolean_from_string(self, monkeypatch):
        """Config correctly parses boolean values from string env vars."""
        # Test "true" string
        monkeypatch.setenv("HEADLESS", "true")

        import importlib

        from src.config import config as config_module

        importlib.reload(config_module)
        assert config_module.Config.HEADLESS is True

        # Test "false" string
        monkeypatch.setenv("HEADLESS", "false")
        importlib.reload(config_module)
        assert config_module.Config.HEADLESS is False

        # Test "True" with capital
        monkeypatch.setenv("HEADLESS", "True")
        importlib.reload(config_module)
        assert config_module.Config.HEADLESS is True

    def test_config_parses_integers_from_strings(self, monkeypatch):
        """Config correctly parses integer values from string env vars."""
        monkeypatch.setenv("DEFAULT_TIMEOUT", "15")
        monkeypatch.setenv("PAGE_LOAD_TIMEOUT", "45")
        monkeypatch.setenv("WINDOW_WIDTH", "1280")

        import importlib

        from src.config import config as config_module

        importlib.reload(config_module)

        assert config_module.Config.DEFAULT_TIMEOUT == 15
        assert config_module.Config.PAGE_LOAD_TIMEOUT == 45
        assert config_module.Config.WINDOW_WIDTH == 1280


class TestConfigBehaviorContract:
    """
    Tests that define the contract Config must fulfill.
    These will be used to validate ConfigService implementation.
    """

    def test_config_base_url_is_accessible(self):
        """BASE_URL can be accessed as class attribute."""
        url = Config.BASE_URL
        assert url is not None

    def test_config_credentials_are_accessible(self):
        """USERNAME and PASSWORD can be accessed."""
        username = Config.USERNAME
        password = Config.PASSWORD
        assert username is not None
        assert password is not None

    def test_config_timeout_values_are_positive(self):
        """All timeout values are positive integers."""
        assert Config.DEFAULT_TIMEOUT > 0
        assert Config.PAGE_LOAD_TIMEOUT > 0
        assert Config.IMPLICIT_WAIT >= 0

    def test_config_provides_selenium_grid_url_method(self):
        """get_selenium_grid_url() method exists and returns string."""
        assert callable(Config.get_selenium_grid_url)
        result = Config.get_selenium_grid_url()
        assert isinstance(result, str)
        assert "hub" in result

    def test_config_provides_ensure_directories_method(self):
        """ensure_directories() method exists and is callable."""
        assert callable(Config.ensure_directories)
        # Should not raise exception
        Config.ensure_directories()


class TestConfigDefaultValues:
    """Test default values provided by Config."""

    def test_default_browser_is_chrome(self):
        """Default browser is chrome if not specified."""
        # This captures current behavior
        assert Config.DEFAULT_BROWSER in ["chrome", "firefox", "edge"]

    def test_default_timeout_is_reasonable(self):
        """Default timeout is between 5-30 seconds."""
        assert 5 <= Config.DEFAULT_TIMEOUT <= 30

    def test_default_window_size_is_fullhd_or_larger(self):
        """Default window size is at least 1920x1080."""
        assert Config.WINDOW_WIDTH >= 1280
        assert Config.WINDOW_HEIGHT >= 720

    def test_screenshots_enabled_by_default(self):
        """Screenshots on failure are enabled by default."""
        # This captures current expected behavior
        assert Config.SCREENSHOT_ON_FAILURE is True


@pytest.fixture(autouse=True)
def reset_config_after_test():
    """
    Reset Config to original state after each test.
    This prevents test pollution.
    """
    import importlib

    from src.config import config as config_module

    yield

    # Reload config module to reset to .env values
    importlib.reload(config_module)
