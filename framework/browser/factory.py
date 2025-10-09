"""
WebDriver Factory implementing Factory and Strategy patterns.
Provides centralized driver creation with different strategies.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.remote.webdriver import WebDriver
from framework.config.settings import Config
from framework.config.defaults import FrameworkDefaults, BrowserDefaults
from framework.utils.logger import TestLogger
from framework.utils.exceptions import ConfigurationException


class BrowserStrategy(ABC):
    """
    Abstract base class for browser strategies (Strategy Pattern + Template Method).

    Provides common functionality while allowing browser-specific customization.
    """

    @abstractmethod
    def _create_browser_options(self) -> Any:
        """Create browser-specific options object (must be implemented by subclasses)."""
        pass

    @abstractmethod
    def _apply_headless(self, options: Any, headless: bool) -> None:
        """Apply headless mode (browser-specific syntax)."""
        pass

    def create_options(self, headless: bool = False, **kwargs) -> Any:
        """
        Template method for creating browser options.

        Defines the skeleton of the algorithm, delegating browser-specific
        steps to subclasses.

        Args:
            headless: Whether to run in headless mode
            **kwargs: Additional options (extra_args, prefs)

        Returns:
            Browser-specific options object
        """
        options = self._create_browser_options()
        self._apply_common_arguments(options)
        self._apply_headless(options, headless)
        self._apply_window_size(options)
        self._apply_custom_preferences(options, kwargs.get('prefs', {}))
        self._apply_extra_arguments(options, kwargs.get('extra_args', []))
        return options

    def _apply_common_arguments(self, options: Any) -> None:
        """Apply common arguments to all browsers."""
        for arg in BrowserDefaults.COMMON_BROWSER_ARGS:
            options.add_argument(arg)

    def _apply_window_size(self, options: Any) -> None:
        """Apply window size configuration."""
        options.add_argument(
            f"--window-size={Config.WINDOW_WIDTH},{Config.WINDOW_HEIGHT}"
        )

    def _apply_custom_preferences(self, options: Any, prefs: Dict) -> None:
        """Apply custom preferences (override in subclass if needed)."""
        if prefs and hasattr(options, 'add_experimental_option'):
            options.add_experimental_option("prefs", prefs)

    def _apply_extra_arguments(self, options: Any, extra_args: List[str]) -> None:
        """Apply additional custom arguments."""
        for arg in extra_args:
            options.add_argument(arg)

    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """Get browser-specific capabilities."""
        pass


class ChromeStrategy(BrowserStrategy):
    """Chrome browser strategy with performance optimizations."""

    def _create_browser_options(self) -> ChromeOptions:
        """Create Chrome options object."""
        options = ChromeOptions()
        # Apply Chrome-specific performance optimizations
        for arg in BrowserDefaults.CHROME_PERFORMANCE_ARGS:
            options.add_argument(arg)
        return options

    def _apply_headless(self, options: ChromeOptions, headless: bool) -> None:
        """Apply Chrome headless mode (new headless syntax)."""
        if headless:
            options.add_argument(BrowserDefaults.CHROME_HEADLESS_ARG)

    def get_capabilities(self) -> Dict[str, Any]:
        """Get Chrome capabilities with browser logging."""
        return {
            'browserName': 'chrome',
            'goog:loggingPrefs': {'browser': 'ALL'}
        }


class FirefoxStrategy(BrowserStrategy):
    """Firefox browser strategy."""

    def _create_browser_options(self) -> FirefoxOptions:
        """Create Firefox options object."""
        return FirefoxOptions()

    def _apply_headless(self, options: FirefoxOptions, headless: bool) -> None:
        """Apply Firefox headless mode."""
        if headless:
            options.add_argument(BrowserDefaults.FIREFOX_HEADLESS_ARG)

    def _apply_window_size(self, options: FirefoxOptions) -> None:
        """Apply window size (Firefox uses different syntax)."""
        options.add_argument(f"--width={Config.WINDOW_WIDTH}")
        options.add_argument(f"--height={Config.WINDOW_HEIGHT}")

    def _apply_custom_preferences(self, options: FirefoxOptions, prefs: Dict) -> None:
        """Firefox uses set_preference instead of experimental options."""
        for key, value in prefs.items():
            options.set_preference(key, value)

    def get_capabilities(self) -> Dict[str, Any]:
        """Get Firefox capabilities."""
        return {'browserName': 'firefox'}


class EdgeStrategy(BrowserStrategy):
    """Edge browser strategy (Chromium-based)."""

    def _create_browser_options(self) -> EdgeOptions:
        """Create Edge options object."""
        return EdgeOptions()

    def _apply_headless(self, options: EdgeOptions, headless: bool) -> None:
        """Apply Edge headless mode."""
        if headless:
            options.add_argument(BrowserDefaults.EDGE_HEADLESS_ARG)

    def get_capabilities(self) -> Dict[str, Any]:
        """Get Edge capabilities."""
        return {'browserName': 'MicrosoftEdge'}


class DriverFactory:
    """
    Factory class for creating WebDriver instances (Factory Pattern).

    Supports:
    - Local driver creation
    - Remote driver (Selenium Grid)
    - Different browser strategies
    - Custom capabilities and options
    """

    _strategies: Dict[str, BrowserStrategy] = {
        'chrome': ChromeStrategy(),
        'firefox': FirefoxStrategy(),
        'edge': EdgeStrategy(),
    }

    def __init__(self):
        """Initialize the driver factory."""
        self.logger = TestLogger.get_logger(self.__class__.__name__)

    @classmethod
    def register_strategy(cls, browser_name: str, strategy: BrowserStrategy) -> None:
        """
        Register a new browser strategy.

        Args:
            browser_name: Name of the browser
            strategy: Browser strategy instance
        """
        cls._strategies[browser_name.lower()] = strategy

    def create_driver(
        self,
        browser: str = None,
        headless: bool = None,
        remote: bool = True,
        grid_url: str = None,
        **kwargs
    ) -> WebDriver:
        """
        Create a WebDriver instance.

        Args:
            browser: Browser name (chrome, firefox, edge)
            headless: Run in headless mode
            remote: Use remote driver (Selenium Grid)
            grid_url: Selenium Grid URL
            **kwargs: Additional options (extra_args, prefs, capabilities)

        Returns:
            WebDriver instance

        Raises:
            ConfigurationException: If browser is not supported
        """
        browser = (browser or Config.DEFAULT_BROWSER).lower()
        headless = headless if headless is not None else Config.HEADLESS
        grid_url = grid_url or Config.get_selenium_grid_url()

        self.logger.info(f"Creating WebDriver: browser={browser}, headless={headless}, remote={remote}")

        # Get browser strategy
        strategy = self._strategies.get(browser)
        if not strategy:
            raise ConfigurationException(
                'browser',
                f"Unsupported browser: {browser}. Supported: {list(self._strategies.keys())}"
            )

        # Create options
        options = strategy.create_options(headless=headless, **kwargs)

        # Merge capabilities
        capabilities = strategy.get_capabilities()
        custom_caps = kwargs.get('capabilities', {})
        capabilities.update(custom_caps)

        # Create driver
        if remote:
            driver = webdriver.Remote(
                command_executor=grid_url,
                options=options
            )
        else:
            driver = self._create_local_driver(browser, options)

        # Configure driver
        self._configure_driver(driver)

        self.logger.info(f"WebDriver created successfully: {browser}")
        return driver

    def _create_local_driver(self, browser: str, options: Any) -> WebDriver:
        """
        Create local WebDriver instance.

        Args:
            browser: Browser name
            options: Browser options

        Returns:
            WebDriver instance
        """
        if browser == 'chrome':
            return webdriver.Chrome(options=options)
        elif browser == 'firefox':
            return webdriver.Firefox(options=options)
        elif browser == 'edge':
            return webdriver.Edge(options=options)
        else:
            raise ConfigurationException('browser', f"Unsupported browser: {browser}")

    def _configure_driver(self, driver: WebDriver) -> None:
        """
        Configure WebDriver instance with common settings.

        Args:
            driver: WebDriver instance
        """
        driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

        if Config.MAXIMIZE_WINDOW:
            driver.maximize_window()
        else:
            driver.set_window_size(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)

        self.logger.debug("WebDriver configured with timeouts and window settings")
