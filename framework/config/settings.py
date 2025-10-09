"""
Configuration module for test framework.
Loads environment variables and provides configuration settings.
Implements ConfigInterface for dependency injection.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """
    Configuration class implementing ConfigInterface.

    Provides test settings loaded from environment variables.
    Supports both class-level access (backward compatible) and instance-level access.
    """

    # Class-level attributes (backward compatible)
    _BASE_URL = os.getenv('URL')
    _USERNAME = os.getenv('ORANGEHRM_USERNAME')
    _PASSWORD = os.getenv('ORANGEHRM_PASSWORD')
    _SELENIUM_GRID_URL = os.getenv('SELENIUM_GRID_URL')
    _DEFAULT_BROWSER = os.getenv('BROWSER', 'chrome')
    _HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
    _DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT', '10'))
    _PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
    _IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '5'))
    _WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', '1920'))
    _WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', '1080'))
    _MAXIMIZE_WINDOW = os.getenv('MAXIMIZE_WINDOW', 'True').lower() == 'true'
    _SCREENSHOT_ON_FAILURE = os.getenv('SCREENSHOT_ON_FAILURE', 'True').lower() == 'true'
    _SCREENSHOTS_DIR = Path(__file__).parent.parent.parent / 'reports' / 'screenshots'
    _REPORTS_DIR = Path(__file__).parent.parent.parent / 'reports'
    _ALLURE_RESULTS_DIR = _REPORTS_DIR / 'allure-results'
    _ALLURE_REPORT_DIR = _REPORTS_DIR / 'allure-report'

    # Backward compatible class attributes (static access)
    BASE_URL = _BASE_URL
    USERNAME = _USERNAME
    PASSWORD = _PASSWORD
    SELENIUM_GRID_URL = _SELENIUM_GRID_URL
    DEFAULT_BROWSER = _DEFAULT_BROWSER
    HEADLESS = _HEADLESS
    DEFAULT_TIMEOUT = _DEFAULT_TIMEOUT
    PAGE_LOAD_TIMEOUT = _PAGE_LOAD_TIMEOUT
    IMPLICIT_WAIT = _IMPLICIT_WAIT
    WINDOW_WIDTH = _WINDOW_WIDTH
    WINDOW_HEIGHT = _WINDOW_HEIGHT
    MAXIMIZE_WINDOW = _MAXIMIZE_WINDOW
    SCREENSHOT_ON_FAILURE = _SCREENSHOT_ON_FAILURE
    SCREENSHOTS_DIR = _SCREENSHOTS_DIR
    REPORTS_DIR = _REPORTS_DIR
    ALLURE_RESULTS_DIR = _ALLURE_RESULTS_DIR
    ALLURE_REPORT_DIR = _ALLURE_REPORT_DIR

    # ConfigInterface implementation (instance properties)
    @property
    def base_url(self) -> str:
        """Base URL of the application under test."""
        return self._BASE_URL

    @property
    def username(self) -> str:
        """Default username for authentication."""
        return self._USERNAME

    @property
    def password(self) -> str:
        """Default password for authentication."""
        return self._PASSWORD

    @property
    def selenium_grid_url(self) -> str:
        """Selenium Grid hub URL."""
        return self._SELENIUM_GRID_URL

    @property
    def default_browser(self) -> str:
        """Default browser name (chrome, firefox, edge)."""
        return self._DEFAULT_BROWSER

    @property
    def headless(self) -> bool:
        """Whether to run browser in headless mode."""
        return self._HEADLESS

    @property
    def default_timeout(self) -> int:
        """Default timeout for element waits."""
        return self._DEFAULT_TIMEOUT

    @property
    def page_load_timeout(self) -> int:
        """Timeout for page loads."""
        return self._PAGE_LOAD_TIMEOUT

    @property
    def implicit_wait(self) -> int:
        """Implicit wait timeout (usually 0 for explicit waits only)."""
        return self._IMPLICIT_WAIT

    @property
    def window_width(self) -> int:
        """Browser window width."""
        return self._WINDOW_WIDTH

    @property
    def window_height(self) -> int:
        """Browser window height."""
        return self._WINDOW_HEIGHT

    @property
    def maximize_window(self) -> bool:
        """Whether to maximize browser window."""
        return self._MAXIMIZE_WINDOW

    @property
    def screenshot_on_failure(self) -> bool:
        """Whether to take screenshot on test failure."""
        return self._SCREENSHOT_ON_FAILURE

    @property
    def screenshots_dir(self) -> Path:
        """Directory for storing screenshots."""
        return self._SCREENSHOTS_DIR

    @property
    def reports_dir(self) -> Path:
        """Directory for storing test reports."""
        return self._REPORTS_DIR

    @property
    def allure_results_dir(self) -> Path:
        """Directory for Allure results."""
        return self._ALLURE_RESULTS_DIR

    @property
    def allure_report_dir(self) -> Path:
        """Directory for generated Allure reports."""
        return self._ALLURE_REPORT_DIR

    @classmethod
    def get_selenium_grid_url(cls, browser: str = None) -> str:
        """
        Get the Selenium Grid URL for remote WebDriver.

        Args:
            browser: Browser name (chrome, firefox, edge)

        Returns:
            Selenium Grid URL
        """
        return f"{cls.SELENIUM_GRID_URL}/wd/hub"

    @classmethod
    def validate(cls) -> None:
        """
        Validate that all required configuration is present.

        Raises:
            ValueError: If required configuration is missing or invalid
        """
        errors = []

        # Validate required configurations
        if not cls.BASE_URL:
            errors.append("URL environment variable is required (BASE_URL)")

        if not cls.USERNAME:
            errors.append("ORANGEHRM_USERNAME environment variable is required")

        if not cls.PASSWORD:
            errors.append("ORANGEHRM_PASSWORD environment variable is required")

        if not cls.SELENIUM_GRID_URL:
            errors.append("SELENIUM_GRID_URL environment variable is required")

        # Validate numeric configurations
        if cls.DEFAULT_TIMEOUT <= 0:
            errors.append(f"DEFAULT_TIMEOUT must be positive (got {cls.DEFAULT_TIMEOUT})")

        if cls.PAGE_LOAD_TIMEOUT <= 0:
            errors.append(f"PAGE_LOAD_TIMEOUT must be positive (got {cls.PAGE_LOAD_TIMEOUT})")

        if cls.WINDOW_WIDTH <= 0:
            errors.append(f"WINDOW_WIDTH must be positive (got {cls.WINDOW_WIDTH})")

        if cls.WINDOW_HEIGHT <= 0:
            errors.append(f"WINDOW_HEIGHT must be positive (got {cls.WINDOW_HEIGHT})")

        # Validate browser
        valid_browsers = ['chrome', 'firefox', 'edge']
        if cls.DEFAULT_BROWSER.lower() not in valid_browsers:
            errors.append(
                f"DEFAULT_BROWSER must be one of {valid_browsers} (got '{cls.DEFAULT_BROWSER}')"
            )

        if errors:
            error_message = "Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
            raise ValueError(error_message)

    @classmethod
    def ensure_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        cls.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.ALLURE_RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.ALLURE_REPORT_DIR.mkdir(parents=True, exist_ok=True)
