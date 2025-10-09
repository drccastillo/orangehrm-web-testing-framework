"""
Mock configuration for testing purposes.
Implements ConfigInterface without external dependencies.
"""
from pathlib import Path
from typing import Optional


class MockConfig:
    """
    Mock configuration for testing.
    
    Implements ConfigInterface without loading from environment variables.
    Allows setting custom values for testing scenarios.
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8080",
        username: str = "test_user",
        password: str = "test_password",
        selenium_grid_url: str = "http://localhost:4444",
        default_browser: str = "chrome",
        headless: bool = True,
        default_timeout: int = 10,
        page_load_timeout: int = 30,
        implicit_wait: int = 0,
        window_width: int = 1920,
        window_height: int = 1080,
        maximize_window: bool = False,
        screenshot_on_failure: bool = False,
        screenshots_dir: Optional[Path] = None,
        reports_dir: Optional[Path] = None,
        allure_results_dir: Optional[Path] = None,
        allure_report_dir: Optional[Path] = None,
    ):
        """
        Initialize mock configuration with custom values.

        Args:
            base_url: Base URL of the application
            username: Test username
            password: Test password
            selenium_grid_url: Selenium Grid hub URL
            default_browser: Browser name
            headless: Run in headless mode
            default_timeout: Default element wait timeout
            page_load_timeout: Page load timeout
            implicit_wait: Implicit wait timeout
            window_width: Browser window width
            window_height: Browser window height
            maximize_window: Whether to maximize browser window
            screenshot_on_failure: Whether to take screenshots on failure
            screenshots_dir: Directory for screenshots (defaults to /tmp/screenshots)
            reports_dir: Directory for reports (defaults to /tmp/reports)
            allure_results_dir: Directory for Allure results
            allure_report_dir: Directory for Allure reports
        """
        self._base_url = base_url
        self._username = username
        self._password = password
        self._selenium_grid_url = selenium_grid_url
        self._default_browser = default_browser
        self._headless = headless
        self._default_timeout = default_timeout
        self._page_load_timeout = page_load_timeout
        self._implicit_wait = implicit_wait
        self._window_width = window_width
        self._window_height = window_height
        self._maximize_window = maximize_window
        self._screenshot_on_failure = screenshot_on_failure
        self._screenshots_dir = screenshots_dir or Path("/tmp/test_screenshots")
        self._reports_dir = reports_dir or Path("/tmp/test_reports")
        self._allure_results_dir = allure_results_dir or (self._reports_dir / "allure-results")
        self._allure_report_dir = allure_report_dir or (self._reports_dir / "allure-report")

    # ConfigInterface implementation
    @property
    def base_url(self) -> str:
        """Base URL of the application under test."""
        return self._base_url

    @property
    def username(self) -> str:
        """Default username for authentication."""
        return self._username

    @property
    def password(self) -> str:
        """Default password for authentication."""
        return self._password

    @property
    def selenium_grid_url(self) -> str:
        """Selenium Grid hub URL."""
        return self._selenium_grid_url

    @property
    def default_browser(self) -> str:
        """Default browser name (chrome, firefox, edge)."""
        return self._default_browser

    @property
    def headless(self) -> bool:
        """Whether to run browser in headless mode."""
        return self._headless

    @property
    def default_timeout(self) -> int:
        """Default timeout for element waits."""
        return self._default_timeout

    @property
    def page_load_timeout(self) -> int:
        """Timeout for page loads."""
        return self._page_load_timeout

    @property
    def implicit_wait(self) -> int:
        """Implicit wait timeout (usually 0 for explicit waits only)."""
        return self._implicit_wait

    @property
    def window_width(self) -> int:
        """Browser window width."""
        return self._window_width

    @property
    def window_height(self) -> int:
        """Browser window height."""
        return self._window_height

    @property
    def maximize_window(self) -> bool:
        """Whether to maximize browser window."""
        return self._maximize_window

    @property
    def screenshot_on_failure(self) -> bool:
        """Whether to take screenshot on test failure."""
        return self._screenshot_on_failure

    @property
    def screenshots_dir(self) -> Path:
        """Directory for storing screenshots."""
        return self._screenshots_dir

    @property
    def reports_dir(self) -> Path:
        """Directory for storing test reports."""
        return self._reports_dir

    @property
    def allure_results_dir(self) -> Path:
        """Directory for Allure results."""
        return self._allure_results_dir

    @property
    def allure_report_dir(self) -> Path:
        """Directory for generated Allure reports."""
        return self._allure_report_dir

    def get_selenium_grid_url(self, browser: str = None) -> str:
        """
        Get the Selenium Grid URL for remote WebDriver.

        Args:
            browser: Browser name (optional)

        Returns:
            Selenium Grid URL with /wd/hub endpoint
        """
        return f"{self._selenium_grid_url}/wd/hub"

    def validate(self) -> None:
        """
        Validate that all required configuration is present and valid.

        Raises:
            ValueError: If required configuration is missing or invalid
        """
        errors = []

        # Validate required configurations
        if not self._base_url:
            errors.append("base_url is required")

        if not self._username:
            errors.append("username is required")

        if not self._password:
            errors.append("password is required")

        if not self._selenium_grid_url:
            errors.append("selenium_grid_url is required")

        # Validate numeric configurations
        if self._default_timeout <= 0:
            errors.append(f"default_timeout must be positive (got {self._default_timeout})")

        if self._page_load_timeout <= 0:
            errors.append(f"page_load_timeout must be positive (got {self._page_load_timeout})")

        if self._window_width <= 0:
            errors.append(f"window_width must be positive (got {self._window_width})")

        if self._window_height <= 0:
            errors.append(f"window_height must be positive (got {self._window_height})")

        # Validate browser
        valid_browsers = ['chrome', 'firefox', 'edge']
        if self._default_browser.lower() not in valid_browsers:
            errors.append(
                f"default_browser must be one of {valid_browsers} (got '{self._default_browser}')"
            )

        if errors:
            error_message = "MockConfig validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
            raise ValueError(error_message)

    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self._screenshots_dir.mkdir(parents=True, exist_ok=True)
        self._reports_dir.mkdir(parents=True, exist_ok=True)
        self._allure_results_dir.mkdir(parents=True, exist_ok=True)
        self._allure_report_dir.mkdir(parents=True, exist_ok=True)
