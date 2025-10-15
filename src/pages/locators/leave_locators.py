"""
Unified locators for the Leave Page.

These locators work with ANY automation framework (Selenium, Playwright, etc.)
through the Locator value object abstraction.
"""

from src.core.locator import LocatorStrategy
from src.core.selenium_locator import SeleniumLocator


class LeaveLocators:
    """
    Unified locator value objects for the Leave Page.

    These locators use SeleniumLocator which implements the Locator protocol.
    The browser adapters convert them to framework-specific format via to_native().

    Example (Selenium):
        >>> selenium_browser = SeleniumBrowserAdapter(driver)
        >>> page = LeavePage(selenium_browser)
        >>> page.click(LeaveLocators.APPLY_BUTTON)
        >>> # SeleniumBrowserAdapter calls APPLY_BUTTON.to_native()
        >>> # Returns: (By.XPATH, "//a[text()='Apply']")

    Example (Playwright):
        >>> playwright_browser = PlaywrightBrowserAdapter(page)
        >>> page = LeavePage(playwright_browser)
        >>> page.click(LeaveLocators.APPLY_BUTTON)
        >>> # PlaywrightBrowserAdapter calls APPLY_BUTTON.to_native() -> "xpath=//a[text()='Apply']"
    """

    # Navigation elements
    LEAVE_MENU_ITEM = SeleniumLocator(
        LocatorStrategy.XPATH, "//span[text()='Leave']", "Leave menu item in sidebar"
    )

    # Page header
    PAGE_TITLE = SeleniumLocator(
        LocatorStrategy.CSS, ".oxd-topbar-header-breadcrumb h6", "Leave page title"
    )

    # Action buttons in header (using CSS for better Playwright compatibility)
    APPLY_BUTTON = SeleniumLocator(
        LocatorStrategy.XPATH,
        "//a[@class='oxd-topbar-body-nav-tab-item' and text()='Apply']",
        "Apply leave button",
    )

    MY_LEAVE_BUTTON = SeleniumLocator(
        LocatorStrategy.XPATH,
        "//a[@class='oxd-topbar-body-nav-tab-item' and text()='My Leave']",
        "My Leave button",
    )

    ENTITLEMENTS_BUTTON = SeleniumLocator(
        LocatorStrategy.XPATH,
        "//span[@class='oxd-topbar-body-nav-tab-item' and contains(text(), 'Entitlements')]",
        "Entitlements button",
    )

    REPORTS_BUTTON = SeleniumLocator(
        LocatorStrategy.XPATH,
        "//span[@class='oxd-topbar-body-nav-tab-item' and contains(text(), 'Reports')]",
        "Reports button",
    )

    CONFIGURE_BUTTON = SeleniumLocator(
        LocatorStrategy.XPATH,
        "//span[@class='oxd-topbar-body-nav-tab-item' and contains(text(), 'Configure')]",
        "Configure button",
    )

    LEAVE_LIST_BUTTON = SeleniumLocator(
        LocatorStrategy.XPATH,
        "//a[@class='oxd-topbar-body-nav-tab-item' and text()='Leave List']",
        "Leave List button",
    )

    ASSIGN_LEAVE_BUTTON = SeleniumLocator(
        LocatorStrategy.XPATH,
        "//a[@class='oxd-topbar-body-nav-tab-item' and text()='Assign Leave']",
        "Assign Leave button",
    )

    # Apply Leave Form fields
    LEAVE_TYPE_DROPDOWN = SeleniumLocator(
        LocatorStrategy.CSS,
        ".oxd-select-text--active",
        "Leave type dropdown in Apply form",
    )

    FROM_DATE_INPUT = SeleniumLocator(
        LocatorStrategy.XPATH,
        "//label[text()='From Date']/parent::div/following-sibling::div//input",
        "From date input field",
    )

    TO_DATE_INPUT = SeleniumLocator(
        LocatorStrategy.XPATH,
        "//label[text()='To Date']/parent::div/following-sibling::div//input",
        "To date input field",
    )

    COMMENTS_TEXTAREA = SeleniumLocator(
        LocatorStrategy.CSS, ".oxd-textarea", "Comments textarea in Apply form"
    )

    SUBMIT_BUTTON = SeleniumLocator(
        LocatorStrategy.CSS, "button[type='submit']", "Submit button in Apply form"
    )

    CANCEL_BUTTON = SeleniumLocator(
        LocatorStrategy.XPATH, "//button[contains(text(), 'Cancel')]", "Cancel button"
    )

    # Leave List - Search/Filter section
    EMPLOYEE_NAME_INPUT = SeleniumLocator(
        LocatorStrategy.XPATH,
        "//label[text()='Employee Name']/parent::div/following-sibling::div//input",
        "Employee name autocomplete input",
    )

    LEAVE_STATUS_DROPDOWN = SeleniumLocator(
        LocatorStrategy.XPATH,
        (
            "//label[text()='Leave Status']/parent::div/"
            "following-sibling::div//div[@class='oxd-select-text-input']"
        ),
        "Leave status dropdown filter",
    )

    SEARCH_BUTTON = SeleniumLocator(
        LocatorStrategy.CSS, "button[type='submit']", "Search button in filter form"
    )

    RESET_BUTTON = SeleniumLocator(
        LocatorStrategy.XPATH, "//button[@type='reset']", "Reset filter button"
    )

    # Leave List - Results table
    LEAVE_LIST_TABLE = SeleniumLocator(LocatorStrategy.CSS, ".oxd-table", "Leave list table")

    LEAVE_LIST_ROWS = SeleniumLocator(
        LocatorStrategy.CSS, ".oxd-table-body .oxd-table-card", "Leave list table rows"
    )

    # Status badge
    STATUS_BADGE = SeleniumLocator(LocatorStrategy.CSS, ".oxd-chip", "Status badge in leave list")

    # Messages
    SUCCESS_MESSAGE = SeleniumLocator(
        LocatorStrategy.CSS, ".oxd-toast-content--success", "Success toast message"
    )

    ERROR_MESSAGE = SeleniumLocator(
        LocatorStrategy.CSS, ".oxd-toast-content--error", "Error toast message"
    )

    NO_RECORDS_MESSAGE = SeleniumLocator(
        LocatorStrategy.XPATH, "//span[contains(text(), 'No Records Found')]", "No records message"
    )
