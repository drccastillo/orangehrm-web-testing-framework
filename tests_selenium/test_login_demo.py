"""
Demo test with slow execution to view in VNC.
"""

import time

import pytest

from src.config.config import Config
from src.pages_selenium.login_page import LoginPage
from utils.logger import TestLogger

# Initialize logger
logger = TestLogger.get_logger(__name__)


@pytest.mark.smoke
def test_login_slow_demo(login_page: LoginPage):
    """
    Slow demo test to view in VNC viewer.
    Connect to http://localhost:7900 to watch in browser!
    """
    logger.info("Demo test starting - Connect to http://localhost:7900 to watch!")
    time.sleep(2)

    # Highlight and enter username
    logger.info("Entering username...")
    login_page.highlight_element(login_page.USERNAME_INPUT, duration=1)
    login_page.enter_username(Config.USERNAME)
    time.sleep(1)

    # Highlight and enter password
    logger.info("Entering password...")
    login_page.highlight_element(login_page.PASSWORD_INPUT, duration=1)
    login_page.enter_password(Config.PASSWORD)
    time.sleep(1)

    # Blink and click login button
    logger.info("Clicking login button...")
    login_page.blink_element(login_page.LOGIN_BUTTON, times=2)
    login_page.click_login_button()
    time.sleep(2)

    # Verify success
    current_url = login_page.get_current_url()
    logger.info(f"Current URL: {current_url}")

    assert "dashboard" in current_url.lower()
    logger.info("Login successful!")
    time.sleep(3)
