"""
Playwright functional locators for the Leave Page.

Following Playwright best practices, these use user-facing locators where possible:
- get_by_role() for buttons and links
- get_by_text() for navigation items
- get_by_label() for form fields
- CSS selectors only when necessary

Reference: https://playwright.dev/python/docs/locators
"""

# ruff: noqa: N802
# Locator functions use UPPERCASE naming convention for consistency with constants


class LeaveLocators:
    """
    Playwright functional locators for the Leave Page.

    These use Playwright's recommended locator methods for better resilience
    and maintainability.

    Example:
        >>> leave_page = LeavePage(page)
        >>> leave_page.click(LeaveLocators.APPLY_BUTTON(page))
    """

    # Navigation elements
    @staticmethod
    def LEAVE_MENU_ITEM(page):
        """Leave menu item in sidebar (role + name for precision)."""
        return page.get_by_role("link", name="Leave", exact=True)

    # Page header
    @staticmethod
    def PAGE_TITLE(page):
        """Leave page title (heading role)."""
        return page.get_by_role("heading", name="Leave", exact=True)

    # Action buttons in header - using get_by_role for better accessibility
    @staticmethod
    def APPLY_BUTTON(page):
        """Apply leave button (link role, text-based)."""
        return page.get_by_role("link", name="Apply")

    @staticmethod
    def MY_LEAVE_BUTTON(page):
        """My Leave button (link role, text-based)."""
        return page.get_by_role("link", name="My Leave")

    @staticmethod
    def ENTITLEMENTS_BUTTON(page):
        """Entitlements button (text-based)."""
        return page.get_by_text("Entitlements")

    @staticmethod
    def REPORTS_BUTTON(page):
        """Reports button (text-based)."""
        return page.get_by_text("Reports")

    @staticmethod
    def CONFIGURE_BUTTON(page):
        """Configure button (text-based)."""
        return page.get_by_text("Configure")

    @staticmethod
    def LEAVE_LIST_BUTTON(page):
        """Leave List button (link role, text-based)."""
        return page.get_by_role("link", name="Leave List")

    @staticmethod
    def ASSIGN_LEAVE_BUTTON(page):
        """Assign Leave button (link role, text-based)."""
        return page.get_by_role("link", name="Assign Leave")

    # Apply Leave Form fields
    @staticmethod
    def LEAVE_TYPE_DROPDOWN(page):
        """Leave type dropdown (CSS fallback - complex widget)."""
        return page.locator(".oxd-select-text--active")

    @staticmethod
    def FROM_DATE_INPUT(page):
        """From date input field (label-based)."""
        return page.get_by_label("From Date")

    @staticmethod
    def TO_DATE_INPUT(page):
        """To date input field (label-based)."""
        return page.get_by_label("To Date")

    @staticmethod
    def COMMENTS_TEXTAREA(page):
        """Comments textarea (CSS fallback)."""
        return page.locator(".oxd-textarea")

    @staticmethod
    def SUBMIT_BUTTON(page):
        """Submit button in Apply form (role-based)."""
        return page.get_by_role("button", name="Submit")

    @staticmethod
    def CANCEL_BUTTON(page):
        """Cancel button (role-based)."""
        return page.get_by_role("button", name="Cancel")

    # Leave List - Search/Filter section
    @staticmethod
    def EMPLOYEE_NAME_INPUT(page):
        """Employee name autocomplete input (label-based)."""
        return page.get_by_label("Employee Name")

    @staticmethod
    def LEAVE_STATUS_DROPDOWN(page):
        """Leave status dropdown filter (label-based with locator)."""
        # Note: This is a custom dropdown widget, might need CSS fallback
        return page.get_by_label("Leave Status")

    @staticmethod
    def SEARCH_BUTTON(page):
        """Search button in filter form (role-based)."""
        return page.get_by_role("button", name="Search")

    @staticmethod
    def RESET_BUTTON(page):
        """Reset filter button (role-based)."""
        return page.get_by_role("button", name="Reset")

    # Leave List - Results table
    @staticmethod
    def LEAVE_LIST_TABLE(page):
        """Leave list table (CSS fallback)."""
        return page.locator(".oxd-table")

    @staticmethod
    def LEAVE_LIST_ROWS(page):
        """Leave list table rows (CSS fallback)."""
        return page.locator(".oxd-table-body .oxd-table-card")

    # Status badge
    @staticmethod
    def STATUS_BADGE(page):
        """Status badge in leave list (CSS fallback)."""
        return page.locator(".oxd-chip")

    # Messages
    @staticmethod
    def SUCCESS_MESSAGE(page):
        """Success toast message (CSS fallback)."""
        return page.locator(".oxd-toast-content--success")

    @staticmethod
    def ERROR_MESSAGE(page):
        """Error toast message (CSS fallback)."""
        return page.locator(".oxd-toast-content--error")

    @staticmethod
    def NO_RECORDS_MESSAGE(page):
        """No records message (text-based)."""
        return page.get_by_text("No Records Found")
