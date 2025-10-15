"""
Page Object protocols and implementations.
Provides framework-agnostic interfaces for page objects.
"""

from src.pages.protocols import LoginPageProtocol, PageObjectProtocol

__all__ = ["PageObjectProtocol", "LoginPageProtocol"]
