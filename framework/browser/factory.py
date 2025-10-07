"""
WebDriver Factory implementing Factory and Strategy patterns.
Provides centralized driver creation with different strategies.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.remote.webdriver import WebDriver
from framework.config.settings import Config
from framework.utils.logger import TestLogger
from framework.utils.exceptions import ConfigurationException


class BrowserStrategy(ABC):
    """Abstract base class for browser strategies (Strategy Pattern)."""

    @abstractmethod
    def create_options(self, headless: bool = False, **kwargs) -> Any:
        """Create browser-specific options."""
        pass

    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """Get browser-specific capabilities."""
        pass


class ChromeStrategy(BrowserStrategy):
    """Chrome browser strategy."""

    def create_options(self, headless: bool = False, **kwargs) -> ChromeOptions:
        """Create Chrome options with best practices."""
        options = ChromeOptions()

        # Performance optimizations
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")

        # Headless mode
        if headless:
            options.add_argument("--headless=new")

        # Window size
        options.add_argument(f"--window-size={Config.WINDOW_WIDTH},{Config.WINDOW_HEIGHT}")

        # Additional custom arguments
        for arg in kwargs.get('extra_args', []):
            options.add_argument(arg)

        # Preferences
        prefs = kwargs.get('prefs', {})
        if prefs:
            options.add_experimental_option("prefs", prefs)

        return options

    def get_capabilities(self) -> Dict[str, Any]:
        """Get Chrome capabilities."""
        return {
            'browserName': 'chrome',
            'goog:loggingPrefs': {'browser': 'ALL'}
        }


class FirefoxStrategy(BrowserStrategy):
    """Firefox browser strategy."""

    def create_options(self, headless: bool = False, **kwargs) -> FirefoxOptions:
        """Create Firefox options with best practices."""
        options = FirefoxOptions()

        # Headless mode
        if headless:
            options.add_argument("--headless")

        # Window size
        options.add_argument(f"--width={Config.WINDOW_WIDTH}")
        options.add_argument(f"--height={Config.WINDOW_HEIGHT}")

        # Additional custom arguments
        for arg in kwargs.get('extra_args', []):
            options.add_argument(arg)

        # Preferences
        prefs = kwargs.get('prefs', {})
        for key, value in prefs.items():
            options.set_preference(key, value)

        return options

    def get_capabilities(self) -> Dict[str, Any]:
        """Get Firefox capabilities."""
        return {
            'browserName': 'firefox',
        }


class EdgeStrategy(BrowserStrategy):
    """Edge browser strategy."""

    def create_options(self, headless: bool = False, **kwargs) -> EdgeOptions:
        """Create Edge options with best practices."""
        options = EdgeOptions()

        # Performance optimizations
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Headless mode
        if headless:
            options.add_argument("--headless")

        # Window size
        options.add_argument(f"--window-size={Config.WINDOW_WIDTH},{Config.WINDOW_HEIGHT}")

        # Additional custom arguments
        for arg in kwargs.get('extra_args', []):
            options.add_argument(arg)

        # Preferences
        prefs = kwargs.get('prefs', {})
        if prefs:
            options.add_experimental_option("prefs", prefs)

        return options

    def get_capabilities(self) -> Dict[str, Any]:
        """Get Edge capabilities."""
        return {
            'browserName': 'MicrosoftEdge',
        }


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


class DriverManager:
    """
    Singleton manager for WebDriver lifecycle (Singleton Pattern).
    Ensures proper cleanup and resource management.
    """

    _instance: Optional['DriverManager'] = None
    _drivers: Dict[str, WebDriver] = {}

    def __new__(cls):
        """Implement Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logger = TestLogger.get_logger(cls.__name__)
        return cls._instance

    def get_driver(
        self,
        driver_id: str = 'default',
        **kwargs
    ) -> WebDriver:
        """
        Get or create a WebDriver instance.

        Args:
            driver_id: Unique identifier for the driver
            **kwargs: Arguments for driver creation

        Returns:
            WebDriver instance
        """
        if driver_id not in self._drivers:
            factory = DriverFactory()
            self._drivers[driver_id] = factory.create_driver(**kwargs)
            self.logger.info(f"Created new driver with ID: {driver_id}")

        return self._drivers[driver_id]

    def quit_driver(self, driver_id: str = 'default') -> None:
        """
        Quit a specific WebDriver instance.

        Args:
            driver_id: Driver identifier
        """
        if driver_id in self._drivers:
            self._drivers[driver_id].quit()
            del self._drivers[driver_id]
            self.logger.info(f"Driver quit: {driver_id}")

    def quit_all_drivers(self) -> None:
        """Quit all WebDriver instances."""
        for driver_id in list(self._drivers.keys()):
            self.quit_driver(driver_id)
        self.logger.info("All drivers quit")

    def __del__(self):
        """Cleanup on destruction."""
        self.quit_all_drivers()
