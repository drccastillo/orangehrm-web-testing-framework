"""
Adapters for Playwright automation framework.
Implements framework-agnostic protocols using Adapter pattern.
"""

from src.adapters.playwright_element import PlaywrightWebElement

__all__ = ["PlaywrightWebElement"]
