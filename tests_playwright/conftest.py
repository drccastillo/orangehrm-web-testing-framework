"""
Pytest configuration and fixtures for Playwright tests.
Contains setup and teardown logic for Playwright-based tests.
"""

from datetime import datetime
from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext, Page

from src.config.config import Config
from src.config.environment_config import EnvironmentConfigService
from src.config.protocols import ConfigService
from src.pages_playwright.login_page_pw import LoginPagePW
from utils.logger import TestLogger

# Initialize logger for conftest
logger = TestLogger.get_logger(__name__)


def pytest_configure(config):
    """Create necessary directories before running tests."""
    Config.ensure_directories()

    # Create Playwright-specific directories
    reports_dir = Path(__file__).parent.parent / "reports_playwright"
    screenshots_dir = reports_dir / "screenshots"
    videos_dir = reports_dir / "videos"
    traces_dir = reports_dir / "traces"

    for directory in [reports_dir, screenshots_dir, videos_dir, traces_dir]:
        directory.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def config_service() -> ConfigService:
    """
    Provide configuration service via dependency injection.

    This replaces direct Config class access, enabling testability.
    Tests should inject config_service instead of using Config.X directly.

    Returns:
        ConfigService implementation (EnvironmentConfigService)
    """
    return EnvironmentConfigService()


@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig):
    """
    Configure browser launch arguments.

    Returns:
        Dict of browser launch arguments
    """
    # Get headless from pytestconfig, default to headless unless --headed is specified
    headed = pytestconfig.getoption("--headed", default=False)

    return {
        "headless": not headed,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_type_launch_args):
    """
    Configure browser context arguments.

    Returns:
        Dict of browser context arguments

    Note:
        Videos are currently recorded for ALL tests to reports_playwright/videos/.
        To save disk space and only record on failures, you can:
        1. Set record_video_dir conditionally based on test outcome, or
        2. Use pytest-playwright's built-in --video option:
           - pytest --video=retain-on-failure (recommended)
           - pytest --video=on (record all)
           - pytest --video=off (record none)
    """
    return {
        "viewport": {"width": Config.WINDOW_WIDTH, "height": Config.WINDOW_HEIGHT},
        "ignore_https_errors": True,
        # Video recording: records all tests to this directory
        "record_video_dir": str(Path(__file__).parent.parent / "reports_playwright" / "videos"),
        "record_video_size": {"width": 1280, "height": 720},
    }


@pytest.fixture(scope="function")
def page(context: BrowserContext):
    """
    Override pytest-playwright's page fixture with custom configuration.
    This ensures all tests get a properly configured page instance.

    Args:
        context: Browser context from pytest-playwright

    Yields:
        Configured Page instance
    """
    # Create new page from context
    page = context.new_page()

    # Set default timeout (CRITICAL: this now actually applies to all tests)
    page.set_default_timeout(Config.DEFAULT_TIMEOUT * 1000)  # milliseconds

    # Set viewport size if not maximized
    if not Config.MAXIMIZE_WINDOW:
        page.set_viewport_size({"width": Config.WINDOW_WIDTH, "height": Config.WINDOW_HEIGHT})

    yield page

    # Teardown
    page.close()


@pytest.fixture(scope="function")
def login_page_pw(page: Page):
    """
    Create LoginPagePW instance and navigate to login page.

    Args:
        page: Playwright Page instance

    Yields:
        LoginPagePW instance
    """
    login_page = LoginPagePW(page, timeout=Config.DEFAULT_TIMEOUT)
    login_page.navigate_to(Config.BASE_URL)
    login_page.wait_for_login_page_to_load()

    yield login_page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test results and take screenshots on failure.

    Args:
        item: Test item
        call: Test call information

    Note:
        pytest-playwright automatically captures screenshots on failure
        to test-results/ directory. This hook provides additional custom
        screenshot capture to reports_playwright/screenshots/.
    """
    outcome = yield
    report = outcome.get_result()

    # Take screenshot on test failure
    if report.when == "call" and report.failed and Config.SCREENSHOT_ON_FAILURE:
        logger.error(f"Test failed: {item.name}")

        # Try to get page object from any available fixture
        page_obj = None
        if "page" in item.funcargs:
            page_obj = item.funcargs["page"]
        elif "login_page_pw" in item.funcargs:
            page_obj = item.funcargs["login_page_pw"].page

        if page_obj:
            _take_screenshot(page_obj, item.name)


def _take_screenshot(page: Page, test_name: str):
    """
    Take a screenshot and save it to the screenshots directory.

    Args:
        page: Playwright Page instance
        test_name: Name of the test
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"{test_name}_{timestamp}.png"
    screenshot_dir = Path(__file__).parent.parent / "reports_playwright" / "screenshots"
    screenshot_path = screenshot_dir / screenshot_name

    try:
        page.screenshot(path=str(screenshot_path), full_page=True)
        logger.info(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        logger.error(f"Failed to save screenshot: {e}")


# Browser-specific configurations (pytest-playwright integration)
# Note: These fixtures are currently NOT used because pytest-playwright requires
# a single fixture named exactly 'browser_type_launch_args' (without browser suffix).
# To use browser-specific configs, you need to modify browser_type_launch_args
# fixture to check pytestconfig.getoption("--browser-name") and return different
# configs based on the selected browser.


@pytest.fixture(scope="session")
def browser_type_launch_args_chromium():
    """
    Chromium-specific launch arguments.

    IMPORTANT: This fixture is NOT automatically used by pytest-playwright.
    It's kept here as a reference. To activate, merge these args into
    browser_type_launch_args fixture with conditional logic.
    """
    return {
        "args": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
        ]
    }


@pytest.fixture(scope="session")
def browser_type_launch_args_firefox():
    """
    Firefox-specific launch arguments.

    IMPORTANT: This fixture is NOT automatically used by pytest-playwright.
    It's kept here as a reference. To activate, merge these args into
    browser_type_launch_args fixture with conditional logic.
    """
    return {
        "firefox_user_prefs": {
            "browser.cache.disk.enable": False,
            "browser.cache.memory.enable": False,
        }
    }
