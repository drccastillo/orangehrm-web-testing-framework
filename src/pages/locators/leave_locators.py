"""
Playwright locators for the Leave Page.

These locators use Playwright selector syntax for modern web automation.
"""

from src.core.playwright_locator import PlaywrightLocator


class LeaveLocators:
    """
    Playwright locator value objects for the Leave Page.

    These locators use PlaywrightLocator with native Playwright selector syntax
    for optimal performance and reliability.

    Example:
        >>> playwright_browser = PlaywrightBrowserAdapter(page)
        >>> page = LeavePage(playwright_browser)
        >>> page.click(LeaveLocators.APPLY_BUTTON)
    """

    # Navigation elements
    LEAVE_MENU_ITEM = PlaywrightLocator("//span[text()='Leave']", "Leave menu item in sidebar")

    # Page header
    PAGE_TITLE = PlaywrightLocator(".oxd-topbar-header-breadcrumb h6", "Leave page title")

    # Action buttons in header
    APPLY_BUTTON = PlaywrightLocator(
        "//a[@class='oxd-topbar-body-nav-tab-item' and text()='Apply']",
        "Apply leave button",
    )

    MY_LEAVE_BUTTON = PlaywrightLocator(
        "//a[@class='oxd-topbar-body-nav-tab-item' and text()='My Leave']",
        "My Leave button",
    )

    ENTITLEMENTS_BUTTON = PlaywrightLocator(
        "//span[@class='oxd-topbar-body-nav-tab-item' and contains(text(), 'Entitlements')]",
        "Entitlements button",
    )

    REPORTS_BUTTON = PlaywrightLocator(
        "//span[@class='oxd-topbar-body-nav-tab-item' and contains(text(), 'Reports')]",
        "Reports button",
    )

    CONFIGURE_BUTTON = PlaywrightLocator(
        "//span[@class='oxd-topbar-body-nav-tab-item' and contains(text(), 'Configure')]",
        "Configure button",
    )

    LEAVE_LIST_BUTTON = PlaywrightLocator(
        "//a[@class='oxd-topbar-body-nav-tab-item' and text()='Leave List']",
        "Leave List button",
    )

    ASSIGN_LEAVE_BUTTON = PlaywrightLocator(
        "//a[@class='oxd-topbar-body-nav-tab-item' and text()='Assign Leave']",
        "Assign Leave button",
    )

    # Apply Leave Form fields
    LEAVE_TYPE_DROPDOWN = PlaywrightLocator(
        ".oxd-select-text--active",
        "Leave type dropdown in Apply form",
    )

    FROM_DATE_INPUT = PlaywrightLocator(
        "//label[text()='From Date']/parent::div/following-sibling::div//input",
        "From date input field",
    )

    TO_DATE_INPUT = PlaywrightLocator(
        "//label[text()='To Date']/parent::div/following-sibling::div//input",
        "To date input field",
    )

    COMMENTS_TEXTAREA = PlaywrightLocator(".oxd-textarea", "Comments textarea in Apply form")

    SUBMIT_BUTTON = PlaywrightLocator("button[type='submit']", "Submit button in Apply form")

    CANCEL_BUTTON = PlaywrightLocator("//button[contains(text(), 'Cancel')]", "Cancel button")

    # Leave List - Search/Filter section
    EMPLOYEE_NAME_INPUT = PlaywrightLocator(
        "//label[text()='Employee Name']/parent::div/following-sibling::div//input",
        "Employee name autocomplete input",
    )

    LEAVE_STATUS_DROPDOWN = PlaywrightLocator(
        "//label[text()='Leave Status']/parent::div/"
        "following-sibling::div//div[@class='oxd-select-text-input']",
        "Leave status dropdown filter",
    )

    SEARCH_BUTTON = PlaywrightLocator("button[type='submit']", "Search button in filter form")

    RESET_BUTTON = PlaywrightLocator("//button[@type='reset']", "Reset filter button")

    # Leave List - Results table
    LEAVE_LIST_TABLE = PlaywrightLocator(".oxd-table", "Leave list table")

    LEAVE_LIST_ROWS = PlaywrightLocator(
        ".oxd-table-body .oxd-table-card", "Leave list table rows"
    )

    # Status badge
    STATUS_BADGE = PlaywrightLocator(".oxd-chip", "Status badge in leave list")

    # Messages
    SUCCESS_MESSAGE = PlaywrightLocator(
        ".oxd-toast-content--success", "Success toast message"
    )

    ERROR_MESSAGE = PlaywrightLocator(".oxd-toast-content--error", "Error toast message")

    NO_RECORDS_MESSAGE = PlaywrightLocator(
        "//span[contains(text(), 'No Records Found')]", "No records message"
    )
