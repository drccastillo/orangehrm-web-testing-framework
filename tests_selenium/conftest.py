"""
Pytest configuration and fixtures for the test framework.
Contains setup and teardown logic for tests.
"""

from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from src.config.config import Config
from src.pages_selenium.login_page import LoginPage
from utils.logger import TestLogger

# Initialize logger for conftest
logger = TestLogger.get_logger(__name__)


def pytest_configure(config):
    """Create necessary directories before running tests."""
    Config.ensure_directories()


@pytest.fixture(scope="session")
def browser_name(request):
    """
    Get browser name from command line or use default.
    Usage: pytest --browser=firefox
    """
    return request.config.getoption("--browser", default=Config.DEFAULT_BROWSER)


@pytest.fixture(scope="session")
def headless(request):
    """
    Get headless mode from command line or use default.
    Usage: pytest --headless
    """
    return request.config.getoption("--headless", default=Config.HEADLESS)


@pytest.fixture(scope="function")
def driver(browser_name, headless):
    """
    Create and configure WebDriver instance for tests.

    Args:
        browser_name: Name of the browser to use
        headless: Whether to run in headless mode

    Yields:
        WebDriver instance
    """
    # Configure browser options
    options = _get_browser_options(browser_name, headless)

    # Create remote WebDriver connected to Selenium Grid
    driver = webdriver.Remote(command_executor=Config.get_selenium_grid_url(), options=options)

    # Configure driver
    driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
    # Note: Not using implicit waits - relying on explicit waits only for better control

    if Config.MAXIMIZE_WINDOW:
        driver.maximize_window()
    else:
        driver.set_window_size(Config.WINDOW_WIDTH, Config.WINDOW_HEIGHT)

    yield driver

    # Teardown
    driver.quit()


@pytest.fixture(scope="function")
def login_page(driver):
    """
    Create LoginPage instance and navigate to login page.

    Args:
        driver: WebDriver instance

    Yields:
        LoginPage instance
    """
    page = LoginPage(driver, timeout=Config.DEFAULT_TIMEOUT)
    page.navigate_to(Config.BASE_URL)
    yield page


def _get_browser_options(browser_name: str, headless: bool):
    """
    Get browser-specific options.

    Args:
        browser_name: Name of the browser
        headless: Whether to run in headless mode

    Returns:
        Browser options object
    """
    if browser_name.lower() == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        return options

    elif browser_name.lower() == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        return options

    elif browser_name.lower() == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return options

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure.

    Args:
        item: Test item
        call: Test call information
    """
    outcome = yield
    report = outcome.get_result()

    # Take screenshot on test failure
    if report.when == "call" and report.failed:
        logger.error(f"Test failed: {item.name}")
        if Config.SCREENSHOT_ON_FAILURE:
            driver = item.funcargs.get("driver")
            if driver:
                _take_screenshot(driver, item.name)


def _take_screenshot(driver, test_name: str):
    """
    Take a screenshot and save it to the screenshots directory.

    Args:
        driver: WebDriver instance
        test_name: Name of the test
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"{test_name}_{timestamp}.png"
    screenshot_path = Config.SCREENSHOTS_DIR / screenshot_name

    try:
        driver.save_screenshot(str(screenshot_path))
        logger.info(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        logger.error(f"Failed to save screenshot: {e}")


def pytest_addoption(parser):
    """
    Add custom command line options for pytest.

    Args:
        parser: Pytest parser
    """
    parser.addoption(
        "--browser",
        action="store",
        default=Config.DEFAULT_BROWSER,
        help="Browser to use for tests: chrome, firefox, edge",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=Config.HEADLESS,
        help="Run tests in headless mode",
    )
