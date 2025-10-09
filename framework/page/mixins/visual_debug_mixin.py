"""
Visual Debug Mixin - provides visual debugging capabilities.
Implements Interface Segregation Principle (Optional capability).
"""
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from framework.page.components import VisualDebugger


class VisualDebugMixin:
    """
    Mixin for pages that need visual debugging capabilities (optional).

    Provides methods for visual feedback during debugging.
    Requires the class to have a 'visual_debugger' attribute of type VisualDebugger.

    Note: This is an optional mixin. Only include it in pages that need debugging features.
    """

    visual_debugger: 'VisualDebugger'  # Type hint for required attribute

    def highlight_element(
        self,
        locator: Tuple[str, str],
        duration: int = None,
        color: str = None,
        border: str = None
    ) -> None:
        """
        Highlight an element on the page for visual debugging.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            duration: Duration to highlight in seconds
            color: Border color for highlighting
            border: Border style
        """
        return self.visual_debugger.highlight_element(locator, duration, color, border)

    def blink_element(
        self,
        locator: Tuple[str, str],
        times: int = None,
        color: str = None
    ) -> None:
        """
        Blink an element multiple times for visual debugging.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            times: Number of times to blink
            color: Border color for blinking
        """
        return self.visual_debugger.blink_element(locator, times, color)

    def highlight_multiple_elements(
        self,
        locators: list,
        duration: int = None,
        color: str = None
    ) -> None:
        """
        Highlight multiple elements simultaneously.

        Args:
            locators: List of locator tuples
            duration: Duration to highlight in seconds
            color: Border color for highlighting
        """
        return self.visual_debugger.highlight_multiple_elements(locators, duration, color)

    def flash_background(self, locator: Tuple[str, str], color: str = "yellow", times: int = 3) -> None:
        """
        Flash the background color of an element.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            color: Background color to flash
            times: Number of times to flash
        """
        return self.visual_debugger.flash_background(locator, color, times)

    def outline_element(self, locator: Tuple[str, str], color: str = "red", width: str = "3px") -> None:
        """
        Add a permanent outline to an element (until page refresh).

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            color: Outline color
            width: Outline width
        """
        return self.visual_debugger.outline_element(locator, color, width)
