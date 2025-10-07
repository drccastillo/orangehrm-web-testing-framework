"""
OrangeHRM Navigation Component.
Handles the main navigation bar present across all pages.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from framework.page import BasePage


class OrangeHRMNavigation(BasePage):
    """
    Navigation bar component for OrangeHRM.

    This component appears on all pages after login and provides
    access to different modules.
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

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """Initialize navigation component."""
        super().__init__(driver, timeout)

    def navigate_to_admin(self) -> None:
        """Navigate to Admin module."""
        self.logger.info("Navigating to Admin module")
        self.click(self.ADMIN_MENU)

    def navigate_to_pim(self) -> None:
        """Navigate to PIM (Personnel Information Management) module."""
        self.logger.info("Navigating to PIM module")
        self.click(self.PIM_MENU)

    def navigate_to_leave(self) -> None:
        """Navigate to Leave module."""
        self.logger.info("Navigating to Leave module")
        self.click(self.LEAVE_MENU)

    def navigate_to_time(self) -> None:
        """Navigate to Time module."""
        self.logger.info("Navigating to Time module")
        self.click(self.TIME_MENU)

    def navigate_to_recruitment(self) -> None:
        """Navigate to Recruitment module."""
        self.logger.info("Navigating to Recruitment module")
        self.click(self.RECRUITMENT_MENU)

    def navigate_to_dashboard(self) -> None:
        """Navigate to Dashboard."""
        self.logger.info("Navigating to Dashboard")
        self.click(self.DASHBOARD_MENU)

    def logout(self) -> None:
        """Logout from OrangeHRM."""
        self.logger.info("Logging out")
        self.click(self.USER_DROPDOWN)
        self.click(self.LOGOUT_LINK)

    def is_navigation_visible(self) -> bool:
        """Check if navigation bar is visible (indicates logged in state)."""
        return self.is_element_visible(self.DASHBOARD_MENU)
