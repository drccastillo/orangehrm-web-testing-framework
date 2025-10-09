"""
Navigation Mixin - provides page navigation capabilities.
Implements Interface Segregation Principle.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from framework.page.components import NavigationHelper


class NavigationMixin:
    """
    Mixin for pages that need navigation capabilities.

    Provides methods for page navigation and URL operations.
    Requires the class to have a 'navigation' attribute of type NavigationHelper.
    """

    navigation: 'NavigationHelper'  # Type hint for required attribute

    def navigate_to(self, url: str) -> None:
        """
        Navigate to a specific URL.

        Args:
            url: URL to navigate to
        """
        return self.navigation.navigate_to(url)

    def get_current_url(self) -> str:
        """
        Get the current URL of the page.

        Returns:
            Current URL as string
        """
        return self.navigation.get_current_url()

    def get_page_title(self) -> str:
        """
        Get the title of the current page.

        Returns:
            Page title as string
        """
        return self.navigation.get_page_title()

    def refresh_page(self) -> None:
        """Refresh the current page."""
        return self.navigation.refresh_page()

    def go_back(self) -> None:
        """Navigate back in browser history."""
        return self.navigation.go_back()

    def go_forward(self) -> None:
        """Navigate forward in browser history."""
        return self.navigation.go_forward()

    def get_page_source(self) -> str:
        """
        Get the page source HTML.

        Returns:
            Page source as string
        """
        return self.navigation.get_page_source()

    def switch_to_frame(self, frame_reference) -> None:
        """
        Switch to an iframe.

        Args:
            frame_reference: Frame index, name, or WebElement
        """
        return self.navigation.switch_to_frame(frame_reference)

    def switch_to_default_content(self) -> None:
        """Switch back to the main content from an iframe."""
        return self.navigation.switch_to_default_content()

    def switch_to_window(self, window_handle: str) -> None:
        """
        Switch to a different browser window/tab.

        Args:
            window_handle: Window handle to switch to
        """
        return self.navigation.switch_to_window(window_handle)

    def get_window_handles(self) -> list:
        """
        Get all window handles.

        Returns:
            List of window handles
        """
        return self.navigation.get_window_handles()

    def get_current_window_handle(self) -> str:
        """
        Get the current window handle.

        Returns:
            Current window handle
        """
        return self.navigation.get_current_window_handle()
