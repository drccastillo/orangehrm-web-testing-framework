"""
BrowserFactory: Simplified factory for creating Playwright browser instances.

Phase 2 refactor: Returns Page directly instead of adapter wrapper.
Uses BrowserType Enum for type safety.
"""

from playwright.sync_api import Page, Playwright, sync_playwright

from src.constants.browser_types import BrowserType
from utils.logger import TestLogger


class BrowserFactory:
    """
    Factory for creating Playwright browser instances.

    This factory supports multiple browsers (Chrome, Chromium, Firefox, Edge, WebKit)
    through Playwright's automation API and returns Page instances directly.

    Design Patterns:
        - Factory Pattern: Creates browser instances
        - Type Safety: Uses BrowserType Enum
        - YAGNI: Returns Page directly, no adapter wrapping

    Example:
        >>> # Create Playwright Chrome browser
        >>> page, pw = BrowserFactory.create(
        ...     browser=BrowserType.CHROME,
        ...     headless=True,
        ...     timeout=10
        ... )
        >>> page.goto("https://example.com")
        >>> pw.stop()  # Cleanup
    """

    # Logger for debugging
    _logger = TestLogger.get_logger(__name__)

    @classmethod
    def create(  # pylint: disable=too-many-positional-arguments
        cls,
        browser: BrowserType | str = BrowserType.CHROME,
        headless: bool = False,
        timeout: int = 10,
        maximize_window: bool = True,
        window_width: int = 1920,
        window_height: int = 1080,
    ) -> tuple[Page, Playwright]:
        """
        Create a Playwright browser instance.

        Args:
            browser: Browser type (BrowserType enum or string)
            headless: Whether to run in headless mode
            timeout: Default timeout for operations in seconds
            maximize_window: Whether to maximize the browser window
            window_width: Window width if not maximized
            window_height: Window height if not maximized

        Returns:
            tuple: (Playwright Page instance, Playwright instance for cleanup)

        Raises:
            ValueError: If browser is not supported

        Example:
            >>> # Using Enum (recommended)
            >>> page, pw = BrowserFactory.create(
            ...     browser=BrowserType.FIREFOX,
            ...     headless=True
            ... )
            >>>
            >>> # Using string (auto-converted to Enum)
            >>> page, pw = BrowserFactory.create(
            ...     browser="chrome",
            ...     timeout=15
            ... )
        """
        # Convert string to Enum if needed
        browser_type = BrowserType.from_string(browser) if isinstance(browser, str) else browser

        cls._logger.info(
            f"Creating Playwright browser: {browser_type.value} "
            f"(headless={headless}, timeout={timeout})"
        )

        return cls._create_playwright_browser(
            browser_type,
            headless,
            timeout,
            maximize_window,
            window_width,
            window_height,
        )

    @classmethod
    def _create_playwright_browser(  # pylint: disable=too-many-positional-arguments
        cls,
        browser: BrowserType,
        headless: bool,
        timeout: int,
        maximize_window: bool,
        window_width: int,
        window_height: int,
    ) -> tuple[Page, Playwright]:
        """
        Create Playwright browser and return Page directly.

        Args:
            browser: BrowserType enum
            headless: Headless mode flag
            timeout: Default timeout in seconds
            maximize_window: Whether to maximize window
            window_width: Window width if not maximized
            window_height: Window height if not maximized

        Returns:
            tuple: (Page, Playwright instance for cleanup)
        """
        # Start Playwright instance
        playwright = sync_playwright().start()

        # Launch browser based on type
        if browser in (BrowserType.CHROME, BrowserType.CHROMIUM):
            browser_instance = playwright.chromium.launch(headless=headless)
        elif browser == BrowserType.FIREFOX:
            browser_instance = playwright.firefox.launch(headless=headless)
        elif browser == BrowserType.EDGE:
            # Edge uses Chromium engine
            browser_instance = playwright.chromium.launch(channel="msedge", headless=headless)
        elif browser == BrowserType.WEBKIT:
            browser_instance = playwright.webkit.launch(headless=headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        cls._logger.info(f"Launched Playwright browser: {browser.value} (headless={headless})")

        # Create context and page
        if maximize_window:
            context = browser_instance.new_context(no_viewport=True)
        else:
            context = browser_instance.new_context(
                viewport={"width": window_width, "height": window_height}
            )

        page = context.new_page()

        # Set default timeout in milliseconds
        timeout_ms = timeout * 1000
        page.set_default_timeout(timeout_ms)

        return page, playwright

    @classmethod
    def get_supported_browsers(cls) -> list[str]:
        """
        Get list of supported browsers.

        Returns:
            List of browser names
        """
        return [browser.value for browser in BrowserType]

    @classmethod
    def is_browser_supported(cls, browser: str) -> bool:
        """
        Check if a browser is supported.

        Args:
            browser: Browser name

        Returns:
            True if browser is supported, False otherwise
        """
        try:
            BrowserType.from_string(browser)
            return True
        except ValueError:
            return False
