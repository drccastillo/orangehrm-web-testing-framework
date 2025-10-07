"""
Common workflows and actions used across multiple features.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from framework.config import Config
from orangehrm.authentication.pages.login_page import LoginPage
from shared.components.navigation import OrangeHRMNavigation


def quick_login(driver: WebDriver, username: str = None, password: str = None) -> None:
    """
    Perform a quick login without Page Objects.
    Useful for test setup when login itself is not being tested.

    Args:
        driver: WebDriver instance
        username: Username (defaults to Config.USERNAME)
        password: Password (defaults to Config.PASSWORD)
    """
    username = username or Config.USERNAME
    password = password or Config.PASSWORD

    login_page = LoginPage(driver)
    login_page.navigate_to(Config.BASE_URL)
    login_page.login(username, password)


def quick_logout(driver: WebDriver) -> None:
    """
    Perform a quick logout using navigation component.

    Args:
        driver: WebDriver instance
    """
    nav = OrangeHRMNavigation(driver)
    nav.logout()


def navigate_to_module(driver: WebDriver, module: str) -> None:
    """
    Navigate to a specific module.

    Args:
        driver: WebDriver instance
        module: Module name (admin, pim, leave, time, recruitment, dashboard)
    """
    nav = OrangeHRMNavigation(driver)
    module_map = {
        'admin': nav.navigate_to_admin,
        'pim': nav.navigate_to_pim,
        'leave': nav.navigate_to_leave,
        'time': nav.navigate_to_time,
        'recruitment': nav.navigate_to_recruitment,
        'dashboard': nav.navigate_to_dashboard,
    }

    if module.lower() in module_map:
        module_map[module.lower()]()
    else:
        raise ValueError(f"Unknown module: {module}")
