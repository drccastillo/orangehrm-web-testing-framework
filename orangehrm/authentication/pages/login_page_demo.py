"""
LoginPage Demo - Extended version for visual debugging demos.

This extends LoginPage with VisualDebugMixin for demonstration purposes.
Inherits all functionality from LoginPage and adds visual debugging.

Use LoginPage for production tests.
Use LoginPageDemo for visual debugging and demo tests.
"""
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver

# Import VisualDebug components
from framework.page.mixins import VisualDebugMixin
from framework.page.components import VisualDebugger

# Import base LoginPage
from orangehrm.authentication.pages.login_page import LoginPage
from framework.config.interface import ConfigInterface


class LoginPageDemo(LoginPage, VisualDebugMixin):
    """
    LoginPage Demo - Extends LoginPage with visual debugging.

    Inherits from:
    - LoginPage: All standard login functionality (4 mixins)
    - VisualDebugMixin: Visual debugging (highlight_element, blink_element)

    This approach:
    - Eliminates code duplication
    - Follows DRY (Don't Repeat Yourself)
    - Only adds what's needed (VisualDebugMixin)
    """

    def __init__(
        self,
        driver: WebDriver,
        timeout: int = 10,
        config: Optional[ConfigInterface] = None
    ):
        """
        Initialize LoginPageDemo with visual debugging support.

        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout for waits
            config: Optional configuration (defaults to Config class)
        """
        # Initialize parent LoginPage (gets all 4 base components)
        super().__init__(driver, timeout, config)

        # Add ONLY the visual debugger component
        self.visual_debugger = VisualDebugger(driver, timeout)

        self.logger.debug("LoginPageDemo initialized with visual debugging support")
