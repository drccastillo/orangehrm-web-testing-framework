# Authentication Feature

## Overview

This feature handles all authentication-related functionality for OrangeHRM including:
- User login
- User logout
- Password reset
- Session management

## Structure

```
authentication/
├── pages/              # Page Objects
│   ├── login_page.py   # Login page object
│   └── locators.py     # Page locators
├── tests/              # Test cases
│   ├── conftest.py     # Feature-specific fixtures
│   └── test_login.py   # Login tests
└── data/               # Test data
    └── credentials.py  # User credentials
```

## Running Tests

```bash
# Run all authentication tests
uv run pytest orangehrm/authentication/ -v

# Run only smoke tests
uv run pytest orangehrm/authentication/ -m smoke

# Run specific test file
uv run pytest orangehrm/authentication/tests/test_login.py

# Run with specific browser
uv run pytest orangehrm/authentication/ --browser=firefox

# Run headless
uv run pytest orangehrm/authentication/ --headless
```

## Usage Examples

### Using Login Page

```python
from orangehrm.authentication import LoginPage, valid_admin_user
from framework.config import Config

def test_example(driver):
    # Create login page
    login_page = LoginPage(driver)
    login_page.navigate_to(Config.BASE_URL)

    # Get valid user
    user = valid_admin_user()

    # Login
    login_page.login(user.username, user.password)

    # Verify
    assert "dashboard" in login_page.get_current_url()
```

### Using Quick Login (Workflow)

```python
from shared.workflows import quick_login

def test_example(driver):
    # Quick login without page objects
    quick_login(driver)

    # Continue with test...
```

## Test Data

Available test data functions in `data/credentials.py`:

- `valid_admin_user()` - Valid admin credentials
- `invalid_user()` - Invalid credentials
- `valid_login_credentials()` - Valid LoginCredentials object
- `empty_username_credentials()` - Empty username scenario
- `empty_password_credentials()` - Empty password scenario

## Adding New Tests

1. Create test file in `tests/` directory
2. Use `login_page` fixture (from `tests/conftest.py`)
3. Add appropriate markers (`@pytest.mark.authentication`, `@pytest.mark.smoke`, etc.)
4. Document test cases with docstrings

Example:

```python
import pytest
from orangehrm.authentication.pages import LoginPage

@pytest.mark.authentication
@pytest.mark.regression
def test_new_scenario(login_page: LoginPage):
    """
    Test description here.

    Given: ...
    When: ...
    Then: ...
    """
    # Test implementation
    pass
```

## Dependencies

This feature depends on:
- **framework/**: `BasePage`, `Config`, `DriverFactory`
- **shared/**: `OrangeHRMNavigation` (for verification)
