"""
Test data for authentication feature.
"""
from framework.config import Config
from framework.data import UserDataBuilder, UserRole, LoginCredentials


def valid_admin_user():
    """Get valid admin user credentials."""
    return UserDataBuilder()\
        .with_username(Config.USERNAME)\
        .with_password(Config.PASSWORD)\
        .with_role(UserRole.ADMIN)\
        .build()


def invalid_user():
    """Get invalid user credentials."""
    return UserDataBuilder()\
        .with_username("invalid_user")\
        .with_password("invalid_password")\
        .build()


def valid_login_credentials():
    """Get valid login credentials."""
    return LoginCredentials(
        username=Config.USERNAME,
        password=Config.PASSWORD,
        expected_result="success"
    )


def empty_username_credentials():
    """Get credentials with empty username."""
    return LoginCredentials(
        username="",
        password=Config.PASSWORD,
        expected_result="empty_field"
    )


def empty_password_credentials():
    """Get credentials with empty password."""
    return LoginCredentials(
        username=Config.USERNAME,
        password="",
        expected_result="empty_field"
    )
