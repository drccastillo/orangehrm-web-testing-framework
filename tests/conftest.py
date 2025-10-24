"""
Pytest configuration for Playwright-based tests.

This conftest provides fixtures for Playwright browser automation
using native Playwright Page objects.
"""

# pylint: disable=import-error  # src and utils modules are in project root
# pylint: disable=redefined-outer-name  # pytest fixtures pattern
import re
from datetime import datetime

import pytest
from playwright.sync_api import expect

from src.config.environment_config import EnvironmentConfigService
from src.config.protocols import ConfigService
from src.factories.browser_factory import BrowserFactory
from src.ui.pages.base_page import BasePage
from src.ui.pages.login.login_page import LoginPage
from utils.logger import TestLogger

# LeaveListPage is now created by NavigationHeader.navigate_to_leave()
# from src.ui.pages.leave.list.leave_list_page import LeaveListPage

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


@pytest.fixture
def browser(browser_name, headless, config_service):
    """
    Create Playwright Page instance using BrowserFactory.

    This fixture creates a Playwright Page directly, eliminating adapter overhead.

    Args:
        browser_name: Browser to use (chrome, chromium, firefox, edge)
        headless: Whether to run in headless mode
        config_service: Configuration service

    Yields:
        Page: Playwright Page instance

    Example:
        # Run with default browser (chromium/chrome)
        pytest tests/

        # Run with Firefox
        pytest tests/ --browser=firefox

        # Run in headed mode (default is headless)
        pytest tests/ --headed
    """
    logger.info(f"Creating Playwright browser: {browser_name} (headless={headless})")

    # Create browser using BrowserFactory - returns (Page, Playwright)
    page, playwright = BrowserFactory.create(
        browser=browser_name,
        headless=headless,
        timeout=config_service.default_timeout,
        maximize_window=config_service.maximize_window,
        window_width=config_service.window_width,
        window_height=config_service.window_height,
    )

    yield page

    # Teardown with robust error handling
    logger.info("Closing browser")

    # Close page
    try:
        page.close()
        logger.debug("Page closed successfully")
    except Exception as e:
        logger.error(f"Error closing page: {e}")

    # Close context
    try:
        if page.context:
            page.context.close()
            logger.debug("Context closed successfully")
    except Exception as e:
        logger.error(f"Error closing context: {e}")

    # Close browser
    try:
        if page.context and page.context.browser:
            page.context.browser.close()
            logger.debug("Browser closed successfully")
    except Exception as e:
        logger.error(f"Error closing browser: {e}")

    # Stop Playwright
    try:
        playwright.stop()
        logger.debug("Playwright stopped successfully")
    except Exception as e:
        logger.error(f"Error stopping Playwright: {e}")


@pytest.fixture
def login_page(browser, config_service):
    """
    Create LoginPage instance and navigate to login page.

    Args:
        browser: Playwright Page instance (from browser fixture)
        config_service: Configuration service

    Yields:
        LoginPage: Login page instance

    Example:
        def test_login(login_page, config_service):
            login_page.login(config_service.username, config_service.password)
            expect(login_page.page).to_have_url(re.compile(r"dashboard", re.IGNORECASE))
    """
    page = LoginPage(browser, timeout=config_service.default_timeout)
    page.navigate_to(config_service.base_url)

    yield page  # noqa: PT022  # Keep yield for consistency and future teardown


@pytest.fixture
def dashboard_page(browser, config_service, login_page):
    """
    Create BasePage instance at Dashboard (default landing page after login).

    This fixture is ideal for navigation and cross-module tests as it starts
    at the Dashboard, which is the default page users see after login.

    Args:
        browser: Playwright Page instance (from browser fixture)
        config_service: Configuration service
        login_page: Login page fixture (to perform login first)

    Yields:
        BasePage: Page object at Dashboard with nav_header available

    Cleanup:
        Optionally logs out to ensure clean state between tests.

    Example:
        def test_navigate_to_leave(dashboard_page):
            nav = dashboard_page.nav_header
            nav.navigate_to_leave()
            expect(dashboard_page.page).to_have_url(re.compile(r"leave", re.IGNORECASE))
    """
    # Setup: Login and verify we're at Dashboard
    login_page.login(config_service.username, config_service.password)

    # Create BasePage instance (Dashboard is default landing page)
    page = BasePage(browser, timeout=config_service.default_timeout)

    # Verify we're on dashboard (default after login)
    expect(page.page).to_have_url(re.compile(r"dashboard", re.IGNORECASE), timeout=10000)
    logger.info("Dashboard page loaded successfully")

    yield page

    # Teardown: Logout to ensure clean state for next test
    try:
        if hasattr(page, "nav_header") and page.nav_header:
            logger.debug("Logging out in dashboard_page teardown")
            page.nav_header.logout()
            logger.info("Logout successful in teardown")
    except Exception as e:
        logger.debug(f"Logout in teardown skipped or failed: {e}")
        # Not critical - browser fixture will close everything anyway


@pytest.fixture
def leave_page(dashboard_page):
    """
    Create LeaveListPage instance after navigating to Leave from Dashboard.

    This fixture starts from Dashboard (already logged in via dashboard_page)
    and navigates to the Leave module using NavigationHeader.

    Args:
        dashboard_page: Dashboard page fixture (already logged in)

    Yields:
        LeaveListPage: Leave page instance ready for interaction

    Cleanup:
        No explicit cleanup needed - dashboard_page fixture handles logout.

    Example:
        def test_apply_leave(leave_page):
            leave_page.navigate_to_apply_leave()
            # ... test leave-specific functionality

    Note:
        NavigationHeader.navigate_to_leave() now returns the page object directly,
        eliminating the need to manually create LeaveListPage instance.
    """
    # Navigate to Leave from Dashboard - nav_header returns the page object
    page = dashboard_page.nav_header.navigate_to_leave()

    # Wait for page to load - verify page title is visible
    expect(page.page_title).to_be_visible(timeout=10000)
    logger.info("Leave page loaded successfully")

    yield page  # noqa: PT022  # Keep yield for consistency and future teardown


@pytest.fixture
def leave_period_page(leave_page):
    """
    Create LeavePeriodPage instance by navigating from Leave page.

    This fixture:
    1. Starts from leave_page (already in Leave module context)
    2. Uses leave_page.navigate_to_leave_period() to get page object
    3. Returns LeavePeriodPage instance ready for testing

    Args:
        leave_page: Leave page fixture (already in Leave module)

    Yields:
        LeavePeriodPage: Leave Period page instance ready for interaction

    Example:
        def test_configure_period(leave_period_page):
            leave_period_page.configure_leave_period("January", "01")
            leave_period_page.save()

    Note:
        LeaveBasePage.navigate_to_leave_period() now returns the page object directly,
        eliminating the need to manually create LeavePeriodPage instance or pass
        browser/config_service parameters.

        Hierarchy: dashboard -> leave -> leave_period (clean and logical)
    """
    # Navigate to Leave Period from Leave page - returns the page object
    page = leave_page.navigate_to_leave_period()

    # Wait for page to load - verify page title is visible
    expect(page.page_title).to_be_visible(timeout=10000)

    logger.info("Leave Period page loaded successfully")
    yield page  # noqa: PT022


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure.

    Single Responsibility: Reporting only. Screenshot capture delegated.

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
            page = item.funcargs.get("browser")  # Now a Page instance
            if page:
                _take_screenshot(page, item.name)


def _take_screenshot(page, test_name: str):
    """
    Take a screenshot and save it to the screenshots directory.

    Args:
        page: Playwright Page instance
        test_name: Name of the test
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"{test_name}_{timestamp}.png"
    screenshot_path = _config.screenshots_dir / screenshot_name

    try:
        page.screenshot(path=str(screenshot_path))
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
