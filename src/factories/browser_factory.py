"""
BrowserFactory: Factory for creating Playwright browser instances.

This factory creates Playwright browser adapters with configurable options
for different browsers (Chrome, Chromium, Firefox, Edge).
"""

from playwright.sync_api import sync_playwright

from src.adapters.playwright_browser import PlaywrightBrowserAdapter
from src.core.browser_protocol import BrowserProtocol
from utils.logger import TestLogger


class BrowserFactory:
    """
    Factory for creating Playwright browser instances.

    This factory supports multiple browsers (Chrome, Chromium, Firefox, Edge)
    through Playwright's automation API.

    Design Patterns:
        - Factory Pattern: Creates browser instances
        - Adapter Pattern: Wraps Playwright API with BrowserProtocol

    Example:
        >>> # Create Playwright Chrome browser
        >>> browser = BrowserFactory.create(
        ...     browser="chrome",
        ...     headless=True,
        ...     timeout=10
        ... )
        >>> browser.navigate("https://example.com")

        >>> # Create Playwright Firefox browser
        >>> browser = BrowserFactory.create(
        ...     browser="firefox",
        ...     timeout=15
        ... )
    """

    # Supported browsers
    _supported_browsers = ["chrome", "chromium", "firefox", "edge"]

    # Logger for debugging
    _logger = TestLogger.get_logger(__name__)

    @classmethod
    def create(
        cls,
        browser: str = "chrome",
        headless: bool = False,
        timeout: int = 10,
        maximize_window: bool = True,
        window_width: int = 1920,
        window_height: int = 1080,
    ) -> BrowserProtocol:
        """
        Create a Playwright browser instance.

        Args:
            browser: Browser name ("chrome", "chromium", "firefox", "edge")
            headless: Whether to run in headless mode
            timeout: Default timeout for operations in seconds
            maximize_window: Whether to maximize the browser window
            window_width: Window width if not maximized
            window_height: Window height if not maximized

        Returns:
            BrowserProtocol: Playwright browser adapter implementing BrowserProtocol

        Raises:
            ValueError: If browser is not supported

        Example:
            >>> # Playwright Chrome
            >>> browser = BrowserFactory.create(
            ...     browser="chrome",
            ...     headless=True,
            ...     timeout=10
            ... )

            >>> # Playwright Firefox
            >>> browser = BrowserFactory.create(
            ...     browser="firefox",
            ...     timeout=15
            ... )
        """
        browser_lower = browser.lower()

        cls._logger.info(
            f"Creating Playwright browser: {browser_lower} (headless={headless}, timeout={timeout})"
        )

        return cls._create_playwright_browser(
            browser_lower, headless, timeout, maximize_window, window_width, window_height
        )

    @classmethod
    def _create_playwright_browser(
        cls,
        browser: str,
        headless: bool,
        timeout: int,
        maximize_window: bool,
        window_width: int,
        window_height: int,
    ) -> BrowserProtocol:
        """Create Playwright browser adapter."""
        # Playwright instance
        playwright = sync_playwright().start()

        # Launch browser
        if browser in ("chrome", "chromium"):
            browser_instance = playwright.chromium.launch(headless=headless)
        elif browser == "firefox":
            browser_instance = playwright.firefox.launch(headless=headless)
        elif browser == "edge":
            # Edge uses Chromium engine
            browser_instance = playwright.chromium.launch(channel="msedge", headless=headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        cls._logger.info(f"Launched Playwright browser: {browser} (headless={headless})")

        # Create context and page
        if maximize_window:
            context = browser_instance.new_context(no_viewport=True)
        else:
            context = browser_instance.new_context(
                viewport={"width": window_width, "height": window_height}
            )
        page = context.new_page()

        # Wrap in adapter and pass playwright instance for proper cleanup
        return PlaywrightBrowserAdapter(page, timeout=timeout, playwright=playwright)

    @classmethod
    def get_supported_browsers(cls) -> list[str]:
        """
        Get list of supported browsers.

        Returns:
            List of browser names
        """
        return cls._supported_browsers.copy()

    @classmethod
    def is_browser_supported(cls, browser: str) -> bool:
        """
        Check if a browser is supported.

        Args:
            browser: Browser name

        Returns:
            True if browser is supported, False otherwise
        """
        return browser.lower() in cls._supported_browsers
