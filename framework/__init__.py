"""
Test Automation Framework - Infrastructure Layer (Clean Architecture).

This module provides reusable infrastructure using Mixins pattern.
Not specific to OrangeHRM.

For page objects, use:
- framework.page.mixins (ElementFinderMixin, ElementInteractorMixin, etc.)
- framework.page.components (ElementFinder, ElementInteractor, etc.)

See CLEAN_ARCHITECTURE_MIGRATION_COMPLETE.md for usage guide.
"""

__version__ = '2.0.0'  # Major version bump - Breaking change (removed BasePage)

# Framework exports
from .browser import DriverFactory
from .config import Config
from .utils import TestLogger, FrameworkException

__all__ = [
    'DriverFactory',
    'Config',
    'TestLogger',
    'FrameworkException',
]
