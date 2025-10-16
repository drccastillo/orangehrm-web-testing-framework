"""
Simplified Leave Page Object Model for OrangeHRM application.

This LeavePage uses Playwright Page directly, eliminating adapter overhead.
"""

from playwright.sync_api import Page

from src.pages.base_page import BasePage
from src.pages.locators.leave_locators import LeaveLocators


class LeavePage(BasePage):
    """
    Page Object Model for the OrangeHRM Leave Page using Playwright.

    Benefits:
        - Direct access to Playwright API
        - No adapter overhead
        - Simpler, more maintainable code
        - Full power of Playwright features

    Example:
        >>> from playwright.sync_api import sync_playwright
        >>> with sync_playwright() as p:
        ...     browser = p.chromium.launch()
        ...     page = browser.new_page()
        ...     leave_page = LeavePage(page, timeout=10)
        ...     leave_page.navigate_to_leave_list()
    """

    def __init__(self, page: Page, timeout: int = 10):
        """
        Initialize the Leave Page.

        Args:
            page: Playwright Page instance
            timeout: Default timeout for operations in seconds
        """
        super().__init__(page, timeout)
        self.locators = LeaveLocators

    def navigate_to_leave_menu(self) -> "LeavePage":
        """
        Navigate to Leave section by clicking Leave menu item.

        Returns:
            Self for method chaining
        """
        self.logger.info("Navigating to Leave section")
        self.click(self.locators.LEAVE_MENU_ITEM(self.page))
        return self

    def navigate_to_apply_leave(self) -> None:
        """
        Navigate to Apply Leave page.

        Clicks the Apply button in the Leave section header.
        """
        self.logger.info("Navigating to Apply Leave")
        self.click(self.locators.APPLY_BUTTON(self.page))

    def navigate_to_leave_list(self) -> None:
        """
        Navigate to Leave List page.

        Clicks the Leave List button in the Leave section header.
        """
        self.logger.info("Navigating to Leave List")
        self.click(self.locators.LEAVE_LIST_BUTTON(self.page))

    def navigate_to_my_leave(self) -> None:
        """
        Navigate to My Leave page.

        Clicks the My Leave button in the Leave section header.
        """
        self.logger.info("Navigating to My Leave")
        self.click(self.locators.MY_LEAVE_BUTTON(self.page))

    def navigate_to_assign_leave(self) -> None:
        """Navigate to Assign Leave page."""
        self.logger.info("Navigating to Assign Leave")
        self.click(self.locators.ASSIGN_LEAVE_BUTTON(self.page))

    def is_apply_button_visible(self) -> bool:
        """
        Check if the Apply button is visible.

        Returns:
            True if Apply button is visible, False otherwise
        """
        return self.is_element_visible(self.locators.APPLY_BUTTON(self.page))

    def is_leave_list_button_visible(self) -> bool:
        """
        Check if the Leave List button is visible.

        Returns:
            True if Leave List button is visible, False otherwise
        """
        return self.is_element_visible(self.locators.LEAVE_LIST_BUTTON(self.page))

    def is_my_leave_button_visible(self) -> bool:
        """
        Check if the My Leave button is visible.

        Returns:
            True if My Leave button is visible, False otherwise
        """
        return self.is_element_visible(self.locators.MY_LEAVE_BUTTON(self.page))

    def apply_leave(
        self, leave_type: str, from_date: str, to_date: str, comments: str = ""
    ) -> None:
        """
        Apply for leave with specified details.

        This is a high-level method that fills out the entire Apply Leave form.

        Args:
            leave_type: Type of leave to apply for (e.g., "CAN - FMLA")
            from_date: Start date of leave (format: YYYY-MM-DD)
            to_date: End date of leave (format: YYYY-MM-DD)
            comments: Optional comments for leave request

        Example:
            >>> leave_page.apply_leave("CAN - FMLA", "2025-01-15", "2025-01-17", "Family emergency")
        """
        self.logger.info(f"Applying for leave: {leave_type} from {from_date} to {to_date}")

        # Select leave type
        self.click(self.locators.LEAVE_TYPE_DROPDOWN(self.page))
        # Note: Actual dropdown selection would need more complex logic
        # This is simplified for demonstration

        # Enter dates
        self.send_keys(self.locators.FROM_DATE_INPUT(self.page), from_date)
        self.send_keys(self.locators.TO_DATE_INPUT(self.page), to_date)

        # Enter comments if provided
        if comments:
            self.send_keys(self.locators.COMMENTS_TEXTAREA(self.page), comments)

        # Submit the form
        self.click(self.locators.SUBMIT_BUTTON(self.page))

    def search_leave(self, employee_name: str = "", status: str = "") -> None:
        """
        Search for leave records with filters.

        Args:
            employee_name: Employee name to filter (optional)
            status: Leave status to filter (optional)

        Example:
            >>> leave_page.search_leave(employee_name="John Doe", status="Pending Approval")
        """
        self.logger.info(f"Searching leave: employee='{employee_name}', status='{status}'")

        # Enter employee name if provided
        if employee_name:
            self.send_keys(self.locators.EMPLOYEE_NAME_INPUT(self.page), employee_name)

        # Select status if provided
        if status:
            self.click(self.locators.LEAVE_STATUS_DROPDOWN(self.page))
            # Note: Actual dropdown selection would need more complex logic

        # Click search button
        self.click(self.locators.SEARCH_BUTTON(self.page))

    def reset_search(self) -> None:
        """Reset all search filters."""
        self.logger.info("Resetting search filters")
        self.click(self.locators.RESET_BUTTON(self.page))

    def get_leave_count(self) -> int:
        """
        Get the count of leave records displayed in the list.

        Returns:
            Number of leave records in the list

        Example:
            >>> count = leave_page.get_leave_count()
            >>> assert count > 0, "Should have at least one leave record"
        """
        elements = self.find_elements(self.locators.LEAVE_LIST_ROWS(self.page))
        count = len(elements)
        self.logger.debug(f"Found {count} leave records")
        return count

    def is_leave_list_table_visible(self) -> bool:
        """
        Check if the leave list table is visible.

        Returns:
            True if table is visible, False otherwise
        """
        return self.is_element_visible(self.locators.LEAVE_LIST_TABLE(self.page))

    def is_success_message_displayed(self) -> bool:
        """
        Check if success message is displayed.

        Returns:
            True if success message is visible, False otherwise
        """
        return self.is_element_visible(self.locators.SUCCESS_MESSAGE(self.page))

    def get_success_message(self) -> str:
        """
        Get the text of the success message.

        Returns:
            Success message text
        """
        return self.get_text(self.locators.SUCCESS_MESSAGE(self.page))

    def is_error_message_displayed(self) -> bool:
        """
        Check if error message is displayed.

        Returns:
            True if error message is visible, False otherwise
        """
        return self.is_element_visible(self.locators.ERROR_MESSAGE(self.page))

    def get_error_message(self) -> str:
        """
        Get the text of the error message.

        Returns:
            Error message text
        """
        return self.get_text(self.locators.ERROR_MESSAGE(self.page))

    def is_no_records_message_displayed(self) -> bool:
        """
        Check if 'No Records Found' message is displayed.

        Returns:
            True if no records message is visible, False otherwise
        """
        return self.is_element_visible(self.locators.NO_RECORDS_MESSAGE(self.page))

    def is_page_loaded(self) -> bool:
        """
        Verify if the leave page is fully loaded.

        Checks that critical elements are visible:
            - Leave menu item or page title

        Returns:
            True if leave page is loaded, False otherwise
        """
        return self.is_element_visible(
            self.locators.LEAVE_MENU_ITEM(self.page)
        ) or self.is_element_visible(self.locators.PAGE_TITLE(self.page))
