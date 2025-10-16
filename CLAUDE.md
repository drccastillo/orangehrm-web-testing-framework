# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a web test automation framework for OrangeHRM using Python, Pytest, and both Selenium Grid and Playwright. The framework implements the Page Object Model (POM) design pattern with dual automation support.

**Recent Refactoring (Phase 1 - Foundation):**
The framework has been refactored following SOLID principles:
- ✅ **Phase 1.1**: Config Singleton → Dependency Injection (ConfigService protocol)
- ✅ **Phase 1.2**: Property Pollution removed from Page Objects
- ✅ **Phase 1.3**: ElementHighlighter extracted from BasePage (SRP)
- ✅ **Phase 1.4**: Visual debugging constants consolidated

See REFACTOR_PLAN.md for the complete refactoring roadmap.

## Build & Test Commands

### Setup
```bash
# Install dependencies using UV package manager
uv sync

# Install Playwright browsers (if using Playwright)
uv run playwright install chromium firefox

# Start Selenium Grid (for Selenium tests)
docker-compose up -d

# Verify Selenium Grid is running: http://localhost:4444/ui
```

### Running Tests

**Selenium Tests:**
```bash
# Run all Selenium tests
uv run pytest tests_selenium/

# Run specific test file
uv run pytest tests_selenium/test_login.py

# Run with specific browser (chrome, firefox, edge)
uv run pytest tests_selenium/ --browser=firefox

# Run in headless mode
uv run pytest tests_selenium/ --headless

# Run with markers
uv run pytest tests_selenium/ -m smoke
uv run pytest tests_selenium/ -m regression

# Run in parallel
uv run pytest tests_selenium/ -n auto

# Generate HTML report
uv run pytest tests_selenium/ --html=reports_selenium/report.html --self-contained-html

# Generate Allure report
uv run pytest tests_selenium/ --alluredir=reports_selenium/allure-results
allure serve reports_selenium/allure-results
```

**Playwright Tests:**
```bash
# Run all Playwright tests
uv run pytest tests_playwright/

# Run with specific browser (chromium, firefox, webkit)
uv run pytest tests_playwright/ --browser chromium

# Run in headed mode (see browser)
uv run pytest tests_playwright/ --headed

# Generate Allure report
uv run pytest tests_playwright/ --alluredir=reports_playwright/allure-results
allure serve reports_playwright/allure-results

# Run with custom URL
URL="https://opensource-demo.orangehrmlive.com" uv run pytest tests_playwright/
```

**Unit Tests:**
```bash
# Run all unit tests (framework components only, no browser needed)
uv run pytest unittests/ -v
```

### Code Quality

```bash
# Run all pre-commit hooks manually
pre-commit run --all-files

# Run specific tools
uv run ruff check . --fix              # Lint and auto-fix
uv run ruff format .                   # Format code
uv run isort . --profile black         # Sort imports
uv run mypy src/ utils/                # Type checking with mypy
uv run pyright src/ utils/             # Type checking with pyright
uv run pylint src/ utils/              # Lint with pylint
uv run bandit -r src/ utils/           # Security scan
```

## Architecture

### Dual Framework Structure

This framework uniquely supports **both Selenium Grid and Playwright**, allowing teams to leverage the strengths of each:
- **Selenium Grid**: Remote execution, Docker-based, multi-browser support (Chrome/Firefox/Edge)
- **Playwright**: Modern automation, faster, better auto-waiting, built-in tracing

### Directory Structure

```
src/
├── config/
│   ├── config.py                 # Legacy Config class (being phased out)
│   ├── protocols.py              # ConfigService protocol (Phase 1.1)
│   └── environment_config.py     # EnvironmentConfigService implementation (Phase 1.1)
├── constants/
│   └── visual_debugging.py       # Visual debugging constants (Phase 1.4)
├── pages_selenium/               # Selenium page objects
│   ├── base_page.py             # BasePage with common Selenium methods
│   ├── login_page.py            # Login page implementation
│   └── locators/                # Selenium locators (tuples: By.ID, "value")
├── pages_playwright/             # Playwright page objects
│   ├── base_page_pw.py          # BasePagePW with common Playwright methods
│   ├── login_page_pw.py         # Login page implementation
│   └── locators/                # Playwright locators (strings: "#value")
└── utils/
    └── element_highlighter.py    # Element highlighting for debugging (Phase 1.3)

tests_selenium/                   # Selenium test suite
├── conftest.py                  # Selenium fixtures & WebDriver setup
└── test_*.py                    # Test files

tests_playwright/                 # Playwright test suite
├── conftest.py                  # Playwright fixtures & Page setup
└── test_*.py                    # Test files

utils/
├── logger.py                    # Centralized logging with TestLogger class
└── exceptions.py                # Custom exception hierarchy

unittests/                        # Framework unit tests (no browser)
```

### Key Architectural Patterns

**1. Page Object Model (POM)**
- Each page is a class that encapsulates locators and actions
- Tests interact with page methods, not raw WebDriver/Page objects
- Example: `login_page.login(username, password)` instead of direct element interactions

**2. Base Page Pattern**
- `BasePage` (Selenium): Common methods with explicit waits, element highlighting, logging
- `BasePagePW` (Playwright): Common methods with auto-waiting, expect assertions, logging
- All page objects inherit from respective base classes

**3. Locator Separation**
- Selenium locators: Tuples `(By.ID, "username")` in `pages_selenium/locators/`
- Playwright locators: String selectors `"input[name='username']"` in `pages_playwright/locators/`
- Centralized in separate files for easier maintenance

**4. Factory Pattern**
- Dynamic browser configuration in `conftest.py`
- Browser-specific options (Chrome, Firefox, Edge) via CLI args

**5. Dependency Injection (Phase 1.1)**
- Configuration injected via `config_service` fixture (replaced Singleton)
- `ConfigService` protocol defines interface for configuration
- `EnvironmentConfigService` implementation loads from `.env` file
- Tests receive config via dependency injection: `def test_login(config_service: ConfigService)`
- Legacy `Config` class maintained for backward compatibility during migration

**6. Method Chaining**
- Page objects support fluent interface: `page.enter_username("admin").enter_password("pass")`

**7. Single Responsibility Principle (Phase 1.3)**
- `ElementHighlighter` extracted from BasePage for visual debugging
- BasePage injects highlighter: `self.highlighter = highlighter or ElementHighlighter(driver)`
- Visual debugging constants consolidated in `src/constants/visual_debugging.py` (Phase 1.4)
- Separation of concerns: Page interaction vs. visual debugging

### Critical Differences: Selenium vs Playwright

| Aspect | Selenium | Playwright |
|--------|----------|------------|
| **Locators** | Tuples `(By.ID, "value")` | Strings `"#value"` |
| **Waits** | Explicit waits required (`WebDriverWait`) | Auto-waiting built-in |
| **Click** | `element.click()` | `page.click(selector)` |
| **Input** | `send_keys(text)` | `fill(selector, text)` |
| **Setup** | Selenium Grid (Docker) | Local (simpler) |
| **Base Class** | `BasePage` | `BasePagePW` |
| **Conftest** | `tests_selenium/conftest.py` | `tests_playwright/conftest.py` |

### WebDriver/Page Lifecycle

**Selenium:**
- `driver` fixture: Creates Remote WebDriver connected to Selenium Grid at `http://localhost:4444`
- Scope: function-level (new driver per test)
- Configuration: Browser options set via `--browser` CLI flag
- Cleanup: `driver.quit()` called after each test

**Playwright:**
- `page` fixture: Creates Playwright Page from BrowserContext
- Scope: function-level (new page per test)
- Configuration: Browser type set via `--browser` CLI flag, headed/headless via `--headed` flag
- Cleanup: `page.close()` called after each test

### Configuration System

**Environment Variables (.env):**
```env
URL=http://localhost:8080/web/index.php
ORANGEHRM_USERNAME=Admin
ORANGEHRM_PASSWORD=admin123
SELENIUM_GRID_URL=http://localhost:4444
BROWSER=chrome
HEADLESS=False
DEFAULT_TIMEOUT=10
```

**Accessing Config (New Pattern - Phase 1.1):**
```python
from src.config.protocols import ConfigService

# In tests, config is injected via fixture
def test_login(login_page, config_service: ConfigService):
    login_page.login(config_service.username, config_service.password)
    assert "dashboard" in login_page.get_current_url()
```

**Legacy Pattern (being phased out):**
```python
from src.config.config import Config

Config.BASE_URL          # Application URL
Config.USERNAME          # Login username
Config.PASSWORD          # Login password
Config.DEFAULT_TIMEOUT   # Timeout in seconds
```

### Logging System

**Features:**
- Dual output: Console (INFO+) and file (DEBUG+)
- Daily rotating logs in `logs/test_automation_YYYYMMDD.log`
- Available via `TestLogger.get_logger(__name__)`
- Integrated into BasePage/BasePagePW via `self.logger`

**Usage in tests:**
```python
from utils.logger import TestLogger, log_test_step

logger = TestLogger.get_logger(__name__)

@log_test_step("Verify login functionality")
def test_login(login_page):
    logger.info("Starting login test")
    # test code
```

### Custom Exceptions

Framework uses custom exception hierarchy in `utils/exceptions.py`:
- `ElementNotFoundException`: Element not found within timeout
- `ElementNotClickableException`: Element not clickable
- `InvalidParameterException`: Invalid parameter passed
- `PageNotLoadedException`: Page not loaded correctly
- `ConfigurationException`: Configuration error

### Fixtures Architecture

**Selenium (tests_selenium/conftest.py):**
- `browser_name`: Get browser from CLI or default
- `headless`: Get headless mode from CLI
- `driver`: Create Remote WebDriver with browser options
- `login_page`: Create LoginPage and navigate to BASE_URL

**Playwright (tests_playwright/conftest.py):**
- `browser_type_launch_args`: Configure browser launch (headless/headed)
- `browser_context_args`: Configure viewport, video recording
- `page`: Override pytest-playwright's page with custom timeout
- `login_page_pw`: Create LoginPagePW and navigate to BASE_URL

### Pre-commit Hooks

The framework uses pre-commit hooks that run automatically on `git commit`:
- **isort**: Sort imports
- **ruff**: Lint and format (replaces Black)
- **mypy**: Type checking
- **pyright**: Additional type checking
- **pylint**: Code quality checks
- **bandit**: Security scanning
- **autoflake**: Remove unused imports

All tools configured in `pyproject.toml`. To bypass (not recommended): `git commit --no-verify`

## Creating New Page Objects

### Selenium Page Object (Phase 1.2 - No Property Pollution)
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from src.pages_selenium.base_page import BasePage

class DashboardLocators:
    """Centralized locators for Dashboard page."""
    WELCOME_TEXT = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb")
    LOGOUT_BUTTON = (By.XPATH, "//a[@href='/web/index.php/auth/logout']")

class DashboardPage(BasePage):
    """Dashboard page object following Phase 1.2 refactoring."""

    def __init__(self, driver: WebDriver, timeout: int = 10):
        super().__init__(driver, timeout)
        self.locators = DashboardLocators

    def get_welcome_message(self):
        return self.get_text(self.locators.WELCOME_TEXT)

    def logout(self):
        self.click(self.locators.LOGOUT_BUTTON)
```

### Playwright Page Object
```python
from src.pages_playwright.base_page_pw import BasePagePW

class DashboardPagePW(BasePagePW):
    # Locators (strings)
    WELCOME_TEXT = ".oxd-topbar-header-breadcrumb"
    LOGOUT_BUTTON = "a[href='/web/index.php/auth/logout']"

    def get_welcome_message(self):
        return self.get_text(self.WELCOME_TEXT)

    def logout(self):
        self.click(self.LOGOUT_BUTTON)
```

## Writing Tests

### Selenium Test (Phase 1.1 - Dependency Injection)
```python
import pytest
from src.config.protocols import ConfigService

@pytest.mark.selenium
@pytest.mark.smoke
def test_login(login_page, config_service: ConfigService):
    # login_page fixture auto-navigates to config_service.base_url
    # config_service is injected via fixture (no more Config.X)
    login_page.login(config_service.username, config_service.password)
    assert "dashboard" in login_page.get_current_url()
```

### Playwright Test (Phase 1.1 - Dependency Injection)
```python
import pytest
from src.config.protocols import ConfigService

@pytest.mark.playwright
@pytest.mark.smoke
def test_login(login_page_pw, config_service: ConfigService):
    # login_page_pw fixture auto-navigates to config_service.base_url
    # config_service is injected via fixture (no more Config.X)
    login_page_pw.login(config_service.username, config_service.password)
    assert "dashboard" in login_page_pw.get_current_url()
```

## Test Markers

Available pytest markers (configured in `pyproject.toml`):
- `@pytest.mark.smoke`: Quick smoke tests
- `@pytest.mark.regression`: Full regression tests
- `@pytest.mark.login`: Login-specific tests
- `@pytest.mark.selenium`: Selenium-specific tests
- `@pytest.mark.playwright`: Playwright-specific tests

## Debugging

### Selenium
```bash
# View VNC sessions
# Chrome: localhost:5900 | Firefox: localhost:5901 | Edge: localhost:5902
# Password: secret

# Check Selenium Grid status
curl http://localhost:4444/status

# View logs
docker-compose logs -f chrome
```

### Playwright
```bash
# Run in headed mode (see browser)
uv run pytest tests_playwright/ --headed

# Enable trace recording
uv run pytest tests_playwright/ --tracing on

# View trace
uv run playwright show-trace reports_playwright/traces/trace.zip

# Interactive debug mode
PWDEBUG=1 uv run pytest tests_playwright/test_login_pw.py
```

### Framework Logs
```bash
# View today's logs
tail -f logs/test_automation_$(date +%Y%m%d).log

# Search logs
grep "ERROR" logs/test_automation_*.log
```

## Important Notes

1. **Docker Network**: Selenium Grid requires external Docker network `orange-hrm_default`. Create it before running tests: `docker network create orange-hrm_default`

2. **Timeouts**: Selenium uses explicit waits (configured via `Config.DEFAULT_TIMEOUT`). Playwright has auto-waiting built-in but respects timeout settings.

3. **Screenshots**: Automatically captured on test failures in respective `reports_selenium/screenshots/` and `reports_playwright/screenshots/` directories.

4. **Allure Reports**: Professional reporting system with dashboards, trends, and detailed test steps. Requires Allure CLI installation.

5. **Package Manager**: This project uses **UV** (not pip or poetry). All dependency commands use `uv run` or `uv sync`.

6. **No Implicit Waits**: Selenium tests use explicit waits only for better control. Avoid adding implicit waits.

7. **Type Checking**: Framework excludes test directories from type checking. Only `src/` and `utils/` are type-checked by mypy/pyright.
