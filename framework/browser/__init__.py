"""
Browser management module.
Provides driver factory and manager for Selenium WebDriver.
"""
from .factory import (
    DriverFactory,
    DriverManager,
    BrowserStrategy,
    ChromeStrategy,
    FirefoxStrategy,
    EdgeStrategy
)

__all__ = [
    'DriverFactory',
    'DriverManager',
    'BrowserStrategy',
    'ChromeStrategy',
    'FirefoxStrategy',
    'EdgeStrategy',
]
