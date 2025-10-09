"""
Configuration interface following Dependency Inversion Principle.
Allows multiple configuration implementations (env, JSON, mock, etc.)
"""
from typing import Protocol, runtime_checkable
from pathlib import Path


@runtime_checkable
class ConfigInterface(Protocol):
    """
    Configuration interface using Protocol for structural subtyping.

    This allows any class with these properties to be used as configuration
    without explicit inheritance.
    """

    # Application URLs and Credentials
    @property
    def base_url(self) -> str:
        """Base URL of the application under test."""
        ...

    @property
    def username(self) -> str:
        """Default username for authentication."""
        ...

    @property
    def password(self) -> str:
        """Default password for authentication."""
        ...

    # Selenium Grid Configuration
    @property
    def selenium_grid_url(self) -> str:
        """Selenium Grid hub URL."""
        ...

    # Browser Configuration
    @property
    def default_browser(self) -> str:
        """Default browser name (chrome, firefox, edge)."""
        ...

    @property
    def headless(self) -> bool:
        """Whether to run browser in headless mode."""
        ...

    # Timeouts (in seconds)
    @property
    def default_timeout(self) -> int:
        """Default timeout for element waits."""
        ...

    @property
    def page_load_timeout(self) -> int:
        """Timeout for page loads."""
        ...

    @property
    def implicit_wait(self) -> int:
        """Implicit wait timeout (usually 0 for explicit waits only)."""
        ...

    # Window Configuration
    @property
    def window_width(self) -> int:
        """Browser window width."""
        ...

    @property
    def window_height(self) -> int:
        """Browser window height."""
        ...

    @property
    def maximize_window(self) -> bool:
        """Whether to maximize browser window."""
        ...

    # Screenshots Configuration
    @property
    def screenshot_on_failure(self) -> bool:
        """Whether to take screenshot on test failure."""
        ...

    @property
    def screenshots_dir(self) -> Path:
        """Directory for storing screenshots."""
        ...

    # Reports Configuration
    @property
    def reports_dir(self) -> Path:
        """Directory for storing test reports."""
        ...

    @property
    def allure_results_dir(self) -> Path:
        """Directory for Allure results."""
        ...

    @property
    def allure_report_dir(self) -> Path:
        """Directory for generated Allure reports."""
        ...

    # Methods
    def get_selenium_grid_url(self, browser: str = None) -> str:
        """
        Get the Selenium Grid URL for remote WebDriver.

        Args:
            browser: Browser name (optional, for browser-specific URLs)

        Returns:
            Selenium Grid URL with /wd/hub endpoint
        """
        ...

    def validate(self) -> None:
        """
        Validate that all required configuration is present and valid.

        Raises:
            ValueError: If required configuration is missing or invalid
        """
        ...

    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        ...
