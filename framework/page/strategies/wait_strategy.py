"""
Wait Strategy - Chain of Responsibility Pattern for element waits.

This module implements different wait strategies that can be chained together
to handle complex waiting scenarios.

Example:
    # Simple wait
    strategy = VisibilityWaitStrategy()
    element = strategy.wait_for(driver, locator, timeout=10)

    # Chained waits (try visibility, then clickable, then presence)
    strategy = (VisibilityWaitStrategy()
        .set_next(ClickableWaitStrategy())
        .set_next(PresenceWaitStrategy()))

    element = strategy.wait_for(driver, locator, timeout=10)

Reference: https://refactoring.guru/design-patterns/chain-of-responsibility
"""
from abc import ABC, abstractmethod
from typing import Tuple, Optional, List, Union
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from framework.utils.logger import TestLogger


class WaitStrategy(ABC):
    """
    Abstract base class for wait strategies (Chain of Responsibility).

    Each strategy tries to wait for an element using a specific condition.
    If it fails, it passes the request to the next strategy in the chain.
    """

    def __init__(self):
        """Initialize wait strategy."""
        self._next_strategy: Optional['WaitStrategy'] = None
        self.logger = TestLogger.get_logger(self.__class__.__name__)

    def set_next(self, strategy: 'WaitStrategy') -> 'WaitStrategy':
        """
        Set the next strategy in the chain.

        Args:
            strategy: Next wait strategy to try if this one fails

        Returns:
            The next strategy (for method chaining)
        """
        self._next_strategy = strategy
        return strategy

    @abstractmethod
    def can_handle(self) -> str:
        """
        Return the name of the wait condition this strategy handles.

        Returns:
            Strategy name
        """
        pass

    @abstractmethod
    def _wait(
        self,
        driver: WebDriver,
        locator: Tuple[str, str],
        timeout: int
    ) -> Optional[WebElement]:
        """
        Implement the actual wait logic.

        Args:
            driver: WebDriver instance
            locator: Element locator tuple
            timeout: Maximum wait time in seconds

        Returns:
            WebElement if found, None if wait fails
        """
        pass

    def wait_for(
        self,
        driver: WebDriver,
        locator: Tuple[str, str],
        timeout: int = 10
    ) -> Optional[WebElement]:
        """
        Wait for element using this strategy or pass to next in chain.

        Args:
            driver: WebDriver instance
            locator: Element locator tuple
            timeout: Maximum wait time in seconds

        Returns:
            WebElement if found by any strategy in the chain

        Raises:
            TimeoutException: If no strategy in the chain can find the element
        """
        self.logger.debug(f"Trying {self.can_handle()} wait strategy for {locator}")

        try:
            element = self._wait(driver, locator, timeout)
            if element:
                self.logger.debug(f"✅ {self.can_handle()} successful")
                return element
        except TimeoutException:
            self.logger.debug(f"❌ {self.can_handle()} failed, trying next...")

        # If this strategy fails, try the next one
        if self._next_strategy:
            return self._next_strategy.wait_for(driver, locator, timeout)

        # No more strategies to try
        self.logger.error(f"All wait strategies failed for {locator}")
        raise TimeoutException(
            f"Element {locator} not found after trying all wait strategies"
        )


class VisibilityWaitStrategy(WaitStrategy):
    """Wait for element to be visible (most common)."""

    def can_handle(self) -> str:
        """Return strategy name."""
        return "Visibility Wait"

    def _wait(
        self,
        driver: WebDriver,
        locator: Tuple[str, str],
        timeout: int
    ) -> Optional[WebElement]:
        """
        Wait for element to be visible.

        Args:
            driver: WebDriver instance
            locator: Element locator tuple
            timeout: Maximum wait time in seconds

        Returns:
            Visible WebElement
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))


class ClickableWaitStrategy(WaitStrategy):
    """Wait for element to be clickable."""

    def can_handle(self) -> str:
        """Return strategy name."""
        return "Clickable Wait"

    def _wait(
        self,
        driver: WebDriver,
        locator: Tuple[str, str],
        timeout: int
    ) -> Optional[WebElement]:
        """
        Wait for element to be clickable.

        Args:
            driver: WebDriver instance
            locator: Element locator tuple
            timeout: Maximum wait time in seconds

        Returns:
            Clickable WebElement
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))


class PresenceWaitStrategy(WaitStrategy):
    """Wait for element to be present in DOM (may not be visible)."""

    def can_handle(self) -> str:
        """Return strategy name."""
        return "Presence Wait"

    def _wait(
        self,
        driver: WebDriver,
        locator: Tuple[str, str],
        timeout: int
    ) -> Optional[WebElement]:
        """
        Wait for element to be present in DOM.

        Args:
            driver: WebDriver instance
            locator: Element locator tuple
            timeout: Maximum wait time in seconds

        Returns:
            WebElement (may not be visible)
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))


class InvisibilityWaitStrategy(WaitStrategy):
    """Wait for element to become invisible or disappear."""

    def can_handle(self) -> str:
        """Return strategy name."""
        return "Invisibility Wait"

    def _wait(
        self,
        driver: WebDriver,
        locator: Tuple[str, str],
        timeout: int
    ) -> Optional[WebElement]:
        """
        Wait for element to become invisible.

        Args:
            driver: WebDriver instance
            locator: Element locator tuple
            timeout: Maximum wait time in seconds

        Returns:
            None (element is invisible)
        """
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.invisibility_of_element_located(locator))
        return None  # Element is invisible


class TextPresentWaitStrategy(WaitStrategy):
    """Wait for specific text to be present in element."""

    def __init__(self, text: str):
        """
        Initialize with expected text.

        Args:
            text: Text to wait for
        """
        super().__init__()
        self.text = text

    def can_handle(self) -> str:
        """Return strategy name."""
        return f"Text '{self.text}' Wait"

    def _wait(
        self,
        driver: WebDriver,
        locator: Tuple[str, str],
        timeout: int
    ) -> Optional[WebElement]:
        """
        Wait for text to be present in element.

        Args:
            driver: WebDriver instance
            locator: Element locator tuple
            timeout: Maximum wait time in seconds

        Returns:
            WebElement containing the text
        """
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.text_to_be_present_in_element(locator, self.text))
        # Return the element after text is present
        return driver.find_element(*locator)


class PresenceOfAllWaitStrategy(WaitStrategy):
    """Wait for multiple elements to be present in DOM."""

    def can_handle(self) -> str:
        """Return strategy name."""
        return "Presence of All Wait"

    def _wait(
        self,
        driver: WebDriver,
        locator: Tuple[str, str],
        timeout: int
    ) -> Optional[List[WebElement]]:
        """
        Wait for all elements matching locator to be present in DOM.

        Args:
            driver: WebDriver instance
            locator: Element locator tuple
            timeout: Maximum wait time in seconds

        Returns:
            List of WebElements (may not be visible)
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))


# Convenience function for default wait chain
def create_default_wait_chain() -> WaitStrategy:
    """
    Create a default wait chain: Visibility → Clickable → Presence.

    This handles most common scenarios:
    1. Try to find visible element first (most common)
    2. If not visible, try clickable (for buttons/links)
    3. If not clickable, try just presence (hidden elements)

    Returns:
        WaitStrategy chain

    Example:
        strategy = create_default_wait_chain()
        element = strategy.wait_for(driver, locator, timeout=10)
    """
    visibility = VisibilityWaitStrategy()
    clickable = ClickableWaitStrategy()
    presence = PresenceWaitStrategy()

    visibility.set_next(clickable).set_next(presence)

    return visibility
