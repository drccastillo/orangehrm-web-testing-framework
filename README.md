# OrangeHRM Web Testing Automation Framework

Web test automation framework for OrangeHRM using Python, Pytest, Selenium, and Docker.

## 🏗️ Architecture and Design Patterns

### Implemented Patterns:
- **Page Object Model (POM)**: Encapsulation of elements and actions for each page
- **Base Page Pattern**: Base class with reusable methods for all pages
- **Factory Pattern**: Dynamic browser configuration
- **Singleton Pattern**: Centralized configuration management
- **Method Chaining**: Fluent interface for page actions

### Project Structure:
```
web-testing-framework/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py              # Centralized configuration
│   ├── pages_selenium/
│   │   ├── __init__.py
│   │   ├── base_page.py           # Base class with common methods
│   │   └── login_page.py          # Page Object Model for login
│   └── pages_playwright/
│       ├── __init__.py
│       ├── base_page_pw.py        # Base class for Playwright
│       └── login_page_pw.py       # Page Object for Playwright
├── tests_selenium/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures and configuration
│   └── test_login.py              # Login tests
├── tests_playwright/
│   ├── conftest.py                # Playwright fixtures
│   └── test_login_pw.py           # Playwright tests
├── utils/
│   └── __init__.py
├── reports_selenium/               # Selenium HTML reports and screenshots
├── reports_playwright/             # Playwright reports, videos, and traces
├── .env                            # Environment variables
├── .gitignore
├── compose.yml                     # Selenium Grid with Chrome, Firefox, Edge
├── pyproject.toml                  # Dependencies and configuration (uv)
└── README.md
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

## 🧪 Running Tests

### Run all tests:
```bash
uv run pytest
```

### Run specific tests:
```bash
# Only login tests
uv run pytest tests/test_login.py

# Tests with 'smoke' marker
uv run pytest -m smoke

# Tests with 'login' marker
uv run pytest -m login

# Regression tests
uv run pytest -m regression
```

### Run in different browsers:
```bash
# Chrome (default)
uv run pytest --browser=chrome

# Firefox
uv run pytest --browser=firefox

# Edge
uv run pytest --browser=edge
```

### Run in headless mode:
```bash
uv run pytest --headless
```

### Run tests in parallel:
```bash
uv run pytest -n auto
```

### Generate HTML report:
```bash
uv run pytest --html=reports_selenium/report.html --self-contained-html
```

## 🎭 Playwright Framework (New)

### Overview
In addition to the Selenium Grid framework, the project now includes a complete implementation with **Playwright**, which offers better performance, integrated auto-waiting, and advanced debugging tools.

### Playwright Structure:
```
src/pages_playwright/
├── base_page_pw.py           # Base Page for Playwright
├── login_page_pw.py           # Login Page using Playwright
└── locators/
    └── login_locators_pw.py   # Locators (string selectors)

tests_playwright/
├── conftest.py                # Playwright fixtures
├── test_login_pw.py           # Complete tests
└── test_login_simple_pw.py    # Simple tests

reports_playwright/
├── report.html                # HTML report
├── screenshots/               # Screenshots on failures
├── videos/                    # Test videos
└── traces/                    # Traces for debugging
```

### Playwright Installation:

Playwright is already installed with the project dependencies, but you need to install the browsers:

```bash
# Browsers were already installed during setup
# If you need to reinstall them:
uv run playwright install chromium firefox
```

### Running Tests with Playwright:

```bash
# Run all Playwright tests
uv run pytest tests_playwright/ -v

# Run with specific browser (chromium, firefox, webkit)
uv run pytest tests_playwright/ --browser chromium
uv run pytest tests_playwright/ --browser firefox

# Run in headed mode (see the browser)
uv run pytest tests_playwright/ --headed

# Generate HTML report
uv run pytest tests_playwright/ --html=reports_playwright/report.html --self-contained-html

# Run with specific markers
uv run pytest tests_playwright/ -m smoke
uv run pytest tests_playwright/ -m playwright

# Run in parallel
uv run pytest tests_playwright/ -n auto

# Run with custom URL
URL="https://opensource-demo.orangehrmlive.com" uv run pytest tests_playwright/
```

### Playwright Features:

**Advantages over Selenium:**
- ✅ **Auto-waiting**: No need for complex explicit waits
- ✅ **Faster**: Better performance than Selenium
- ✅ **Multi-browser**: Chromium, Firefox, WebKit (Safari)
- ✅ **Trace Viewer**: Time-travel debugging
- ✅ **Videos**: Automatic test recording
- ✅ **Network Interception**: Intercept and mock requests
- ✅ **Multi-context**: Multiple simultaneous browser sessions

**Key differences with Selenium:**

| Aspect | Selenium | Playwright |
|---------|----------|------------|
| Locators | Tuples `(By.ID, "value")` | Strings `"#value"` |
| Waits | Explicit (WebDriverWait) | Integrated auto-waiting |
| Click | `element.click()` | `page.click(selector)` |
| Input | `send_keys(text)` | `fill(selector, text)` |
| Setup | Selenium Grid (Docker) | Local (simpler) |

### Example Test with Playwright:

```python
import pytest
from src.config.config import Config
from src.pages_playwright.login_page_pw import LoginPagePW

@pytest.mark.playwright
@pytest.mark.smoke
def test_login(login_page_pw: LoginPagePW):
    # The login_page_pw fixture already navigates to the page
    login_page_pw.login(Config.USERNAME, Config.PASSWORD)

    # Playwright waits automatically
    assert "dashboard" in login_page_pw.get_current_url()
```

### Debugging with Playwright:

```bash
# Generate traces for debugging
uv run pytest tests_playwright/ --tracing on

# View trace with Playwright Inspector
uv run playwright show-trace reports_playwright/traces/trace.zip

# Interactive debug mode
PWDEBUG=1 uv run pytest tests_playwright/test_login_simple_pw.py

# View videos of executed tests
ls reports_playwright/videos/
```

### Create a New Page Object for Playwright:

```python
from src.pages_playwright.base_page_pw import BasePagePW

class DashboardPagePW(BasePagePW):
    # Locators (strings instead of tuples)
    WELCOME_TEXT = ".oxd-topbar-header-breadcrumb"

    def __init__(self, page, timeout=10):
        super().__init__(page, timeout)

    def get_welcome_message(self):
        return self.get_text(self.WELCOME_TEXT)
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

## 📝 Writing New Tests

### Example using LoginPage:

```python
import pytest
from src.config.config import Config
from src.pages_selenium.login_page import LoginPage

@pytest.mark.smoke
def test_my_login(login_page: LoginPage):
    # The 'login_page' fixture already navigates to the page

    # Option 1: Direct method
    login_page.login(Config.USERNAME, Config.PASSWORD)

    # Option 2: Method chaining
    login_page.enter_username(Config.USERNAME)\
              .enter_password(Config.PASSWORD)
    login_page.click_login_button()

    # Verifications
    assert "dashboard" in login_page.get_current_url()
```

### Create a New Page Object:

```python
from selenium.webdriver.common.by import By
from src.pages_selenium.base_page import BasePage

class DashboardPage(BasePage):
    # Locators
    WELCOME_TEXT = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb")

    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)

    def get_welcome_message(self):
        return self.get_text(self.WELCOME_TEXT)
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
