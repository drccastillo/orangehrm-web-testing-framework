# Web Test Automation Framework - Refactor Plan

**Version:** 1.0
**Framework:** OrangeHRM Test Automation (Pytest + Selenium + Playwright)
**Approach:** Incremental, Test-Driven, Pattern-Justified

---

## Executive Summary

This refactor plan addresses critical code smells and anti-patterns in the test automation framework while improving maintainability, extensibility, and reducing duplication between Selenium and Playwright implementations. The plan follows the RGR Loop (Red-Green-Refactor), applying SOLID principles and introducing design patterns only when they solve real coupling or extensibility problems.

### Key Problems Identified:
1. **90% code duplication** between Selenium and Playwright implementations
2. **Unjustified Singleton pattern** in Config class
3. **God Class anti-pattern** in BasePage classes (30+ methods, multiple responsibilities)
4. **Primitive Obsession** with locators as tuples/strings
5. **Property pollution** in page objects
6. **Tight coupling** to Config and fixtures
7. **Feature Envy** in tests accessing page internals

### Target Improvements:
- Reduce duplication by 70%+
- Improve testability via dependency injection
- Apply SRP to break down God Classes
- Create extensible architecture for new automation tools
- Maintain 100% test coverage throughout refactor

---

## Phase 1: Foundation Refactoring (Weeks 1-2)

**Goal:** Clean up code smells without introducing patterns yet. Establish safety net.

### 1.1 Extract Configuration from Singleton to Injectable Service

**Problem:** `Config` class uses unjustified Singleton pattern, making testing difficult.

**Code Smell:** Singleton, Global State

**Refactor Steps:**
1. Create `ConfigService` protocol (interface)
2. Create `EnvironmentConfigService` implementation
3. Inject config into page objects and tests via fixtures
4. Add characterization tests for current Config behavior
5. Replace all `Config.X` direct access with injected config

**Before:**
```python
# src/config/config.py
class Config:
    BASE_URL = os.getenv("URL", "http://localhost:8080")
    USERNAME = os.getenv("ORANGEHRM_USERNAME", "Admin")
    # ... class methods everywhere

# In tests:
login_page.login(Config.USERNAME, Config.PASSWORD)
```

**After:**
```python
# src/config/protocols.py
from typing import Protocol

class ConfigService(Protocol):
    @property
    def base_url(self) -> str: ...
    @property
    def username(self) -> str: ...
    @property
    def password(self) -> str: ...

# src/config/environment_config.py
class EnvironmentConfigService:
    def __init__(self, env_path: Path = None):
        load_dotenv(env_path)
        self._base_url = os.getenv("URL", "http://localhost:8080")
        # ... load other config

    @property
    def base_url(self) -> str:
        return self._base_url

# In conftest.py
@pytest.fixture(scope="session")
def config_service() -> ConfigService:
    return EnvironmentConfigService()

# In tests:
def test_login(login_page, config_service):
    login_page.login(config_service.username, config_service.password)
```

**Acceptance Criteria:**
- All tests pass
- No direct `Config.X` access remains
- Config is mockable in unit tests
- Config can be swapped for TestConfigService

---

### 1.2 Remove Property Pollution from Page Objects

**Problem:** LoginPage exposes 7 properties just to wrap locators. This is unnecessary indirection.

**Code Smell:** Feature Envy, Unnecessary Abstraction

**Refactor Steps:**
1. Remove property wrappers in LoginPage
2. Access locators directly via `self.locators.USERNAME_INPUT`
3. Update tests to not access locators directly (they shouldn't anyway)
4. Run tests to ensure no regression

**Before:**
```python
class LoginPage(BasePage):
    @property
    def USERNAME_INPUT(self):
        return self.locators.USERNAME_INPUT
    # ... 6 more properties

    def enter_username(self, username: str):
        self.send_keys(self.USERNAME_INPUT, username)  # Using property
```

**After:**
```python
class LoginPage(BasePage):
    # No properties needed

    def enter_username(self, username: str):
        self.send_keys(self.locators.USERNAME_INPUT, username)  # Direct access
```

**Acceptance Criteria:**
- All tests pass
- No properties exposing locators remain
- Tests interact only through methods, not properties

---

### 1.3 Extract Visual Debugging Methods to Separate Class

**Problem:** BasePage has 30+ methods, including debugging methods (highlight, blink). Violates SRP.

**Code Smell:** God Class, Too Many Responsibilities

**Refactor Steps:**
1. Create `ElementHighlighter` class
2. Move `highlight_element`, `blink_element`, and `_set_element_style` to new class
3. Inject highlighter into BasePage
4. Update tests to use highlighter methods

**Before:**
```python
class BasePage:
    def click(self, locator): ...
    def send_keys(self, locator, text): ...
    def highlight_element(self, locator): ...  # Debugging method
    def blink_element(self, locator): ...       # Debugging method
    # ... 26 more methods
```

**After:**
```python
# src/helpers/element_highlighter.py
class ElementHighlighter:
    """Handles visual debugging of elements."""

    def highlight(self, element: WebElement, duration: int = 2, color: str = "red"):
        """Highlight element with border."""
        # Implementation

    def blink(self, element: WebElement, times: int = 3, color: str = "red"):
        """Blink element for visibility."""
        # Implementation

# src/pages_selenium/base_page.py
class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.highlighter = ElementHighlighter(driver)  # Composed

    # Only interaction methods remain
    def click(self, locator): ...
    def send_keys(self, locator, text): ...
```

**Acceptance Criteria:**
- BasePage has <20 methods
- ElementHighlighter is reusable for both Selenium and Playwright
- All tests pass
- Visual debugging still works

---

### 1.4 Consolidate Magic Constants

**Problem:** Constants scattered across base classes: `BLINK_DELAY_SECONDS = 0.2`, `DEFAULT_HIGHLIGHT_COLOR = "red"`

**Code Smell:** Magic Numbers, Lack of Centralization

**Refactor Steps:**
1. Create `src/constants/visual_debugging.py`
2. Move all visual debugging constants there
3. Import constants where needed
4. Remove class-level constants from BasePage

**Before:**
```python
class BasePage:
    BLINK_DELAY_SECONDS = 0.2
    DEFAULT_BORDER_WIDTH = "3px"
    DEFAULT_HIGHLIGHT_COLOR = "red"
```

**After:**
```python
# src/constants/visual_debugging.py
class VisualDebuggingConfig:
    BLINK_DELAY_SECONDS: float = 0.2
    DEFAULT_BORDER_WIDTH: str = "3px"
    DEFAULT_HIGHLIGHT_COLOR: str = "red"
    DEFAULT_BLINK_COLOR: str = "red"
    DEFAULT_BLINK_TIMES: int = 3
    DEFAULT_HIGHLIGHT_DURATION: int = 2

# In ElementHighlighter:
from src.constants.visual_debugging import VisualDebuggingConfig

class ElementHighlighter:
    def highlight(self, element, duration=None, color=None):
        duration = duration or VisualDebuggingConfig.DEFAULT_HIGHLIGHT_DURATION
        color = color or VisualDebuggingConfig.DEFAULT_HIGHLIGHT_COLOR
```

**Acceptance Criteria:**
- All constants centralized
- Easy to modify defaults
- All tests pass

---

## Phase 2: Introduce Value Objects & Abstractions (Weeks 3-4)

**Goal:** Replace primitive obsession with rich domain objects. Create protocols for extensibility.

### 2.1 Replace Locator Tuples/Strings with Value Objects

**Problem:** Locators are primitives `(By.ID, "username")` or `"#username"`. No behavior, no validation.

**Code Smell:** Primitive Obsession, Feature Envy

**Refactor Steps:**
1. Create `Locator` abstract base class
2. Create `SeleniumLocator` and `PlaywrightLocator` implementations
3. Create `LocatorFactory` to convert existing tuples/strings
4. Update page objects to use Locator objects
5. Add validation and helper methods to Locator

**Implementation:**
```python
# src/core/locator.py
from abc import ABC, abstractmethod
from enum import Enum

class LocatorStrategy(Enum):
    ID = "id"
    NAME = "name"
    CSS = "css"
    XPATH = "xpath"
    CLASS_NAME = "class"

class Locator(ABC):
    """Abstract locator representing how to find an element."""

    def __init__(self, strategy: LocatorStrategy, value: str, description: str = ""):
        self.strategy = strategy
        self.value = value
        self.description = description or f"{strategy.value}: {value}"

    @abstractmethod
    def to_native(self):
        """Convert to framework-specific format."""
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({self.description})"

# src/core/selenium_locator.py
from selenium.webdriver.common.by import By

class SeleniumLocator(Locator):
    """Selenium-specific locator implementation."""

    STRATEGY_MAP = {
        LocatorStrategy.ID: By.ID,
        LocatorStrategy.NAME: By.NAME,
        LocatorStrategy.CSS: By.CSS_SELECTOR,
        LocatorStrategy.XPATH: By.XPATH,
        LocatorStrategy.CLASS_NAME: By.CLASS_NAME,
    }

    def to_native(self) -> tuple[str, str]:
        """Convert to Selenium (By.X, "value") tuple."""
        by_type = self.STRATEGY_MAP[self.strategy]
        return (by_type, self.value)

# src/core/playwright_locator.py
class PlaywrightLocator(Locator):
    """Playwright-specific locator implementation."""

    def to_native(self) -> str:
        """Convert to Playwright selector string."""
        if self.strategy == LocatorStrategy.ID:
            return f"#{self.value}"
        elif self.strategy == LocatorStrategy.CSS:
            return self.value
        elif self.strategy == LocatorStrategy.XPATH:
            return f"xpath={self.value}"
        # ... other strategies

# Usage in page objects:
class LoginLocators:
    USERNAME = SeleniumLocator(LocatorStrategy.NAME, "username", "Username input field")
    PASSWORD = SeleniumLocator(LocatorStrategy.NAME, "password", "Password input field")
```

**Benefits:**
- Rich domain model
- Validation at creation time
- Descriptive error messages
- Easier to add new locator strategies
- Framework-agnostic representation

**Acceptance Criteria:**
- All locators converted to value objects
- Backward compatibility maintained via `to_native()`
- All tests pass
- Locators are self-documenting

---

### 2.2 Create WebElement Abstraction Protocol

**Problem:** BasePage methods work directly with framework-specific elements (Selenium WebElement vs Playwright Locator).

**Code Smell:** Tight Coupling, No Abstraction

**Refactor Steps:**
1. Create `WebElementProtocol` interface
2. Create `SeleniumWebElement` and `PlaywrightWebElement` adapters
3. Update BasePage to work with protocol, not concrete types
4. This enables unification in Phase 3

**Implementation:**
```python
# src/core/protocols.py
from typing import Protocol, runtime_checkable

@runtime_checkable
class WebElementProtocol(Protocol):
    """Protocol for interacting with web elements across frameworks."""

    def click(self) -> None:
        """Click the element."""
        ...

    def send_keys(self, text: str) -> None:
        """Type text into element."""
        ...

    def get_text(self) -> str:
        """Get element text."""
        ...

    def get_attribute(self, name: str) -> str | None:
        """Get element attribute."""
        ...

    def is_visible(self) -> bool:
        """Check if element is visible."""
        ...

    def is_enabled(self) -> bool:
        """Check if element is enabled."""
        ...

# src/adapters/selenium_element.py
from selenium.webdriver.remote.webelement import WebElement

class SeleniumWebElement:
    """Adapter for Selenium WebElement to WebElementProtocol."""

    def __init__(self, element: WebElement):
        self._element = element

    def click(self) -> None:
        self._element.click()

    def send_keys(self, text: str) -> None:
        self._element.send_keys(text)

    # ... implement other methods

# src/adapters/playwright_element.py
from playwright.sync_api import Locator

class PlaywrightWebElement:
    """Adapter for Playwright Locator to WebElementProtocol."""

    def __init__(self, locator: Locator):
        self._locator = locator

    def click(self) -> None:
        self._locator.click()

    def send_keys(self, text: str) -> None:
        self._locator.fill(text)

    # ... implement other methods
```

**Acceptance Criteria:**
- Protocol defines contract
- Both frameworks implement protocol
- Tests can work with either implementation
- All tests pass

---

### 2.3 Create Page Object Protocol

**Problem:** No common interface for page objects. Tests are tightly coupled to concrete implementations.

**Code Smell:** Lack of Abstraction, Tight Coupling

**Refactor Steps:**
1. Define `PageObjectProtocol` interface
2. Create `LoginPageProtocol` extending base protocol
3. Ensure both Selenium and Playwright implementations satisfy protocols
4. Use protocols in test type hints

**Implementation:**
```python
# src/pages/protocols.py
from typing import Protocol

class PageObjectProtocol(Protocol):
    """Base protocol for all page objects."""

    def navigate_to(self, url: str) -> None:
        """Navigate to URL."""
        ...

    def get_current_url(self) -> str:
        """Get current page URL."""
        ...

    def is_page_loaded(self) -> bool:
        """Check if page is loaded."""
        ...

class LoginPageProtocol(PageObjectProtocol, Protocol):
    """Protocol for login page objects."""

    def enter_username(self, username: str) -> "LoginPageProtocol":
        """Enter username."""
        ...

    def enter_password(self, password: str) -> "LoginPageProtocol":
        """Enter password."""
        ...

    def click_login_button(self) -> None:
        """Click login button."""
        ...

    def login(self, username: str, password: str) -> None:
        """Perform complete login."""
        ...

    def get_error_message(self) -> str:
        """Get error message text."""
        ...

# In tests:
def test_login(login_page: LoginPageProtocol, config_service: ConfigService):
    """Test login - works with any LoginPage implementation."""
    login_page.login(config_service.username, config_service.password)
    assert "dashboard" in login_page.get_current_url()
```

**Benefits:**
- Tests are framework-agnostic
- Easy to add new automation tools
- Contract enforced at type-check time
- Explicit expectations

**Acceptance Criteria:**
- All page objects implement protocols
- Tests use protocol types
- Type checking passes (mypy/pyright)
- All tests pass

---

## Phase 3: Unify Selenium/Playwright with Adapter Pattern (Weeks 5-6)

**Goal:** Eliminate 90% duplication between Selenium and Playwright implementations.

### 3.1 Create Unified Browser Abstraction

**Problem:** Separate `driver` and `page` fixtures. Duplicate conftest.py files.

**Code Smell:** Code Duplication, Parallel Class Hierarchies

**Refactor Steps:**
1. Create `BrowserProtocol` interface
2. Create `SeleniumBrowserAdapter` and `PlaywrightBrowserAdapter`
3. Create `BrowserFactory` with Strategy pattern
4. Unify fixtures into single `browser` fixture
5. Page objects accept `BrowserProtocol` instead of driver/page

**Implementation:**
```python
# src/core/browser_protocol.py
from typing import Protocol
from src.core.locator import Locator
from src.core.protocols import WebElementProtocol

class BrowserProtocol(Protocol):
    """Unified browser interface for any automation framework."""

    def navigate(self, url: str) -> None:
        """Navigate to URL."""
        ...

    def find_element(self, locator: Locator) -> WebElementProtocol:
        """Find single element."""
        ...

    def find_elements(self, locator: Locator) -> list[WebElementProtocol]:
        """Find multiple elements."""
        ...

    def execute_script(self, script: str, *args) -> any:
        """Execute JavaScript."""
        ...

    def get_current_url(self) -> str:
        """Get current URL."""
        ...

    def quit(self) -> None:
        """Close browser."""
        ...

# src/adapters/selenium_browser.py
from selenium.webdriver.remote.webdriver import WebDriver

class SeleniumBrowserAdapter:
    """Adapter for Selenium WebDriver to BrowserProtocol."""

    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)

    def navigate(self, url: str) -> None:
        self._driver.get(url)

    def find_element(self, locator: Locator) -> WebElementProtocol:
        native_locator = locator.to_native()
        element = self._wait.until(
            EC.presence_of_element_located(native_locator)
        )
        return SeleniumWebElement(element)

    # ... implement other methods

# src/adapters/playwright_browser.py
from playwright.sync_api import Page

class PlaywrightBrowserAdapter:
    """Adapter for Playwright Page to BrowserProtocol."""

    def __init__(self, page: Page):
        self._page = page

    def navigate(self, url: str) -> None:
        self._page.goto(url)

    def find_element(self, locator: Locator) -> WebElementProtocol:
        native_selector = locator.to_native()
        pw_locator = self._page.locator(native_selector)
        return PlaywrightWebElement(pw_locator)

    # ... implement other methods

# src/factories/browser_factory.py
class BrowserFactory:
    """Factory for creating browser instances."""

    @staticmethod
    def create_browser(framework: str, **kwargs) -> BrowserProtocol:
        """
        Create browser instance based on framework.

        Args:
            framework: "selenium" or "playwright"
            **kwargs: Framework-specific options

        Returns:
            BrowserProtocol implementation
        """
        if framework == "selenium":
            driver = create_selenium_driver(**kwargs)
            return SeleniumBrowserAdapter(driver)
        elif framework == "playwright":
            page = create_playwright_page(**kwargs)
            return PlaywrightBrowserAdapter(page)
        else:
            raise ValueError(f"Unknown framework: {framework}")
```

**Unified Fixture:**
```python
# conftest.py (single file)
@pytest.fixture(scope="function")
def browser(request) -> BrowserProtocol:
    """
    Create browser based on --framework flag.
    Works with both Selenium and Playwright.
    """
    framework = request.config.getoption("--framework", default="selenium")
    browser_name = request.config.getoption("--browser", default="chrome")

    browser = BrowserFactory.create_browser(
        framework=framework,
        browser=browser_name
    )

    yield browser

    browser.quit()
```

**Acceptance Criteria:**
- Single conftest.py file
- Tests work with both frameworks via `--framework` flag
- No code duplication between frameworks
- All tests pass with both Selenium and Playwright

---

### 3.2 Create Unified Base Page

**Problem:** BasePage and BasePagePW are 90% duplicated.

**Code Smell:** Code Duplication, Parallel Class Hierarchies

**Refactor Steps:**
1. Create single `BasePage` class
2. Accept `BrowserProtocol` instead of driver/page
3. Remove BasePage and BasePagePW
4. Update all page objects to use unified BasePage

**Implementation:**
```python
# src/pages/base_page.py
from src.core.browser_protocol import BrowserProtocol
from src.core.locator import Locator
from src.helpers.element_highlighter import ElementHighlighter
from utils.logger import TestLogger

class BasePage:
    """
    Unified base page for all page objects.
    Works with any browser framework via BrowserProtocol.
    """

    def __init__(self, browser: BrowserProtocol, timeout: int = 10):
        self.browser = browser
        self.timeout = timeout
        self.highlighter = ElementHighlighter(browser)
        self.logger = TestLogger.get_logger(self.__class__.__name__)

    def navigate_to(self, url: str) -> None:
        """Navigate to URL."""
        self.logger.debug(f"Navigating to: {url}")
        self.browser.navigate(url)

    def find_element(self, locator: Locator) -> WebElementProtocol:
        """Find single element."""
        try:
            return self.browser.find_element(locator)
        except TimeoutException as e:
            self.logger.error(f"Element not found: {locator}")
            raise ElementNotFoundException(locator) from e

    def click(self, locator: Locator) -> None:
        """Click element."""
        element = self.find_element(locator)
        element.click()

    def send_keys(self, locator: Locator, text: str) -> None:
        """Type text into element."""
        element = self.find_element(locator)
        element.send_keys(text)

    def get_text(self, locator: Locator) -> str:
        """Get element text."""
        element = self.find_element(locator)
        return element.get_text()

    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.browser.get_current_url()

    # ... other common methods
```

**Unified Login Page:**
```python
# src/pages/login_page.py
from src.pages.base_page import BasePage
from src.pages.locators.login_locators import LoginLocators
from src.core.browser_protocol import BrowserProtocol

class LoginPage(BasePage):
    """
    Login page object - works with any framework.
    No more LoginPage vs LoginPagePW!
    """

    def __init__(self, browser: BrowserProtocol, timeout: int = 10):
        super().__init__(browser, timeout)
        self.locators = LoginLocators

    def enter_username(self, username: str) -> "LoginPage":
        self.send_keys(self.locators.USERNAME, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        self.send_keys(self.locators.PASSWORD, password)
        return self

    def click_login_button(self) -> None:
        self.click(self.locators.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    # ... other methods
```

**Benefits:**
- **70-90% reduction in code duplication**
- Single page object works with both frameworks
- Easy to add new frameworks (just implement adapters)
- Tests are truly framework-agnostic

**Acceptance Criteria:**
- Single BasePage replaces both versions
- Single LoginPage replaces both versions
- Tests run with `--framework=selenium` and `--framework=playwright`
- All tests pass
- No regression in functionality

---

### 3.3 Consolidate Locators

**Problem:** Separate locator files for Selenium and Playwright.

**Refactor Steps:**
1. Create single `src/pages/locators/` directory
2. Use Locator value objects (framework-agnostic)
3. Remove duplicate locator definitions

**Implementation:**
```python
# src/pages/locators/login_locators.py
from src.core.locator import Locator, LocatorStrategy

class LoginLocators:
    """
    Unified locators for login page.
    Work with any framework via Locator abstraction.
    """

    USERNAME = Locator(LocatorStrategy.NAME, "username", "Username input")
    PASSWORD = Locator(LocatorStrategy.NAME, "password", "Password input")
    LOGIN_BUTTON = Locator(LocatorStrategy.CSS, "button[type='submit']", "Login button")
    ERROR_MESSAGE = Locator(LocatorStrategy.CSS, ".oxd-alert-content-text", "Error message")
    FORGOT_PASSWORD = Locator(LocatorStrategy.CSS, ".orangehrm-login-forgot-header", "Forgot password link")
    LOGIN_LOGO = Locator(LocatorStrategy.CSS, ".orangehrm-login-branding img", "Login logo")
    LOGIN_TITLE = Locator(LocatorStrategy.CSS, ".orangehrm-login-title", "Login title")
```

**Acceptance Criteria:**
- Single locator file per page
- No framework-specific locators
- All tests pass

---

## Phase 4: Apply Advanced Patterns (Weeks 7-8)

**Goal:** Introduce patterns to solve remaining extensibility and maintainability issues.

### 4.1 Apply Strategy Pattern for Browser Configuration

**Problem:** If/elif chains for browser options in conftest.py.

**Code Smell:** Switch Statement Smell, Open/Closed Principle Violation

**Refactor Steps:**
1. Create `BrowserOptionsStrategy` interface
2. Create concrete strategies: `ChromeOptionsStrategy`, `FirefoxOptionsStrategy`, `EdgeOptionsStrategy`
3. Use strategy in BrowserFactory
4. Easy to add new browsers

**Implementation:**
```python
# src/strategies/browser_options_strategy.py
from abc import ABC, abstractmethod

class BrowserOptionsStrategy(ABC):
    """Strategy for configuring browser-specific options."""

    @abstractmethod
    def create_options(self, headless: bool = False) -> any:
        """Create browser-specific options."""
        pass

# src/strategies/chrome_options_strategy.py
from selenium.webdriver.chrome.options import Options as ChromeOptions

class ChromeOptionsStrategy(BrowserOptionsStrategy):
    """Chrome-specific options strategy."""

    def create_options(self, headless: bool = False) -> ChromeOptions:
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        return options

# Similar for Firefox, Edge, etc.

# src/factories/browser_factory.py
class BrowserFactory:
    """Factory with Strategy pattern for browser creation."""

    _strategies = {
        "chrome": ChromeOptionsStrategy(),
        "firefox": FirefoxOptionsStrategy(),
        "edge": EdgeOptionsStrategy(),
    }

    @classmethod
    def register_strategy(cls, browser: str, strategy: BrowserOptionsStrategy):
        """Register new browser strategy (Open for extension)."""
        cls._strategies[browser] = strategy

    @classmethod
    def create_browser(cls, framework: str, browser: str, **kwargs) -> BrowserProtocol:
        strategy = cls._strategies.get(browser)
        if not strategy:
            raise ValueError(f"Unknown browser: {browser}")

        options = strategy.create_options(kwargs.get("headless", False))
        # ... create and return browser
```

**Benefits:**
- Open/Closed Principle: open for extension, closed for modification
- Easy to add new browsers without touching factory
- Each browser strategy is independent

**Acceptance Criteria:**
- No if/elif chains
- Can add new browser by registering strategy
- All tests pass
- All browsers (Chrome, Firefox, Edge) work

---

### 4.2 Apply Builder Pattern for Complex Page Creation

**Problem:** Page objects with many optional parameters becoming unwieldy.

**Code Smell:** Long Parameter List, Telescoping Constructor

**Refactor Steps:**
1. Create `PageBuilder` for complex page creation
2. Use builder when page needs multiple optional configurations
3. Keep simple constructors for simple pages

**Implementation:**
```python
# src/builders/page_builder.py
from src.pages.base_page import BasePage
from src.core.browser_protocol import BrowserProtocol

class PageBuilder:
    """
    Builder for creating page objects with optional configurations.
    Use for complex pages; simple pages use direct construction.
    """

    def __init__(self, page_class: type[BasePage], browser: BrowserProtocol):
        self._page_class = page_class
        self._browser = browser
        self._timeout = 10
        self._config = None
        self._logger_level = "INFO"
        self._auto_navigate = False
        self._url = None

    def with_timeout(self, timeout: int) -> "PageBuilder":
        self._timeout = timeout
        return self

    def with_config(self, config: ConfigService) -> "PageBuilder":
        self._config = config
        return self

    def with_logger_level(self, level: str) -> "PageBuilder":
        self._logger_level = level
        return self

    def auto_navigate_to(self, url: str) -> "PageBuilder":
        self._auto_navigate = True
        self._url = url
        return self

    def build(self) -> BasePage:
        """Build the page object."""
        page = self._page_class(self._browser, self._timeout)

        if self._config:
            page.config = self._config

        if self._logger_level:
            page.logger.setLevel(self._logger_level)

        if self._auto_navigate and self._url:
            page.navigate_to(self._url)

        return page

# Usage in conftest:
@pytest.fixture
def login_page(browser, config_service):
    """Create login page with builder."""
    return (
        PageBuilder(LoginPage, browser)
        .with_config(config_service)
        .with_timeout(15)
        .auto_navigate_to(config_service.base_url)
        .build()
    )
```

**When to Use:**
- Pages with 4+ optional parameters
- Pages requiring complex setup
- **Don't use for simple pages** (YAGNI)

**Acceptance Criteria:**
- Builder used only for complex pages
- Simple pages use direct construction
- All tests pass
- Improved readability

---

### 4.3 Apply Template Method for Common Test Flows

**Problem:** Test structure is duplicated across many test methods.

**Code Smell:** Code Duplication, Boilerplate

**Refactor Steps:**
1. Create `LoginTestTemplate` abstract base class
2. Define template method with test flow
3. Subclasses override specific steps
4. Reduce duplication in test files

**Implementation:**
```python
# tests/templates/login_test_template.py
from abc import ABC, abstractmethod
import allure
from src.pages.protocols import LoginPageProtocol
from src.config.protocols import ConfigService

class LoginTestTemplate(ABC):
    """
    Template Method pattern for login tests.
    Defines the skeleton of login test algorithm.
    """

    def run_login_test(self, login_page: LoginPageProtocol, config: ConfigService):
        """Template method - defines test algorithm."""
        with allure.step("Prepare test data"):
            username, password = self.prepare_credentials(config)

        with allure.step("Perform login"):
            self.perform_login(login_page, username, password)

        with allure.step("Verify result"):
            self.verify_result(login_page)

        with allure.step("Cleanup"):
            self.cleanup(login_page)

    @abstractmethod
    def prepare_credentials(self, config: ConfigService) -> tuple[str, str]:
        """Prepare test credentials (hook for subclasses)."""
        pass

    def perform_login(self, login_page: LoginPageProtocol, username: str, password: str):
        """Default login action (can be overridden)."""
        login_page.login(username, password)

    @abstractmethod
    def verify_result(self, login_page: LoginPageProtocol):
        """Verify test result (hook for subclasses)."""
        pass

    def cleanup(self, login_page: LoginPageProtocol):
        """Cleanup after test (hook for subclasses)."""
        pass  # Default: no cleanup

# Concrete test classes:
class ValidLoginTest(LoginTestTemplate):
    """Test valid login."""

    def prepare_credentials(self, config):
        return config.username, config.password

    def verify_result(self, login_page):
        assert "dashboard" in login_page.get_current_url()

class InvalidLoginTest(LoginTestTemplate):
    """Test invalid login."""

    def prepare_credentials(self, config):
        return "invalid_user", "invalid_pass"

    def verify_result(self, login_page):
        assert login_page.is_error_message_displayed()

# Usage in tests:
def test_valid_login(login_page, config_service):
    ValidLoginTest().run_login_test(login_page, config_service)

def test_invalid_login(login_page, config_service):
    InvalidLoginTest().run_login_test(login_page, config_service)
```

**Benefits:**
- Reduces test boilerplate
- Ensures consistent test structure
- Easy to modify test flow
- Don't use if tests are too different (YAGNI)

**Acceptance Criteria:**
- Template reduces duplication by 50%+
- Only used for similar test flows
- All tests pass
- Improved readability

---

### 4.4 Apply Decorator Pattern for Retry and Logging

**Problem:** Need to add retry logic and detailed logging without modifying base page methods.

**Code Smell:** Cross-Cutting Concerns, Open/Closed Principle Violation

**Refactor Steps:**
1. Create decorators for retry, logging, screenshot on error
2. Apply decorators to page methods
3. No modification to base methods (Open/Closed)

**Implementation:**
```python
# src/decorators/retry_decorator.py
import functools
import time
from typing import Callable

def retry(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)):
    """
    Decorator to retry a function on failure.

    Args:
        max_attempts: Maximum retry attempts
        delay: Delay between retries in seconds
        exceptions: Tuple of exceptions to catch
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

# src/decorators/screenshot_decorator.py
def screenshot_on_error(screenshot_dir: str = "./screenshots"):
    """Decorator to take screenshot on method failure."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                # Take screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{func.__name__}_{timestamp}.png"
                self.browser.take_screenshot(f"{screenshot_dir}/{filename}")
                raise
        return wrapper
    return decorator

# Usage in page objects:
class LoginPage(BasePage):

    @retry(max_attempts=3, delay=1.0, exceptions=(ElementNotFoundException,))
    @screenshot_on_error()
    def click_login_button(self):
        """Click login button with retry and screenshot on error."""
        self.click(self.locators.LOGIN_BUTTON)
```

**Benefits:**
- Add behavior without modifying methods
- Composable decorators
- Reusable across pages
- Open/Closed Principle

**Acceptance Criteria:**
- Decorators work correctly
- Can stack multiple decorators
- All tests pass
- No modification to base methods

---

## Phase 5: Advanced Architectures (Optional - Weeks 9-10)

**Goal:** Introduce advanced patterns for large-scale frameworks. **Only if needed.**

### 5.1 Repository Pattern for Page Object Management

**Problem:** Tests create page objects directly. Hard to manage page lifecycles.

**When to Apply:** Large frameworks with 20+ page objects.

**Implementation:**
```python
# src/repositories/page_repository.py
class PageRepository:
    """
    Repository for managing page object instances.
    Implements Registry pattern.
    """

    def __init__(self, browser: BrowserProtocol):
        self._browser = browser
        self._pages: dict[type, BasePage] = {}

    def get_page(self, page_class: type[BasePage]) -> BasePage:
        """Get or create page instance."""
        if page_class not in self._pages:
            self._pages[page_class] = page_class(self._browser)
        return self._pages[page_class]

    def clear(self):
        """Clear all cached pages."""
        self._pages.clear()

# Usage in tests:
@pytest.fixture
def page_repo(browser):
    return PageRepository(browser)

def test_login_flow(page_repo):
    login_page = page_repo.get_page(LoginPage)
    login_page.login("admin", "pass")

    dashboard_page = page_repo.get_page(DashboardPage)
    assert dashboard_page.is_loaded()
```

**Acceptance Criteria:**
- Centralized page management
- Lazy page creation
- Easy to clear cache
- Only apply if framework has 20+ pages

---

### 5.2 Screenplay Pattern (Alternative to POM)

**Problem:** POM doesn't scale for complex business workflows with multiple actors.

**When to Apply:** Complex applications with multiple user roles and intricate flows.

**Note:** This is an alternative architecture, not a refactor of current POM. Consider only if POM becomes limiting.

**Implementation:**
```python
# src/screenplay/actor.py
class Actor:
    """An actor who interacts with the system."""

    def __init__(self, name: str, browser: BrowserProtocol):
        self.name = name
        self.browser = browser
        self.abilities = []

    def can(self, ability: "Ability") -> "Actor":
        """Give actor an ability."""
        self.abilities.append(ability)
        return self

    def attempts_to(self, *tasks: "Task") -> None:
        """Perform tasks."""
        for task in tasks:
            task.perform_as(self)

# src/screenplay/task.py
class Task(ABC):
    """A task an actor can perform."""

    @abstractmethod
    def perform_as(self, actor: Actor) -> None:
        pass

# src/screenplay/tasks/login.py
class Login(Task):
    """Task: Log into the system."""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    @staticmethod
    def with_credentials(username: str, password: str) -> "Login":
        return Login(username, password)

    def perform_as(self, actor: Actor):
        login_page = LoginPage(actor.browser)
        login_page.login(self.username, self.password)

# Usage in tests:
def test_user_can_login(browser):
    user = Actor("Test User", browser).can(BrowseTheWeb(browser))
    user.attempts_to(Login.with_credentials("admin", "pass"))
    user.should_see(DashboardPage.loaded())
```

**When to Apply:**
- Multiple user roles (Admin, User, Guest)
- Complex multi-step workflows
- Need better readability for business stakeholders
- **Don't apply** for simple applications (YAGNI)

---

## Phase 6: Testing & Validation (Ongoing)

### 6.1 Characterization Tests

**Before any refactor:**
1. Write characterization tests for existing behavior
2. Lock down current functionality
3. Use tests as safety net during refactor
4. Never refactor without tests

**Example:**
```python
# tests/characterization/test_base_page_behavior.py
def test_click_finds_and_clicks_element(mock_browser):
    """Lock down click behavior before refactoring."""
    page = BasePage(mock_browser)
    locator = Locator(LocatorStrategy.ID, "button")

    page.click(locator)

    mock_browser.find_element.assert_called_once_with(locator)
    # ... verify click was called
```

### 6.2 Mutation Testing

**After refactoring:**
1. Run mutation tests to ensure refactored code is properly tested
2. Use `mutmut` or similar tool
3. Aim for >80% mutation score

```bash
pip install mutmut
mutmut run --paths-to-mutate=src/
mutmut results
```

### 6.3 Complexity Metrics

**Track improvement:**
```bash
# Cyclomatic complexity
radon cc src/ --min C

# Maintainability Index
radon mi src/ --min B

# Run before and after each phase
# Aim to reduce complexity by 20-30%
```

---

## Migration Strategy

### Incremental Adoption:

1. **Phase 1-2:** Can be done independently without breaking existing code
2. **Phase 3:** Requires tests to use new unified architecture
3. **Phase 4:** Optional patterns applied as needed

### Parallel Operation:

During Phase 3, maintain both old and new architectures temporarily:

```
src/
├── pages_selenium/          # Old (deprecated)
├── pages_playwright/        # Old (deprecated)
└── pages/                   # New (unified)
```

Migrate tests one at a time. Remove old code when all tests migrated.

### Feature Flags:

```python
# Allow gradual rollout
USE_UNIFIED_ARCHITECTURE = os.getenv("USE_UNIFIED_ARCH", "false") == "true"

if USE_UNIFIED_ARCHITECTURE:
    from src.pages.login_page import LoginPage
else:
    from src.pages_selenium.login_page import LoginPage
```

---

## Success Metrics

### Quantitative:
- **Code duplication:** Reduce from ~90% to <15%
- **Cyclomatic complexity:** Reduce average from ~10 to <5
- **Test execution time:** No regression (maintain or improve)
- **Lines of code:** Reduce by 40-50%
- **Number of classes:** Reduce by 30% (eliminate duplicates)

### Qualitative:
- **Maintainability:** Single change updates all frameworks
- **Extensibility:** Add new framework in <1 day
- **Testability:** 100% unit test coverage of core components
- **Readability:** New developer understands architecture in <2 hours
- **Stability:** Zero regression bugs during refactor

---

## Risk Mitigation

### Risks:
1. **Regression bugs:** Mitigated by characterization tests
2. **Over-engineering:** Mitigated by YAGNI and incremental approach
3. **Performance degradation:** Mitigated by benchmarks before/after
4. **Team adoption:** Mitigated by good documentation and training
5. **Incomplete refactor:** Mitigated by clear phase boundaries

### Rollback Plan:
- Each phase is reversible
- Git tags at phase boundaries
- Feature flags for gradual adoption
- Old code kept until migration complete

---

## Conclusion

This refactor plan addresses critical code smells and anti-patterns while maintaining functional stability. The incremental approach ensures:

1. **Safety:** Tests lock down behavior at each step
2. **Pragmatism:** Patterns introduced only when justified
3. **Extensibility:** Easy to add new tools/browsers/frameworks
4. **Maintainability:** DRY principle reduces duplication by 70%+
5. **Professionalism:** SOLID principles improve design quality

**Estimated Timeline:** 8-10 weeks for Phases 1-4
**Recommended Team Size:** 2-3 engineers
**Required Skills:** Python, Design Patterns, Selenium, Playwright, Pytest

**Next Steps:**
1. Review and approve plan
2. Create Phase 1 tickets in Jira/GitHub
3. Set up characterization tests
4. Begin Phase 1.1: Config refactor
