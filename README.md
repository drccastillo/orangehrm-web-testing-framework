# OrangeHRM Web Testing Automation Framework

Web test automation framework for OrangeHRM using Python, Pytest, Selenium, and Docker.

## 🏗️ Architecture and Design Patterns

### Implemented Patterns:
- **Page Object Model (POM)**: Encapsulation of elements and actions for each page
- **Base Page Pattern**: Base class with reusable methods for all pages
- **Factory Pattern**: Dynamic browser configuration
- **Singleton Pattern**: Centralized configuration management
- **Method Chaining**: Fluent interface for page actions

### Project Structure (Unified Architecture):
```
web-testing-framework/
├── src/
│   ├── core/                       # Core abstractions
│   │   ├── browser_protocol.py    # Unified browser interface
│   │   ├── element_protocol.py    # Unified element interface
│   │   └── locator.py              # Locator value objects
│   ├── adapters/                   # Framework adapters
│   │   ├── selenium_browser.py    # Selenium adapter
│   │   ├── playwright_browser.py  # Playwright adapter
│   │   ├── selenium_element.py    # Selenium element adapter
│   │   └── playwright_element.py  # Playwright element adapter
│   ├── factories/
│   │   └── browser_factory.py     # Browser creation with Strategy pattern
│   ├── pages/                      # Unified page objects
│   │   ├── base_page.py           # Works with BOTH frameworks
│   │   ├── login_page.py          # Works with BOTH frameworks
│   │   ├── protocols.py           # Page protocols
│   │   └── locators/
│   │       └── login_locators.py  # Framework-agnostic locators
│   ├── config/
│   │   ├── protocols.py           # ConfigService protocol
│   │   └── environment_config.py  # Config implementation
│   └── utils/
│       ├── logger.py              # Logging system
│       ├── exceptions.py          # Custom exceptions
│       └── element_highlighter.py # Visual debugging
├── tests/                          # Unified tests
│   ├── conftest.py                # Supports --framework flag
│   └── test_login_unified.py      # Works with both Selenium & Playwright
├── unittests/                      # Framework unit tests (142 tests)
├── reports/                        # Test reports and screenshots
├── logs/                           # Daily test logs
├── .env                            # Environment variables
├── compose.yml                     # Selenium Grid (Docker)
├── pyproject.toml                  # Dependencies (uv)
├── CHECKPOINT.md                   # Quick status reference
└── REFACTORING_SUMMARY.md         # Complete refactoring documentation
```

## 🚀 Initial Setup

### Prerequisites:
- Python 3.10+
- Docker and Docker Compose
- UV package manager

### Installation:

1. **Install UV** (if you don't have it):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Install dependencies**:
```bash
uv sync
```

3. **Configure environment variables**:
The `.env` file already contains:
```env
URL=http://localhost:8080/web/index.php
USER=******
PASSWORD=********
```

4. **Start Selenium Grid**:
```bash
docker-compose up -d
```

Verify the grid is running:
- Hub: http://localhost:4444
- Grid Console: http://localhost:4444/ui

## 🧪 Running Tests (Unified Architecture)

### Run with Selenium (Default):
```bash
# All tests
uv run pytest tests/ -p no:playwright

# Specific test file
uv run pytest tests/test_login_unified.py -p no:playwright

# With specific browser
uv run pytest tests/ --framework=selenium --browser=firefox -p no:playwright

# Headless mode
uv run pytest tests/ --framework=selenium --headless -p no:playwright

# With markers
uv run pytest tests/ -m smoke -p no:playwright
```

### Run with Playwright:
```bash
# All tests
uv run pytest tests/ --framework=playwright -p no:playwright

# With specific browser (chromium, firefox, webkit)
uv run pytest tests/ --framework=playwright --browser=chromium -p no:playwright

# Headless mode (default for Playwright)
uv run pytest tests/ --framework=playwright --headless -p no:playwright

# With markers
uv run pytest tests/ --framework=playwright -m smoke -p no:playwright
```

### Run Unit Tests:
```bash
# All 142 unit tests
uv run pytest unittests/ -v

# Specific test module
uv run pytest unittests/test_browser_adapters.py -v
uv run pytest unittests/test_page_protocols.py -v
```

### Run in parallel:
```bash
uv run pytest tests/ -n auto -p no:playwright
```

### Generate HTML report:
```bash
uv run pytest tests/ --html=reports/report.html --self-contained-html -p no:playwright
```

## 🎯 Unified Architecture - Key Features

### One Codebase, Two Frameworks!

This framework uses a **unified architecture** that allows the same page objects and tests to work with **both Selenium and Playwright**:

**Key Benefits:**
- ✅ **90% Less Code Duplication**: Single page objects work with both frameworks
- ✅ **Switch Frameworks via Flag**: `--framework=selenium` or `--framework=playwright`
- ✅ **Protocol-Based Design**: Type-safe interfaces with structural typing
- ✅ **Adapter Pattern**: Clean separation between framework specifics and business logic
- ✅ **Single Source of Truth**: Maintain one LoginPage instead of two

**Architecture Layers:**

1. **BrowserProtocol**: Unified interface for browser operations
2. **Adapters**: Convert framework-specific APIs (WebDriver/Page) to BrowserProtocol
3. **Unified Pages**: Single page objects using BrowserProtocol
4. **Framework-Agnostic Tests**: Tests work with any framework via `--framework` flag

**Example - Same Test, Both Frameworks:**

```python
import pytest
from src.pages.protocols import LoginPageProtocol

@pytest.mark.smoke
def test_login(login_page: LoginPageProtocol, config_service):
    """This test works with BOTH Selenium and Playwright!"""

    login_page.login(config_service.username, config_service.password)

    assert "dashboard" in login_page.get_current_url()

# Run with Selenium:
# pytest tests/test_login_unified.py --framework=selenium -p no:playwright

# Run with Playwright:
# pytest tests/test_login_unified.py --framework=playwright -p no:playwright
```

**Locator Conversion Innovation:**

The framework automatically converts Selenium-style locators to Playwright selectors:

```python
# Define once (Selenium format)
USERNAME = SeleniumLocator(LocatorStrategy.NAME, "username", "Username field")

# Selenium uses: (By.NAME, "username")
# Playwright converts to: "[name='username']"
# Both work automatically!
```

## 📊 Allure Reports

El framework está configurado con **Allure Reports**, uno de los frameworks de reportes más profesionales para pruebas de automatización.

### Características de Allure:
- ✅ **Reportes visuales interactivos**: Dashboards con gráficos y estadísticas
- ✅ **Historial de ejecuciones**: Tracking de tendencias y flakiness
- ✅ **Categorización de errores**: Análisis automático de fallos
- ✅ **Attachments**: Screenshots, logs, videos, traces
- ✅ **Steps detallados**: Visualización paso a paso de cada test
- ✅ **Integración con CI/CD**: Jenkins, GitHub Actions, GitLab CI

### Instalación de Allure CLI:

**Linux/WSL:**
```bash
# Instalar Allure CLI
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

**macOS:**
```bash
brew install allure
```

**Windows:**
```bash
scoop install allure
```

### Ejecutar tests y generar reportes Allure:

```bash
# SELENIUM: Limpiar, ejecutar y generar reporte
rm -rf reports_selenium/allure-results/ reports_selenium/allure-report/
uv run pytest tests_selenium/ --alluredir=reports_selenium/allure-results
allure serve reports_selenium/allure-results

# PLAYWRIGHT: Limpiar, ejecutar y generar reporte
rm -rf reports_playwright/allure-results/ reports_playwright/allure-report/
uv run pytest tests_playwright/ --alluredir=reports_playwright/allure-results
allure serve reports_playwright/allure-results

# PLAYWRIGHT con Firefox
uv run pytest tests_playwright/ --browser firefox --alluredir=reports_playwright/allure-results
allure serve reports_playwright/allure-results

# PLAYWRIGHT con WebKit
uv run pytest tests_playwright/ --browser webkit --alluredir=reports_playwright/allure-results
allure serve reports_playwright/allure-results
```

### Comandos útiles de Allure:

```bash
# Generar reporte HTML estático (Selenium)
allure generate reports_selenium/allure-results -o reports_selenium/allure-report --clean
allure open reports_selenium/allure-report

# Generar reporte HTML estático (Playwright)
allure generate reports_playwright/allure-results -o reports_playwright/allure-report --clean
allure open reports_playwright/allure-report

# Limpiar resultados de Selenium
rm -rf reports_selenium/allure-results/ reports_selenium/allure-report/

# Limpiar resultados de Playwright
rm -rf reports_playwright/allure-results/ reports_playwright/allure-report/
```

### Estructura de decoradores Allure en tests:

Los tests ya incluyen decoradores de Allure para mejor organización:

```python
import allure
from src.config.config import Config

@allure.feature("Authentication")
@allure.story("User Login")
@allure.title("Successful login with valid credentials")
@allure.severity(allure.severity_level.CRITICAL)
def test_successful_login(login_page):
    with allure.step("Verify login page is loaded"):
        assert login_page.is_login_page_loaded()

    with allure.step(f"Enter username: {Config.USERNAME}"):
        login_page.enter_username(Config.USERNAME)

    with allure.step("Enter password"):
        login_page.enter_password(Config.PASSWORD)

    with allure.step("Click login button"):
        login_page.click_login_button()

    with allure.step("Verify successful redirect to dashboard"):
        current_url = login_page.get_current_url()
        allure.attach(current_url, name="Current URL",
                     attachment_type=allure.attachment_type.TEXT)
        assert "dashboard" in current_url.lower()
```

### Niveles de severidad Allure:

- `allure.severity_level.BLOCKER`: Pruebas críticas que bloquean el sistema
- `allure.severity_level.CRITICAL`: Funcionalidades críticas del negocio
- `allure.severity_level.NORMAL`: Funcionalidades importantes
- `allure.severity_level.MINOR`: Funcionalidades secundarias
- `allure.severity_level.TRIVIAL`: Tests de UI/UX menores

### Tipos de Attachments:

```python
# Texto
allure.attach(text, name="Description", attachment_type=allure.attachment_type.TEXT)

# JSON
allure.attach(json_data, name="Response", attachment_type=allure.attachment_type.JSON)

# PNG (screenshots automáticos en fallos)
allure.attach.file(screenshot_path, name="Screenshot",
                   attachment_type=allure.attachment_type.PNG)

# HTML
allure.attach(html_content, name="Page Source",
              attachment_type=allure.attachment_type.HTML)
```

### Integración con CI/CD:

**GitHub Actions:**
```yaml
- name: Run tests with Allure
  run: uv run pytest --alluredir=allure-results

- name: Generate Allure Report
  run: allure generate allure-results -o allure-report

- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./allure-report
```

### Filtrar tests por severidad:

```bash
# Solo tests CRITICAL (Selenium)
uv run pytest tests_selenium/ --allure-severities=critical --alluredir=reports_selenium/allure-results

# CRITICAL y BLOCKER (Playwright)
uv run pytest tests_playwright/ --allure-severities=blocker,critical --alluredir=reports_playwright/allure-results
```

### Ver el reporte generado:

```bash
# Opción 1: Servidor temporal (recomendado)
allure serve reports_playwright/allure-results

# Opción 2: Abrir HTML estático
allure open reports_playwright/allure-report
```

## 📝 Writing New Tests (Unified Architecture)

### Example using Unified LoginPage:

```python
import pytest
from src.pages.protocols import LoginPageProtocol
from src.config.protocols import ConfigService

@pytest.mark.smoke
def test_my_login(login_page: LoginPageProtocol, config_service: ConfigService):
    """
    This test works with BOTH Selenium and Playwright!
    No framework-specific code needed.
    """
    # The 'login_page' fixture already navigates to the page

    # Option 1: Direct method
    login_page.login(config_service.username, config_service.password)

    # Option 2: Method chaining (fluent interface)
    login_page.enter_username(config_service.username)\
              .enter_password(config_service.password)
    login_page.click_login_button()

    # Verifications
    assert "dashboard" in login_page.get_current_url()
```

### Create a New Unified Page Object:

```python
from src.core.locator import LocatorStrategy
from src.core.selenium_locator import SeleniumLocator
from src.core.browser_protocol import BrowserProtocol
from src.pages.base_page import BasePage

class DashboardLocators:
    """Framework-agnostic locators"""
    WELCOME_TEXT = SeleniumLocator(
        LocatorStrategy.CSS,
        ".oxd-topbar-header-breadcrumb",
        "Welcome message text"
    )
    LOGOUT_BUTTON = SeleniumLocator(
        LocatorStrategy.XPATH,
        "//a[@href='/web/index.php/auth/logout']",
        "Logout button"
    )

class DashboardPage(BasePage):
    """Unified Dashboard page - works with both Selenium and Playwright!"""

    def __init__(self, browser: BrowserProtocol, timeout: int = 10):
        super().__init__(browser, timeout)
        self.locators = DashboardLocators

    def get_welcome_message(self) -> str:
        """Get the welcome message text"""
        return self.get_text(self.locators.WELCOME_TEXT)

    def logout(self) -> None:
        """Click the logout button"""
        self.click(self.locators.LOGOUT_BUTTON)

# Use it in tests - works with both frameworks!
def test_dashboard(browser):  # browser can be Selenium or Playwright adapter
    dashboard = DashboardPage(browser)
    message = dashboard.get_welcome_message()
    assert "Dashboard" in message
```

## 🔧 Advanced Configuration

### Available Environment Variables (.env):
```env
# Application
URL=http://localhost:8080/web/index.php
USER=********
PASSWORD=*******

# Selenium Grid
SELENIUM_GRID_URL=http://localhost:4444

# Browser
BROWSER=chrome
HEADLESS=False

# Timeouts
DEFAULT_TIMEOUT=10
PAGE_LOAD_TIMEOUT=30
IMPLICIT_WAIT=5

# Window
WINDOW_WIDTH=1920
WINDOW_HEIGHT=1080
MAXIMIZE_WINDOW=True

# Screenshots
SCREENSHOT_ON_FAILURE=True
```

## 🎯 Framework Features

### Base Page (base_page.py):
- ✅ Automatic explicit waits
- ✅ Reusable methods (click, send_keys, get_text, etc.)
- ✅ Frame handling
- ✅ JavaScript execution
- ✅ Scroll to elements
- ✅ Visibility and presence verification
- ✅ Integrated logging in all actions

### Login Page (login_page.py):
- ✅ Centralized locators
- ✅ High-level methods (login, enter_username, etc.)
- ✅ Method chaining
- ✅ Page-specific validations
- ✅ Login action logging

### Fixtures (conftest.py):
- ✅ `driver`: Configured WebDriver connected to Grid
- ✅ `login_page`: LoginPage with automatic navigation
- ✅ Automatic screenshots on failures
- ✅ Browser configuration from CLI
- ✅ WebDriver lifecycle logging

### Logger Utility (utils/logger.py):
- ✅ Centralized logger with automatic configuration
- ✅ Console logs (INFO and above)
- ✅ File logs (DEBUG and above)
- ✅ Daily log files in `logs/` (project root)
- ✅ Decorators `@log_test_step` and `@log_action`
- ✅ Mixin `LoggerMixin` to add logging to any class

### Custom Exceptions (utils/exceptions.py):
- ✅ Custom exception hierarchy
- ✅ `FrameworkException`: Base exception
- ✅ `ElementNotFoundException`: Element not found
- ✅ `ElementNotClickableException`: Element not clickable
- ✅ `InvalidParameterException`: Invalid parameter
- ✅ `PageNotLoadedException`: Page not loaded
- ✅ `ConfigurationException`: Configuration error

### Locators (src/pages/locators/):
- ✅ Centralized locators in separate files
- ✅ Easier maintenance
- ✅ Reusability between tests
- ✅ Separation of concerns

### Pytest Markers:
- `@pytest.mark.smoke`: Quick smoke tests
- `@pytest.mark.regression`: Complete regression tests
- `@pytest.mark.login`: Login-specific tests
- `@pytest.mark.playwright`: Tests using Playwright
- `@pytest.mark.selenium`: Tests using Selenium

## 📊 Reports and Logs

Reports are automatically generated in:
- **Selenium HTML Report**: `reports_selenium/report.html`
- **Selenium Screenshots**: `reports_selenium/screenshots/` (only on failures)
- **Playwright Reports**: `reports_playwright/` (HTML, screenshots, videos, traces)
- **Logs**: `logs/test_automation_YYYYMMDD.log` (daily logs in root)

## 🧪 Unit Tests

The project includes unit tests to validate framework components without needing a browser:

```bash
# Run all unit tests
uv run pytest unittests/ -v

# Run tests from a specific module
uv run pytest unittests/test_config.py -v
uv run pytest unittests/test_logger.py -v
uv run pytest unittests/test_exceptions.py -v
uv run pytest unittests/test_locators.py -v
```

### Available Unit Tests:
- **test_config.py**: Configuration and environment variables tests
- **test_logger.py**: Logging system tests
- **test_exceptions.py**: Custom exceptions tests
- **test_locators.py**: Page locators tests

## 🐳 Docker Compose

The `docker-compose.yml` includes:
- Selenium Hub (port 4444)
- Chrome Node (VNC: 5900)
- Firefox Node (VNC: 5901)
- Edge Node (VNC: 5902)

### Useful commands:
```bash
# Start grid
docker-compose up -d

# View logs
docker-compose logs -f

# Stop grid
docker-compose down

# Scale nodes
docker-compose up -d --scale chrome=3
```

## 🔍 Debugging

### View browser sessions with VNC:
```bash
# Install VNC viewer, then connect to:
# Chrome: localhost:5900
# Firefox: localhost:5901
# Edge: localhost:5902
# Password: secret (default)
```

### View logs in real-time:
```bash
# View today's logs
tail -f logs/test_automation_$(date +%Y%m%d).log

# View logs with filter
grep "ERROR" logs/test_automation_*.log
grep "LoginPage" logs/test_automation_*.log
```

## 📝 Logger Usage

### In Page Objects:
```python
from utils.logger import TestLogger

class MyPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Logger is already available via self.logger from BasePage

    def my_action(self):
        self.logger.info("Executing my action")
        # ... code ...
```

### In Tests:
```python
from utils.logger import TestLogger, log_test_step

logger = TestLogger.get_logger(__name__)

@log_test_step("Verify user can login")
def test_login(login_page):
    logger.info("Starting login test")
    # ... test code ...
```

### Using LoggerMixin:
```python
from utils.logger import LoggerMixin

class MyHelper(LoggerMixin):
    def do_something(self):
        self.logger.info("Doing something")
        # ... code ...
```

### Log Levels:
- **DEBUG**: Detailed information for debugging (file only)
- **INFO**: Confirmation that things are working (console and file)
- **WARNING**: Indication of something unexpected
- **ERROR**: Error that doesn't stop execution
- **CRITICAL**: Serious error that may stop the program

## 🔍 Code Quality & Pre-commit Hooks

The project includes pre-commit hooks to ensure code quality and enforce coding standards automatically before each commit.

### What are Pre-commit Hooks?

Pre-commit hooks are automated checks that run before every git commit, helping to:
- ✅ **Catch errors early**: Find issues before they reach the repository
- ✅ **Enforce code style**: Maintain consistent formatting across the codebase
- ✅ **Remove unused imports**: Keep code clean automatically
- ✅ **Type checking**: Validate type hints with mypy
- ✅ **Security checks**: Detect potential security issues

### Included Hooks:

The `.pre-commit-config.yaml` file includes the following checks:

1. **General file checks**:
   - Trim trailing whitespace
   - Fix end of files
   - Check YAML/TOML/JSON syntax
   - Check for large files
   - Check for merge conflicts
   - Check for debug statements

2. **Python import sorting** (isort):
   - Automatically sorts imports alphabetically
   - Groups imports by standard library, third-party, and local

3. **Code formatting** (Black):
   - Enforces consistent code style
   - Line length: 100 characters
   - Follows PEP 8 standards

4. **Linting** (Ruff):
   - Fast Python linter (replaces flake8)
   - Checks for code smells and potential bugs
   - Enforces naming conventions
   - Suggests code simplifications

5. **Type checking** (mypy):
   - Validates type hints
   - Helps catch type-related bugs early

6. **Security scanning** (Bandit):
   - Scans for common security issues
   - Excludes test files from security checks

7. **Unused imports removal** (autoflake):
   - Automatically removes unused imports
   - Removes unused variables
   - Removes duplicate keys

### Pre-commit Installation:

Pre-commit is already installed with the development dependencies:

```bash
# Install all dev dependencies (includes pre-commit)
uv sync --dev

# Install the pre-commit hooks to your git repository
pre-commit install
```

### Using Pre-commit:

Once installed, hooks run automatically on every commit:

```bash
# Make changes to your code
git add .

# Hooks run automatically on commit
git commit -m "Your commit message"

# If hooks fail, they will modify files automatically
# Add the modified files and commit again
git add .
git commit -m "Your commit message"
```

### Manual Pre-commit Execution:

```bash
# Run pre-commit on all files (useful for initial setup)
pre-commit run --all-files

# Run pre-commit on staged files only
pre-commit run

# Run a specific hook
pre-commit run black --all-files
pre-commit run ruff --all-files
pre-commit run mypy --all-files

# Update hooks to latest versions
pre-commit autoupdate
```

### Bypassing Hooks (Not Recommended):

If you need to commit without running hooks (use sparingly):

```bash
git commit -m "Emergency fix" --no-verify
```

### Configuration Files:

- **`.pre-commit-config.yaml`**: Pre-commit hooks configuration
- **`pyproject.toml`**: Tool-specific settings (black, ruff, isort, mypy, etc.)

### Tool-Specific Commands:

Run tools manually without pre-commit:

```bash
# Format code with Black
uv run black . --line-length 100

# Sort imports with isort
uv run isort . --profile black

# Lint with Ruff
uv run ruff check . --fix

# Type check with mypy
uv run mypy src/ utils/

# Security check with Bandit
uv run bandit -r src/ utils/ -c pyproject.toml

# Remove unused imports
uv run autoflake --in-place --remove-all-unused-imports -r .
```

### Benefits:

- **Consistent code style**: All contributors follow the same formatting rules
- **Catch bugs early**: Type checking and linting find issues before code review
- **Save time**: Automated formatting means no manual style adjustments
- **Better code reviews**: Focus on logic, not formatting
- **Documentation**: Type hints serve as inline documentation

### Troubleshooting:

**Hook fails with "command not found":**
```bash
# Reinstall pre-commit
uv pip install --upgrade pre-commit
pre-commit install
```

**Want to skip a specific hook:**
Edit `.pre-commit-config.yaml` and comment out the hook:
```yaml
# - repo: https://github.com/psf/black
#   rev: 24.10.0
#   hooks:
#     - id: black
```

**Hooks take too long:**
```bash
# Pre-commit caches environments, but you can clear the cache:
pre-commit clean
```

## 📚 Reference

Framework based on principles from: https://github.com/taquimon/webauto2025

## 🤝 Contributing

1. Follow the Page Object Model pattern
2. Use the BasePage class for new pages
3. Add tests with appropriate markers
4. Document public methods
5. Run tests before committing

## 📄 License

MIT
