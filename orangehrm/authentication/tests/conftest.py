"""
Pytest fixtures specific to authentication feature.
Uses NEW clean architecture - config injection with ConfigInterface.
"""
import pytest
from orangehrm.authentication.pages import LoginPage, LoginPageDemo
from orangehrm.authentication.data import valid_admin_user, invalid_user


@pytest.fixture
def login_page(driver, config_provider):
    """
    Create LoginPage with config injection (NEW ARCHITECTURE).

    Args:
        driver: WebDriver fixture from root conftest
        config_provider: ConfigInterface fixture from root conftest

    Returns:
        LoginPage instance with injected config
    """
    page = LoginPage(driver, timeout=config_provider.default_timeout, config=config_provider)
    page.navigate_to_login()
    return page


@pytest.fixture
def valid_user(config_provider):
    """
    Provide valid user data from injected config.

    Args:
        config_provider: ConfigInterface fixture

    Returns:
        User data with username and password from config
    """
    # Return user from config or use default valid_admin_user
    user = valid_admin_user()
    # Override with config values if available
    user.username = config_provider.username
    user.password = config_provider.password
    return user


@pytest.fixture
def invalid_user_data():
    """Provide invalid user data."""
    return invalid_user()


@pytest.fixture
def login_page_demo(driver, config_provider):
    """
    Create LoginPageDemo with visual debugging support (FOR DEMO TESTS ONLY).

    This fixture provides LoginPageDemo which includes VisualDebugMixin
    for highlight_element and blink_element methods.

    Args:
        driver: WebDriver fixture from root conftest
        config_provider: ConfigInterface fixture from root conftest

    Returns:
        LoginPageDemo instance with visual debugging capabilities
    """
    page = LoginPageDemo(driver, timeout=config_provider.default_timeout, config=config_provider)
    page.navigate_to_login()
    return page
