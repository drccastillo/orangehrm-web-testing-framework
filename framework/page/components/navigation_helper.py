"""
Navigation helper component - responsible for page navigation and URL operations.
Single Responsibility: Handle navigation, URLs, and page metadata.
"""
from selenium.webdriver.remote.webdriver import WebDriver
from framework.utils.logger import TestLogger
from framework.utils.exceptions import InvalidParameterException


class NavigationHelper:
    """
    Component responsible for page navigation operations.

    Single Responsibility: Navigate pages, get URLs, manage page state.
    """

    def __init__(self, driver: WebDriver):
        """
        Initialize the navigation helper.

        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.logger = TestLogger.get_logger(self.__class__.__name__)

    def navigate_to(self, url: str) -> None:
        """
        Navigate to a specific URL.

        Args:
            url: URL to navigate to

        Raises:
            InvalidParameterException: If URL is None or empty

        Example:
            >>> navigation.navigate_to("https://example.com")
        """
        if not url or not isinstance(url, str):
            raise InvalidParameterException("url", url, "URL must be a non-empty string")

        self.logger.info(f"Navigating to URL: {url}")
        self.driver.get(url)
        self.logger.info(f"Navigation completed to: {url}")

    def get_current_url(self) -> str:
        """
        Get the current URL of the page.

        Returns:
            Current URL as string
        """
        return self.driver.current_url

    def get_page_title(self) -> str:
        """
        Get the title of the current page.

        Returns:
            Page title as string
        """
        return self.driver.title

    def refresh_page(self) -> None:
        """Refresh the current page."""
        self.logger.debug("Refreshing page")
        self.driver.refresh()
        self.logger.debug("Page refreshed")

    def go_back(self) -> None:
        """Navigate back in browser history."""
        self.logger.debug("Navigating back")
        self.driver.back()
        self.logger.debug("Navigated back")

    def go_forward(self) -> None:
        """Navigate forward in browser history."""
        self.logger.debug("Navigating forward")
        self.driver.forward()
        self.logger.debug("Navigated forward")

    def get_page_source(self) -> str:
        """
        Get the page source HTML.

        Returns:
            Page source as string
        """
        return self.driver.page_source

    def switch_to_frame(self, frame_reference) -> None:
        """
        Switch to an iframe.

        Args:
            frame_reference: Frame index, name, or WebElement
        """
        self.logger.debug(f"Switching to frame: {frame_reference}")
        self.driver.switch_to.frame(frame_reference)
        self.logger.debug(f"Switched to frame: {frame_reference}")

    def switch_to_default_content(self) -> None:
        """Switch back to the main content from an iframe."""
        self.logger.debug("Switching to default content")
        self.driver.switch_to.default_content()
        self.logger.debug("Switched to default content")

    def switch_to_window(self, window_handle: str) -> None:
        """
        Switch to a different browser window/tab.

        Args:
            window_handle: Window handle to switch to
        """
        self.logger.debug(f"Switching to window: {window_handle}")
        self.driver.switch_to.window(window_handle)
        self.logger.debug(f"Switched to window: {window_handle}")

    def get_window_handles(self) -> list:
        """
        Get all window handles.

        Returns:
            List of window handles
        """
        return self.driver.window_handles

    def get_current_window_handle(self) -> str:
        """
        Get the current window handle.

        Returns:
            Current window handle
        """
        return self.driver.current_window_handle
