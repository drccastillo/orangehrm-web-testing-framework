"""
Dashboard Page Object Model using Mixins pattern (ISP).
This is an example of the new architecture using Interface Segregation Principle.
"""
import allure
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver

# Import only the mixins we need
from framework.page.mixins import (
    ElementFinderMixin,
    ElementInteractorMixin,
    ElementValidatorMixin,
    NavigationMixin,
)

# Import components
from framework.page.components import (
    ElementFinder,
    ElementInteractor,
    ElementValidator,
    NavigationHelper,
)

# Import config and locators
from framework.config.interface import ConfigInterface
from framework.config.settings import Config
from framework.utils.logger import TestLogger
from orangehrm.dashboard.pages.locators.dashboard_locators import DashboardLocators as Locators


class DashboardPage(
    ElementFinderMixin,
    ElementInteractorMixin,
    ElementValidatorMixin,
    NavigationMixin,
):
    """
    Dashboard Page using Mixins pattern (NEW ARCHITECTURE).

    This page demonstrates the new architecture following ISP:
    - Only includes capabilities actually needed
    - Uses composition for components
    - Supports dependency injection via ConfigInterface
    - No inheritance from BasePage

    Mixins included:
    - ElementFinderMixin: Finding elements
    - ElementInteractorMixin: Clicking, typing, etc.
    - ElementValidatorMixin: Checking visibility, presence
    - NavigationMixin: URL navigation

    Note: VisualDebugMixin and JavaScriptMixin NOT included (not needed).
    """

    def __init__(
        self,
        driver: WebDriver,
        timeout: int = 10,
        config: Optional[ConfigInterface] = None
    ):
        """
        Initialize Dashboard Page with only required components.

        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout for waits
            config: Optional configuration (defaults to Config class)
        """
        # Store essentials
        self.driver = driver
        self.timeout = timeout
        self.config = config if config is not None else Config()
        self.logger = TestLogger.get_logger(self.__class__.__name__)

        # Initialize ONLY the components we need (Composition)
        self.finder = ElementFinder(driver, timeout)
        self.interactor = ElementInteractor(driver, timeout)
        self.validator = ElementValidator(driver, timeout)
        self.navigation = NavigationHelper(driver)

        # Note: No VisualDebugger, no JavaScriptExecutor
        # This is ISP - only include what you need!

    @allure.step("Navigate to dashboard")
    def navigate_to_dashboard(self) -> 'DashboardPage':
        """
        Navigate to dashboard page using injected config.

        Returns:
            Self for method chaining
        """
        # base_url already includes /web/index.php
        dashboard_url = f"{self.config.base_url}/dashboard/index"
        self.navigate_to(dashboard_url)
        return self

    @allure.step("Verify dashboard is loaded")
    def is_dashboard_loaded(self) -> bool:
        """
        Check if dashboard page is fully loaded.

        Returns:
            True if dashboard is loaded, False otherwise
        """
        self.logger.debug("Checking if dashboard is loaded")
        is_loaded = (
            self.is_element_visible(Locators.DASHBOARD_TITLE) and
            self.is_element_visible(Locators.USER_DROPDOWN)
        )
        self.logger.debug(f"Dashboard loaded: {is_loaded}")
        return is_loaded

    @allure.step("Get dashboard title")
    def get_dashboard_title(self) -> str:
        """
        Get the dashboard page title.

        Returns:
            Dashboard title text
        """
        return self.get_text(Locators.DASHBOARD_TITLE)

    @allure.step("Get user name from dropdown")
    def get_user_name(self) -> str:
        """
        Get the logged-in user name from dropdown.

        Returns:
            User name text
        """
        return self.get_text(Locators.USER_DROPDOWN_NAME)

    @allure.step("Click user dropdown")
    def click_user_dropdown(self) -> 'DashboardPage':
        """
        Click on the user dropdown to show logout option.

        Returns:
            Self for method chaining
        """
        self.click(Locators.USER_DROPDOWN)
        return self

    @allure.step("Check if quick launch is visible")
    def is_quick_launch_visible(self) -> bool:
        """
        Check if Quick Launch section is visible.

        Returns:
            True if visible, False otherwise
        """
        return self.is_element_visible(Locators.QUICK_LAUNCH)

    @allure.step("Click Assign Leave quick link")
    def click_assign_leave(self) -> 'DashboardPage':
        """
        Click Assign Leave quick launch button.

        Returns:
            Self for method chaining
        """
        self.click(Locators.ASSIGN_LEAVE)
        return self

    @allure.step("Click Apply Leave quick link")
    def click_apply_leave(self) -> 'DashboardPage':
        """
        Click Apply Leave quick launch button.

        Returns:
            Self for method chaining
        """
        self.click(Locators.APPLY_LEAVE)
        return self

    @allure.step("Click Admin menu")
    def click_admin_menu(self) -> 'DashboardPage':
        """
        Click Admin in the side menu.

        Returns:
            Self for method chaining
        """
        self.click(Locators.ADMIN_MENU)
        return self

    @allure.step("Click PIM menu")
    def click_pim_menu(self) -> 'DashboardPage':
        """
        Click PIM in the side menu.

        Returns:
            Self for method chaining
        """
        self.click(Locators.PIM_MENU)
        return self

    @allure.step("Click Leave menu")
    def click_leave_menu(self) -> 'DashboardPage':
        """
        Click Leave in the side menu.

        Returns:
            Self for method chaining
        """
        self.click(Locators.LEAVE_MENU)
        return self

    def is_time_at_work_widget_visible(self) -> bool:
        """Check if Time at Work widget is visible."""
        return self.is_element_visible(Locators.TIME_AT_WORK_WIDGET)

    def is_my_actions_widget_visible(self) -> bool:
        """Check if My Actions widget is visible."""
        return self.is_element_visible(Locators.MY_ACTIONS_WIDGET)

    def is_quick_launch_widget_visible(self) -> bool:
        """Check if Quick Launch widget is visible."""
        return self.is_element_visible(Locators.QUICK_LAUNCH_WIDGET)
