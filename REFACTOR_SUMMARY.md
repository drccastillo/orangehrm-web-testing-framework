# Refactor Plan - Executive Summary

## Critical Code Smells Identified

### 🔴 **Priority 1: Code Duplication (90%)**
- **Location:** `BasePage` vs `BasePagePW`, `LoginPage` vs `LoginPagePW`
- **Impact:** Every change requires updating 2 files
- **Solution:** Unified architecture with Adapter Pattern (Phase 3)
- **Expected Reduction:** 70-90% less code

### 🔴 **Priority 1: God Class Anti-Pattern**
- **Location:** `BasePage` and `BasePagePW` (30+ methods each)
- **Violations:** Single Responsibility Principle
- **Responsibilities:** Interaction + Waiting + Validation + Debugging + JavaScript execution
- **Solution:** Extract `ElementHighlighter` class (Phase 1.3)
- **Expected Improvement:** <20 methods per class

### 🟡 **Priority 2: Unjustified Singleton**
- **Location:** `Config` class
- **Issue:** Global state, hard to test, tight coupling
- **Solution:** Dependency Injection with `ConfigService` protocol (Phase 1.1)
- **Benefits:** Testability, flexibility, no global state

### 🟡 **Priority 2: Primitive Obsession**
- **Location:** Locators as `(By.ID, "username")` or `"#username"`
- **Issue:** No behavior, no validation, framework-specific
- **Solution:** `Locator` value objects (Phase 2.1)
- **Benefits:** Self-documenting, validated, framework-agnostic

### 🟢 **Priority 3: Property Pollution**
- **Location:** `LoginPage` - 7 properties wrapping locators
- **Issue:** Unnecessary indirection, feature envy
- **Solution:** Remove properties, direct locator access (Phase 1.2)
- **Benefits:** Less boilerplate, clearer intent

---

## Design Pattern Applications

### ✅ **Already Implemented (Good!)**
1. **Page Object Model** - Encapsulates page behavior
2. **Base Page Pattern** - Common functionality in base class
3. **Method Chaining** - Fluent interface for actions
4. **Custom Exceptions** - Well-defined error hierarchy

### 🔧 **To Implement - Justified by Problems**

#### **Adapter Pattern** (Phase 3) - Solves Duplication
```
Problem: 90% duplication between Selenium and Playwright
Solution: BrowserProtocol + SeleniumAdapter + PlaywrightAdapter
Benefit: Single codebase works with both frameworks
```

#### **Strategy Pattern** (Phase 4.1) - Solves Switch Statements
```
Problem: if/elif chains for browser configuration
Solution: BrowserOptionsStrategy with Chrome/Firefox/Edge strategies
Benefit: Open/Closed principle, easy to add browsers
```

#### **Builder Pattern** (Phase 4.2) - Solves Long Parameter Lists
```
Problem: Page objects with many optional parameters
Solution: PageBuilder with fluent API
Benefit: Readable, flexible construction (use only when needed)
```

#### **Template Method** (Phase 4.3) - Solves Test Duplication
```
Problem: Repeated test structure across many tests
Solution: LoginTestTemplate with abstract hooks
Benefit: DRY tests, consistent structure (use selectively)
```

#### **Decorator Pattern** (Phase 4.4) - Solves Cross-Cutting Concerns
```
Problem: Need retry/logging without modifying methods
Solution: @retry, @screenshot_on_error decorators
Benefit: Composable behavior, Open/Closed principle
```

---

## Refactor Phases

### **Phase 1: Foundation (Weeks 1-2)**
- Remove Singleton (Config → ConfigService)
- Remove property pollution
- Extract ElementHighlighter (God Class → SRP)
- Consolidate constants
- **Risk:** Low | **Tests:** Must pass

### **Phase 2: Abstractions (Weeks 3-4)**
- Locator value objects (Primitive Obsession → Rich Domain)
- WebElement protocol (Tight Coupling → Loose Coupling)
- PageObject protocol (No Contract → Explicit Contract)
- **Risk:** Medium | **Tests:** Must pass

### **Phase 3: Unification (Weeks 5-6)**
- Unified BrowserProtocol with adapters
- Single BasePage (remove duplication)
- Single page objects (LoginPage, not LoginPage + LoginPagePW)
- **Risk:** High | **Impact:** Massive reduction in code
- **Tests:** Must pass with both `--framework=selenium` and `--framework=playwright`

### **Phase 4: Patterns (Weeks 7-8)**
- Strategy for browser options
- Builder for complex pages (optional)
- Template Method for tests (optional)
- Decorators for retry/logging
- **Risk:** Low | **Apply only when justified**

### **Phase 5: Advanced (Optional, Weeks 9-10)**
- Repository pattern for page management (20+ pages)
- Screenplay pattern (alternative architecture for complex flows)
- **Apply only if needed** (YAGNI)

---

## Before/After Comparison

### **Before (Current State)**

```python
# Two separate files: 90% duplication
# src/pages_selenium/login_page.py
class LoginPage(BasePage):
    def __init__(self, driver: WebDriver, timeout: int = 10):
        super().__init__(driver, timeout)
        self.locators = LoginLocators

    @property
    def USERNAME_INPUT(self):  # Property pollution
        return self.locators.USERNAME_INPUT

    def enter_username(self, username: str):
        self.send_keys(self.USERNAME_INPUT, username)

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

# src/pages_playwright/login_page_pw.py
class LoginPagePW(BasePagePW):  # DUPLICATE!
    def __init__(self, page: Page, timeout: int = 10):
        super().__init__(page, timeout)
        self.locators = LoginLocatorsPW

    def enter_username(self, username: str):
        self.fill(self.locators.USERNAME_INPUT, username)

    def login(self, username, password):  # DUPLICATE!
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

# In tests - tight coupling to Config
login_page.login(Config.USERNAME, Config.PASSWORD)
```

### **After (Target State)**

```python
# Single file: unified architecture
# src/pages/login_page.py
class LoginPage(BasePage):
    """Works with ANY framework via BrowserProtocol."""

    def __init__(self, browser: BrowserProtocol, timeout: int = 10):
        super().__init__(browser, timeout)
        self.locators = LoginLocators  # Framework-agnostic Locator objects

    def enter_username(self, username: str) -> "LoginPage":
        self.send_keys(self.locators.USERNAME, username)
        return self

    def login(self, username: str, password: str) -> None:
        """Perform complete login."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

# Single locators file - framework-agnostic
# src/pages/locators/login_locators.py
class LoginLocators:
    USERNAME = Locator(LocatorStrategy.NAME, "username", "Username field")
    PASSWORD = Locator(LocatorStrategy.NAME, "password", "Password field")
    LOGIN_BUTTON = Locator(LocatorStrategy.CSS, "button[type='submit']")

# In tests - dependency injection
def test_login(login_page: LoginPageProtocol, config: ConfigService):
    login_page.login(config.username, config.password)
    assert "dashboard" in login_page.get_current_url()

# Run with any framework:
# pytest --framework=selenium
# pytest --framework=playwright
```

---

## Success Metrics

### **Quantitative Goals**
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Code duplication | 90% | <15% | **75% reduction** |
| Lines of code | ~5000 | ~3000 | **40% reduction** |
| Cyclomatic complexity | ~10 avg | <5 avg | **50% reduction** |
| Number of page classes | 20+ (10 Selenium + 10 Playwright) | 10 (unified) | **50% reduction** |
| BasePage methods | 30+ | <20 | **33% reduction** |

### **Qualitative Goals**
- ✅ **Maintainability:** Update one file, affects all frameworks
- ✅ **Extensibility:** Add new framework in <1 day (just implement adapter)
- ✅ **Testability:** Mock config, browser, any component
- ✅ **Readability:** Self-documenting code with protocols and value objects
- ✅ **Stability:** Zero regression (tests guarantee)

---

## Acceptance Criteria (Per Phase)

### **Every Phase Must Satisfy:**
1. ✅ All existing tests pass
2. ✅ No new code smells introduced
3. ✅ Cyclomatic complexity reduced or stable
4. ✅ Code coverage maintained or improved
5. ✅ Documentation updated
6. ✅ Team review and approval

### **Phase 3 Specific (Critical):**
1. ✅ Tests run with `pytest --framework=selenium`
2. ✅ Tests run with `pytest --framework=playwright`
3. ✅ Single BasePage replaces both versions
4. ✅ Single LoginPage replaces both versions
5. ✅ 70%+ reduction in duplicate code
6. ✅ Zero functional regression

---

## Anti-Patterns Eliminated

### ✅ **Unjustified Singleton** → Dependency Injection
### ✅ **God Class** → Single Responsibility
### ✅ **Primitive Obsession** → Value Objects
### ✅ **Code Duplication** → Adapter Pattern
### ✅ **Switch Statements** → Strategy Pattern
### ✅ **Property Pollution** → Direct Access
### ✅ **Tight Coupling** → Protocols & Injection
### ✅ **Long Parameter Lists** → Builder Pattern
### ✅ **Feature Envy** → Tell, Don't Ask

---

## SOLID Principles Applied

### **S - Single Responsibility**
- BasePage split: Interaction vs Debugging (ElementHighlighter)
- Config split: Loading vs Access (ConfigService)

### **O - Open/Closed**
- Strategy pattern: Add browsers without modifying factory
- Decorator pattern: Add behavior without modifying methods

### **L - Liskov Substitution**
- Protocols ensure implementations are substitutable
- Tests work with any PageObject implementation

### **I - Interface Segregation**
- PageObjectProtocol, LoginPageProtocol (specific interfaces)
- WebElementProtocol (minimal interface)

### **D - Dependency Inversion**
- Depend on protocols, not concrete classes
- ConfigService protocol, BrowserProtocol

---

## Risk Assessment

| Phase | Risk Level | Mitigation | Reversibility |
|-------|-----------|------------|---------------|
| Phase 1 | 🟢 Low | Characterization tests | Easy (git revert) |
| Phase 2 | 🟡 Medium | Type checking, unit tests | Moderate |
| Phase 3 | 🔴 High | Feature flags, parallel operation | Moderate (rollback plan) |
| Phase 4 | 🟢 Low | Apply patterns incrementally | Easy |
| Phase 5 | 🟢 Low | Optional, only if needed | N/A (not required) |

---

## Key Decisions

### ✅ **DO:**
1. Introduce protocols for abstractions
2. Use Adapter pattern to unify frameworks
3. Apply patterns when they solve real problems
4. Maintain 100% test coverage
5. Refactor incrementally (small steps)
6. Use characterization tests as safety net

### ❌ **DON'T:**
1. Apply patterns "just because"
2. Over-engineer simple solutions
3. Refactor without tests
4. Change multiple things at once
5. Break existing functionality
6. Add abstractions for single use cases (YAGNI)

---

## Recommended Reading

### **Books:**
- *Refactoring* by Martin Fowler
- *Clean Code* by Robert C. Martin
- *Design Patterns* by Gang of Four
- *Working Effectively with Legacy Code* by Michael Feathers

### **Patterns Catalog:**
- [Refactoring Guru](https://refactoring.guru/)
- [Source Making](https://sourcemaking.com/)

---

## Next Steps

1. **Review Plan:** Team review and approval (1 day)
2. **Setup:** Create feature branch, characterization tests (2 days)
3. **Phase 1 Kickoff:** Start with Config refactor (Week 1)
4. **Daily Standups:** Track progress, blockers
5. **Phase Reviews:** Demo and retrospective after each phase
6. **Documentation:** Update CLAUDE.md, README after Phase 3

---

## Questions?

**Q: Why not just keep separate Selenium/Playwright implementations?**
A: 90% duplication means every bug fix, feature, or improvement requires double work. Unification reduces maintenance burden by 50%+.

**Q: Won't abstractions hurt performance?**
A: Minimal impact. Adapters add ~1-2% overhead. Benefits (maintainability, extensibility) far outweigh cost.

**Q: What if we need to add a third framework (Cypress, Puppeteer)?**
A: After Phase 3, just implement `CypressBrowserAdapter`. ~1 day of work. No test changes needed.

**Q: Is this over-engineered?**
A: No. Every pattern solves a real problem (duplication, coupling, extensibility). We follow YAGNI (Phase 5 is optional).

**Q: What's the ROI?**
A: Initial investment: 8-10 weeks. Payback: Every change is 2x faster. Break-even: ~6 months. Long-term savings: Significant.

---

**Document Version:** 1.0
**Last Updated:** 2025-01-15
**Author:** Senior Software Architect
**Status:** Pending Approval
