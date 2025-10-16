"""
Core components for the Playwright testing framework.
Contains protocols and value objects for framework abstraction.
"""

from src.core.browser_protocol import BrowserProtocol, LocatorProtocol
from src.core.element_protocol import WebElementProtocol
from src.core.playwright_locator import PlaywrightLocator

__all__ = [
    "BrowserProtocol",
    "LocatorProtocol",
    "PlaywrightLocator",
    "WebElementProtocol",
]
