"""
Demo test with slow execution for visual debugging with Playwright.
Demonstrates highlight_element and blink_element methods.
"""

import re
from pathlib import Path

import pytest
from playwright.sync_api import expect

from src.config.config import Config
from src.pages_playwright.login_page_pw import LoginPagePW
from utils.logger import TestLogger

# Initialize logger
logger = TestLogger.get_logger(__name__)


@pytest.mark.smoke
def test_login_visual_demo_pw(login_page_pw: LoginPagePW):
    """
    Visual demo test using Playwright's highlight and blink features.

    Note:
        - Run with --headed to watch the test execute in browser
        - Video is automatically recorded to reports_playwright/videos/
        - Screenshots on failure are saved to reports_playwright/screenshots/

    Usage:
        pytest tests_playwright/test_login_demo_pw.py --headed -v
    """
    logger.info("Playwright demo test starting - run with --headed to watch!")

    # Visual delay for demo purposes (Playwright-style)
    login_page_pw.page.wait_for_timeout(2000)  # 2 seconds

    # Highlight and enter username
    logger.info("Highlighting and entering username...")
    login_page_pw.highlight_element(login_page_pw.locators.USERNAME_INPUT, duration=1, color="blue")
    login_page_pw.enter_username(Config.USERNAME)
    login_page_pw.page.wait_for_timeout(1000)

    # Highlight and enter password
    logger.info("Highlighting and entering password...")
    login_page_pw.highlight_element(
        login_page_pw.locators.PASSWORD_INPUT, duration=1, color="green"
    )
    login_page_pw.enter_password(Config.PASSWORD)
    login_page_pw.page.wait_for_timeout(1000)

    # Blink and click login button
    logger.info("Blinking and clicking login button...")
    login_page_pw.blink_element(login_page_pw.locators.LOGIN_BUTTON, times=3, color="red")
    login_page_pw.click_login_button()

    # Wait for navigation to complete
    login_page_pw.page.wait_for_timeout(2000)

    # Verify successful login using Playwright's expect (best practice)
    current_url = login_page_pw.get_current_url()
    logger.info(f"Current URL: {current_url}")

    # Playwright-style assertion with auto-waiting
    expect(login_page_pw.page).to_have_url(re.compile(r".*dashboard.*"))

    logger.info("Login successful - demo completed!")
    login_page_pw.page.wait_for_timeout(2000)


@pytest.mark.smoke
def test_login_demo_with_screenshots_pw(login_page_pw: LoginPagePW):
    """
    Demo test showing screenshot capabilities at different stages.
    Demonstrates visual debugging workflow with Playwright.

    Usage:
        pytest tests_playwright/test_login_demo_pw.py::test_login_demo_with_screenshots_pw --headed
    """
    screenshots_dir = Path(__file__).parent.parent / "reports_playwright" / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    # Screenshot 1: Initial login page
    login_page_pw.highlight_element(login_page_pw.locators.LOGIN_LOGO, duration=1)
    login_page_pw.screenshot(str(screenshots_dir / "01_login_page_loaded.png"), full_page=True)
    logger.info("Screenshot 1: Login page loaded")

    # Screenshot 2: After entering credentials
    login_page_pw.enter_username(Config.USERNAME)
    login_page_pw.enter_password(Config.PASSWORD)
    login_page_pw.highlight_element(login_page_pw.locators.LOGIN_BUTTON, duration=1, color="green")
    login_page_pw.screenshot(str(screenshots_dir / "02_credentials_entered.png"), full_page=True)
    logger.info("Screenshot 2: Credentials entered")

    # Screenshot 3: Before clicking login
    login_page_pw.blink_element(login_page_pw.locators.LOGIN_BUTTON, times=2)
    login_page_pw.screenshot(str(screenshots_dir / "03_ready_to_login.png"), full_page=False)
    logger.info("Screenshot 3: Ready to login")

    # Perform login
    login_page_pw.click_login_button()
    login_page_pw.page.wait_for_timeout(2000)

    # Screenshot 4: Dashboard after login
    login_page_pw.screenshot(str(screenshots_dir / "04_dashboard_after_login.png"), full_page=True)
    logger.info("Screenshot 4: Dashboard loaded")

    # Verify success with Playwright expect
    expect(login_page_pw.page).to_have_url(re.compile(r".*dashboard.*"))
    logger.info("Demo with screenshots completed successfully!")


@pytest.mark.smoke
def test_login_demo_blink_variations_pw(login_page_pw: LoginPagePW):
    """
    Demo showcasing different blink variations and colors.
    Educational test to demonstrate visual debugging capabilities.

    Usage:
        pytest tests_playwright/test_login_demo_pw.py::test_login_demo_blink_variations_pw --headed -s
    """
    # Blink username field with different colors
    logger.info("Blinking username field - blue color...")
    login_page_pw.blink_element(login_page_pw.locators.USERNAME_INPUT, times=2, color="blue")

    # Blink password field with green
    logger.info("Blinking password field - green color...")
    login_page_pw.blink_element(login_page_pw.locators.PASSWORD_INPUT, times=2, color="green")

    # Blink login button multiple times with red
    logger.info("Blinking login button - red color (5 times)...")
    login_page_pw.blink_element(login_page_pw.locators.LOGIN_BUTTON, times=5, color="red")

    # Perform actual login
    login_page_pw.login(Config.USERNAME, Config.PASSWORD)

    # Verify using Playwright's built-in assertions
    expect(login_page_pw.page).to_have_url(re.compile(r".*dashboard.*"))
    logger.info("Blink variations demo completed!")
