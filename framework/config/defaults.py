"""
Framework default constants.
Centralizes magic numbers and default values used throughout the framework.
"""


class FrameworkDefaults:
    """Default values for framework components."""

    # Timeout defaults (seconds)
    DEFAULT_TIMEOUT = 10
    DEFAULT_PAGE_LOAD_TIMEOUT = 30
    DEFAULT_IMPLICIT_WAIT = 0  # We use explicit waits only

    # Window defaults
    DEFAULT_WINDOW_WIDTH = 1920
    DEFAULT_WINDOW_HEIGHT = 1080

    # Visual debugging defaults
    DEFAULT_BLINK_TIMES = 3
    DEFAULT_BLINK_DELAY_SECONDS = 0.2
    DEFAULT_HIGHLIGHT_DURATION = 2
    DEFAULT_BORDER_WIDTH = "3px"
    DEFAULT_HIGHLIGHT_COLOR = "red"
    DEFAULT_BLINK_COLOR = "red"

    # Supported browsers
    SUPPORTED_BROWSERS = ['chrome', 'firefox', 'edge']
    DEFAULT_BROWSER = 'chrome'

    # Logging defaults
    DEFAULT_LOG_LEVEL = "INFO"
    FILE_LOG_LEVEL = "DEBUG"


class BrowserDefaults:
    """Default values for browser configuration."""

    # Common browser arguments
    COMMON_BROWSER_ARGS = [
        "--no-sandbox",
        "--disable-dev-shm-usage",
    ]

    # Chrome-specific
    CHROME_PERFORMANCE_ARGS = [
        "--disable-gpu",
        "--disable-extensions",
        "--disable-infobars",
    ]

    # Headless mode arguments
    CHROME_HEADLESS_ARG = "--headless=new"
    FIREFOX_HEADLESS_ARG = "--headless"
    EDGE_HEADLESS_ARG = "--headless"
