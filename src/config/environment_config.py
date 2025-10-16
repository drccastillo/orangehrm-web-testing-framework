"""
Environment-based configuration service implementation.
Loads configuration from environment variables and .env file.

This replaces the Singleton Config class with an injectable service.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from src.config.config_defaults import defaults
from src.enums.browser_types import BrowserType
from utils.exceptions import ConfigurationException


class EnvironmentConfigService:
    """
    Configuration service that loads from environment variables.

    Implements ConfigService protocol. This is the production implementation
    that reads from .env file and environment variables, matching the
    behavior of the original Config class.

    Example:
        >>> config = EnvironmentConfigService()
        >>> url = config.base_url
        >>> config.ensure_directories()
    """

    def __init__(self, env_path: Path | None = None):
        """
        Initialize configuration from environment.

        Args:
            env_path: Optional path to .env file. If None, uses default location.
        """
        # Load environment variables from .env file
        if env_path is None:
            env_path = Path(__file__).parent.parent.parent / ".env"
            # For default path, don't override existing env vars (tests may set them)
            load_dotenv(dotenv_path=env_path, override=False)
        else:
            # For custom path, override existing env vars
            load_dotenv(dotenv_path=env_path, override=True)

        # Load all configuration values from environment
        self._load_configuration()

    def _load_configuration(self) -> None:
        """Load and validate all configuration values from environment variables."""
        # Application URLs and Credentials
        self._base_url = os.getenv("URL", defaults.BASE_URL)
        self._username = os.getenv("ORANGEHRM_USERNAME", defaults.USERNAME)
        self._password = os.getenv("ORANGEHRM_PASSWORD", defaults.PASSWORD)

        # Browser Configuration - validate using BrowserType enum
        browser_str = os.getenv("BROWSER", defaults.BROWSER)
        try:
            browser_enum = BrowserType.from_string(browser_str)
            self._default_browser = browser_enum.value
        except ValueError as e:
            raise ConfigurationException(f"Invalid BROWSER configuration: {e}") from e

        self._headless = os.getenv("HEADLESS", defaults.HEADLESS).lower() == "true"

        # Timeouts (in seconds) - validate positive values
        self._default_timeout = self._parse_positive_int(
            "DEFAULT_TIMEOUT", defaults.DEFAULT_TIMEOUT
        )
        self._page_load_timeout = self._parse_positive_int(
            "PAGE_LOAD_TIMEOUT", defaults.PAGE_LOAD_TIMEOUT
        )

        # Window Configuration - validate positive dimensions
        self._window_width = self._parse_positive_int("WINDOW_WIDTH", defaults.WINDOW_WIDTH)
        self._window_height = self._parse_positive_int("WINDOW_HEIGHT", defaults.WINDOW_HEIGHT)
        self._maximize_window = (
            os.getenv("MAXIMIZE_WINDOW", defaults.MAXIMIZE_WINDOW).lower() == "true"
        )

        # Screenshots Configuration
        self._screenshot_on_failure = (
            os.getenv("SCREENSHOT_ON_FAILURE", defaults.SCREENSHOT_ON_FAILURE).lower() == "true"
        )
        self._screenshots_dir = Path(__file__).parent.parent.parent / "reports" / "screenshots"

        # Reports Configuration
        self._reports_dir = Path(__file__).parent.parent.parent / "reports"

    def _parse_positive_int(self, env_key: str, default: str) -> int:
        """
        Parse environment variable as positive integer with validation.

        Args:
            env_key: Environment variable name
            default: Default value as string

        Returns:
            Parsed positive integer value

        Raises:
            ConfigurationException: If value is not a valid positive integer
        """
        value_str = os.getenv(env_key, default)
        try:
            value = int(value_str)
        except ValueError as e:
            raise ConfigurationException(f"{env_key} must be an integer, got: {value_str}") from e

        if value <= 0:
            raise ConfigurationException(f"{env_key} must be positive, got: {value}")

        return value

    # Application Configuration Properties
    @property
    def base_url(self) -> str:
        """Get the base URL of the application under test."""
        return self._base_url

    @property
    def username(self) -> str:
        """Get the default username for authentication."""
        return self._username

    @property
    def password(self) -> str:
        """Get the default password for authentication."""
        return self._password

    # Browser Configuration
    @property
    def default_browser(self) -> str:
        """Get the default browser to use (chrome, firefox, edge)."""
        return self._default_browser

    @property
    def headless(self) -> bool:
        """Get whether to run browser in headless mode."""
        return self._headless

    # Timeout Configuration
    @property
    def default_timeout(self) -> int:
        """Get the default timeout in seconds for explicit waits."""
        return self._default_timeout

    @property
    def page_load_timeout(self) -> int:
        """Get the page load timeout in seconds."""
        return self._page_load_timeout

    # Window Configuration
    @property
    def window_width(self) -> int:
        """Get the browser window width in pixels."""
        return self._window_width

    @property
    def window_height(self) -> int:
        """Get the browser window height in pixels."""
        return self._window_height

    @property
    def maximize_window(self) -> bool:
        """Get whether to maximize browser window."""
        return self._maximize_window

    # Screenshot Configuration
    @property
    def screenshot_on_failure(self) -> bool:
        """Get whether to take screenshots on test failure."""
        return self._screenshot_on_failure

    @property
    def screenshots_dir(self) -> Path:
        """Get the directory path for storing screenshots."""
        return self._screenshots_dir

    # Reports Configuration
    @property
    def reports_dir(self) -> Path:
        """Get the directory path for storing test reports."""
        return self._reports_dir

    # Methods
    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self._screenshots_dir.mkdir(parents=True, exist_ok=True)
        self._reports_dir.mkdir(parents=True, exist_ok=True)

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"EnvironmentConfigService("
            f"base_url={self.base_url}, "
            f"browser={self.default_browser}, "
            f"headless={self.headless})"
        )
