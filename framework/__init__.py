"""
Test Automation Framework - Infrastructure Layer.

This module provides reusable infrastructure that can be used in ANY web testing project.
Not specific to OrangeHRM.
"""

__version__ = '1.0.0'

# Framework exports
from .browser import DriverFactory, DriverManager
from .page import BasePage
from .config import Config
from .utils import TestLogger, FrameworkException

__all__ = [
    'DriverFactory',
    'DriverManager',
    'BasePage',
    'Config',
    'TestLogger',
    'FrameworkException',
]
