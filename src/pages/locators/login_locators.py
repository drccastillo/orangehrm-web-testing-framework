"""
Playwright functional locators for the Login Page.

Following Playwright best practices, these use user-facing locators:
- get_by_placeholder() for input fields
- get_by_role() for buttons
- get_by_text() for messages
- CSS selectors only when necessary

Reference: https://playwright.dev/python/docs/locators
"""

# ruff: noqa: N802
# Locator functions use UPPERCASE naming convention for consistency with constants


class LoginLocators:
    """
    Playwright functional locators for the Login Page.

    These use Playwright's recommended locator methods that reflect how users
    perceive the page. Functional locators are more resilient to DOM changes.

    Benefits:
        - User-facing (matches how users interact)
        - More resilient to implementation changes
        - Better accessibility (encourages semantic HTML)
        - Self-documenting (readable locators)

    Playwright Locator Priority:
        1. get_by_role() - Accessibility attributes
        2. get_by_label() - Form labels
        3. get_by_placeholder() - Input placeholders
        4. get_by_text() - Visible text
        5. CSS/XPath - Last resort only

    Example:
        >>> login_page = LoginPage(page)
        >>> # These now return callables that create locators dynamically
        >>> login_page.send_keys(LoginLocators.USERNAME_INPUT, "admin")
    """

    # Input fields - using placeholder text (user-facing)
    @staticmethod
    def USERNAME_INPUT(page):
        """Username input field located by placeholder text."""
        return page.get_by_placeholder("Username")

    @staticmethod
    def PASSWORD_INPUT(page):
        """Password input field located by placeholder text."""
        return page.get_by_placeholder("Password")

    # Buttons - using role (accessibility-first)
    @staticmethod
    def LOGIN_BUTTON(page):
        """Login submit button located by role."""
        return page.get_by_role("button", name="Login")

    # Messages and alerts - using CSS as fallback (no text guarantee)
    @staticmethod
    def ERROR_MESSAGE(page):
        """Login error message (CSS selector - text varies)."""
        return page.locator(".oxd-alert-content-text")

    # Branding elements - using CSS (no better option)
    @staticmethod
    def LOGIN_LOGO(page):
        """OrangeHRM logo image (CSS selector)."""
        return page.locator(".orangehrm-login-branding img")

    @staticmethod
    def LOGIN_TITLE(page):
        """Login page title (CSS selector)."""
        return page.locator(".orangehrm-login-title")
