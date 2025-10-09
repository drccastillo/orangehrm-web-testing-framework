# Mixins Usage Examples

## Overview

Mixins implement the Interface Segregation Principle (ISP), allowing page objects to include only the capabilities they need.

---

## Example 1: Read-Only Page (Minimal Capabilities)

A page that only needs to find elements and validate their presence:

```python
from selenium.webdriver.remote.webdriver import WebDriver
from framework.page.components import ElementFinder, ElementValidator
from framework.page.mixins import ElementFinderMixin, ElementValidatorMixin


class ReadOnlyDashboardPage(ElementFinderMixin, ElementValidatorMixin):
    """
    Read-only dashboard page.
    Only includes finding and validation capabilities.
    """

    def __init__(self, driver: WebDriver, timeout: int = 10):
        # Initialize only the components we need
        self.finder = ElementFinder(driver, timeout)
        self.validator = ElementValidator(driver, timeout)

    def is_dashboard_loaded(self) -> bool:
        """Check if dashboard is loaded."""
        return self.is_element_visible(("css", ".dashboard-header"))

    def get_dashboard_title(self) -> str:
        """Get dashboard title text."""
        element = self.find_element(("css", "h1.title"))
        return element.text
```

---

## Example 2: Interactive Form Page (Standard Capabilities)

A page with forms that needs finding, interaction, and validation:

```python
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from framework.page.components import ElementFinder, ElementInteractor, ElementValidator
from framework.page.mixins import (
    ElementFinderMixin,
    ElementInteractorMixin,
    ElementValidatorMixin
)


class LoginPage(ElementFinderMixin, ElementInteractorMixin, ElementValidatorMixin):
    """
    Login page with form interaction capabilities.
    Includes finding, interaction, and validation.
    """

    # Locators
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-btn")

    def __init__(self, driver: WebDriver, timeout: int = 10):
        # Initialize components we need
        self.finder = ElementFinder(driver, timeout)
        self.interactor = ElementInteractor(driver, timeout)
        self.validator = ElementValidator(driver, timeout)

    def login(self, username: str, password: str) -> None:
        """Perform login."""
        self.send_keys(self.USERNAME_INPUT, username)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def is_login_page_loaded(self) -> bool:
        """Check if login page is loaded."""
        return self.is_element_visible(self.LOGIN_BUTTON)
```

---

## Example 3: Complex Page (Full Capabilities)

A page that needs all capabilities including navigation and JavaScript:

```python
from selenium.webdriver.remote.webdriver import WebDriver
from framework.page.components import (
    ElementFinder,
    ElementInteractor,
    ElementValidator,
    NavigationHelper,
    JavaScriptExecutor,
)
from framework.page.mixins import (
    ElementFinderMixin,
    ElementInteractorMixin,
    ElementValidatorMixin,
    NavigationMixin,
    JavaScriptMixin,
)


class ComplexPage(
    ElementFinderMixin,
    ElementInteractorMixin,
    ElementValidatorMixin,
    NavigationMixin,
    JavaScriptMixin,
):
    """
    Complex page with all capabilities except visual debugging.
    """

    def __init__(self, driver: WebDriver, timeout: int = 10):
        # Initialize all components
        self.finder = ElementFinder(driver, timeout)
        self.interactor = ElementInteractor(driver, timeout)
        self.validator = ElementValidator(driver, timeout)
        self.navigation = NavigationHelper(driver)
        self.js_executor = JavaScriptExecutor(driver, timeout)

    def navigate_and_interact(self, url: str) -> None:
        """Navigate to URL and perform JavaScript interaction."""
        self.navigate_to(url)
        self.scroll_to_bottom()
        # ... more interactions
```

---

## Example 4: Debug Page (All Capabilities + Visual Debugging)

A page used during development that includes visual debugging:

```python
from selenium.webdriver.remote.webdriver import WebDriver
from framework.page.components import (
    ElementFinder,
    ElementInteractor,
    ElementValidator,
    NavigationHelper,
    JavaScriptExecutor,
    VisualDebugger,
)
from framework.page.mixins import (
    ElementFinderMixin,
    ElementInteractorMixin,
    ElementValidatorMixin,
    NavigationMixin,
    JavaScriptMixin,
    VisualDebugMixin,
)


class DebugPage(
    ElementFinderMixin,
    ElementInteractorMixin,
    ElementValidatorMixin,
    NavigationMixin,
    JavaScriptMixin,
    VisualDebugMixin,
):
    """
    Debug page with all capabilities including visual debugging.
    Use during development/debugging, remove VisualDebugMixin in production.
    """

    def __init__(self, driver: WebDriver, timeout: int = 10):
        # Initialize all components including visual debugger
        self.finder = ElementFinder(driver, timeout)
        self.interactor = ElementInteractor(driver, timeout)
        self.validator = ElementValidator(driver, timeout)
        self.navigation = NavigationHelper(driver)
        self.js_executor = JavaScriptExecutor(driver, timeout)
        self.visual_debugger = VisualDebugger(driver, timeout)

    def debug_click(self, locator):
        """Click with visual feedback."""
        self.highlight_element(locator, duration=2, color="yellow")
        self.click(locator)
```

---

## Comparison: BasePage vs Mixins

### Using BasePage (Current Approach)

```python
# All pages inherit everything from BasePage
class MyPage(BasePage):
    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)
        # Has ALL capabilities whether needed or not
```

**Pros**:
- Simple to use
- Backward compatible
- All methods available

**Cons**:
- Violates ISP (forced to have capabilities not needed)
- Heavier memory footprint
- Not clear what capabilities page actually uses

### Using Mixins (New Approach)

```python
# Only include capabilities you need
class MyPage(ElementFinderMixin, ElementInteractorMixin):
    def __init__(self, driver, timeout=10):
        self.finder = ElementFinder(driver, timeout)
        self.interactor = ElementInteractor(driver, timeout)
        # Only has finding and interaction capabilities
```

**Pros**:
- Follows ISP perfectly
- Lighter memory footprint
- Clear intent (what page can do)
- More testable (mock only what's needed)

**Cons**:
- Slightly more verbose initialization
- Need to choose correct mixins

---

## Migration Strategy

### Phase 1: Backward Compatibility (Current)

Keep BasePage as is. New pages can use Mixins.

```python
# Old code continues to work
class OldPage(BasePage):
    pass

# New code uses Mixins
class NewPage(ElementFinderMixin, ElementInteractorMixin):
    pass
```

### Phase 2: Gradual Migration

Migrate pages one by one to Mixins:

```python
# Before
class LoginPage(BasePage):
    pass

# After
class LoginPage(ElementFinderMixin, ElementInteractorMixin, ElementValidatorMixin):
    def __init__(self, driver, timeout=10):
        self.finder = ElementFinder(driver, timeout)
        self.interactor = ElementInteractor(driver, timeout)
        self.validator = ElementValidator(driver, timeout)
```

### Phase 3: Full Migration (Future)

Once all pages use Mixins, BasePage can be deprecated.

---

## Best Practices

### 1. Choose Minimal Mixins

Only include mixins you actually use:

```python
# ❌ Bad: Including all mixins when only need a few
class SimplePage(
    ElementFinderMixin,
    ElementInteractorMixin,
    ElementValidatorMixin,
    NavigationMixin,
    JavaScriptMixin,
    VisualDebugMixin,  # Not needed!
):
    pass

# ✅ Good: Only include what you need
class SimplePage(ElementFinderMixin, ElementValidatorMixin):
    pass
```

### 2. VisualDebugMixin is Optional

Only use VisualDebugMixin during development:

```python
# During development
class MyPage(ElementFinderMixin, VisualDebugMixin):
    pass

# In production (remove visual debugging)
class MyPage(ElementFinderMixin):
    pass
```

### 3. Initialize Only Required Components

```python
class MyPage(ElementFinderMixin, ElementInteractorMixin):
    def __init__(self, driver, timeout=10):
        # Only initialize what mixins require
        self.finder = ElementFinder(driver, timeout)
        self.interactor = ElementInteractor(driver, timeout)
        # Don't initialize validator if not using ElementValidatorMixin
```

---

## Benefits Summary

| Aspect | BasePage | Mixins |
|--------|----------|--------|
| **ISP Compliance** | ❌ No | ✅ Yes |
| **Memory Usage** | ⚠️ Higher | ✅ Lower |
| **Flexibility** | ⚠️ All or nothing | ✅ Pick what you need |
| **Testability** | ⚠️ Mock all components | ✅ Mock only what's used |
| **Intent Clarity** | ⚠️ Unclear capabilities | ✅ Clear from mixins |
| **Setup Complexity** | ✅ Simple | ⚠️ Slightly more code |
| **Backward Compat** | ✅ Yes | ✅ Yes (coexist) |

---

## Conclusion

**Recommendation**: Use Mixins for new pages to follow SOLID principles. Existing pages can continue using BasePage for backward compatibility.

**Future**: Gradual migration to Mixins will improve code quality and reduce technical debt.
