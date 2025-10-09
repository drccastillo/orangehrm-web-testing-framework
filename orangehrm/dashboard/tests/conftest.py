"""
Pytest fixtures specific to dashboard feature.
Uses NEW clean architecture - config injection with ConfigInterface.
"""
import pytest
from orangehrm.dashboard.pages import DashboardPage


@pytest.fixture
def dashboard_page(authenticated_session, config_provider):
    """
    Create DashboardPage with config injection (NEW ARCHITECTURE).

    Uses shared authenticated_session fixture from root conftest to avoid
    duplicating login logic across features.

    Args:
        authenticated_session: Authenticated WebDriver fixture from root conftest
        config_provider: ConfigInterface fixture from root conftest

    Returns:
        DashboardPage instance with injected config

    Note:
        The authenticated_session fixture already handles login, so this
        fixture only needs to navigate to dashboard and create the page object.
    """
    # Create and return dashboard page (already authenticated)
    page = DashboardPage(
        authenticated_session,
        timeout=config_provider.default_timeout,
        config=config_provider
    )
    page.navigate_to_dashboard()
    return page
