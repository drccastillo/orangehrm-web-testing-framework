"""
Pytest configuration for Playwright-based tests.

This conftest provides fixtures for Playwright browser automation
through the BrowserProtocol abstraction layer.
"""

from datetime import datetime

import pytest

from src.config.environment_config import EnvironmentConfigService
from src.config.protocols import ConfigService
from src.factories.browser_factory import BrowserFactory
from src.pages.leave_page import LeavePage
from src.pages.login_page import LoginPage
from utils.logger import TestLogger

# Initialize logger for conftest
logger = TestLogger.get_logger(__name__)

# Initialize config service for module-level access
_config = EnvironmentConfigService()


def pytest_configure(config):
    """Create necessary directories before running tests."""
    _config.ensure_directories()


@pytest.fixture(scope="session")
def config_service() -> ConfigService:
    """
    Provide configuration service via dependency injection.

    Returns:
        ConfigService implementation (EnvironmentConfigService)
    """
    return _config


@pytest.fixture(scope="session")
def browser_name(request):
    """
    Get browser name from command line or use default.

    Usage:
        pytest --browser=firefox
        pytest --browser=chromium  (default from pytest-playwright)

    Returns:
        Browser name
    """
    # pytest-playwright uses 'chromium', 'firefox', 'webkit'
    # Map to our naming: chromium->chrome
    pw_browser = request.config.getoption("--browser", default="chromium")
    if pw_browser == "chromium":
        return "chrome"  # Our factory uses 'chrome'
    return pw_browser


@pytest.fixture(scope="session")
def headless(request):
    """
    Get headless mode from command line or use default.

    Usage:
        pytest --headed  (to run in headed mode)
        Default is headless mode

    Returns:
        True for headless (default), False if --headed flag is used
    """
    # pytest-playwright uses --headed flag (default is headless)
    headed = request.config.getoption("--headed", default=False)
    return not headed  # Invert: headed=False means headless=True


@pytest.fixture(scope="function")
def browser(browser_name, headless):
    """
    Create Playwright browser instance using BrowserFactory.

    This fixture creates a Playwright browser adapter that implements
    BrowserProtocol for framework-agnostic test code.

    Args:
        browser_name: Browser to use (chrome, chromium, firefox, edge)
        headless: Whether to run in headless mode

    Yields:
        BrowserProtocol: Playwright browser adapter

    Example:
        # Run with default browser (chromium/chrome)
        pytest tests/

        # Run with Firefox
        pytest tests/ --browser=firefox

        # Run in headed mode (default is headless)
        pytest tests/ --headed
    """
    logger.info(f"Creating Playwright browser: {browser_name} (headless={headless})")

    # Create browser using BrowserFactory
    browser_instance = BrowserFactory.create(
        browser=browser_name,
        headless=headless,
        timeout=_config.default_timeout,
        maximize_window=_config.maximize_window,
        window_width=_config.window_width,
        window_height=_config.window_height,
    )

    yield browser_instance

    # Teardown
    logger.info("Closing browser")
    browser_instance.quit()


@pytest.fixture(scope="function")
def login_page(browser, config_service):
    """
    Create LoginPage instance and navigate to login page.

    The LoginPage uses BrowserProtocol for framework-agnostic operations.

    Args:
        browser: Playwright browser adapter (from browser fixture)
        config_service: Configuration service

    Yields:
        LoginPage: Login page instance

    Example:
        def test_login(login_page, config_service):
            login_page.login(config_service.username, config_service.password)
            assert "dashboard" in login_page.get_current_url()
    """
    page = LoginPage(browser, timeout=config_service.default_timeout)
    page.navigate_to(config_service.base_url)
    yield page


@pytest.fixture(scope="function")
def leave_page(browser, config_service, login_page):
    """
    Create LeavePage instance after login.

    The LeavePage uses BrowserProtocol for framework-agnostic operations.

    Args:
        browser: Playwright browser adapter (from browser fixture)
        config_service: Configuration service
        login_page: Login page fixture (to perform login first)

    Yields:
        LeavePage: Leave page instance

    Example:
        def test_navigate_to_leave_list(leave_page):
            leave_page.navigate_to_leave_list()
            assert "leave/viewLeaveList" in leave_page.get_current_url()
    """
    # First login to access leave module
    login_page.login(config_service.username, config_service.password)

    # Create leave page instance
    page = LeavePage(browser, timeout=config_service.default_timeout)

    # Navigate to Leave section
    page.navigate_to_leave_menu()

    # Wait for page to load
    assert page.is_page_loaded(), "Leave page should be loaded after navigation"

    yield page


@pytest.fixture(scope="session")
def test_username(config_service):
    """
    Provide test username for login tests.

    Returns:
        Username string
    """
    return config_service.username


@pytest.fixture(scope="session")
def test_password(config_service):
    """
    Provide test password for login tests.

    Returns:
        Password string
    """
    return config_service.password


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
        if _config.screenshot_on_failure:
            browser = item.funcargs.get("browser")
            if browser:
                _take_screenshot(browser, item.name)


def _take_screenshot(browser, test_name: str):
    """
    Take a screenshot and save it to the screenshots directory.

    Args:
        browser: BrowserProtocol instance (Playwright adapter)
        test_name: Name of the test
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"{test_name}_{timestamp}.png"
    screenshot_path = _config.screenshots_dir / screenshot_name

    try:
        browser.take_screenshot(str(screenshot_path))
        logger.info(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        logger.error(f"Failed to save screenshot: {e}")


def pytest_addoption(parser):
    """
    Add custom command line options for pytest.

    Note: pytest-playwright already provides --browser and --headless options,
    so we don't need to register them again. We use the existing options.

    Args:
        parser: Pytest parser
    """
    # pytest-playwright already provides --browser and --headless options
    # We'll use those directly in our fixtures
