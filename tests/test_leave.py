"""
Leave test suite with Playwright assertions and Gherkin-style documentation.

All tests follow AAA (Arrange-Act-Assert) pattern using Playwright's native
expect() assertions for auto-waiting and better error messages.

Run tests:
    pytest tests/test_leave.py -v

Run with specific browser:
    pytest tests/test_leave.py --browser=firefox
    pytest tests/test_leave.py --browser=chromium
"""
