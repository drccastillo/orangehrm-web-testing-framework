"""
BrowserFactory: Factory for creating browser instances using Strategy pattern.

This factory creates browser adapters for different automation frameworks
(Selenium, Playwright) with configurable options.
"""

from abc import ABC, abstractmethod
from typing import Any

from playwright.sync_api import sync_playwright
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from src.adapters.playwright_browser import PlaywrightBrowserAdapter
from src.adapters.selenium_browser import SeleniumBrowserAdapter
from src.core.browser_protocol import BrowserProtocol
from utils.logger import TestLogger


class BrowserOptionsStrategy(ABC):
    """
    Abstract strategy for browser-specific options configuration.

    Design Pattern:
        Strategy Pattern - Different strategies for different browsers
    """

    @abstractmethod
    def create_options(self, headless: bool = False) -> Any:
        """
        Create browser-specific options.

        Args:
            headless: Whether to run in headless mode

        Returns:
            Browser-specific options object
        """


class ChromeOptionsStrategy(BrowserOptionsStrategy):
    """Chrome/Chromium browser options strategy."""

    def create_options(self, headless: bool = False) -> ChromeOptions:
        """Create Chrome options."""
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        return options


class FirefoxOptionsStrategy(BrowserOptionsStrategy):
    """Firefox browser options strategy."""

    def create_options(self, headless: bool = False) -> FirefoxOptions:
        """Create Firefox options."""
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        return options


class EdgeOptionsStrategy(BrowserOptionsStrategy):
    """Edge browser options strategy."""

    def create_options(self, headless: bool = False) -> EdgeOptions:
        """Create Edge options."""
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return options


class BrowserFactory:
    """
    Factory for creating browser instances with Strategy pattern.

    This factory supports multiple automation frameworks (Selenium, Playwright)
    and multiple browsers (Chrome, Firefox, Edge) through the Strategy pattern.

    Design Patterns:
        - Factory Pattern: Creates browser instances
        - Strategy Pattern: Different strategies for browser configuration
        - Adapter Pattern: Wraps framework-specific APIs

    Example:
        >>> # Create Selenium Chrome browser
        >>> browser = BrowserFactory.create(
        ...     framework="selenium",
        ...     browser="chrome",
        ...     headless=True,
        ...     timeout=10
        ... )
        >>> browser.navigate("https://example.com")

        >>> # Create Playwright Firefox browser
        >>> browser = BrowserFactory.create(
        ...     framework="playwright",
        ...     browser="firefox",
        ...     timeout=10
        ... )
    """

    # Registry of browser options strategies
    _strategies: dict[str, BrowserOptionsStrategy] = {
        "chrome": ChromeOptionsStrategy(),
        "chromium": ChromeOptionsStrategy(),  # Alias for Chrome
        "firefox": FirefoxOptionsStrategy(),
        "edge": EdgeOptionsStrategy(),
    }

    # Logger for debugging
    _logger = TestLogger.get_logger(__name__)

    @classmethod
    def register_strategy(cls, browser: str, strategy: BrowserOptionsStrategy) -> None:
        """
        Register a new browser options strategy.

        This enables extending the factory with new browsers without modifying the class.
        Follows the Open/Closed Principle.

        Args:
            browser: Browser name
            strategy: Browser options strategy implementation

        Example:
            >>> class SafariOptionsStrategy(BrowserOptionsStrategy):
            ...     def create_options(self, headless=False):
            ...         # Safari-specific options
            ...         pass
            >>> BrowserFactory.register_strategy("safari", SafariOptionsStrategy())
        """
        cls._strategies[browser.lower()] = strategy
        cls._logger.info(f"Registered strategy for browser: {browser}")

    @classmethod
    def create(  # pylint: disable=too-many-positional-arguments
        cls,
        framework: str,
        browser: str = "chrome",
        headless: bool = False,
        timeout: int = 10,
        selenium_grid_url: str | None = None,
        maximize_window: bool = True,
        window_width: int = 1920,
        window_height: int = 1080,
        page_load_timeout: int = 30,
    ) -> BrowserProtocol:
        """
        Create a browser instance based on framework and configuration.

        Args:
            framework: Automation framework ("selenium" or "playwright")
            browser: Browser name ("chrome", "chromium", "firefox", "edge")
            headless: Whether to run in headless mode
            timeout: Default timeout for operations in seconds
            selenium_grid_url: Selenium Grid URL (for Selenium only)
            maximize_window: Whether to maximize the browser window
            window_width: Window width if not maximized
            window_height: Window height if not maximized
            page_load_timeout: Page load timeout in seconds

        Returns:
            BrowserProtocol: Browser adapter implementing BrowserProtocol

        Raises:
            ValueError: If framework or browser is not supported

        Example:
            >>> # Selenium Chrome
            >>> browser = BrowserFactory.create(
            ...     framework="selenium",
            ...     browser="chrome",
            ...     headless=True,
            ...     selenium_grid_url="http://localhost:4444"
            ... )

            >>> # Playwright Firefox
            >>> browser = BrowserFactory.create(
            ...     framework="playwright",
            ...     browser="firefox",
            ...     timeout=15
            ... )
        """
        framework_lower = framework.lower()
        browser_lower = browser.lower()

        cls._logger.info(
            f"Creating {framework_lower} browser: {browser_lower} "
            f"(headless={headless}, timeout={timeout})"
        )

        if framework_lower == "selenium":
            return cls._create_selenium_browser(
                browser_lower,
                headless,
                timeout,
                selenium_grid_url,
                maximize_window,
                window_width,
                window_height,
                page_load_timeout,
            )
        if framework_lower == "playwright":
            return cls._create_playwright_browser(
                browser_lower, headless, timeout, maximize_window, window_width, window_height
            )
        raise ValueError(f"Unsupported framework: {framework}")

    @classmethod
    def _create_selenium_browser(  # pylint: disable=too-many-positional-arguments
        cls,
        browser: str,
        headless: bool,
        timeout: int,
        grid_url: str | None,
        maximize_window: bool,
        window_width: int,
        window_height: int,
        page_load_timeout: int,
    ) -> BrowserProtocol:
        """Create Selenium browser adapter."""
        # Get options strategy
        strategy = cls._strategies.get(browser)
        if not strategy:
            raise ValueError(f"Unsupported browser: {browser}")

        # Create browser options
        options = strategy.create_options(headless)

        # Create WebDriver
        if grid_url:
            # Remote WebDriver (Selenium Grid)
            driver = webdriver.Remote(command_executor=grid_url, options=options)
            cls._logger.info(f"Created remote WebDriver: {grid_url}")
        else:
            # Local WebDriver
            if browser in ("chrome", "chromium"):
                driver = webdriver.Chrome(options=options)
            elif browser == "firefox":
                driver = webdriver.Firefox(options=options)
            elif browser == "edge":
                driver = webdriver.Edge(options=options)
            else:
                raise ValueError(f"Unsupported browser: {browser}")
            cls._logger.info(f"Created local WebDriver: {browser}")

        # Configure driver
        driver.set_page_load_timeout(page_load_timeout)

        if maximize_window:
            driver.maximize_window()
        else:
            driver.set_window_size(window_width, window_height)

        # Wrap in adapter
        return SeleniumBrowserAdapter(driver, timeout=timeout)

    @classmethod
    def _create_playwright_browser(  # pylint: disable=too-many-positional-arguments
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
        return list(cls._strategies.keys())

    @classmethod
    def is_browser_supported(cls, browser: str) -> bool:
        """
        Check if a browser is supported.

        Args:
            browser: Browser name

        Returns:
            True if browser is supported, False otherwise
        """
        return browser.lower() in cls._strategies
