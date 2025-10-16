"""
Core components for the Playwright testing framework.

Phase 4 refactor: Removed BrowserProtocol and WebElementProtocol.
Now using Playwright Page and Locator directly.
"""

from src.core.playwright_locator import PlaywrightLocator

__all__ = [
    "PlaywrightLocator",
]
