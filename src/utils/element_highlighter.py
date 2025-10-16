"""
Element Highlighter for visual debugging.

Simplified to use Playwright Page directly (Phase 1 refactor).
Improved error handling - no more bare except clauses.
"""

import time

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from src.enums.visual_debugging import (
    BLINK_DELAY_SECONDS,
    DEFAULT_BLINK_COLOR,
    DEFAULT_BLINK_TIMES,
    DEFAULT_BORDER_WIDTH,
    DEFAULT_HIGHLIGHT_COLOR,
    DEFAULT_HIGHLIGHT_DURATION,
)
from utils.logger import TestLogger


class ElementHighlighter:
    """
    Handles visual debugging operations using Playwright directly.

    Responsibilities:
    - Highlight elements with borders and colors
    - Blink elements for attention
    - Manage visual debugging styling

    This class follows SRP by focusing solely on visual debugging.

    Design Pattern:
        - Single Responsibility: Visual debugging only
        - Direct use of Playwright Page (no adapter layer)
    """

    def __init__(self, page: Page):
        """
        Initialize the element highlighter.

        Args:
            page: Playwright Page instance
        """
        self.page = page
        self.logger = TestLogger.get_logger(self.__class__.__name__)

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

        try:
            # JavaScript to highlight element
            original_style = self.page.evaluate(
                """
                ([selector, border, color]) => {
                    const element = document.querySelector(selector);
                    if (!element) return null;

                    const originalStyle = element.getAttribute('style') || '';
                    const newStyle = originalStyle +
                        '; border: ' + border + ' ' + color + ' !important;';
                    element.setAttribute('style', newStyle);

                    return originalStyle;
                }
                """,
                [selector, border, color],
            )

            time.sleep(duration)

            # Restore original style
            self.page.evaluate(
                """
                ([selector, originalStyle]) => {
                    const element = document.querySelector(selector);
                    if (element) {
                        element.setAttribute('style', originalStyle);
                    }
                }
                """,
                [selector, original_style or ""],
            )
        except PlaywrightTimeoutError as e:
            self.logger.warning(f"Timeout highlighting element {selector}: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error highlighting element {selector}: {e}")

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

        try:
            # Get original style
            original_style = self.page.evaluate(
                """
                (selector) => {
                    const element = document.querySelector(selector);
                    if (!element) return null;
                    return element.getAttribute('style') || '';
                }
                """,
                selector,
            )

            for _ in range(times):
                # Highlight on
                border_style = f"{DEFAULT_BORDER_WIDTH} solid"
                self.page.evaluate(
                    """
                    ([selector, color, border, originalStyle]) => {
                        const element = document.querySelector(selector);
                        if (element) {
                            const style = originalStyle + '; border: ' + border + ' ' +
                                color + ' !important; background-color: yellow !important;';
                            element.setAttribute('style', style);
                        }
                    }
                    """,
                    [selector, color, border_style, original_style],
                )
                time.sleep(BLINK_DELAY_SECONDS)

                # Highlight off
                self.page.evaluate(
                    """
                    ([selector, originalStyle]) => {
                        const element = document.querySelector(selector);
                        if (element) {
                            element.setAttribute('style', originalStyle);
                        }
                    }
                    """,
                    [selector, original_style],
                )
                time.sleep(BLINK_DELAY_SECONDS)
        except PlaywrightTimeoutError as e:
            self.logger.warning(f"Timeout blinking element {selector}: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error blinking element {selector}: {e}")
