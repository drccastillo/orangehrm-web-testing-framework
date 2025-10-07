# OrangeHRM Test Automation Framework

**Modern test automation framework for OrangeHRM using Screaming Architecture principles.**

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Pytest](https://img.shields.io/badge/pytest-8.0%2B-green.svg)](https://pytest.org)
[![Selenium](https://img.shields.io/badge/selenium-4.35%2B-yellow.svg)](https://selenium.dev)

---

## 🎯 Architecture

This project uses **Screaming Architecture** where the structure "screams" what the system does:

```
orangehrm/                  # ← Features (what the system tests)
├── authentication/         # ← Authentication feature
├── employees/              # ← Employee management (future)
└── leave/                  # ← Leave management (future)

framework/                  # ← Generic infrastructure
shared/                     # ← OrangeHRM shared components
```

**See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.**

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
│   ├── page/               # Base page classes
│   │   └── unittests/      # Unit tests
│   ├── data/               # Data factories
│   │   └── unittests/      # Unit tests
│   ├── config/             # Configuration
│   │   └── unittests/      # Unit tests (12 tests)
│   └── utils/              # Logger, exceptions
│       └── unittests/      # Unit tests (32 tests)
│
├── shared/                 # 🔄 SHARED (OrangeHRM-specific)
│   ├── components/         # UI components (navigation)
│   ├── locators/           # Shared locators
│   └── workflows/          # Common actions (quick_login)
│       └── unittests/      # Unit tests (12 tests)
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
from orangehrm.authentication.pages import LoginPage
from orangehrm.authentication.data import valid_admin_user

@pytest.mark.authentication
@pytest.mark.smoke
def test_login(login_page: LoginPage):
    """Test successful login."""
    user = valid_admin_user()

    login_page.login(user.username, user.password)

    assert "dashboard" in login_page.get_current_url()
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

### Using Shared Components
```python
from shared.components import OrangeHRMNavigation
from shared.workflows import quick_login

def test_navigation(driver):
    quick_login(driver)

    nav = OrangeHRMNavigation(driver)
    nav.navigate_to_pim()
```

---

## 🏗️ Design Patterns

- **Screaming Architecture**: Structure shows features, not tools
- **Factory Pattern**: `DriverFactory` for browser creation
- **Strategy Pattern**: `BrowserStrategy` for different browsers
- **Builder Pattern**: `UserDataBuilder` for test data
- **Repository Pattern**: `TestDataRepository` for data management
- **Page Object Model**: Encapsulate page logic
- **Co-located Tests**: Unit tests next to code they test

**See [IMPROVEMENTS.md](IMPROVEMENTS.md) for details.**

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

✅ **Screaming Architecture** - Clear feature organization
✅ **Unit Tests Co-located** - Tests next to code (56 tests)
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

### Architecture & Guides
- [ARCHITECTURE.md](ARCHITECTURE.md) - Complete architecture documentation
- [QUICK_START.md](QUICK_START.md) - 5-minute getting started guide
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) - Migration from old structure
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Implementation details

### Testing & Quality
- [UNIT_TESTS_GUIDE.md](UNIT_TESTS_GUIDE.md) - Unit testing comprehensive guide
- [UNIT_TESTS_MIGRATION_COMPLETE.md](UNIT_TESTS_MIGRATION_COMPLETE.md) - Unit tests migration summary
- [LOGS_AND_REPORTS.md](LOGS_AND_REPORTS.md) - Logs and reports documentation

### Design & CI/CD
- [IMPROVEMENTS.md](IMPROVEMENTS.md) - Design patterns & CI/CD
- [CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md) - Cleanup actions performed

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
- Workflows tests: 12 tests in `shared/workflows/unittests/`

### E2E Tests Breakdown
- Login tests: 8 tests in `orangehrm/authentication/tests/test_login.py`

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
- ✅ Put feature code in `orangehrm/[feature]/`
- ✅ Generic code goes in `framework/`
- ✅ Shared OrangeHRM code goes in `shared/`
- ✅ Unit tests next to code they test
- ✅ Add appropriate pytest markers
- ✅ Document in README files

---

## 📄 License

MIT

---

**Built with ❤️ using Screaming Architecture principles**
