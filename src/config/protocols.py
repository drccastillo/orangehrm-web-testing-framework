"""
Configuration service protocols.
Defines interfaces for configuration services using Protocol (PEP 544).

This enables dependency injection and makes the framework testable.
"""

# pylint: disable=unnecessary-ellipsis
from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class ConfigService(Protocol):
    """
    Protocol for configuration services.

    Any configuration service must implement these properties and methods.
    This enables dependency injection and allows for multiple implementations
    (EnvironmentConfigService, TestConfigService, MockConfigService, etc.).

    Example:
        >>> config: ConfigService = EnvironmentConfigService()
        >>> url = config.base_url
        >>> username = config.username
    """

    # Application Configuration
    @property
    def base_url(self) -> str:
        """Get the base URL of the application under test."""
        ...

    @property
    def username(self) -> str:
        """Get the default username for authentication."""
        ...

    @property
    def password(self) -> str:
        """Get the default password for authentication."""
        ...

    # Browser Configuration
    @property
    def default_browser(self) -> str:
        """Get the default browser to use (chrome, firefox, edge)."""
        ...

    @property
    def headless(self) -> bool:
        """Get whether to run browser in headless mode."""
        ...

    # Timeout Configuration
    @property
    def default_timeout(self) -> int:
        """Get the default timeout in seconds for explicit waits."""
        ...

    @property
    def page_load_timeout(self) -> int:
        """Get the page load timeout in seconds."""
        ...

    # Window Configuration
    @property
    def window_width(self) -> int:
        """Get the browser window width in pixels."""
        ...

    @property
    def window_height(self) -> int:
        """Get the browser window height in pixels."""
        ...

    @property
    def maximize_window(self) -> bool:
        """Get whether to maximize browser window."""
        ...

    # Screenshot Configuration
    @property
    def screenshot_on_failure(self) -> bool:
        """Get whether to take screenshots on test failure."""
        ...

    @property
    def screenshots_dir(self) -> Path:
        """Get the directory path for storing screenshots."""
        ...

    # Reports Configuration
    @property
    def reports_dir(self) -> Path:
        """Get the directory path for storing test reports."""
        ...

    # Methods
    def ensure_directories(self) -> None:
        """
        Create necessary directories if they don't exist.
        Should create screenshots_dir and reports_dir.
        """
        ...
