# OrangeHRM Web Testing Automation Framework

[![CI/CD Pipeline](https://github.com/drccastillo/orangehrm-web-testing-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/drccastillo/orangehrm-web-testing-framework/actions/workflows/ci.yml)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.55.0-green.svg)](https://playwright.dev/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

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
│   │   └── browser_types.py          # Browser type enumeration
│   ├── factories/
│   │   └── browser_factory.py        # Playwright browser factory
│   └── ui/                           # UI automation layer
│       ├── components/
│       │   └── navigation_header.py  # Global navigation component
│       └── pages/
│           ├── base_page.py          # Base page with common methods
│           ├── login/
│           │   └── login_page.py     # Login page implementation
│           └── leave/                # Leave module pages
│               ├── leave_base_page.py    # Leave module navigation
│               ├── apply/
│               ├── assign/
│               ├── configure/
│               ├── entitlements/
│               ├── list/
│               ├── my_leave/
│               └── reports/
├── tests/
│   ├── conftest.py                   # Playwright fixtures
│   ├── test_login.py                 # Login tests
│   └── test_leave.py                 # Leave module tests
├── unittests/                        # Framework unit tests
├── utils/
│   ├── logger.py                     # Centralized logging system
│   └── exceptions.py                 # Custom exception hierarchy
├── logs/                             # Daily test logs
├── .env                              # Environment variables
└── pyproject.toml                    # Dependencies (uv)
```

## 🚀 Initial Setup

### Prerequisites:
- Python 3.13+
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

Edit `.env` with your credentials (see `.env.example` for all required variables):
```env
# Application Configuration
URL=https://opensource-demo.orangehrmlive.com/web/index.php
ORANGEHRM_USERNAME=Admin
ORANGEHRM_PASSWORD=admin123

# Browser Configuration
BROWSER=chromium
HEADLESS=False

# Timeout Configuration (seconds)
DEFAULT_TIMEOUT=10
PAGE_LOAD_TIMEOUT=30

# Window Configuration
WINDOW_WIDTH=1920
WINDOW_HEIGHT=1080
MAXIMIZE_WINDOW=True

# Screenshot Configuration
SCREENSHOT_ON_FAILURE=True
```

**⚠️ Important**: All environment variables are REQUIRED. The framework uses strict validation and will raise `ConfigurationException` if any variable is missing.

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

## 🚀 CI/CD Pipeline

### GitHub Actions Workflows

This project uses GitHub Actions for continuous integration and automated testing.

#### Main CI Workflow

**Triggers:**
- Push to `main` branch
- Pull requests to `main`
- Manual dispatch

**Jobs:**
- **code-quality**: Linting (ruff), type checking (mypy, pyright), security scan (bandit) - ~2 min
- **unit-tests**: Framework unit tests (no browser required) - ~1 min
- **smoke-tests**: Critical path integration tests (chromium only) - ~3-5 min
- **regression-tests**: Full test suite with multiple browsers (chromium, firefox, webkit) - ~25-35 min (main branch only)

**Execution Time:**
- PR checks: ~5-7 minutes (parallel execution)
- Main branch: Adds regression tests (~25-35 min total)

#### Scheduled Tests

**Triggers:**
- Daily at 2 AM UTC
- Manual dispatch

**Purpose:** Nightly regression tests across all browsers and test categories for continuous monitoring.

### Required GitHub Secrets

To enable CI/CD, configure these secrets in your repository:

**Navigate to:** Repository → Settings → Secrets and variables → Actions → New repository secret

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `ORANGEHRM_USERNAME` | OrangeHRM login username | `Admin` |
| `ORANGEHRM_PASSWORD` | OrangeHRM login password | `admin123` |
| `ORANGEHRM_URL` | OrangeHRM base URL (optional) | Defaults to public demo site |

### Status Checks for PR Merge

Pull requests must pass these checks before merging to `main`:
- ✅ Code quality (linting, formatting, type checking)
- ✅ Unit tests
- ✅ Smoke tests

**Configure branch protection:**
1. Go to repository **Settings → Branches → Add branch protection rule**
2. Branch name pattern: `main`
3. Enable: **Require status checks to pass before merging**
4. Select status checks: `code-quality`, `unit-tests`, `smoke-tests`
5. Save changes

### Local CI Validation

Test your changes locally before pushing to ensure CI will pass:

```bash
# Run comprehensive validation script
./scripts/ci-validate.sh

# Or manually run checks
uv run ruff format --check .
uv run ruff check .
uv run mypy src/ utils/
uv run pytest unittests/ -v
uv run pytest tests/ -m smoke -v
```

### Viewing Test Results

**GitHub Actions Dashboard:**
1. Go to repository **Actions** tab
2. Select workflow run to view logs and results
3. Download artifacts (Playwright reports, logs, screenshots)

**Artifacts Generated:**
- Playwright HTML reports
- Test results (screenshots, videos, traces)
- Test logs
- Retention: 30 days for main workflow, 14 days for scheduled tests

### Troubleshooting CI Failures

| Issue | Solution |
|-------|----------|
| Tests pass locally but fail in CI | Verify GitHub Secrets are configured correctly |
| Timeout errors | Tests may be slower in CI; check logs for specific failures |
| Cache issues | Clear cache in Actions tab → Caches |
| Browser compatibility issues | Review browser-specific logs in artifacts |

For detailed workflow documentation, see [.github/workflows/README.md](.github/workflows/README.md).

## 📊 Test Reports

The framework supports multiple report formats for test results.

### HTML Report (pytest-html)

Generate a simple HTML report with test results:

```bash
# Generate HTML report
uv run pytest tests/ --html=reports/pytest-report.html --self-contained-html

# Open the report
open reports/pytest-report.html  # macOS
xdg-open reports/pytest-report.html  # Linux
```

**Features:**
- ✅ Single self-contained HTML file
- ✅ Test pass/fail summary
- ✅ Execution time details
- ✅ Error messages and logs
- ✅ Quick overview of test results

---

## 📊 Allure Reports

The framework supports Allure Reports for professional test reporting with advanced features.

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
rm -rf reports/allure-results/ reports/allure-report/

# Run tests with Allure
uv run pytest tests/ --alluredir=reports/allure-results

# Serve report (opens browser automatically)
allure serve reports/allure-results

# Generate static HTML report
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

### Allure Report Features:
- ✅ Interactive dashboards with graphs and statistics
- ✅ Execution history and trend analysis
- ✅ Automatic error categorization
- ✅ Screenshots, logs, videos, and traces attached
- ✅ Detailed step-by-step visualization
- ✅ CI/CD integration (Jenkins, GitHub Actions, GitLab CI)

---

### CI/CD Reports

Reports are **automatically generated** in GitHub Actions workflows:

**Accessing Reports:**
1. Go to **Actions** tab in GitHub repository
2. Select a workflow run
3. Scroll down to **Artifacts** section
4. Download available artifacts:
   - `html-report-*` - pytest HTML report (single file)
   - `allure-results-*` - Allure JSON results (raw data)
   - `allure-report` - Complete Allure HTML report (ready to view)
   - `test-results-*` - Screenshots, logs, and traces

**Viewing Allure Report Online (GitHub Pages):**

After each CI run, an Allure report is automatically generated and published to GitHub Pages:

1. Enable GitHub Pages in your repository:
   - Go to **Settings** → **Pages**
   - Source: **Deploy from a branch**
   - Branch: **gh-pages** → **/ (root)**
   - Click **Save**

2. Access the report at:
   ```
   https://<your-username>.github.io/<repository-name>/
   ```

3. The report includes:
   - ✅ Combined results from all test jobs (smoke + regression)
   - ✅ Historical trends (up to 20 previous runs)
   - ✅ Interactive charts and statistics
   - ✅ Detailed test execution timeline

**Viewing Downloaded Allure Reports:**
```bash
# Option 1: Download complete allure-report artifact (recommended)
unzip allure-report.zip
cd allure-history
python3 -m http.server 8000
# Open http://localhost:8000 in browser

# Option 2: Download allure-results and generate locally
unzip allure-results-smoke.zip
allure serve allure-results/
```

**Combined Reports:**
Both HTML and Allure reports are generated with every test run:
```bash
# This is automatically run in CI:
uv run pytest tests/ \
  --alluredir=reports/allure-results \
  --html=reports/pytest-report.html \
  --self-contained-html
```

---

## 📝 Writing Tests

### Example Test:

```python
import re
import pytest
from playwright.sync_api import expect
from src.ui.pages.login.login_page import LoginPage
from src.config.protocols import ConfigService

@pytest.mark.smoke
def test_login(login_page: LoginPage, config_service: ConfigService):
    """Test successful login with valid credentials."""
    # The login_page fixture already navigates to the page
    login_page.login(config_service.username, config_service.password)

    # Verify successful login using Playwright's expect
    expect(login_page.page).to_have_url(re.compile(r"dashboard"), timeout=10000)

@pytest.mark.smoke
def test_login_chaining(login_page: LoginPage, config_service: ConfigService):
    """Test login using method chaining (fluent interface)."""
    login_page.enter_username(config_service.username)\
              .enter_password(config_service.password)\
              .click_login_button()

    expect(login_page.page).to_have_url(re.compile(r"dashboard"), timeout=10000)
```

### Create a New Page Object:

**Quick Example:**

```python
# Create page object: src/ui/pages/dashboard/dashboard_page.py
from playwright.sync_api import Page
from src.ui.pages.base_page import BasePage

class DashboardPage(BasePage):
    """Dashboard page implementation."""

    def __init__(self, page: Page, timeout: int = 10):
        super().__init__(page, timeout)

        # Define locators using Playwright functional locators
        self.page_title = page.get_by_role("heading", name="Dashboard")
        self.user_dropdown = page.get_by_role("button", name="user-dropdown")

    def get_page_title(self) -> str:
        """Get the page title text."""
        return self.get_text(self.page_title)

    def click_user_dropdown(self):
        """Click the user dropdown menu."""
        self.click(self.user_dropdown)
        return self  # Return self for method chaining

# Use in tests
def test_dashboard(dashboard_page):
    title = dashboard_page.get_page_title()
    expect(dashboard_page.page_title).to_contain_text("Dashboard")
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

### Base Page (src/ui/pages/base_page.py):
- ✅ Automatic waits (Playwright's auto-waiting)
- ✅ Reusable methods (click, send_keys, get_text, etc.)
- ✅ NavigationHeader component for global navigation
- ✅ Frame handling
- ✅ JavaScript execution
- ✅ Scroll to elements
- ✅ Visibility and presence verification
- ✅ Integrated logging in all actions
- ✅ Direct Playwright Locator support

### Configuration System:
- ✅ Dependency Injection via ConfigService protocol
- ✅ Environment-based configuration (.env)
- ✅ Strict validation - all variables required (no defaults)
- ✅ Type-safe configuration access
- ✅ Raises ConfigurationException for missing/invalid variables

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
@pytest.mark.smoke         # Quick smoke tests
@pytest.mark.regression    # Complete regression tests
@pytest.mark.login         # Login-specific tests
@pytest.mark.navigation    # Navigation tests
@pytest.mark.component     # Component tests
@pytest.mark.integration   # Integration tests
@pytest.mark.cross_module  # Cross-module navigation tests
@pytest.mark.performance   # Performance tests
@pytest.mark.leave         # Leave module tests
```

## 📊 Reports and Logs

Reports are automatically generated in:
- **Playwright HTML Report**: `playwright-report/` (run `playwright show-report`)
- **Screenshots**: `test-results/` (only on failures)
- **Videos**: `test-results/` (if enabled)
- **Traces**: `test-results/` (if enabled)
- **Allure Reports**: `reports/allure-results/`
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
from src.ui.pages.base_page import BasePage

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

### Design Principles Applied:

1. **Single Responsibility Principle (SRP)**:
   - Each page class has one responsibility
   - Components separated from pages (NavigationHeader)
   - Module-specific navigation in base classes (LeaveBasePage)

2. **Open/Closed Principle (OCP)**:
   - Add new pages without modifying existing code
   - Extend functionality through inheritance and composition

3. **Dependency Inversion Principle (DIP)**:
   - Depend on ConfigService protocol, not concrete implementation
   - Injected via fixtures, not imported directly

4. **YAGNI (You Aren't Gonna Need It)**:
   - Removed unnecessary abstractions (adapters, page-specific protocols)
   - Direct Playwright API usage (no wrappers)
   - Component composition over deep inheritance

### Recent Improvements:

The framework has undergone significant refactoring to improve simplicity and maintainability:

- **Architecture Simplification**: Removed dual Selenium/Playwright support (Playwright only)
- **Direct API Usage**: Eliminated adapter layer (direct Playwright API usage)
- **YAGNI Principle**: Removed page-specific protocols and unnecessary abstractions
- **Functional Locators**: Implemented Playwright's user-facing locators
- **Component Model**: Restructured to `src/ui/` with components and pages separation
- **Navigation System**: Global (NavigationHeader) and module-specific (LeaveBasePage) navigation

**Result**: 51% code reduction, simpler architecture, better maintainability

## 🤝 Contributing

1. **Follow the Page Object Model pattern** - Create pages in `src/ui/pages/`
2. **Use Playwright functional locators** - Prefer `get_by_role()`, `get_by_label()` over CSS/XPath
3. **Define locators inline** - No separate locator files (define in `__init__`)
4. **Use dependency injection** - Configuration via fixtures, not global imports
5. **Add appropriate test markers** - Use `@pytest.mark.smoke`, `@pytest.mark.regression`, etc.
6. **Return self for chaining** - Enable fluent interface pattern
7. **Use expect() for assertions** - Playwright's `expect()` with auto-waiting
8. **Document public methods** - Add docstrings explaining purpose and usage
9. **Run pre-commit hooks** - Ensure code quality before committing
10. **Component composition** - Reusable components (like NavigationHeader) over deep inheritance

## 📄 License

MIT
