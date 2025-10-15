"""
Unified pytest configuration for framework-agnostic tests.

This conftest supports BOTH Selenium and Playwright through BrowserProtocol.
Use --framework flag to choose: pytest --framework=selenium or --framework=playwright
"""

import argparse
import contextlib
from datetime import datetime

import pytest

from src.config.environment_config import EnvironmentConfigService
from src.config.protocols import ConfigService
from src.factories.browser_factory import BrowserFactory
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
def framework(request):
    """
    Get automation framework from command line or use default (selenium).

    Usage:
        pytest --framework=selenium  (default)
        pytest --framework=playwright

    Returns:
        Framework name (selenium or playwright)
    """
    return request.config.getoption("--framework", default="selenium")


@pytest.fixture(scope="session")
def browser_name(request):
    """
    Get browser name from command line or use default.

    Usage:
        pytest --browser=firefox
        pytest --browser=chrome  (default)

    Returns:
        Browser name
    """
    return request.config.getoption("--browser", default=_config.default_browser)


@pytest.fixture(scope="session")
def headless(request):
    """
    Get headless mode from command line or use default.

    Usage:
        pytest --headless

    Returns:
        True if headless mode, False otherwise
    """
    return request.config.getoption("--headless", default=_config.headless)


@pytest.fixture(scope="function")
def browser(framework, browser_name, headless):
    """
    Create unified browser instance using BrowserFactory.

    This fixture works with ANY automation framework (Selenium, Playwright)
    based on the --framework flag.

    Args:
        framework: Automation framework (selenium or playwright)
        browser_name: Browser to use (chrome, firefox, edge)
        headless: Whether to run in headless mode

    Yields:
        BrowserProtocol: Unified browser adapter

    Example:
        # Run with Selenium (default)
        pytest tests/ --browser=chrome

        # Run with Playwright
        pytest tests/ --framework=playwright --browser=firefox

        # Run headless
        pytest tests/ --framework=selenium --headless
    """
    logger.info(f"Creating {framework} browser: {browser_name} (headless={headless})")

    # Create browser using BrowserFactory
    browser_instance = BrowserFactory.create(
        framework=framework,
        browser=browser_name,
        headless=headless,
        timeout=_config.default_timeout,
        selenium_grid_url=_config.get_selenium_grid_url() if framework == "selenium" else None,
        maximize_window=_config.maximize_window,
        window_width=_config.window_width,
        window_height=_config.window_height,
        page_load_timeout=_config.page_load_timeout,
    )

    yield browser_instance

    # Teardown
    logger.info("Closing browser")
    browser_instance.quit()


@pytest.fixture(scope="function")
def login_page(browser, config_service):
    """
    Create unified LoginPage instance and navigate to login page.

    This LoginPage works with ANY framework through BrowserProtocol.

    Args:
        browser: Browser adapter (from browser fixture)
        config_service: Configuration service

    Yields:
        LoginPage: Unified login page instance

    Example:
        def test_login(login_page, config_service):
            login_page.login(config_service.username, config_service.password)
            assert "dashboard" in login_page.get_current_url()
    """
    page = LoginPage(browser, timeout=config_service.default_timeout)
    page.navigate_to(config_service.base_url)
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
        browser: BrowserProtocol instance
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

    Args:
        parser: Pytest parser
    """
    # Add --framework option (unique to our implementation)
    with contextlib.suppress(ValueError, argparse.ArgumentError):
        parser.addoption(
            "--framework",
            action="store",
            default="selenium",
            help="Automation framework to use: selenium (default) or playwright",
            choices=["selenium", "playwright"],
        )

    # Add --browser option if not already added by pytest-playwright
    with contextlib.suppress(ValueError, argparse.ArgumentError):
        parser.addoption(
            "--browser",
            action="store",
            default=_config.default_browser,
            help="Browser to use: chrome (default), firefox, edge, chromium",
        )

    # Add --headless option if not already added by pytest-playwright
    with contextlib.suppress(ValueError, argparse.ArgumentError):
        parser.addoption(
            "--headless",
            action="store_true",
            default=_config.headless,
            help="Run tests in headless mode",
        )
