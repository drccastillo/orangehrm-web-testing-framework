"""
Configuration module for test framework.
Loads environment variables and provides configuration settings.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    """Configuration class containing all test settings."""

    # Application URLs and Credentials
    BASE_URL = os.getenv("URL", "http://localhost:8080/web/index.php")
    USERNAME = os.getenv("ORANGEHRM_USERNAME", "Admin")
    PASSWORD = os.getenv("ORANGEHRM_PASSWORD", "admin123")

    # Selenium Grid Configuration
    SELENIUM_GRID_URL = os.getenv("SELENIUM_GRID_URL", "http://localhost:4444")

    # Browser Configuration
    DEFAULT_BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"

    # Timeouts (in seconds)
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "5"))

    # Window Configuration
    WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1920"))
    WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "1080"))
    MAXIMIZE_WINDOW = os.getenv("MAXIMIZE_WINDOW", "True").lower() == "true"

    # Screenshots Configuration
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "True").lower() == "true"
    SCREENSHOTS_DIR = Path(__file__).parent.parent.parent / "reports_selenium" / "screenshots"

    # Reports Configuration
    REPORTS_DIR = Path(__file__).parent.parent.parent / "reports_selenium"

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
    def ensure_directories(cls) -> None:
        """Create necessary directories if they don't exist."""
        cls.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
