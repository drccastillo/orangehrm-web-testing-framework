"""
Custom exceptions for the test automation framework.
Provides specific error types for better error handling and debugging.
"""


class FrameworkException(Exception):
    """Base exception for all framework-related errors."""
    pass


class ElementNotFoundException(FrameworkException):
    """Raised when an element cannot be found on the page."""

    def __init__(self, locator: tuple, message: str = None):
        self.locator = locator
        self.message = message or f"Element not found with locator: {locator}"
        super().__init__(self.message)


class ElementNotClickableException(FrameworkException):
    """Raised when an element is not clickable."""

    def __init__(self, locator: tuple, message: str = None):
        self.locator = locator
        self.message = message or f"Element not clickable with locator: {locator}"
        super().__init__(self.message)


class ElementNotVisibleException(FrameworkException):
    """Raised when an element is not visible on the page."""

    def __init__(self, locator: tuple, message: str = None):
        self.locator = locator
        self.message = message or f"Element not visible with locator: {locator}"
        super().__init__(self.message)


class PageNotLoadedException(FrameworkException):
    """Raised when a page fails to load properly."""

    def __init__(self, page_name: str, message: str = None):
        self.page_name = page_name
        self.message = message or f"Page '{page_name}' did not load properly"
        super().__init__(self.message)


class InvalidParameterException(FrameworkException):
    """Raised when an invalid parameter is passed to a method."""

    def __init__(self, parameter_name: str, value: any, message: str = None):
        self.parameter_name = parameter_name
        self.value = value
        self.message = message or f"Invalid parameter '{parameter_name}': {value}"
        super().__init__(self.message)


class ConfigurationException(FrameworkException):
    """Raised when there's a configuration error."""

    def __init__(self, config_key: str, message: str = None):
        self.config_key = config_key
        self.message = message or f"Configuration error for key: {config_key}"
        super().__init__(self.message)
