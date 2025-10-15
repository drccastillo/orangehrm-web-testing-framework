"""
Demo test with slow execution to view in VNC.
"""

import time

import pytest

from src.pages.protocols import LoginPageProtocol
from utils.logger import TestLogger

# Initialize logger
logger = TestLogger.get_logger(__name__)


@pytest.mark.smoke
def test_login_slow_demo(login_page: LoginPageProtocol, test_username: str, test_password: str):
    """
    Slow demo test to view in VNC viewer.
    Connect to http://localhost:7900 to watch in browser!
    """
    logger.info("Demo test starting - Connect to http://localhost:7900 to watch!")
    time.sleep(2)

    # Enter username
    logger.info("Entering username...")
    login_page.enter_username(test_username)
    time.sleep(1)

    # Enter password
    logger.info("Entering password...")
    login_page.enter_password(test_password)
    time.sleep(1)

    # Click login button
    logger.info("Clicking login button...")
    login_page.click_login_button()
    time.sleep(2)

    # Verify success
    current_url = login_page.get_current_url()
    logger.info(f"Current URL: {current_url}")

    assert "dashboard" in current_url.lower()
    logger.info("Login successful!")
    time.sleep(3)
