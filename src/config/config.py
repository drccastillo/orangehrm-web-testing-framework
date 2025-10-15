"""
Configuration module for test framework.

DEPRECATED: This class is maintained for backward compatibility.
New code should use EnvironmentConfigService with dependency injection.

This class now acts as a Facade that delegates to EnvironmentConfigService,
eliminating code duplication while maintaining the same public API.
"""

from src.config.environment_config import EnvironmentConfigService


class Config:
    """
    Legacy configuration class - now a facade to EnvironmentConfigService.

    DEPRECATED: Use dependency injection with ConfigService protocol instead.
    This class will be removed in Phase 2 of the refactoring.

    Example (old pattern - being phased out):
        >>> from src.config.config import Config
        >>> url = Config.BASE_URL

    Example (new pattern - preferred):
        >>> from src.config.protocols import ConfigService
        >>> def test_something(config_service: ConfigService):
        ...     url = config_service.base_url
    """

    # Private service instance - all Config attributes delegate to this
    _service = EnvironmentConfigService()

    # Application URLs and Credentials
    BASE_URL = _service.base_url
    USERNAME = _service.username
    PASSWORD = _service.password

    # Selenium Grid Configuration
    SELENIUM_GRID_URL = _service.selenium_grid_url

    # Browser Configuration
    DEFAULT_BROWSER = _service.default_browser
    HEADLESS = _service.headless

    # Timeouts (in seconds)
    DEFAULT_TIMEOUT = _service.default_timeout
    PAGE_LOAD_TIMEOUT = _service.page_load_timeout
    IMPLICIT_WAIT = _service.implicit_wait

    # Window Configuration
    WINDOW_WIDTH = _service.window_width
    WINDOW_HEIGHT = _service.window_height
    MAXIMIZE_WINDOW = _service.maximize_window

    # Screenshots Configuration
    SCREENSHOT_ON_FAILURE = _service.screenshot_on_failure
    SCREENSHOTS_DIR = _service.screenshots_dir

    # Reports Configuration
    REPORTS_DIR = _service.reports_dir

    @classmethod
    def get_selenium_grid_url(cls, browser: str | None = None) -> str:
        """
        Get the Selenium Grid URL for remote WebDriver.

        Args:
            browser: Browser name (chrome, firefox, edge)

        Returns:
            Selenium Grid URL with /wd/hub endpoint
        """
        return cls._service.get_selenium_grid_url(browser)

    @classmethod
    def ensure_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        # Use class attributes (not service) to support monkeypatching in tests
        cls.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
