"""
Authentication Feature for OrangeHRM.

This module handles all authentication-related functionality including:
- User login
- User logout
- Password reset
- Session management
"""

__version__ = '1.0.0'

# Public API
from .pages import LoginPage
from .data import valid_admin_user, invalid_user

__all__ = [
    'LoginPage',
    'valid_admin_user',
    'invalid_user',
]
