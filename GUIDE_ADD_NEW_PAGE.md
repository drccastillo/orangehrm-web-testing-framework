# Guía: Agregar una Nueva Página al Framework Unificado

## 🎯 Visión General

Con la arquitectura unificada, **NO necesitas crear tests separados para Selenium y Playwright**.
Los mismos tests funcionan con AMBOS frameworks.

---

## 📝 Ejemplo: Agregar Dashboard Page

Vamos a crear la página de Dashboard como ejemplo completo.

### Paso 1: Crear Locators Unificados

**Archivo:** `src/pages/locators/dashboard_locators.py`

```python
"""
Unified locators for the Dashboard Page.

These locators work with ANY automation framework (Selenium, Playwright, etc.)
through the Locator value object abstraction.
"""

from src.core.locator import LocatorStrategy
from src.core.selenium_locator import SeleniumLocator


class DashboardLocators:
    """
    Unified locator value objects for the Dashboard Page.

    These locators use SeleniumLocator which implements the Locator protocol.
    The browser adapters convert them to framework-specific format via to_native().
    """

    # Header elements
    WELCOME_MESSAGE = SeleniumLocator(
        LocatorStrategy.CSS,
        ".oxd-topbar-header-breadcrumb h6",
        "Welcome message in header"
    )

    USER_DROPDOWN = SeleniumLocator(
        LocatorStrategy.CSS,
        ".oxd-userdropdown",
        "User dropdown menu"
    )

    LOGOUT_LINK = SeleniumLocator(
        LocatorStrategy.XPATH,
        "//a[contains(text(), 'Logout')]",
        "Logout link in dropdown"
    )

    # Dashboard widgets
    TIME_AT_WORK_WIDGET = SeleniumLocator(
        LocatorStrategy.CSS,
        ".orangehrm-attendance-card",
        "Time at Work widget"
    )

    QUICK_LAUNCH_WIDGET = SeleniumLocator(
        LocatorStrategy.CSS,
        ".orangehrm-dashboard-widget",
        "Quick Launch widget"
    )

    # Navigation menu
    MENU_ITEM_ADMIN = SeleniumLocator(
        LocatorStrategy.XPATH,
        "//span[text()='Admin']",
        "Admin menu item"
    )

    MENU_ITEM_PIM = SeleniumLocator(
        LocatorStrategy.XPATH,
        "//span[text()='PIM']",
        "PIM menu item"
    )
```

**💡 Nota importante:** Usa `SeleniumLocator` para todos los locators. El framework los convierte automáticamente:
- **Selenium:** `(By.CSS, ".oxd-topbar-header-breadcrumb h6")`
- **Playwright:** `".oxd-topbar-header-breadcrumb h6"`

---

### Paso 2: Crear el Protocol (Opcional pero Recomendado)

**Archivo:** `src/pages/protocols.py` (agregar al archivo existente)

```python
@runtime_checkable
class DashboardPageProtocol(PageObjectProtocol, Protocol):
    """
    Protocol for dashboard page objects.

    Extends PageObjectProtocol with dashboard-specific operations.
    Both Selenium and Playwright implementations must satisfy this interface.
    """

    def get_welcome_message(self) -> str:
        """
        Get the welcome message displayed in the header.

        Returns:
            Welcome message text

        Example:
            >>> msg = dashboard.get_welcome_message()
            >>> assert "Dashboard" in msg
        """
        ...

    def click_user_dropdown(self) -> "DashboardPageProtocol":
        """
        Click the user dropdown menu.

        Returns:
            Self for method chaining
        """
        ...

    def logout(self) -> None:
        """
        Perform logout action.

        Example:
            >>> dashboard.logout()
            >>> # Should redirect to login page
        """
        ...

    def is_time_at_work_widget_visible(self) -> bool:
        """
        Check if Time at Work widget is visible.

        Returns:
            True if visible, False otherwise
        """
        ...

    def navigate_to_admin(self) -> None:
        """Navigate to Admin page."""
        ...

    def navigate_to_pim(self) -> None:
        """Navigate to PIM page."""
        ...
```

---

### Paso 3: Crear el Unified Page Object

**Archivo:** `src/pages/dashboard_page.py`

```python
"""
Unified Dashboard Page Object Model for OrangeHRM application.

This DashboardPage works with ANY automation framework (Selenium, Playwright, etc.)
through the BrowserProtocol interface.
"""

from src.core.browser_protocol import BrowserProtocol
from src.pages.base_page import BasePage
from src.pages.locators.dashboard_locators import DashboardLocators


class DashboardPage(BasePage):
    """
    Unified Page Object Model for the OrangeHRM Dashboard Page.

    This single implementation works with both Selenium and Playwright.

    Example (Selenium):
        >>> from src.adapters.selenium_browser import SeleniumBrowserAdapter
        >>> selenium_browser = SeleniumBrowserAdapter(driver, timeout=10)
        >>> dashboard = DashboardPage(selenium_browser)
        >>> dashboard.logout()

    Example (Playwright):
        >>> from src.adapters.playwright_browser import PlaywrightBrowserAdapter
        >>> playwright_browser = PlaywrightBrowserAdapter(page, timeout=10)
        >>> dashboard = DashboardPage(playwright_browser)
        >>> dashboard.logout()
    """

    def __init__(self, browser: BrowserProtocol, timeout: int = 10):
        """
        Initialize the Dashboard Page.

        Args:
            browser: Browser adapter implementing BrowserProtocol
            timeout: Default timeout for operations in seconds
        """
        super().__init__(browser, timeout)
        self.locators = DashboardLocators

    def get_welcome_message(self) -> str:
        """
        Get the welcome message displayed in the header.

        Returns:
            Welcome message text
        """
        return self.get_text(self.locators.WELCOME_MESSAGE)

    def click_user_dropdown(self) -> "DashboardPage":
        """
        Click the user dropdown menu.

        Returns:
            Self for method chaining
        """
        self.click(self.locators.USER_DROPDOWN)
        return self

    def logout(self) -> None:
        """
        Perform logout action.

        Clicks user dropdown and then logout link.
        """
        self.logger.info("Logging out from dashboard")
        self.click_user_dropdown()
        self.click(self.locators.LOGOUT_LINK)

    def is_time_at_work_widget_visible(self) -> bool:
        """
        Check if Time at Work widget is visible.

        Returns:
            True if visible, False otherwise
        """
        return self.is_element_visible(self.locators.TIME_AT_WORK_WIDGET)

    def is_quick_launch_widget_visible(self) -> bool:
        """
        Check if Quick Launch widget is visible.

        Returns:
            True if visible, False otherwise
        """
        return self.is_element_visible(self.locators.QUICK_LAUNCH_WIDGET)

    def navigate_to_admin(self) -> None:
        """Navigate to Admin page."""
        self.logger.info("Navigating to Admin")
        self.click(self.locators.MENU_ITEM_ADMIN)

    def navigate_to_pim(self) -> None:
        """Navigate to PIM page."""
        self.logger.info("Navigating to PIM")
        self.click(self.locators.MENU_ITEM_PIM)

    def is_page_loaded(self) -> bool:
        """
        Verify if the dashboard page is fully loaded.

        Checks that critical elements are visible:
            - Welcome message
            - User dropdown

        Returns:
            True if dashboard is loaded, False otherwise
        """
        return (
            self.is_element_visible(self.locators.WELCOME_MESSAGE)
            and self.is_element_visible(self.locators.USER_DROPDOWN)
        )
```

---

### Paso 4: Crear el Fixture en conftest.py

**Archivo:** `tests/conftest.py` (agregar al archivo existente)

```python
from src.pages.dashboard_page import DashboardPage

@pytest.fixture(scope="function")
def dashboard_page(browser, config_service, login_page):
    """
    Create unified DashboardPage instance after login.

    This DashboardPage works with ANY framework through BrowserProtocol.

    Args:
        browser: Browser adapter (from browser fixture)
        config_service: Configuration service
        login_page: Login page fixture

    Yields:
        DashboardPage: Unified dashboard page instance

    Example:
        def test_logout(dashboard_page):
            dashboard_page.logout()
            # Should redirect to login page
    """
    # First login to access dashboard
    login_page.login(config_service.username, config_service.password)

    # Create dashboard page
    page = DashboardPage(browser, timeout=config_service.default_timeout)

    # Wait for page to load
    assert page.is_page_loaded(), "Dashboard page should be loaded after login"

    yield page
```

---

### Paso 5: Crear Tests Unificados (¡UN SOLO ARCHIVO!)

**Archivo:** `tests/test_dashboard_unified.py`

```python
"""
Unified dashboard tests that work with ANY automation framework.

These tests use the unified page objects and work with both Selenium and Playwright
through the BrowserProtocol interface.

Run with Selenium (default):
    pytest tests/test_dashboard_unified.py --framework=selenium

Run with Playwright:
    pytest tests/test_dashboard_unified.py --framework=playwright

Run with specific browser:
    pytest tests/test_dashboard_unified.py --browser=firefox
    pytest tests/test_dashboard_unified.py --framework=playwright --browser=chromium
"""

import pytest

from src.pages.protocols import DashboardPageProtocol


@pytest.mark.smoke
def test_dashboard_page_loads(dashboard_page: DashboardPageProtocol):
    """
    Test that dashboard page loads successfully.

    This test works with ANY framework (Selenium, Playwright, etc.)
    through the DashboardPageProtocol interface.
    """
    # Verify dashboard is loaded
    assert dashboard_page.is_page_loaded(), "Dashboard should be fully loaded"


@pytest.mark.smoke
def test_welcome_message_displayed(dashboard_page: DashboardPageProtocol):
    """Test that welcome message is displayed on dashboard."""
    welcome_msg = dashboard_page.get_welcome_message()
    assert welcome_msg, "Welcome message should be displayed"
    assert len(welcome_msg) > 0, "Welcome message should not be empty"


@pytest.mark.smoke
def test_widgets_visible(dashboard_page: DashboardPageProtocol):
    """Test that dashboard widgets are visible."""
    # This might fail if widgets don't exist - adjust based on your OrangeHRM version
    assert dashboard_page.is_time_at_work_widget_visible() or \
           dashboard_page.is_quick_launch_widget_visible(), \
           "At least one dashboard widget should be visible"


@pytest.mark.regression
def test_logout_functionality(dashboard_page: DashboardPageProtocol):
    """
    Test logout functionality from dashboard.

    Args:
        dashboard_page: Dashboard page instance (framework-agnostic)
    """
    # Perform logout
    dashboard_page.logout()

    # Verify redirected to login page
    current_url = dashboard_page.get_current_url()
    assert "auth/login" in current_url, f"Should redirect to login page, got: {current_url}"


@pytest.mark.regression
def test_navigate_to_admin(dashboard_page: DashboardPageProtocol):
    """Test navigation to Admin page."""
    dashboard_page.navigate_to_admin()

    # Wait a bit for navigation
    import time
    time.sleep(1)

    # Verify URL changed
    current_url = dashboard_page.get_current_url()
    assert "admin" in current_url.lower(), f"Should navigate to admin page, got: {current_url}"


@pytest.mark.regression
def test_navigate_to_pim(dashboard_page: DashboardPageProtocol):
    """Test navigation to PIM page."""
    dashboard_page.navigate_to_pim()

    # Wait a bit for navigation
    import time
    time.sleep(1)

    # Verify URL changed
    current_url = dashboard_page.get_current_url()
    assert "pim" in current_url.lower(), f"Should navigate to PIM page, got: {current_url}"
```

---

### Paso 6: Crear Unit Tests (Opcional)

**Archivo:** `unittests/test_dashboard_protocols.py`

```python
"""
Unit tests for Dashboard Page protocols with unified architecture.
"""

import unittest
from unittest.mock import Mock

from src.pages.dashboard_page import DashboardPage
from src.pages.protocols import DashboardPageProtocol, PageObjectProtocol


class TestDashboardProtocolCompliance(unittest.TestCase):
    """Test that Dashboard page implements DashboardPageProtocol."""

    def test_dashboard_page_implements_protocol(self):
        """Test that DashboardPage implements DashboardPageProtocol."""
        mock_browser = Mock()
        page = DashboardPage(mock_browser)
        self.assertIsInstance(page, DashboardPageProtocol)

    def test_dashboard_page_implements_page_object_protocol(self):
        """Test that DashboardPage implements PageObjectProtocol."""
        mock_browser = Mock()
        page = DashboardPage(mock_browser)
        self.assertIsInstance(page, PageObjectProtocol)

    def test_dashboard_page_has_all_protocol_methods(self):
        """Test that DashboardPage has all protocol methods."""
        protocol_methods = [
            # PageObjectProtocol methods
            "navigate_to",
            "get_current_url",
            "is_page_loaded",
            # DashboardPageProtocol methods
            "get_welcome_message",
            "click_user_dropdown",
            "logout",
            "is_time_at_work_widget_visible",
            "navigate_to_admin",
            "navigate_to_pim",
        ]

        mock_browser = Mock()
        page = DashboardPage(mock_browser)

        for method_name in protocol_methods:
            with self.subTest(method=method_name):
                self.assertTrue(
                    hasattr(page, method_name),
                    f"DashboardPage missing method: {method_name}",
                )
                self.assertTrue(
                    callable(getattr(page, method_name)),
                    f"DashboardPage.{method_name} is not callable",
                )


if __name__ == "__main__":
    unittest.main()
```

---

## 🚀 Ejecutar los Tests

```bash
# Unit tests primero (no requieren browser)
uv run pytest unittests/test_dashboard_protocols.py -v

# Con Selenium
URL="http://orangehrm_app/web/index.php" \
uv run pytest tests/test_dashboard_unified.py --framework=selenium -v -p no:playwright

# Con Playwright
uv run pytest tests/test_dashboard_unified.py --framework=playwright -v -p no:playwright

# Ambos frameworks
URL="http://orangehrm_app/web/index.php" \
uv run pytest tests/test_dashboard_unified.py --framework=selenium -v -p no:playwright && \
uv run pytest tests/test_dashboard_unified.py --framework=playwright -v -p no:playwright
```

---

## ✅ Checklist Completo

- [ ] **Paso 1:** Crear `src/pages/locators/dashboard_locators.py`
- [ ] **Paso 2:** Agregar `DashboardPageProtocol` en `src/pages/protocols.py`
- [ ] **Paso 3:** Crear `src/pages/dashboard_page.py`
- [ ] **Paso 4:** Agregar fixture `dashboard_page` en `tests/conftest.py`
- [ ] **Paso 5:** Crear `tests/test_dashboard_unified.py`
- [ ] **Paso 6:** (Opcional) Crear `unittests/test_dashboard_protocols.py`
- [ ] **Paso 7:** Ejecutar unit tests
- [ ] **Paso 8:** Ejecutar tests con Selenium
- [ ] **Paso 9:** Ejecutar tests con Playwright
- [ ] **Paso 10:** Commit cambios

---

## 🎯 Ventajas de la Arquitectura Unificada

### ❌ Arquitectura Anterior (Duplicada)
```
tests_selenium/test_dashboard.py     ← 100 líneas
tests_playwright/test_dashboard_pw.py ← 100 líneas
pages_selenium/dashboard_page.py     ← 150 líneas
pages_playwright/dashboard_page_pw.py ← 150 líneas
-------------------------------------------
TOTAL: 500 líneas de código duplicado
```

### ✅ Arquitectura Nueva (Unificada)
```
tests/test_dashboard_unified.py    ← 100 líneas (funciona con AMBOS)
src/pages/dashboard_page.py        ← 150 líneas (funciona con AMBOS)
src/pages/locators/dashboard_locators.py ← 50 líneas
src/pages/protocols.py             ← +30 líneas
-------------------------------------------
TOTAL: 330 líneas (34% menos código)
```

**Beneficios:**
- ✅ 34% menos código
- ✅ Un solo archivo de tests
- ✅ Un solo page object
- ✅ Tests funcionan con Selenium Y Playwright
- ✅ Fácil de mantener
- ✅ Type-safe con protocolos
- ✅ Cumple con SOLID

---

## 🔑 Puntos Clave

1. **NO crees archivos separados para Playwright** - los mismos tests funcionan con ambos
2. **Usa `SeleniumLocator` para TODOS los locators** - se convierten automáticamente
3. **Inyecta `BrowserProtocol`** en el constructor del page object
4. **Usa protocols** para type safety y contratos claros
5. **Hereda de `BasePage`** para funcionalidad común
6. **Crea fixtures** en `conftest.py` para setup/teardown
7. **Ejecuta con `--framework=selenium` o `--framework=playwright`**

---

## 📚 Referencias

- Ver `src/pages/login_page.py` como ejemplo completo
- Ver `tests/test_login_unified.py` para patrones de testing
- Ver `src/pages/protocols.py` para definición de protocolos
- Ver `REFACTOR_SUMMARY.md` para arquitectura completa
