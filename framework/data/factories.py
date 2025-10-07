"""
Test Data Factory using Builder and Factory patterns.
Provides reusable test data generation with validation.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum
import random
import string
from datetime import datetime


class UserRole(Enum):
    """User role enumeration."""
    ADMIN = "Admin"
    ESS = "ESS"
    SUPERVISOR = "Supervisor"


@dataclass
class UserData:
    """User data model."""
    username: str
    password: str
    role: UserRole = UserRole.ADMIN
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    employee_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate user data after initialization."""
        if not self.username:
            raise ValueError("Username cannot be empty")
        if not self.password:
            raise ValueError("Password cannot be empty")


@dataclass
class LoginCredentials:
    """Login credentials model."""
    username: str
    password: str
    remember_me: bool = False
    expected_result: str = "success"  # success, invalid_credentials, empty_field


class TestDataBuilder(ABC):
    """Abstract builder for test data (Builder Pattern)."""

    @abstractmethod
    def reset(self) -> None:
        """Reset the builder to initial state."""
        pass

    @abstractmethod
    def build(self) -> Any:
        """Build and return the final object."""
        pass


class UserDataBuilder(TestDataBuilder):
    """
    Builder for UserData objects (Builder Pattern).

    Example:
        user = UserDataBuilder()\\
            .with_username("admin")\\
            .with_password("admin123")\\
            .with_role(UserRole.ADMIN)\\
            .with_email("admin@example.com")\\
            .build()
    """

    def __init__(self):
        """Initialize the builder."""
        self.reset()

    def reset(self) -> None:
        """Reset builder to default state."""
        self._username: Optional[str] = None
        self._password: Optional[str] = None
        self._role: UserRole = UserRole.ADMIN
        self._email: Optional[str] = None
        self._first_name: Optional[str] = None
        self._last_name: Optional[str] = None
        self._employee_id: Optional[str] = None
        self._metadata: Dict[str, Any] = {}

    def with_username(self, username: str) -> 'UserDataBuilder':
        """Set username."""
        self._username = username
        return self

    def with_password(self, password: str) -> 'UserDataBuilder':
        """Set password."""
        self._password = password
        return self

    def with_role(self, role: UserRole) -> 'UserDataBuilder':
        """Set user role."""
        self._role = role
        return self

    def with_email(self, email: str) -> 'UserDataBuilder':
        """Set email."""
        self._email = email
        return self

    def with_name(self, first_name: str, last_name: str) -> 'UserDataBuilder':
        """Set first and last name."""
        self._first_name = first_name
        self._last_name = last_name
        return self

    def with_employee_id(self, employee_id: str) -> 'UserDataBuilder':
        """Set employee ID."""
        self._employee_id = employee_id
        return self

    def with_metadata(self, key: str, value: Any) -> 'UserDataBuilder':
        """Add metadata."""
        self._metadata[key] = value
        return self

    def build(self) -> UserData:
        """Build and return UserData object."""
        user = UserData(
            username=self._username,
            password=self._password,
            role=self._role,
            email=self._email,
            first_name=self._first_name,
            last_name=self._last_name,
            employee_id=self._employee_id,
            metadata=self._metadata
        )
        self.reset()
        return user


class TestDataFactory:
    """
    Factory for creating test data objects (Factory Pattern).
    Provides predefined test data scenarios.
    """

    @staticmethod
    def generate_random_string(length: int = 8, prefix: str = "") -> str:
        """Generate random alphanumeric string."""
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        return f"{prefix}{random_str}"

    @staticmethod
    def generate_timestamp() -> str:
        """Generate timestamp string."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def create_valid_user() -> UserData:
        """Create valid user with default credentials."""
        return UserDataBuilder()\
            .with_username("Admin")\
            .with_password("admin123")\
            .with_role(UserRole.ADMIN)\
            .with_email("admin@orangehrm.com")\
            .build()

    @staticmethod
    def create_invalid_user() -> UserData:
        """Create user with invalid credentials."""
        return UserDataBuilder()\
            .with_username("invalid_user")\
            .with_password("wrong_password")\
            .build()

    @staticmethod
    def create_random_user() -> UserData:
        """Create user with random credentials."""
        timestamp = TestDataFactory.generate_timestamp()
        username = TestDataFactory.generate_random_string(prefix=f"user_{timestamp}_")
        password = TestDataFactory.generate_random_string(12)

        return UserDataBuilder()\
            .with_username(username)\
            .with_password(password)\
            .with_email(f"{username}@test.com")\
            .with_metadata("created_at", timestamp)\
            .build()

    @staticmethod
    def create_login_credentials(
        username: str,
        password: str,
        expected_result: str = "success"
    ) -> LoginCredentials:
        """Create login credentials object."""
        return LoginCredentials(
            username=username,
            password=password,
            expected_result=expected_result
        )

    @staticmethod
    def get_valid_login_scenarios() -> List[LoginCredentials]:
        """Get list of valid login test scenarios."""
        return [
            TestDataFactory.create_login_credentials("Admin", "admin123", "success"),
        ]

    @staticmethod
    def get_invalid_login_scenarios() -> List[LoginCredentials]:
        """Get list of invalid login test scenarios."""
        return [
            TestDataFactory.create_login_credentials("", "", "empty_field"),
            TestDataFactory.create_login_credentials("Admin", "", "empty_field"),
            TestDataFactory.create_login_credentials("", "admin123", "empty_field"),
            TestDataFactory.create_login_credentials("invalid", "invalid", "invalid_credentials"),
            TestDataFactory.create_login_credentials("Admin", "wrongpass", "invalid_credentials"),
        ]

    @staticmethod
    def get_boundary_test_data() -> List[Dict[str, Any]]:
        """Get boundary test data for input validation."""
        return [
            {
                "description": "Max length username",
                "username": "a" * 255,
                "password": "test123",
                "expected": "invalid_credentials"
            },
            {
                "description": "Special characters in username",
                "username": "user@#$%",
                "password": "test123",
                "expected": "invalid_credentials"
            },
            {
                "description": "SQL injection attempt",
                "username": "admin' OR '1'='1",
                "password": "' OR '1'='1",
                "expected": "invalid_credentials"
            },
            {
                "description": "XSS attempt",
                "username": "<script>alert('xss')</script>",
                "password": "test123",
                "expected": "invalid_credentials"
            },
        ]


class TestDataRepository:
    """
    Repository for managing test data (Repository Pattern).
    Provides centralized access to test data with caching.
    """

    _cache: Dict[str, Any] = {}

    @classmethod
    def get_user(cls, user_type: str = "valid") -> UserData:
        """
        Get user from repository with caching.

        Args:
            user_type: Type of user (valid, invalid, random)

        Returns:
            UserData object
        """
        cache_key = f"user_{user_type}"

        if cache_key not in cls._cache:
            if user_type == "valid":
                cls._cache[cache_key] = TestDataFactory.create_valid_user()
            elif user_type == "invalid":
                cls._cache[cache_key] = TestDataFactory.create_invalid_user()
            elif user_type == "random":
                # Don't cache random users
                return TestDataFactory.create_random_user()
            else:
                raise ValueError(f"Unknown user type: {user_type}")

        return cls._cache[cache_key]

    @classmethod
    def clear_cache(cls) -> None:
        """Clear the cache."""
        cls._cache.clear()

    @classmethod
    def get_login_scenarios(cls, scenario_type: str = "all") -> List[LoginCredentials]:
        """
        Get login test scenarios.

        Args:
            scenario_type: Type of scenarios (valid, invalid, all)

        Returns:
            List of LoginCredentials
        """
        if scenario_type == "valid":
            return TestDataFactory.get_valid_login_scenarios()
        elif scenario_type == "invalid":
            return TestDataFactory.get_invalid_login_scenarios()
        elif scenario_type == "all":
            return (
                TestDataFactory.get_valid_login_scenarios() +
                TestDataFactory.get_invalid_login_scenarios()
            )
        else:
            raise ValueError(f"Unknown scenario type: {scenario_type}")
