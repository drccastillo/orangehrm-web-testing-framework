"""
Environment-based configuration service implementation.
Loads configuration from environment variables and .env file.

This replaces the Singleton Config class with an injectable service.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


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
        """Load all configuration values from environment variables."""
        # Application URLs and Credentials
        self._base_url = os.getenv("URL", "http://localhost:8080/web/index.php")
        self._username = os.getenv("ORANGEHRM_USERNAME", "Admin")
        self._password = os.getenv("ORANGEHRM_PASSWORD", "admin123")

        # Selenium Grid Configuration
        self._selenium_grid_url = os.getenv("SELENIUM_GRID_URL", "http://localhost:4444")

        # Browser Configuration
        self._default_browser = os.getenv("BROWSER", "chrome")
        self._headless = os.getenv("HEADLESS", "False").lower() == "true"

        # Timeouts (in seconds)
        self._default_timeout = int(os.getenv("DEFAULT_TIMEOUT", "10"))
        self._page_load_timeout = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
        self._implicit_wait = int(os.getenv("IMPLICIT_WAIT", "5"))

        # Window Configuration
        self._window_width = int(os.getenv("WINDOW_WIDTH", "1920"))
        self._window_height = int(os.getenv("WINDOW_HEIGHT", "1080"))
        self._maximize_window = os.getenv("MAXIMIZE_WINDOW", "True").lower() == "true"

        # Screenshots Configuration
        self._screenshot_on_failure = os.getenv("SCREENSHOT_ON_FAILURE", "True").lower() == "true"
        self._screenshots_dir = (
            Path(__file__).parent.parent.parent / "reports_selenium" / "screenshots"
        )

        # Reports Configuration
        self._reports_dir = Path(__file__).parent.parent.parent / "reports_selenium"

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

    # Selenium Grid Configuration
    @property
    def selenium_grid_url(self) -> str:
        """Get the Selenium Grid URL."""
        return self._selenium_grid_url

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

    @property
    def implicit_wait(self) -> int:
        """Get the implicit wait time in seconds."""
        return self._implicit_wait

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
    def get_selenium_grid_url(self, browser: str | None = None) -> str:
        """
        Get the Selenium Grid URL for remote WebDriver.

        Args:
            browser: Optional browser name (for future browser-specific endpoints)

        Returns:
            Selenium Grid URL with /wd/hub endpoint
        """
        return f"{self._selenium_grid_url}/wd/hub"

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
