"""
Default configuration values for the test framework.

This module centralizes all default configuration values, eliminating
hardcoded values from the EnvironmentConfigService implementation.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ConfigDefaults:
    """
    Default configuration values used when environment variables are not set.

    These values are used as fallbacks by EnvironmentConfigService.
    All values are immutable (frozen dataclass).
    """

    # Application Configuration
    BASE_URL: str = "http://localhost:8080/web/index.php"
    USERNAME: str = "Admin"
    PASSWORD: str = "admin123"

    # Browser Configuration
    BROWSER: str = "chrome"
    HEADLESS: str = "False"

    # Timeout Configuration (as strings for consistency with env vars)
    DEFAULT_TIMEOUT: str = "10"
    PAGE_LOAD_TIMEOUT: str = "30"

    # Window Configuration (as strings for consistency with env vars)
    WINDOW_WIDTH: str = "1920"
    WINDOW_HEIGHT: str = "1080"
    MAXIMIZE_WINDOW: str = "True"

    # Screenshot Configuration
    SCREENSHOT_ON_FAILURE: str = "True"


# Singleton instance for easy import
defaults = ConfigDefaults()
