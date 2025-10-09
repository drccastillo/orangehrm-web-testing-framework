"""
JavaScript Mixin - provides JavaScript execution capabilities.
Implements Interface Segregation Principle.
"""
from typing import Tuple, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from framework.page.components import JavaScriptExecutor


class JavaScriptMixin:
    """
    Mixin for pages that need JavaScript execution capabilities.

    Provides methods to execute JavaScript code.
    Requires the class to have a 'js_executor' attribute of type JavaScriptExecutor.
    """

    js_executor: 'JavaScriptExecutor'  # Type hint for required attribute

    def execute_script(self, script: str, *args) -> Any:
        """
        Execute JavaScript code.

        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script

        Returns:
            Result of the JavaScript execution
        """
        return self.js_executor.execute_script(script, *args)

    def execute_async_script(self, script: str, *args) -> Any:
        """
        Execute asynchronous JavaScript code.

        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script

        Returns:
            Result of the JavaScript execution
        """
        return self.js_executor.execute_async_script(script, *args)

    def scroll_to_element(self, locator: Tuple[str, str]) -> None:
        """
        Scroll to an element on the page.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
        """
        return self.js_executor.scroll_to_element(locator)

    def scroll_to_top(self) -> None:
        """Scroll to the top of the page."""
        return self.js_executor.scroll_to_top()

    def scroll_to_bottom(self) -> None:
        """Scroll to the bottom of the page."""
        return self.js_executor.scroll_to_bottom()

    def scroll_by_pixels(self, x: int, y: int) -> None:
        """
        Scroll by specific pixel amount.

        Args:
            x: Horizontal scroll amount
            y: Vertical scroll amount
        """
        return self.js_executor.scroll_by_pixels(x, y)

    def click_element_via_js(self, locator: Tuple[str, str]) -> None:
        """
        Click an element using JavaScript (useful for hidden/obscured elements).

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
        """
        return self.js_executor.click_element_via_js(locator)

    def set_element_value(self, locator: Tuple[str, str], value: str) -> None:
        """
        Set an element's value using JavaScript.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            value: Value to set
        """
        return self.js_executor.set_element_value(locator, value)

    def get_element_property(self, locator: Tuple[str, str], property_name: str) -> Any:
        """
        Get an element's property using JavaScript.

        Args:
            locator: Tuple containing (By.STRATEGY, "locator_value")
            property_name: Name of the property

        Returns:
            Value of the property
        """
        return self.js_executor.get_element_property(locator, property_name)
