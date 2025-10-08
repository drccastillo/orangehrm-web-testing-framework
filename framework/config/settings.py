"""
Configuration module for test framework.
Loads environment variables and provides configuration settings.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Configuration class containing all test settings."""

    # Application URLs and Credentials
    BASE_URL = os.getenv('URL')
    USERNAME = os.getenv('ORANGEHRM_USERNAME')
    PASSWORD = os.getenv('ORANGEHRM_PASSWORD')

    # Selenium Grid Configuration
    SELENIUM_GRID_URL = os.getenv('SELENIUM_GRID_URL')

    # Browser Configuration
    DEFAULT_BROWSER = os.getenv('BROWSER', 'chrome')
    HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'

    # Timeouts (in seconds)
    DEFAULT_TIMEOUT = int(os.getenv('DEFAULT_TIMEOUT', '10'))
    PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '5'))

    # Window Configuration
    WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', '1920'))
    WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', '1080'))
    MAXIMIZE_WINDOW = os.getenv('MAXIMIZE_WINDOW', 'True').lower() == 'true'

    # Screenshots Configuration
    SCREENSHOT_ON_FAILURE = os.getenv('SCREENSHOT_ON_FAILURE', 'True').lower() == 'true'
    SCREENSHOTS_DIR = Path(__file__).parent.parent.parent / 'reports' / 'screenshots'

    # Reports Configuration
    REPORTS_DIR = Path(__file__).parent.parent.parent / 'reports'
    ALLURE_RESULTS_DIR = REPORTS_DIR / 'allure-results'
    ALLURE_REPORT_DIR = REPORTS_DIR / 'allure-report'

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
