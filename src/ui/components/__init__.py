"""
UI Components Module for OrangeHRM Test Automation Framework.

This module contains reusable UI components that appear across multiple pages
and modules in the OrangeHRM application.

Components follow the Component-Based Abstraction pattern:
    - Reusable across multiple modules/pages
    - Autocontenidos (self-contained)
    - Consistent behavior regardless of context
    - Composition over inheritance

Available Components:
    - NavigationHeader: Global navigation menu (Admin, PIM, Leave, etc.)

Future Components:
    - DataTable: Generic data table with sorting, pagination
    - SearchBox: Search widget with filters
    - ToastNotification: Success/error messages
    - ModalDialog: Confirmation dialogs
    - DatePicker: Date selection widget

Example:
    >>> from src.ui.components import NavigationHeader
    >>> nav_header = NavigationHeader(page)
    >>> nav_header.navigate_to_leave()
"""

from src.ui.components.navigation_header import NavigationHeader

__all__ = ["NavigationHeader"]
