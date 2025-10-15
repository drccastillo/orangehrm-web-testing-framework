"""
Adapters for different automation frameworks.
Implements framework-agnostic protocols using Adapter pattern.
"""

from src.adapters.playwright_element import PlaywrightWebElement
from src.adapters.selenium_element import SeleniumWebElement

__all__ = ["SeleniumWebElement", "PlaywrightWebElement"]
