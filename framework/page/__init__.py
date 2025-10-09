"""
Page object framework - Clean Architecture with Mixins pattern.

This module provides the foundation for page objects using Mixins pattern.
See CLEAN_ARCHITECTURE_MIGRATION_COMPLETE.md for usage guide.

Available:
- Mixins: framework.page.mixins (ElementFinderMixin, ElementInteractorMixin, etc.)
- Components: framework.page.components (ElementFinder, ElementInteractor, etc.)

Example:
    from framework.page.mixins import ElementFinderMixin, ElementInteractorMixin

    class MyPage(ElementFinderMixin, ElementInteractorMixin):
        def __init__(self, driver, timeout=10):
            self.driver = driver
            self.timeout = timeout
            self.finder = ElementFinder(driver, timeout)
            self.interactor = ElementInteractor(driver, timeout)
"""

__all__ = []  # Use mixins and components directly
