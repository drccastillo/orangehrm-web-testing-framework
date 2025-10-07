"""
Global Pytest configuration for OrangeHRM Test Automation.

This conftest provides global fixtures and configuration available to all tests.
Feature-specific fixtures should be defined in feature/tests/conftest.py
"""
import pytest
from datetime import datetime
from pathlib import Path

from framework.browser import DriverFactory, DriverManager
from framework.config import Config
from framework.utils import TestLogger


# Initialize logger
logger = TestLogger.get_logger(__name__)


def pytest_configure(config):
    """Configure pytest session."""
    logger.info("=== Starting OrangeHRM Test Session ===")
    logger.info("Configuring pytest with Screaming Architecture")
    Config.ensure_directories()

    # Register custom markers
    config.addinivalue_line("markers", "authentication: Authentication feature tests")
    config.addinivalue_line("markers", "employees: Employee management tests")
    config.addinivalue_line("markers", "leave: Leave management tests")
    config.addinivalue_line("markers", "smoke: Quick smoke tests")
    config.addinivalue_line("markers", "regression: Full regression tests")


# ============================================
# Session-scoped fixtures (Framework Layer)
# ============================================

@pytest.fixture(scope="session")
def browser_name(request):
    """
    Get browser name from command line or config.

    Usage: pytest --browser=firefox
    """
    return request.config.getoption("--browser", default=Config.DEFAULT_BROWSER)


@pytest.fixture(scope="session")
def headless(request):
    """
    Get headless mode from command line or config.

    Usage: pytest --headless
    """
    return request.config.getoption("--headless", default=Config.HEADLESS)


@pytest.fixture(scope="session")
def driver_factory():
    """
    Provide DriverFactory instance.

    This is a session-scoped factory for creating drivers.
    """
    return DriverFactory()


@pytest.fixture(scope="session")
def driver_manager():
    """
    Provide DriverManager singleton instance.

    Manages driver lifecycle and cleanup.
    """
    manager = DriverManager()
    yield manager
    # Cleanup all drivers at end of session
    manager.quit_all_drivers()


# ============================================
# Function-scoped fixtures
# ============================================

@pytest.fixture(scope="function")
def driver(driver_factory, browser_name, headless):
    """
    Create WebDriver using Factory pattern.

    This is the primary driver fixture used by most tests.
    Creates a new driver for each test function.

    Args:
        driver_factory: DriverFactory instance
        browser_name: Browser to use
        headless: Whether to run headless

    Yields:
        WebDriver instance

    Example:
        def test_something(driver):
            driver.get("https://example.com")
    """
    logger.info(f"Creating driver: browser={browser_name}, headless={headless}")

    driver = driver_factory.create_driver(
        browser=browser_name,
        headless=headless,
        remote=True
    )

    yield driver

    # Teardown
    logger.info("Closing driver")
    driver.quit()


# ============================================
# Hooks
# ============================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook for capturing test results and taking screenshots on failure.

    This hook runs after each test and captures screenshots if the test fails.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        logger.error(f"❌ Test failed: {item.name}")
        logger.error(f"   Location: {item.location}")

        if Config.SCREENSHOT_ON_FAILURE:
            driver = item.funcargs.get('driver')
            if driver:
                _take_screenshot(driver, item.name, item.nodeid)


def _take_screenshot(driver, test_name: str, node_id: str = ""):
    """
    Take screenshot with metadata on test failure.

    Args:
        driver: WebDriver instance
        test_name: Name of the failed test
        node_id: Full pytest node ID
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    screenshot_name = f"{test_name}_{timestamp}.png"
    screenshot_path = Config.SCREENSHOTS_DIR / screenshot_name

    try:
        driver.save_screenshot(str(screenshot_path))
        logger.info(f"📸 Screenshot saved: {screenshot_path}")

        # Save metadata
        metadata_path = screenshot_path.with_suffix('.txt')
        with open(metadata_path, 'w') as f:
            f.write(f"Test: {test_name}\n")
            f.write(f"Node ID: {node_id}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"URL: {driver.current_url}\n")
            f.write(f"Window size: {driver.get_window_size()}\n")

    except Exception as e:
        logger.error(f"Failed to save screenshot: {e}")


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--browser",
        action="store",
        default=Config.DEFAULT_BROWSER,
        help="Browser to use: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=Config.HEADLESS,
        help="Run tests in headless mode"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection.

    Auto-adds markers based on test location and naming conventions.
    """
    for item in items:
        # Auto-mark tests by feature
        if "authentication" in item.nodeid:
            item.add_marker(pytest.mark.authentication)
        if "employees" in item.nodeid:
            item.add_marker(pytest.mark.employees)

        # Auto-mark slow tests
        if "slow" in item.name.lower():
            item.add_marker(pytest.mark.slow)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Add custom summary at the end of test run."""
    logger.info("=== Test Session Complete ===")
    logger.info(f"Exit status: {exitstatus}")
