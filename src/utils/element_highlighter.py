"""
Element Highlighter for visual debugging.
Extracted from BasePage following Single Responsibility Principle.

This version works with BrowserProtocol for framework-agnostic highlighting.
"""

import time

from src.constants.visual_debugging import (
    BLINK_DELAY_SECONDS,
    DEFAULT_BLINK_COLOR,
    DEFAULT_BLINK_TIMES,
    DEFAULT_BORDER_WIDTH,
    DEFAULT_HIGHLIGHT_COLOR,
    DEFAULT_HIGHLIGHT_DURATION,
)


class ElementHighlighter:
    """
    Handles visual debugging operations for web elements.

    This class works with BrowserProtocol, making it framework-agnostic.
    It uses JavaScript execution to highlight elements.

    Responsibilities:
    - Highlight elements with borders and colors
    - Blink elements for attention
    - Manage visual debugging styling

    This class follows SRP by focusing solely on visual debugging,
    extracted from the God Class BasePage.

    Design Pattern:
        - Dependency on abstraction (BrowserProtocol) not concrete implementation
        - Single Responsibility: Visual debugging only
    """

    def __init__(self, browser):
        """
        Initialize the element highlighter.

        Args:
            browser: Browser adapter implementing BrowserProtocol
        """
        self.browser = browser

    def highlight_element(
        self,
        selector: str,
        duration: int | None = None,
        color: str | None = None,
        border: str | None = None,
    ) -> None:
        """
        Highlight an element on the page for visual debugging.

        Args:
            selector: Element selector string (CSS or XPath)
            duration: Duration to highlight in seconds (default: 2)
            color: Border color for highlighting (default: "red")
            border: Border style (default: "3px solid")

        Example:
            >>> highlighter.highlight_element("input[name='username']", duration=3, color="blue")
        """
        duration = duration or DEFAULT_HIGHLIGHT_DURATION
        color = color or DEFAULT_HIGHLIGHT_COLOR
        border = border or f"{DEFAULT_BORDER_WIDTH} solid"

        # JavaScript to highlight element
        highlight_script = """
        (function(selector, border, color) {
            const element = document.querySelector(selector);
            if (!element) return null;

            const originalStyle = element.getAttribute('style') || '';
            element.setAttribute('style', originalStyle + '; border: ' + border + ' ' + color + ' !important;');

            return originalStyle;
        })(arguments[0], arguments[1], arguments[2]);
        """

        try:
            original_style = self.browser.execute_script(highlight_script, selector, border, color)
            time.sleep(duration)

            # Restore original style
            restore_script = """
            (function(selector, originalStyle) {
                const element = document.querySelector(selector);
                if (element) {
                    element.setAttribute('style', originalStyle);
                }
            })(arguments[0], arguments[1]);
            """
            self.browser.execute_script(restore_script, selector, original_style or "")
        except Exception:
            # Silently fail if highlighting doesn't work (e.g., element not found)
            pass

    def blink_element(
        self, selector: str, times: int | None = None, color: str | None = None
    ) -> None:
        """
        Blink an element multiple times for visual debugging.

        Args:
            selector: Element selector string (CSS or XPath)
            times: Number of times to blink (default: 3)
            color: Border color for blinking (default: "red")

        Example:
            >>> highlighter.blink_element("button[type='submit']", times=5, color="green")
        """
        times = times or DEFAULT_BLINK_TIMES
        color = color or DEFAULT_BLINK_COLOR

        blink_script = """
        (function(selector) {
            const element = document.querySelector(selector);
            if (!element) return null;
            return element.getAttribute('style') || '';
        })(arguments[0]);
        """

        try:
            original_style = self.browser.execute_script(blink_script, selector)

            for _ in range(times):
                # Highlight on
                highlight_on = f"""
                (function(selector, color) {{
                    const element = document.querySelector(selector);
                    if (element) {{
                        element.setAttribute('style', '{original_style}; border: {DEFAULT_BORDER_WIDTH} solid ' + color + ' !important; background-color: yellow !important;');
                    }}
                }})(arguments[0], arguments[1]);
                """
                self.browser.execute_script(highlight_on, selector, color)
                time.sleep(BLINK_DELAY_SECONDS)

                # Highlight off
                highlight_off = f"""
                (function(selector) {{
                    const element = document.querySelector(selector);
                    if (element) {{
                        element.setAttribute('style', '{original_style}');
                    }}
                }})(arguments[0]);
                """
                self.browser.execute_script(highlight_off, selector)
                time.sleep(BLINK_DELAY_SECONDS)
        except Exception:
            # Silently fail if blinking doesn't work
            pass
