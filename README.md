# OrangeHRM Web Testing Automation Framework

Modern web test automation framework for OrangeHRM using Python, Pytest, and Playwright.

## 🏗️ Architecture and Design Patterns

### Implemented Patterns:
- **Page Object Model (POM)**: Encapsulation of elements and actions for each page
- **Base Page Pattern**: Base class with reusable methods for all pages
- **Functional Locators**: Playwright's recommended user-facing locators
- **Dependency Injection**: Configuration via ConfigService protocol
- **Method Chaining**: Fluent interface for page actions
- **SOLID Principles**: Single Responsibility, Open/Closed, Dependency Inversion

### Project Structure:
```
orangehrm-web-testing-framework/
├── src/
│   ├── config/
│   │   ├── protocols.py              # ConfigService protocol
│   │   └── environment_config.py     # Config implementation
│   ├── enums/
│   │   ├── browser_types.py          # Browser type enumeration
│   │   └── visual_debugging.py       # Visual debugging constants
│   ├── factories/
│   │   └── browser_factory.py        # Playwright browser factory
│   ├── pages/
│   │   ├── base_page.py              # Base page with common methods
│   │   ├── login_page.py             # Login page implementation
│   │   ├── leave_page.py             # Leave page implementation
│   │   ├── protocols.py              # PageObjectProtocol base interface
│   │   └── locators/
│   │       ├── login_locators.py     # Functional locators for LoginPage
│   │       └── leave_locators.py     # Functional locators for LeavePage
│   └── utils/
│       └── element_highlighter.py    # Visual debugging utility
├── tests/
│   ├── conftest.py                   # Playwright fixtures
│   ├── test_login.py                 # Login tests
│   └── test_leave.py                 # Leave tests
├── unittests/                        # Framework unit tests
├── utils/
│   ├── logger.py                     # Centralized logging system
│   └── exceptions.py                 # Custom exception hierarchy
├── logs/                             # Daily test logs
├── .env                              # Environment variables
├── pyproject.toml                    # Dependencies (uv)
├── GUIDE_ADD_NEW_PAGE.md             # Developer guide for adding pages
├── PHASE_3_CLEANUP_SUMMARY.md        # Refactoring documentation
└── REFACTOR_SUMMARY.md               # Complete refactoring history
```

## 🚀 Initial Setup

### Prerequisites:
- Python 3.10+
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

3. **Install Playwright browsers**:
```bash
uv run playwright install chromium firefox webkit
```

4. **Configure environment variables**:
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
URL=https://opensource-demo.orangehrmlive.com/web/index.php
USER=Admin
PASSWORD=admin123
BROWSER=chromium
HEADLESS=False
DEFAULT_TIMEOUT=10
```

## 🧪 Running Tests

### Run all tests:
```bash
# All tests
uv run pytest tests/ -v

# Specific test file
uv run pytest tests/test_login.py -v
uv run pytest tests/test_leave.py -v
```

### Run with different browsers:
```bash
# Chromium (default)
uv run pytest tests/ --browser chromium

# Firefox
uv run pytest tests/ --browser firefox

# WebKit (Safari)
uv run pytest tests/ --browser webkit
```

### Run in headed mode (see browser):
```bash
uv run pytest tests/ --headed
```

### Run with markers:
```bash
# Smoke tests only
uv run pytest tests/ -m smoke

# Regression tests
uv run pytest tests/ -m regression

# Login tests only
uv run pytest tests/ -m login
```

### Run in parallel:
```bash
uv run pytest tests/ -n auto
```

### Run Unit Tests:
```bash
# All unit tests (no browser needed)
uv run pytest unittests/ -v

# Specific test module
uv run pytest unittests/test_config.py -v
uv run pytest unittests/test_environment_config.py -v
```

## 📊 Allure Reports

The framework supports Allure Reports for professional test reporting.

### Install Allure CLI:

**Linux/WSL:**
```bash
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

### Generate Allure Reports:

```bash
# Clean previous results
rm -rf reports_playwright/allure-results/ reports_playwright/allure-report/

# Run tests with Allure
uv run pytest tests/ --alluredir=reports_playwright/allure-results

# Serve report (opens browser automatically)
allure serve reports_playwright/allure-results

# Generate static HTML report
allure generate reports_playwright/allure-results -o reports_playwright/allure-report --clean
allure open reports_playwright/allure-report
```

### Allure Report Features:
- ✅ Interactive dashboards with graphs and statistics
- ✅ Execution history and trend analysis
- ✅ Automatic error categorization
- ✅ Screenshots, logs, videos, and traces attached
- ✅ Detailed step-by-step visualization
- ✅ CI/CD integration (Jenkins, GitHub Actions, GitLab CI)

## 📝 Writing Tests

### Example Test:

```python
import pytest
from src.config.protocols import ConfigService
from src.pages.login_page import LoginPage

@pytest.mark.smoke
def test_login(login_page: LoginPage, config_service: ConfigService):
    """
    Test successful login with valid credentials.
    """
    # The login_page fixture already navigates to the page
    login_page.login(config_service.username, config_service.password)

    # Verify successful login
    assert "dashboard" in login_page.get_current_url()

@pytest.mark.smoke
def test_login_chaining(login_page: LoginPage, config_service: ConfigService):
    """
    Test login using method chaining (fluent interface).
    """
    login_page.enter_username(config_service.username)\
              .enter_password(config_service.password)\
              .click_login_button()

    assert "dashboard" in login_page.get_current_url()
```

### Create a New Page Object:

See [GUIDE_ADD_NEW_PAGE.md](GUIDE_ADD_NEW_PAGE.md) for a complete step-by-step guide.

**Quick Example:**

```python
# 1. Create locators file: src/pages/locators/dashboard_locators.py
class DashboardLocators:
    """Functional locators for Dashboard page."""

    @staticmethod
    def WELCOME_TEXT(page):
        """Welcome message text."""
        return page.get_by_role("heading", name="Dashboard")

    @staticmethod
    def USER_DROPDOWN(page):
        """User dropdown menu."""
        return page.get_by_role("button", name="user-dropdown")

# 2. Create page object: src/pages/dashboard_page.py
from playwright.sync_api import Page
from src.pages.base_page import BasePage
from src.pages.locators.dashboard_locators import DashboardLocators

class DashboardPage(BasePage):
    """Dashboard page implementation."""

    def __init__(self, page: Page, timeout: int = 10):
        super().__init__(page, timeout)
        self.locators = DashboardLocators

    def get_welcome_message(self) -> str:
        """Get the welcome message text."""
        return self.get_text(self.locators.WELCOME_TEXT(self.page))

    def click_user_dropdown(self) -> None:
        """Click the user dropdown menu."""
        self.click(self.locators.USER_DROPDOWN(self.page))

# 3. Use in tests
def test_dashboard(dashboard_page):
    message = dashboard_page.get_welcome_message()
    assert "Dashboard" in message
```

## 🎯 Framework Features

### Playwright Functional Locators:

The framework uses Playwright's recommended user-facing locators:

1. **`get_by_role()`** - Accessibility-based (MOST RECOMMENDED)
2. **`get_by_label()`** - For form fields
3. **`get_by_placeholder()`** - For inputs with placeholder
4. **`get_by_text()`** - For visible content
5. **CSS/XPath** - ONLY as last resort

**Benefits:**
- More resilient to DOM changes
- Better accessibility
- Self-documenting code
- Reflects how users interact with the page

### Base Page (base_page.py):
- ✅ Automatic waits (Playwright's auto-waiting)
- ✅ Reusable methods (click, send_keys, get_text, etc.)
- ✅ Frame handling
- ✅ JavaScript execution
- ✅ Scroll to elements
- ✅ Visibility and presence verification
- ✅ Integrated logging in all actions
- ✅ Flexible locator support (Locator | str | Callable)

### Configuration System:
- ✅ Dependency Injection via ConfigService protocol
- ✅ Environment-based configuration (.env)
- ✅ Type-safe configuration access
- ✅ No global singletons

### Logger Utility (utils/logger.py):
- ✅ Centralized logger with automatic configuration
- ✅ Console logs (INFO and above)
- ✅ File logs (DEBUG and above)
- ✅ Daily log files in `logs/` directory
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

### Pytest Markers:
```python
@pytest.mark.smoke      # Quick smoke tests
@pytest.mark.regression # Complete regression tests
@pytest.mark.login      # Login-specific tests
```

## 📊 Reports and Logs

Reports are automatically generated in:
- **Playwright HTML Report**: `playwright-report/` (run `playwright show-report`)
- **Screenshots**: `test-results/` (only on failures)
- **Videos**: `test-results/` (if enabled)
- **Traces**: `test-results/` (if enabled)
- **Allure Reports**: `reports_playwright/allure-results/`
- **Logs**: `logs/test_automation_YYYYMMDD.log` (daily logs)

## 🔍 Debugging

### View Playwright Report:
```bash
playwright show-report
```

### Run in headed mode:
```bash
uv run pytest tests/ --headed
```

### Enable traces:
```bash
uv run pytest tests/ --tracing on
```

### Interactive debug mode:
```bash
PWDEBUG=1 uv run pytest tests/test_login.py
```

### View logs in real-time:
```bash
# View today's logs
tail -f logs/test_automation_$(date +%Y%m%d).log

# Search for errors
grep "ERROR" logs/test_automation_*.log

# Search for specific page
grep "LoginPage" logs/test_automation_*.log
```

## 📝 Logger Usage

### In Page Objects:
```python
from src.pages.base_page import BasePage

class MyPage(BasePage):
    def my_action(self):
        self.logger.info("Executing my action")
        # Logger is available via self.logger from BasePage
```

### In Tests:
```python
from utils.logger import TestLogger, log_test_step

logger = TestLogger.get_logger(__name__)

@log_test_step("Verify user can login")
def test_login(login_page):
    logger.info("Starting login test")
    # Test code here
```

### Log Levels:
- **DEBUG**: Detailed information for debugging (file only)
- **INFO**: Confirmation that things are working (console and file)
- **WARNING**: Indication of something unexpected
- **ERROR**: Error that doesn't stop execution
- **CRITICAL**: Serious error that may stop the program

## 🔍 Code Quality & Pre-commit Hooks

The project includes pre-commit hooks to ensure code quality automatically.

### Install Pre-commit:
```bash
uv sync --dev
pre-commit install
```

### Included Hooks:
1. **File checks**: Trim whitespace, fix end of files, check syntax
2. **isort**: Sort imports automatically
3. **ruff**: Fast linting and formatting
4. **mypy**: Type checking
5. **pyright**: Additional type checking
6. **pylint**: Code quality checks
7. **bandit**: Security scanning
8. **autoflake**: Remove unused imports

### Manual Execution:
```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific tool
uv run ruff check . --fix
uv run ruff format .
uv run mypy src/ utils/
uv run pyright src/ utils/
uv run pylint src/ utils/
uv run bandit -r src/ utils/
```

### Benefits:
- ✅ Consistent code style across the project
- ✅ Catch bugs early with type checking
- ✅ Automated formatting (no manual style adjustments)
- ✅ Security issue detection
- ✅ Better code reviews (focus on logic, not style)

## 🏛️ Architecture Principles

### SOLID Principles Applied:

1. **Single Responsibility Principle (SRP)**:
   - Each page class has one responsibility
   - ElementHighlighter separated from BasePage
   - Locators in separate files

2. **Open/Closed Principle (OCP)**:
   - Add new pages without modifying existing code
   - No need to edit protocols.py for new pages

3. **Dependency Inversion Principle (DIP)**:
   - Depend on ConfigService protocol, not concrete implementation
   - Injected via fixtures, not imported directly

4. **YAGNI (You Aren't Gonna Need It)**:
   - Removed unnecessary abstractions (adapters, page-specific protocols)
   - Single implementation = no need for protocols

### Refactoring History:

The framework has undergone significant refactoring to improve simplicity and maintainability:

- **Phase 1**: Removed dual Selenium/Playwright support (Playwright only)
- **Phase 2**: Eliminated adapter layer (direct Playwright API usage)
- **Phase 3**: Removed page-specific protocols (YAGNI principle)
- **Phase 4**: Implemented Playwright functional locators
- **Phase 5**: Removed PlaywrightLocator wrapper class

**Result**: 51% code reduction, simpler architecture, better maintainability

See [PHASE_3_CLEANUP_SUMMARY.md](PHASE_3_CLEANUP_SUMMARY.md) and [REFACTOR_SUMMARY.md](REFACTOR_SUMMARY.md) for details.

## 📚 Documentation

- **[GUIDE_ADD_NEW_PAGE.md](GUIDE_ADD_NEW_PAGE.md)**: Step-by-step guide for adding new pages
- **[PHASE_3_CLEANUP_SUMMARY.md](PHASE_3_CLEANUP_SUMMARY.md)**: Recent refactoring summary
- **[REFACTOR_SUMMARY.md](REFACTOR_SUMMARY.md)**: Complete refactoring history

## 🤝 Contributing

1. Follow the Page Object Model pattern
2. Use Playwright functional locators (get_by_role, get_by_label, etc.)
3. Create locators as @staticmethod functions
4. Use dependency injection for configuration
5. Add tests with appropriate markers
6. Document public methods with docstrings
7. Run pre-commit hooks before committing

## 📄 License

MIT
