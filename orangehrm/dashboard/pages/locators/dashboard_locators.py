"""
Locators for Dashboard page.
"""
from selenium.webdriver.common.by import By


class DashboardLocators:
    """Locators for OrangeHRM Dashboard page."""

    # Header elements
    DASHBOARD_TITLE = (By.CSS_SELECTOR, "h6.oxd-topbar-header-breadcrumb-module")
    USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown")
    USER_DROPDOWN_NAME = (By.CSS_SELECTOR, ".oxd-userdropdown-name")

    # Quick Launch section
    QUICK_LAUNCH = (By.CSS_SELECTOR, ".orangehrm-quick-launch")
    ASSIGN_LEAVE = (By.CSS_SELECTOR, "button[title='Assign Leave']")
    LEAVE_LIST = (By.CSS_SELECTOR, "button[title='Leave List']")
    TIMESHEETS = (By.CSS_SELECTOR, "button[title='Timesheets']")
    APPLY_LEAVE = (By.CSS_SELECTOR, "button[title='Apply Leave']")
    MY_LEAVE = (By.CSS_SELECTOR, "button[title='My Leave']")
    MY_TIMESHEET = (By.CSS_SELECTOR, "button[title='My Timesheet']")

    # Dashboard widgets
    TIME_AT_WORK_WIDGET = (By.XPATH, "//p[text()='Time at Work']")
    MY_ACTIONS_WIDGET = (By.XPATH, "//p[text()='My Actions']")
    QUICK_LAUNCH_WIDGET = (By.XPATH, "//p[text()='Quick Launch']")
    BUZZ_LATEST_POSTS = (By.XPATH, "//p[text()='Buzz Latest Posts']")
    EMPLOYEES_ON_LEAVE_TODAY = (By.XPATH, "//p[text()='Employees on Leave Today']")
    EMPLOYEE_DISTRIBUTION = (By.XPATH, "//p[text()='Employee Distribution by Sub Unit']")
    EMPLOYEE_LOCATION = (By.XPATH, "//p[text()='Employee Distribution by Location']")

    # Side menu
    ADMIN_MENU = (By.XPATH, "//span[text()='Admin']")
    PIM_MENU = (By.XPATH, "//span[text()='PIM']")
    LEAVE_MENU = (By.XPATH, "//span[text()='Leave']")
    TIME_MENU = (By.XPATH, "//span[text()='Time']")
    RECRUITMENT_MENU = (By.XPATH, "//span[text()='Recruitment']")
    MY_INFO_MENU = (By.XPATH, "//span[text()='My Info']")
    PERFORMANCE_MENU = (By.XPATH, "//span[text()='Performance']")
    DASHBOARD_MENU = (By.XPATH, "//span[text()='Dashboard']")
    DIRECTORY_MENU = (By.XPATH, "//span[text()='Directory']")
    MAINTENANCE_MENU = (By.XPATH, "//span[text()='Maintenance']")
    BUZZ_MENU = (By.XPATH, "//span[text()='Buzz']")
