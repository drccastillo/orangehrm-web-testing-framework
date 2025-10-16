# Guía: Agregar una Nueva Página al Framework

## 🎯 Visión General

Este framework usa **Playwright nativo** con locators funcionales siguiendo las mejores prácticas recomendadas.

**No necesitas:**
- ❌ Clases adaptadoras (eliminadas)
- ❌ PlaywrightLocator wrapper (eliminado)
- ❌ Protocols específicos por página (eliminados)

**Sí necesitas:**
- ✅ Locators funcionales (`get_by_role`, `get_by_label`, `get_by_placeholder`)
- ✅ Heredar de `BasePage`
- ✅ Usar Playwright Page directamente

---

## 📝 Ejemplo: Agregar Dashboard Page

Vamos a crear la página de Dashboard como ejemplo completo.

### Paso 1: Crear Locators Funcionales

**Archivo:** `src/pages/locators/dashboard_locators.py`

```python
"""
Playwright functional locators for the Dashboard Page.

Following Playwright best practices:
- get_by_role() for buttons, links, headings
- get_by_text() for navigation items
- CSS selectors only when necessary

Reference: https://playwright.dev/python/docs/locators
"""

# ruff: noqa: N802
# Locator functions use UPPERCASE naming convention for consistency


class DashboardLocators:
    """
    Playwright functional locators for the Dashboard Page.

    These use Playwright's recommended locator methods for better resilience
    and maintainability.
    """

    # Header elements
    @staticmethod
    def WELCOME_MESSAGE(page):
        """Welcome message in header (heading role)."""
        return page.get_by_role("heading", name="Dashboard")

    @staticmethod
    def USER_DROPDOWN(page):
        """User dropdown menu (CSS fallback for complex widget)."""
        return page.locator(".oxd-userdropdown")

    # Logout functionality
    @staticmethod
    def LOGOUT_LINK(page):
        """Logout link (text-based)."""
        return page.get_by_text("Logout")

    # Dashboard widgets
    @staticmethod
    def TIME_AT_WORK_WIDGET(page):
        """Time at Work widget (heading role)."""
        return page.get_by_role("heading", name="Time at Work")

    @staticmethod
    def QUICK_LAUNCH_BUTTON(page):
        """Quick Launch button (role-based)."""
        return page.get_by_role("button", name="Quick Launch")

    # Search
    @staticmethod
    def SEARCH_INPUT(page):
        """Global search input (placeholder-based)."""
        return page.get_by_placeholder("Search")
```

### Paso 2: Crear Page Object

**Archivo:** `src/pages/dashboard_page.py`

```python
"""
Dashboard Page Object Model for OrangeHRM application.

This DashboardPage uses Playwright Page directly, eliminating adapter overhead.
"""

from playwright.sync_api import Page

from src.pages.base_page import BasePage
from src.pages.locators.dashboard_locators import DashboardLocators


class DashboardPage(BasePage):
    """
    Page Object Model for the OrangeHRM Dashboard Page using Playwright.

    Example:
        >>> from playwright.sync_api import sync_playwright
        >>> with sync_playwright() as p:
        ...     browser = p.chromium.launch()
        ...     page = browser.new_page()
        ...     dashboard = DashboardPage(page, timeout=10)
        ...     message = dashboard.get_welcome_message()
    """

    def __init__(self, page: Page, timeout: int = 10):
        """
        Initialize the Dashboard Page.

        Args:
            page: Playwright Page instance
            timeout: Default timeout for operations in seconds
        """
        super().__init__(page, timeout)
        self.locators = DashboardLocators

    def get_welcome_message(self) -> str:
        """
        Get the welcome message displayed in the header.

        Returns:
            Welcome message text

        Example:
            >>> message = dashboard.get_welcome_message()
            >>> assert "Dashboard" in message
        """
        return self.get_text(self.locators.WELCOME_MESSAGE(self.page))

    def click_user_dropdown(self) -> "DashboardPage":
        """
        Click the user dropdown menu.

        Returns:
            Self for method chaining

        Example:
            >>> dashboard.click_user_dropdown().logout()
        """
        self.click(self.locators.USER_DROPDOWN(self.page))
        return self

    def logout(self) -> None:
        """
        Logout from the application.

        Clicks user dropdown and then logout link.

        Example:
            >>> dashboard.logout()
            >>> # User is now logged out
        """
        self.logger.info("Logging out")
        self.click_user_dropdown()
        self.click(self.locators.LOGOUT_LINK(self.page))

    def is_page_loaded(self) -> bool:
        """
        Verify if the dashboard page is fully loaded.

        Returns:
            True if dashboard is loaded, False otherwise

        Example:
            >>> assert dashboard.is_page_loaded()
        """
        return self.is_element_visible(self.locators.WELCOME_MESSAGE(self.page))

    def search(self, query: str) -> "DashboardPage":
        """
        Perform a search using the global search bar.

        Args:
            query: Search query text

        Returns:
            Self for method chaining

        Example:
            >>> dashboard.search("Leave")
        """
        self.send_keys(self.locators.SEARCH_INPUT(self.page), query)
        return self
```

### Paso 3: Crear Fixture en conftest.py

**Archivo:** `tests/conftest.py`

```python
@pytest.fixture(scope="function")
def dashboard_page(browser: Page, login_page: LoginPage, config_service: ConfigService) -> DashboardPage:
    """
    Create DashboardPage fixture (requires login).

    Args:
        browser: Playwright Page fixture
        login_page: LoginPage fixture
        config_service: ConfigService fixture

    Yields:
        DashboardPage: Initialized dashboard page after login

    Example:
        def test_dashboard(dashboard_page):
            assert dashboard_page.is_page_loaded()
    """
    # Login first (dashboard requires authentication)
    login_page.login(config_service.username, config_service.password)

    # Create and return dashboard page
    dashboard = DashboardPage(browser, timeout=config_service.default_timeout)

    # Verify we're on dashboard
    assert dashboard.is_page_loaded(), "Dashboard page should be loaded after login"

    yield dashboard
```

### Paso 4: Crear Tests

**Archivo:** `tests/test_dashboard_unified.py`

```python
"""
Unified tests for Dashboard Page.

These tests work with Playwright using native Page objects.
"""

import pytest

from src.pages.dashboard_page import DashboardPage


@pytest.mark.smoke
def test_dashboard_loads(dashboard_page: DashboardPage):
    """Test that dashboard page loads successfully after login."""
    assert dashboard_page.is_page_loaded(), "Dashboard should be loaded"


@pytest.mark.smoke
def test_welcome_message_displayed(dashboard_page: DashboardPage):
    """Test that welcome message is displayed on dashboard."""
    message = dashboard_page.get_welcome_message()
    assert "Dashboard" in message, f"Expected 'Dashboard' in message, got: {message}"


@pytest.mark.regression
def test_logout_functionality(dashboard_page: DashboardPage):
    """Test that user can logout from dashboard."""
    dashboard_page.logout()

    # Verify redirected to login page
    current_url = dashboard_page.get_current_url()
    assert "login" in current_url, f"Should redirect to login, got: {current_url}"


@pytest.mark.regression
def test_search_functionality(dashboard_page: DashboardPage):
    """Test that search bar works on dashboard."""
    dashboard_page.search("Leave")

    # Verify search was performed (implementation depends on app behavior)
    # Add assertions based on expected behavior


@pytest.mark.regression
def test_user_dropdown_visible(dashboard_page: DashboardPage):
    """Test that user dropdown is visible on dashboard."""
    assert dashboard_page.is_element_visible(
        dashboard_page.locators.USER_DROPDOWN(dashboard_page.page)
    ), "User dropdown should be visible"
```

---

## 🔍 Playwright Locator Best Practices

### Prioridad de Locators

Sigue este orden (de más resiliente a menos):

1. **`get_by_role()`** - Basado en accesibilidad (MÁS RECOMENDADO)
   ```python
   page.get_by_role("button", name="Submit")
   page.get_by_role("heading", name="Dashboard")
   page.get_by_role("link", name="Logout")
   ```

2. **`get_by_label()`** - Para campos de formulario
   ```python
   page.get_by_label("Username")
   page.get_by_label("From Date")
   ```

3. **`get_by_placeholder()`** - Para inputs con placeholder
   ```python
   page.get_by_placeholder("Enter your email")
   page.get_by_placeholder("Search...")
   ```

4. **`get_by_text()`** - Para contenido visible
   ```python
   page.get_by_text("Logout")
   page.get_by_text("Leave", exact=True)
   ```

5. **CSS/XPath** - SOLO como último recurso
   ```python
   page.locator(".oxd-table")  # Tablas complejas
   page.locator(".oxd-chip")   # Widgets custom
   ```

### Ejemplos de Locators Funcionales vs CSS

| Elemento | ❌ CSS (Frágil) | ✅ Functional (Resiliente) |
|----------|----------------|---------------------------|
| Botón | `"button.submit"` | `get_by_role("button", name="Submit")` |
| Input | `"input[name='user']"` | `get_by_label("Username")` |
| Link | `"a.logout"` | `get_by_role("link", name="Logout")` |
| Heading | `"h1.title"` | `get_by_role("heading", name="Dashboard")` |

### Evitar Strict Mode Violations

Si encuentras: `Error: strict mode violation: resolved to 2 elements`

**Solución:** Ser más específico con roles y nombres:

```python
# ❌ Ambiguo - puede matchear múltiples elementos
page.get_by_text("Leave")

# ✅ Específico - usa role para diferenciar
page.get_by_role("link", name="Leave", exact=True)  # Link en sidebar
page.get_by_role("heading", name="Leave", exact=True)  # Heading en header
```

---

## 🎨 Patrón Method Chaining

Permite encadenar métodos para mejor legibilidad:

```python
def click_user_dropdown(self) -> "DashboardPage":
    """Return self for chaining."""
    self.click(self.locators.USER_DROPDOWN(self.page))
    return self  # ← Retorna self

# Uso:
dashboard.click_user_dropdown().logout()
```

---

## ✅ Checklist al Agregar Nueva Página

- [ ] Crear `src/pages/locators/nombre_page_locators.py` con locators funcionales
- [ ] Usar `get_by_role()`, `get_by_label()`, `get_by_placeholder()` cuando sea posible
- [ ] Usar CSS solo como último recurso
- [ ] Agregar `# ruff: noqa: N802` si los locators son funciones en UPPERCASE
- [ ] Crear `src/pages/nombre_page.py` heredando de `BasePage`
- [ ] Todos los métodos de locator llaman a `self.locators.X(self.page)`
- [ ] Implementar `is_page_loaded()` method
- [ ] Agregar docstrings con ejemplos
- [ ] Crear fixture en `tests/conftest.py`
- [ ] Crear `tests/test_nombre_page_unified.py` con tests
- [ ] Agregar markers: `@pytest.mark.smoke`, `@pytest.mark.regression`
- [ ] Correr tests: `uv run pytest tests/test_nombre_page_unified.py -v`

---

## 🚀 Correr Tests

```bash
# Run specific page tests
uv run pytest tests/test_dashboard_unified.py -v

# Run with specific browser
uv run pytest tests/test_dashboard_unified.py --browser chromium -v

# Run in headed mode (see browser)
uv run pytest tests/test_dashboard_unified.py --headed

# Run smoke tests only
uv run pytest tests/test_dashboard_unified.py -m smoke

# Run with HTML report
uv run pytest tests/test_dashboard_unified.py --html=reports/dashboard_report.html

# Run with Allure report
uv run pytest tests/test_dashboard_unified.py --alluredir=reports/allure-results
allure serve reports/allure-results
```

---

## 📚 Referencias

- [Playwright Locators Documentation](https://playwright.dev/python/docs/locators)
- [Playwright Best Practices](https://playwright.dev/python/docs/best-practices)
- [Playwright API Reference](https://playwright.dev/python/docs/api/class-page)

---

## 💡 Tips

1. **Usa Playwright Inspector para debugging:**
   ```bash
   PWDEBUG=1 uv run pytest tests/test_dashboard_unified.py
   ```

2. **Captura screenshots para análisis:**
   ```python
   dashboard_page.take_screenshot("reports/screenshots/dashboard.png")
   ```

3. **Log importante info:**
   ```python
   self.logger.info(f"Dashboard loaded with message: {message}")
   ```

4. **Test locators en Playwright CLI:**
   ```bash
   uv run playwright codegen http://localhost:8080/web/index.php
   ```

---

**¿Preguntas?** Consulta `CLAUDE.md` para más detalles sobre la arquitectura del framework.
