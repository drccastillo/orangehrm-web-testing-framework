"""
OrangeHRM Navigation Component.
Handles the main navigation bar present across all pages.

Migrated to Mixins pattern - Clean Architecture.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Optional

# Import Mixins
from framework.page.mixins import (
    ElementFinderMixin,
    ElementInteractorMixin,
    ElementValidatorMixin,
)

# Import Components
from framework.page.components import (
    ElementFinder,
    ElementInteractor,
    ElementValidator,
)

from framework.config.interface import ConfigInterface
from framework.config.settings import Config
from framework.utils.logger import TestLogger


class OrangeHRMNavigation(
    ElementFinderMixin,
    ElementInteractorMixin,
    ElementValidatorMixin,
):
    """
    Navigation bar component for OrangeHRM (Clean Architecture - Mixins).

    This component appears on all pages after login and provides
    access to different modules.

    Uses Mixins pattern:
    - ElementFinderMixin: Finding navigation elements
    - ElementInteractorMixin: Clicking menu items
    - ElementValidatorMixin: Checking navigation visibility
    """

    # Navigation menu items (specific to OrangeHRM)
    ADMIN_MENU = (By.ID, "menu_admin_viewAdminModule")
    PIM_MENU = (By.ID, "menu_pim_viewPimModule")
    LEAVE_MENU = (By.ID, "menu_leave_viewLeaveModule")
    TIME_MENU = (By.ID, "menu_time_viewTimeModule")
    RECRUITMENT_MENU = (By.ID, "menu_recruitment_viewRecruitmentModule")
    PERFORMANCE_MENU = (By.ID, "menu_performance_viewPerformanceModule")
    DASHBOARD_MENU = (By.ID, "menu_dashboard_index")

    # User menu
    USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")

    def __init__(
        self,
        driver: WebDriver,
        timeout: int = 10,
        config: Optional[ConfigInterface] = None
    ):
        """
        Initialize navigation component with Mixins pattern.

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

        # Initialize only needed components
        self.finder = ElementFinder(driver, timeout)
        self.interactor = ElementInteractor(driver, timeout)
        self.validator = ElementValidator(driver, timeout)

    def navigate_to_admin(self) -> 'OrangeHRMNavigation':
        """
        Navigate to Admin module.

        Returns:
            Self for method chaining
        """
        self.logger.info("Navigating to Admin module")
        self.click(self.ADMIN_MENU)
        return self

    def navigate_to_pim(self) -> 'OrangeHRMNavigation':
        """
        Navigate to PIM (Personnel Information Management) module.

        Returns:
            Self for method chaining
        """
        self.logger.info("Navigating to PIM module")
        self.click(self.PIM_MENU)
        return self

    def navigate_to_leave(self) -> 'OrangeHRMNavigation':
        """
        Navigate to Leave module.

        Returns:
            Self for method chaining
        """
        self.logger.info("Navigating to Leave module")
        self.click(self.LEAVE_MENU)
        return self

    def navigate_to_time(self) -> 'OrangeHRMNavigation':
        """
        Navigate to Time module.

        Returns:
            Self for method chaining
        """
        self.logger.info("Navigating to Time module")
        self.click(self.TIME_MENU)
        return self

    def navigate_to_recruitment(self) -> 'OrangeHRMNavigation':
        """
        Navigate to Recruitment module.

        Returns:
            Self for method chaining
        """
        self.logger.info("Navigating to Recruitment module")
        self.click(self.RECRUITMENT_MENU)
        return self

    def navigate_to_dashboard(self) -> 'OrangeHRMNavigation':
        """
        Navigate to Dashboard.

        Returns:
            Self for method chaining
        """
        self.logger.info("Navigating to Dashboard")
        self.click(self.DASHBOARD_MENU)
        return self

    def logout(self) -> None:
        """Logout from OrangeHRM."""
        self.logger.info("Logging out")
        self.click(self.USER_DROPDOWN)
        self.click(self.LOGOUT_LINK)

    def is_navigation_visible(self) -> bool:
        """
        Check if navigation bar is visible (indicates logged in state).

        Returns:
            True if navigation is visible, False otherwise
        """
        return self.is_element_visible(self.DASHBOARD_MENU)
