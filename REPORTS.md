# 📊 Test Reports Guide

This framework generates multiple report formats to provide comprehensive test execution insights.

## 🎯 Available Report Formats

### 1. **HTML Report** (pytest-html)
- **Location**: `reports/report.html`
- **Format**: Single self-contained HTML file
- **Features**:
  - Test results summary
  - Duration statistics
  - Screenshots on failure
  - Browser/environment info

### 2. **HTML Reporter** (pytest-html-reporter)
- **Location**: `reports/html-report.html`
- **Format**: Enhanced HTML with better styling
- **Features**:
  - Modern UI design
  - Test case details
  - Execution timeline
  - Pass/Fail statistics

### 3. **Excel Report** (pytest-excel)
- **Location**: `reports/report.xlsx`
- **Format**: Microsoft Excel spreadsheet
- **Features**:
  - Tabular test results
  - Easy filtering/sorting
  - Can be shared with non-technical stakeholders
  - Import into other tools

### 4. **Allure Report** (allure-pytest) ⭐ **RECOMMENDED**
- **Results Location**: `reports/allure-results/`
- **Report Location**: `reports/allure-report/`
- **Format**: Interactive web application
- **Features**:
  - Beautiful, interactive dashboards
  - Test execution trends
  - Historical data analysis
  - Screenshots, logs, attachments
  - Test categorization (Features, Stories, Severity)
  - Tags and filters
  - Test step details
  - Retry information
  - Environment info

---

## 🚀 Quick Start

### Running Tests with All Reports

```bash
# Run all tests (generates all report formats automatically)
uv run pytest

# Run specific marker
uv run pytest -m smoke

# Run specific test file
uv run pytest orangehrm/authentication/tests/test_login.py

# Run with specific browser
uv run pytest --browser=firefox

# Run in parallel
uv run pytest -n auto
```

All reports are generated automatically in the `reports/` directory.

---

## 📖 Viewing Reports

### HTML Reports (Basic)

```bash
# Open HTML report in browser
open reports/report.html           # macOS
xdg-open reports/report.html       # Linux
start reports/report.html          # Windows

# Or HTML Reporter
open reports/html-report.html
```

### Excel Report

```bash
# Open Excel report
open reports/report.xlsx           # macOS
xdg-open reports/report.xlsx       # Linux
start reports/report.xlsx          # Windows
```

### Allure Report (Interactive)

#### Option 1: Serve Report (Temporary Server)
```bash
# Start Allure server and view report in browser
allure serve reports/allure-results

# This will:
# 1. Generate the report
# 2. Start a local web server
# 3. Open browser automatically
# 4. Server runs until you press Ctrl+C
```

#### Option 2: Generate Static Report
```bash
# Generate static Allure report
allure generate reports/allure-results -o reports/allure-report --clean

# Open the report
open reports/allure-report/index.html      # macOS
xdg-open reports/allure-report/index.html  # Linux
start reports/allure-report/index.html     # Windows
```

---

## 🔧 Installing Allure CLI

Allure CLI is required to view Allure reports.

### macOS
```bash
brew install allure
```

### Linux (Debian/Ubuntu)
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

### Linux (Manual)
```bash
# Download and extract
wget https://github.com/allure-framework/allure2/releases/latest/download/allure-2.XX.X.zip
unzip allure-2.XX.X.zip -d /opt/
sudo ln -s /opt/allure-2.XX.X/bin/allure /usr/bin/allure

# Verify installation
allure --version
```

### Windows (Scoop)
```bash
scoop install allure
```

### Windows (Manual)
1. Download from: https://github.com/allure-framework/allure2/releases
2. Extract to `C:\allure`
3. Add `C:\allure\bin` to PATH

---

## 📂 Report Directory Structure

```
reports/
├── allure-results/          # Raw Allure test results (JSON)
│   ├── *-result.json
│   ├── *-container.json
│   └── *-attachment.*
├── allure-report/           # Generated Allure HTML report
│   ├── index.html
│   ├── data/
│   ├── export/
│   └── history/
├── screenshots/             # Failure screenshots
│   ├── test_name_*.png
│   └── test_name_*.txt      # Screenshot metadata
├── report.html              # pytest-html report
├── html-report.html         # pytest-html-reporter
└── report.xlsx              # Excel report
```

---

## 🎨 Allure Report Features

### Features & Stories
Tests are organized by business features and user stories:

```python
@allure.feature("Authentication")
@allure.story("Login Success")
class TestLoginSuccess:
    pass
```

### Severity Levels
Tests are prioritized by severity:

- **BLOCKER** - Blocks entire application
- **CRITICAL** - Critical functionality (e.g., login, payments)
- **NORMAL** - Standard functionality
- **MINOR** - Minor issues
- **TRIVIAL** - UI/cosmetic issues

```python
@allure.severity(allure.severity_level.CRITICAL)
def test_login():
    pass
```

### Tags
Filter and group tests by custom tags:

```python
@allure.tag("smoke", "positive", "authentication")
def test_valid_login():
    pass
```

### Test Steps
Detailed test execution steps:

```python
@allure.step("Login with username: {username}")
def login(username, password):
    # Steps are automatically reported
    pass
```

### Attachments
Screenshots, logs, and data attached to tests:

```python
allure.attach(screenshot, "Screenshot", allure.attachment_type.PNG)
allure.attach(response_json, "API Response", allure.attachment_type.JSON)
allure.attach(current_url, "Current URL", allure.attachment_type.TEXT)
```

---

## 📊 Report Comparison

| Feature | HTML | HTML Reporter | Excel | Allure |
|---------|------|---------------|-------|--------|
| **Interactive** | ❌ | ❌ | ⚠️ | ✅ |
| **Screenshots** | ✅ | ✅ | ❌ | ✅ |
| **Test Steps** | ❌ | ❌ | ❌ | ✅ |
| **Trends** | ❌ | ❌ | ❌ | ✅ |
| **History** | ❌ | ❌ | ❌ | ✅ |
| **Categorization** | ⚠️ | ⚠️ | ⚠️ | ✅ |
| **Filtering** | ⚠️ | ⚠️ | ✅ | ✅ |
| **Export** | ❌ | ❌ | ✅ | ✅ |
| **CI/CD Friendly** | ✅ | ✅ | ✅ | ✅ |
| **Stakeholder Friendly** | ⚠️ | ✅ | ✅ | ✅ |
| **Setup Complexity** | Low | Low | Low | Medium |

**Legend**: ✅ Full Support | ⚠️ Partial Support | ❌ Not Supported

---

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
- name: Run Tests
  run: uv run pytest

- name: Generate Allure Report
  if: always()
  run: allure generate reports/allure-results -o reports/allure-report

- name: Upload Allure Report
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: allure-report
    path: reports/allure-report/

- name: Upload Screenshots
  if: failure()
  uses: actions/upload-artifact@v3
  with:
    name: failure-screenshots
    path: reports/screenshots/
```

### Jenkins Example

```groovy
stage('Run Tests') {
    steps {
        sh 'uv run pytest'
    }
    post {
        always {
            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'reports/allure-results']]
            ])
        }
    }
}
```

---

## 🐛 Troubleshooting

### "Command not found: allure"
**Solution**: Install Allure CLI (see Installation section above)

### Empty Allure Report
**Solution**:
```bash
# Ensure allure-results directory exists and has files
ls -la reports/allure-results/

# Re-run tests to generate results
uv run pytest
```

### Port Already in Use (allure serve)
**Solution**:
```bash
# Specify custom port
allure serve reports/allure-results -p 8080
```

### Reports not generated
**Solution**:
```bash
# Check pytest output for errors
uv run pytest -v

# Ensure report directories exist
mkdir -p reports/allure-results reports/screenshots
```

---

## 📝 Best Practices

1. **Always use Allure** for detailed analysis and presentation
2. **Use Excel reports** for sharing with non-technical stakeholders
3. **Keep HTML reports** as backup/quick reference
4. **Commit `allure-results/`** to track test history
5. **Clean old reports** regularly to save disk space:
   ```bash
   rm -rf reports/allure-results/* reports/allure-report/*
   ```
6. **Review reports after each run** to identify flaky tests
7. **Use severity levels** to prioritize bug fixes
8. **Tag tests properly** for better filtering and organization

---

## 📚 Additional Resources

- **Allure Documentation**: https://docs.qameta.io/allure/
- **pytest-html**: https://pytest-html.readthedocs.io/
- **pytest-excel**: https://pypi.org/project/pytest-excel/
- **Allure Examples**: https://demo.qameta.io/allure/

---

## 🆘 Need Help?

If you encounter issues with reports:

1. Check logs: `tail -f logs/test_automation_*.log`
2. Verify dependencies: `uv sync`
3. Validate configuration: Check `pyproject.toml` addopts
4. Clear cache: `rm -rf .pytest_cache reports/*`
5. Re-run tests: `uv run pytest -v`

For Allure-specific issues, run:
```bash
allure --version
allure serve --help
```
