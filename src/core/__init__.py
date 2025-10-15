"""
Core components for the testing framework.
Contains framework-agnostic abstractions and value objects.
"""

from src.core.locator import Locator, LocatorStrategy
from src.core.locator_factory import LocatorFactory
from src.core.playwright_locator import PlaywrightLocator
from src.core.selenium_locator import SeleniumLocator

__all__ = [
    "Locator",
    "LocatorStrategy",
    "SeleniumLocator",
    "PlaywrightLocator",
    "LocatorFactory",
]
