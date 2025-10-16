"""
Locators package for all page objects.

This package contains Playwright functional locators for all pages.
"""

from src.pages.locators.leave_locators import LeaveLocators
from src.pages.locators.login_locators import LoginLocators

__all__ = ["LoginLocators", "LeaveLocators"]
