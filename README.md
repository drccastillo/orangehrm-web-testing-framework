# OrangeHRM Test Automation Framework

**Modern test automation framework for OrangeHRM using Screaming Architecture principles.**

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Pytest](https://img.shields.io/badge/pytest-8.0%2B-green.svg)](https://pytest.org)
[![Selenium](https://img.shields.io/badge/selenium-4.35%2B-yellow.svg)](https://selenium.dev)

---

## 🎯 Architecture

### Modern Clean Architecture (Oct 2024)

**Key Principles**:
- ✅ **NO BasePage** - Complete removal of inheritance hierarchy
- ✅ **Mixins Pattern** - Interface Segregation Principle (ISP)
- ✅ **Composition over Inheritance** - Flexible component-based design
- ✅ **Chain of Responsibility** - Wait strategies with fallback chains
- ✅ **Dependency Injection** - ConfigInterface for testability

### Screaming Architecture

Structure "screams" what the system does:

```
orangehrm/                  # ← Features (what the system tests)
├── authentication/         # ← Authentication feature
│   ├── pages/              # ← Page objects (Mixins)
│   ├── tests/              # ← E2E & unit tests
│   └── data/               # ← Test data
├── dashboard/              # ← Dashboard feature
└── [future features]/      # ← Employee, Leave, Time, etc.

framework/                  # ← Generic infrastructure
├── page/
│   ├── components/         # ← ElementFinder, Interactor, Validator
│   ├── mixins/             # ← Mixins for pages
│   └── strategies/         # ← Wait strategies
├── config/                 # ← ConfigInterface, MockConfig
└── utils/                  # ← Logger, exceptions

shared/                     # ← OrangeHRM shared components
└── components/             # ← OrangeHRMNavigation
```
---

## 🚀 Quick Start

### 1. Install UV
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Dependencies
```bash
uv sync
```

### 3. Start Selenium Grid
```bash
docker-compose up -d
```

### 4. Run Tests
```bash
# All authentication tests
uv run pytest orangehrm/authentication/ -v

# Smoke tests only
uv run pytest -m smoke

# Specific browser
uv run pytest --browser=firefox

# Unit tests only (fast, no browser)
uv run pytest -m unit
```

---

## 📁 Project Structure

```
web-testing-framework/
│
├── orangehrm/              # 🎯 DOMAIN - Features
│   └── authentication/     # Authentication feature
│       ├── pages/          # Page objects
│       ├── tests/          # E2E & unit tests
│       ├── data/           # Test data
│       └── README.md       # Feature docs
│
├── framework/              # 🏗️ INFRASTRUCTURE (Generic)
│   ├── browser/            # WebDriver management
│   │   └── unittests/      # Unit tests
│   ├── page/               # Page components & mixins
│   │   ├── components/     # ElementFinder, Interactor, Validator
│   │   ├── mixins/         # ElementFinderMixin, InteractorMixin, etc.
│   │   ├── strategies/     # Wait strategies (Chain of Responsibility)
│   │   └── unittests/      # Unit tests
│   ├── data/               # Data factories
│   │   └── unittests/      # Unit tests
│   ├── config/             # Configuration (ConfigInterface, MockConfig)
│   │   └── unittests/      # Unit tests (12 tests)
│   └── utils/              # Logger, exceptions
│       └── unittests/      # Unit tests (32 tests)
│
├── shared/                 # 🔄 SHARED (OrangeHRM-specific)
│   └── components/         # UI components (OrangeHRMNavigation)
│       └── tests/          # Component unit tests (19 tests)
│
├── integration/            # 🔗 Integration tests
│
├── logs/                   # 📝 Runtime: Execution logs
│   ├── test_automation_YYYYMMDD.log
│   └── pytest.log
│
├── reports/                # 📊 Runtime: Test reports
│   ├── report.html         # HTML test report
│   └── screenshots/        # Failure screenshots
│
├── conftest.py             # Global pytest config
├── pytest.ini              # Pytest settings
└── pyproject.toml          # Dependencies (UV)
```

**Key Principle**: Unit tests live next to the code they test (`framework/*/unittests/`)

---

## 🧪 Running Tests

### By Test Type
```bash
# Unit tests (fast, no browser) - 56 tests
uv run pytest -m unit -v

# E2E tests (browser required)
uv run pytest -m authentication -v

# All tests
uv run pytest
```

### By Feature
```bash
uv run pytest orangehrm/authentication/
uv run pytest orangehrm/employees/
```

### By Marker
```bash
uv run pytest -m smoke              # Smoke tests
uv run pytest -m authentication     # Auth tests
uv run pytest -m "smoke and authentication"
```

### By Browser
```bash
uv run pytest --browser=chrome      # Chrome
uv run pytest --browser=firefox     # Firefox
uv run pytest --browser=edge        # Edge
uv run pytest --headless            # Headless mode
```

### Parallel Execution
```bash
uv run pytest -n auto               # Auto workers
uv run pytest -n 4                  # 4 workers
```

---

## 📝 Writing Tests

### E2E Test Example
```python
import pytest

@pytest.mark.authentication
@pytest.mark.smoke
def test_login(login_page, valid_user):
    """Test successful login using fixtures."""
    login_page.login(valid_user.username, valid_user.password)
    assert "dashboard" in login_page.get_current_url()

@pytest.mark.dashboard
def test_dashboard_navigation(dashboard_page):
    """Test dashboard using authenticated_session fixture."""
    # dashboard_page already authenticated via authenticated_session
    assert dashboard_page.is_dashboard_loaded()
```

### Unit Test Example
```python
import pytest
import unittest
from framework.config.settings import Config

@pytest.mark.unit
class TestConfig(unittest.TestCase):
    def test_config_has_base_url(self):
        """Test that Config has BASE_URL attribute."""
        self.assertTrue(hasattr(Config, 'BASE_URL'))
        self.assertIsInstance(Config.BASE_URL, str)
```

### Creating Page Objects with Mixins
```python
from framework.page.mixins import (
    ElementFinderMixin,
    ElementInteractorMixin,
    ElementValidatorMixin
)
from framework.page.components import (
    ElementFinder,
    ElementInteractor,
    ElementValidator
)

class DashboardPage(
    ElementFinderMixin,
    ElementInteractorMixin,
    ElementValidatorMixin
):
    """Dashboard page using Mixins pattern (NO BasePage)."""

    WELCOME_TEXT = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb")

    def __init__(self, driver, timeout=10, config=None):
        self.driver = driver
        self.timeout = timeout
        self.config = config or Config()

        # Initialize components (Composition)
        self.finder = ElementFinder(driver, timeout)
        self.interactor = ElementInteractor(driver, timeout)
        self.validator = ElementValidator(driver, timeout)

    def get_welcome_message(self) -> str:
        """Get welcome text using mixin methods."""
        return self.get_text(self.WELCOME_TEXT)
```

### Using Shared Components
```python
from shared.components.navigation import OrangeHRMNavigation

def test_navigation(authenticated_session, config_provider):
    """Test navigation using authenticated_session fixture."""
    nav = OrangeHRMNavigation(authenticated_session, config=config_provider)
    nav.navigate_to_module('pim')  # Dynamic navigation
    nav.logout()
```

---

## 🏗️ Design Patterns & Architecture

**Modern Clean Architecture** (Completed Oct 2024):
- ✅ **NO BasePage** - Completely removed inheritance hierarchy
- ✅ **Mixins Pattern** - Pages use only capabilities they need (ISP)
- ✅ **Composition over Inheritance** - Components instead of rigid inheritance
- ✅ **Chain of Responsibility** - Wait strategies with fallback chains
- ✅ **Dependency Injection** - ConfigInterface for flexible configuration

**Core Patterns**:
- **Screaming Architecture**: Structure shows features, not tools
- **Factory Pattern**: `DriverFactory` for browser creation
- **Strategy Pattern**: Wait strategies (`VisibilityWaitStrategy`, `ClickableWaitStrategy`, etc.)
- **Builder Pattern**: `UserDataBuilder` for test data
- **Repository Pattern**: `TestDataRepository` for data management
- **Page Object Model**: Mixins + Composition (no inheritance)
- **Co-located Tests**: Unit tests next to code they test


---

## 🧩 Fixtures

### Root Conftest (Shared Fixtures)

Located in [conftest.py](conftest.py):

- `driver` - WebDriver connected to Selenium Grid
- `config_provider` - ConfigInterface instance for dependency injection
- `authenticated_session` - Pre-authenticated WebDriver (performs login)
- `logout_session` - Authenticated session with auto-logout after test

### Feature Conftest (Feature-Specific Fixtures)

Each feature has its own conftest with specialized fixtures:

**Authentication** ([orangehrm/authentication/tests/conftest.py](orangehrm/authentication/tests/conftest.py)):
- `login_page` - LoginPage instance with navigation to login URL
- `valid_user` - Valid user data from config
- `invalid_user_data` - Invalid user data for negative tests
- `login_page_demo` - LoginPage with visual debugging

**Dashboard** ([orangehrm/dashboard/tests/conftest.py](orangehrm/dashboard/tests/conftest.py)):
- `dashboard_page` - DashboardPage using `authenticated_session`

### Fixture Usage Example

```python
def test_login(login_page, valid_user):
    """Uses feature-specific fixtures."""
    login_page.login(valid_user.username, valid_user.password)
    assert "dashboard" in login_page.get_current_url()

def test_dashboard(dashboard_page):
    """Uses authenticated_session via dashboard_page fixture."""
    assert dashboard_page.is_dashboard_loaded()

def test_with_logout(logout_session, config_provider):
    """Session automatically logs out after test."""
    nav = OrangeHRMNavigation(logout_session, config=config_provider)
    nav.navigate_to_module('admin')
    # Automatic logout happens in fixture teardown
```

---

## 🔧 Configuration

### Environment Variables (.env)
```env
URL=http://localhost:8080/web/index.php
ORANGEHRM_USERNAME=Admin
ORANGEHRM_PASSWORD=admin123
SELENIUM_GRID_URL=http://localhost:4444
BROWSER=chrome
HEADLESS=False
```

### Selenium Grid
```bash
# Start
docker-compose up -d

# Status
docker-compose ps

# Logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 📊 Reports & Logs

### HTML Reports
```bash
uv run pytest --html=reports/report.html
```

### Locations (Runtime Artifacts)
```
logs/                       # Execution logs (NOT versioned)
├── test_automation_20251006.log
└── pytest.log

reports/                    # Test reports (NOT versioned)
├── report.html
└── screenshots/
    └── test_failed_*.png
```

**See [LOGS_AND_REPORTS.md](LOGS_AND_REPORTS.md) for detailed documentation.**

---

## 🎯 Key Features

✅ **Modern Clean Architecture** - Mixins + Composition (NO BasePage)
✅ **Screaming Architecture** - Clear feature organization
✅ **Chain of Responsibility** - Flexible wait strategies
✅ **SOLID Principles** - All 5 principles implemented
✅ **Dependency Injection** - ConfigInterface for testability
✅ **Unit Tests Co-located** - Tests next to code (56+ tests)
✅ **High Cohesion** - Related code together
✅ **Low Coupling** - Independent features
✅ **Selenium Grid** - Multi-browser testing
✅ **Parallel Execution** - Fast test runs
✅ **HTML Reports** - Beautiful test reports
✅ **Auto Screenshots** - Capture failures
✅ **Comprehensive Logging** - Debug easily
✅ **Type Safety** - MyPy support
✅ **CI/CD Ready** - GitHub Actions workflows

---

## 📚 Documentation

### Features
- [orangehrm/authentication/README.md](orangehrm/authentication/README.md) - Authentication feature

---

## 🧪 Test Statistics

| Test Type | Count | Location | Speed |
|-----------|-------|----------|-------|
| **Unit Tests** | 56 | `framework/*/unittests/`, `shared/*/unittests/` | < 0.1s |
| **E2E Tests** | 8 | `orangehrm/*/tests/` | ~5-10s each |
| **Total** | 64 | - | - |

### Unit Tests Breakdown
- Config tests: 12 tests in `framework/config/unittests/`
- Logger tests: 13 tests in `framework/utils/unittests/`
- Exception tests: 19 tests in `framework/utils/unittests/`
- Navigation tests: 19 tests in `shared/components/tests/`
- Wait strategy tests: Multiple tests in `framework/page/strategies/unittests/`

### E2E Tests Breakdown
- Authentication tests: 8 tests in `orangehrm/authentication/tests/`
- Dashboard tests: Multiple tests in `orangehrm/dashboard/tests/`

---

## 🔮 Future Features

Planned features following the same clean structure:
- `orangehrm/employees/` - Employee management
- `orangehrm/leave/` - Leave management
- `orangehrm/time/` - Time tracking
- `orangehrm/recruitment/` - Recruitment
- `orangehrm/performance/` - Performance reviews

---

## 🛠️ Development

### Linting
```bash
uv run black orangehrm/ framework/ shared/
uv run ruff check orangehrm/ framework/ shared/
uv run mypy orangehrm/ framework/ shared/
```

### Unit Tests
```bash
# Run all unit tests
uv run pytest -m unit -v

# Run specific module tests
uv run pytest framework/config/unittests/ -v
uv run pytest framework/utils/unittests/test_logger.py -v

# With coverage
uv run pytest -m unit --cov=framework --cov-report=html
```

### E2E Tests
```bash
# Run all E2E tests
uv run pytest orangehrm/ -v

# Run specific feature
uv run pytest orangehrm/authentication/ -v
```

---

## 🤝 Contributing

### Adding New Features
1. Create feature directory: `orangehrm/[feature]/`
2. Follow structure:
   ```
   orangehrm/[feature]/
   ├── pages/          # Page objects
   ├── tests/          # E2E & unit tests
   ├── data/           # Test data
   └── README.md       # Feature docs
   ```
3. Add pytest markers in `pytest.ini`
4. Document in feature README

### Adding Framework Components
1. Add code in `framework/[module]/`
2. Add unit tests in `framework/[module]/unittests/`
3. Mark tests with `@pytest.mark.unit`
4. Ensure tests are fast (< 1s)

### Guidelines
- ✅ Follow Screaming Architecture principles
- ✅ Use Mixins pattern (NO BasePage inheritance)
- ✅ Use Composition (initialize components in `__init__`)
- ✅ Inject ConfigInterface for testability
- ✅ Use wait strategies (Chain of Responsibility)
- ✅ Put feature code in `orangehrm/[feature]/`
- ✅ Generic code goes in `framework/`
- ✅ Shared OrangeHRM code goes in `shared/`
- ✅ Unit tests next to code they test
- ✅ Add appropriate pytest markers
- ✅ Document in README files
- ✅ Use fixtures: `authenticated_session`, `logout_session`, `config_provider`

---

## 📄 License

MIT

---

**Built with ❤️ using Screaming Architecture principles**
