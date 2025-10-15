"""
Locator value objects for framework-agnostic element location.
Replaces primitive tuples/strings with rich domain objects (Phase 2.1).
"""

from abc import ABC, abstractmethod
from enum import Enum


class LocatorStrategy(Enum):
    """Enumeration of supported locator strategies."""

    ID = "id"
    NAME = "name"
    CSS = "css"
    XPATH = "xpath"
    CLASS_NAME = "class"
    TAG_NAME = "tag"
    LINK_TEXT = "link_text"
    PARTIAL_LINK_TEXT = "partial_link_text"


class Locator(ABC):
    """
    Abstract base class for locator value objects.

    Replaces primitive tuples (By.ID, "value") and strings ("#value")
    with rich domain objects that provide:
    - Validation
    - Self-documentation
    - Framework-agnostic representation
    - Type safety

    Example:
        >>> locator = SeleniumLocator(LocatorStrategy.ID, "username", "Username field")
        >>> print(locator)  # "SeleniumLocator(Username field)"
        >>> native = locator.to_native()  # (By.ID, "username")
    """

    def __init__(self, strategy: LocatorStrategy, value: str, description: str = ""):
        """
        Initialize locator.

        Args:
            strategy: The locator strategy (ID, CSS, XPATH, etc.)
            value: The locator value
            description: Human-readable description for debugging

        Raises:
            ValueError: If value is empty
        """
        if not value or not isinstance(value, str):
            raise ValueError(f"Locator value must be non-empty string, got: {value}")

        self.strategy = strategy
        self.value = value
        self.description = description or f"{strategy.value}: {value}"

    @abstractmethod
    def to_native(self):
        """
        Convert to framework-specific native format.

        Returns:
            Framework-specific locator format
            - Selenium: tuple (By.X, "value")
            - Playwright: string selector
        """

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"{self.__class__.__name__}({self.description})"

    def __str__(self) -> str:
        """Human-readable string."""
        return self.description

    def __eq__(self, other) -> bool:
        """Equality comparison."""
        if not isinstance(other, Locator):
            return False
        return (
            self.strategy == other.strategy
            and self.value == other.value
            and isinstance(other, type(self))
        )

    def __hash__(self) -> int:
        """Make locator hashable for use in dicts/sets."""
        return hash((type(self).__name__, self.strategy, self.value))
