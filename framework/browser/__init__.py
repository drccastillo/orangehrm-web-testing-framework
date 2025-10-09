"""
Browser management module.
Provides driver factory for Selenium WebDriver.
Driver lifecycle is managed by pytest fixtures in conftest.py
"""
from .factory import (
    DriverFactory,
    BrowserStrategy,
    ChromeStrategy,
    FirefoxStrategy,
    EdgeStrategy
)

__all__ = [
    'DriverFactory',
    'BrowserStrategy',
    'ChromeStrategy',
    'FirefoxStrategy',
    'EdgeStrategy',
]
