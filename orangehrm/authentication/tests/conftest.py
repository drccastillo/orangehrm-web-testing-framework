"""
Pytest fixtures specific to authentication feature.
"""
import pytest
from framework.config import Config
from orangehrm.authentication.pages import LoginPage
from orangehrm.authentication.data import valid_admin_user, invalid_user


@pytest.fixture
def login_page(driver):
    """
    Create LoginPage and navigate to login URL.

    Args:
        driver: WebDriver fixture from root conftest

    Returns:
        LoginPage instance
    """
    page = LoginPage(driver, timeout=Config.DEFAULT_TIMEOUT)
    page.navigate_to(Config.BASE_URL)
    return page


@pytest.fixture
def valid_user():
    """Provide valid user data."""
    return valid_admin_user()


@pytest.fixture
def invalid_user_data():
    """Provide invalid user data."""
    return invalid_user()
