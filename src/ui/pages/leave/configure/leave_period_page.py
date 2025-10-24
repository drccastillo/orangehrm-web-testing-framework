"""
Leave Period Page Object Model for OrangeHRM application.

This page allows configuration of leave period settings including:
- Leave period start month (January-December)
- Leave period start date (1-31)
- Displays calculated end date automatically
- Shows current leave period information
"""

# pylint: disable=import-error  # src module is in project root
from playwright.sync_api import Locator, Page

from src.ui.pages.leave.leave_base_page import LeaveBasePage


class LeavePeriodPage(LeaveBasePage):
    """
    Page Object Model for the OrangeHRM Leave Period Configuration Page.

    Inherits Leave module top bar navigation from LeaveBasePage.
    This page allows configuring the organization's leave period by selecting:
    - Start Month (dropdown): January through December
    - Start Date (dropdown): 1 through 31

    The page automatically calculates and displays:
    - End Date: One day before the start date in the following year
    - Current Leave Period: The currently configured leave period range

    Attributes:
        page_title: "Leave Period" page heading
        start_month_label: Label for start month field
        start_date_label: Label for start date field
        end_date_label: Label for end date display
        current_period_label: Label for current leave period display
        start_month_dropdown: Dropdown for selecting leave period start month
        start_date_dropdown: Dropdown for selecting leave period start date
        dropdown_options: All dropdown options (visible after opening dropdown)
        end_date_text: Read-only text showing calculated end date
        current_period_text: Read-only text showing current leave period
        save_button: Button to save leave period configuration
        reset_button: Button to reset form to previous values
        success_message: Toast message shown after successful save
        error_message: Error message shown for validation failures

    Example:
        >>> # Configure leave period to start on January 1st
        >>> leave_period_page = LeavePeriodPage(page, timeout=10)
        >>> leave_period_page.configure_leave_period("January", "01")
        >>> leave_period_page.save()
        >>> assert leave_period_page.is_save_successful()
        >>>
        >>> # Use method chaining
        >>> leave_period_page.select_start_month("January") \\
        ...     .select_start_date("01") \\
        ...     .save()
    """

    def __init__(self, page: Page, timeout: int = 10):
        """
        Initialize the Leave Period Page.

        Args:
            page: Playwright Page instance
            timeout: Default timeout for operations in seconds
        """
        super().__init__(page, timeout)

        # Page heading (OrangeHRM uses <p> tag with orangehrm-main-title class)
        self.page_title: Locator = page.locator(".orangehrm-main-title").filter(
            has_text="Leave Period",
        )

        # Form labels
        self.start_month_label: Locator = page.get_by_text("Start Month")
        self.start_date_label: Locator = page.get_by_text("Start Date")
        self.end_date_label: Locator = page.get_by_text("End Date")
        self.current_period_label: Locator = page.get_by_text("Current Leave Period")

        # Dropdowns (OrangeHRM uses .oxd-select-text for dropdowns)
        # First dropdown is Start Month, second is Start Date
        self.start_month_dropdown: Locator = page.locator(".oxd-select-text").first
        self.start_date_dropdown: Locator = page.locator(".oxd-select-text").nth(1)

        # Dropdown options (visible after clicking a dropdown)
        self.dropdown_options: Locator = page.locator(".oxd-select-option")

        # Read-only text fields (calculated values)
        # End Date is shown next to the End Date label
        # Current Leave Period is shown next to the Current Leave Period label

        # Buttons
        self.save_button: Locator = page.get_by_role("button", name="Save")
        self.reset_button: Locator = page.get_by_role("button", name="Reset")

        # Messages
        self.success_message: Locator = page.locator(".oxd-toast--success")
        self.error_message: Locator = page.locator(".oxd-input-field-error-message")

    def select_start_month(self, month: str) -> "LeavePeriodPage":
        """
        Select the leave period start month from dropdown.

        Args:
            month: Month name (e.g., "January", "February", "March")
                   Must be one of: January, February, March, April, May, June,
                   July, August, September, October, November, December

        Returns:
            Self for method chaining

        Example:
            >>> leave_period_page.select_start_month("January")
            >>> # Or with chaining
            >>> leave_period_page.select_start_month("April").select_start_date("15")
        """
        self.logger.info(f"Selecting start month: {month}")
        self.click(self.start_month_dropdown)
        # Wait for dropdown options to appear
        self.dropdown_options.first.wait_for(state="visible")
        # Select the month option
        month_option = self.dropdown_options.filter(has_text=month)
        self.click(month_option)
        return self

    def select_start_date(self, date: str) -> "LeavePeriodPage":
        """
        Select the leave period start date from dropdown.

        Args:
            date: Date number as string with leading zero (e.g., "01", "15", "31")
                  Valid range: "01" through "31"

        Returns:
            Self for method chaining

        Example:
            >>> leave_period_page.select_start_date("01")
            >>> # Or with chaining
            >>> leave_period_page.select_start_month("June").select_start_date("30")
        """
        self.logger.info(f"Selecting start date: {date}")
        self.click(self.start_date_dropdown)
        # Wait for dropdown options to appear
        self.dropdown_options.first.wait_for(state="visible")
        # Select the date option
        date_option = self.dropdown_options.filter(has_text=date)
        self.click(date_option)
        return self

    def configure_leave_period(
        self,
        start_month: str,
        start_date: str,
    ) -> "LeavePeriodPage":
        """
        Configure the complete leave period by selecting both month and date.

        This is a convenience method that combines select_start_month and
        select_start_date. The end date is automatically calculated by the
        application as one day before the start date in the following year.

        Args:
            start_month: Month name (e.g., "January", "February")
            start_date: Date number with leading zero (e.g., "01", "15")

        Returns:
            Self for method chaining

        Example:
            >>> # Configure leave period to start on April 1st
            >>> leave_period_page.configure_leave_period("April", "01")
            >>> # End date will automatically be March 31 of the following year
            >>>
            >>> # With method chaining and save
            >>> leave_period_page.configure_leave_period("January", "01").save()
        """
        self.logger.info(
            f"Configuring leave period: Start on {start_month} {start_date}",
        )
        self.select_start_month(start_month)
        self.select_start_date(start_date)
        return self

    def save(self) -> None:
        """
        Click the Save button to save leave period configuration.

        After clicking save, the page will show a success toast message
        if the configuration is saved successfully.

        Example:
            >>> leave_period_page.configure_leave_period("January", "01")
            >>> leave_period_page.save()
            >>> assert leave_period_page.is_save_successful()
        """
        self.logger.info("Clicking Save button")
        self.click(self.save_button)
        # Wait briefly for the save operation to complete
        self.page.wait_for_timeout(1000)

    def reset(self) -> None:
        """
        Click the Reset button to discard changes and restore previous values.

        This resets the form fields to the currently saved leave period values.

        Example:
            >>> leave_period_page.select_start_month("June")
            >>> leave_period_page.reset()  # Discards the change
        """
        self.logger.info("Clicking Reset button")
        self.click(self.reset_button)

    def get_end_date(self) -> str:
        """
        Get the automatically calculated end date.

        The end date is calculated as one day before the start date
        in the following year.

        Returns:
            End date text (e.g., "December 31")

        Example:
            >>> leave_period_page.configure_leave_period("January", "01")
            >>> end_date = leave_period_page.get_end_date()
            >>> assert end_date == "December 31"
        """
        # End date appears as <p> with class orangehrm-leave-period
        # after the "End Date" label
        end_date_locator = self.page.locator("p.orangehrm-leave-period").first
        if end_date_locator.is_visible():
            end_date = self.get_text(end_date_locator)
            self.logger.debug(f"End date: {end_date}")
            return end_date
        return ""

    def get_current_leave_period(self) -> str:
        """
        Get the current leave period range.

        Returns:
            Current leave period text (e.g., "2025-01-01 to 2025-12-31")

        Example:
            >>> current_period = leave_period_page.get_current_leave_period()
            >>> assert "2025" in current_period
        """
        # Current period appears as <p> with class orangehrm-leave-period
        # There are two elements with this class: first is end date, second is current period
        current_period_locator = self.page.locator("p.orangehrm-leave-period").nth(1)
        if current_period_locator.is_visible():
            period = self.get_text(current_period_locator)
            self.logger.debug(f"Current leave period: {period}")
            return period
        return ""

    def is_save_successful(self) -> bool:
        """
        Check if the save operation was successful.

        Returns:
            True if success message is visible, False otherwise

        Example:
            >>> leave_period_page.configure_leave_period("January", "01")
            >>> leave_period_page.save()
            >>> if leave_period_page.is_save_successful():
            ...     print("Leave period saved successfully!")
        """
        return self.success_message.is_visible(timeout=5000)

    def get_error_message(self) -> str:
        """
        Get validation error message if any.

        Returns:
            Error message text, empty string if no error

        Example:
            >>> leave_period_page.save()  # Save without selecting values
            >>> error = leave_period_page.get_error_message()
            >>> assert "Required" in error
        """
        if self.error_message.is_visible():
            return self.get_text(self.error_message)
        return ""

    def is_save_button_enabled(self) -> bool:
        """
        Check if the Save button is enabled.

        Returns:
            True if Save button is enabled, False otherwise

        Example:
            >>> if leave_period_page.is_save_button_enabled():
            ...     leave_period_page.save()
        """
        return self.save_button.is_enabled()

    def is_reset_button_enabled(self) -> bool:
        """
        Check if the Reset button is enabled.

        Returns:
            True if Reset button is enabled, False otherwise
        """
        return self.reset_button.is_enabled()
