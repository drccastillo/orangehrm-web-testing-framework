"""
Logging utility for the test framework.
Provides centralized logging configuration and custom logger.
Thread-safe implementation to prevent handler duplication.
"""
import logging
import sys
import threading
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict
from functools import wraps


class TestLogger:
    """
    Thread-safe custom logger for test automation framework.
    Provides both file and console logging with different formats.

    Uses double-checked locking pattern for thread-safety while maintaining performance.
    """

    _loggers: Dict[str, logging.Logger] = {}
    _lock = threading.Lock()

    @classmethod
    def get_logger(cls, name: str = __name__, log_level: str = "INFO") -> logging.Logger:
        """
        Get or create a logger instance (thread-safe).

        Uses double-checked locking for performance:
        - First check without lock (fast path for existing loggers)
        - Second check with lock (ensures only one logger created)

        Args:
            name: Name of the logger (typically __name__ of the module)
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

        Returns:
            Configured logger instance
        """
        # First check (without lock for performance)
        if name in cls._loggers:
            return cls._loggers[name]

        # Acquire lock for creation
        with cls._lock:
            # Double-check after acquiring lock (another thread might have created it)
            if name in cls._loggers:
                return cls._loggers[name]

            logger = logging.getLogger(name)
            logger.setLevel(getattr(logging, log_level.upper()))

            # Avoid adding handlers multiple times
            if not logger.handlers:
                cls._setup_handlers(logger)

            cls._loggers[name] = logger
            return logger

    @classmethod
    def _setup_handlers(cls, logger: logging.Logger) -> None:
        """
        Setup handlers for logger (called within lock, so thread-safe).

        Args:
            logger: Logger instance to configure
        """
        # Create logs directory in project root (3 levels up from framework/utils/logger.py)
        logs_dir = Path(__file__).parent.parent.parent / 'logs'
        logs_dir.mkdir(parents=True, exist_ok=True)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(cls._get_console_formatter())

        # File handler - log with detailed timestamp
        log_file_name = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        log_file = logs_dir / f'{log_file_name}.log'
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(cls._get_file_formatter())

        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    @staticmethod
    def _get_console_formatter() -> logging.Formatter:
        """Get console formatter (simplified output)."""
        return logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )

    @staticmethod
    def _get_file_formatter() -> logging.Formatter:
        """Get file formatter (detailed output with function/line)."""
        return logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    @classmethod
    def set_level(cls, name: str, level: str) -> None:
        """
        Set logging level for a specific logger (thread-safe).

        Args:
            name: Name of the logger
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        with cls._lock:
            if name in cls._loggers:
                cls._loggers[name].setLevel(getattr(logging, level.upper()))

    @classmethod
    def clear_cache(cls) -> None:
        """
        Clear logger cache (useful for testing).

        WARNING: This should only be used in test cleanup.
        """
        with cls._lock:
            cls._loggers.clear()


class LoggerMixin:
    """
    Mixin class to add logging capabilities to any class.
    Usage: class MyClass(LoggerMixin): ...
    """

    @property
    def logger(self) -> logging.Logger:
        """
        Get logger for the class.

        Returns:
            Logger instance named after the class
        """
        if not hasattr(self, '_logger'):
            self._logger = TestLogger.get_logger(self.__class__.__name__)
        return self._logger


def log_test_step(step_description: str):
    """
    Decorator to log test steps.

    Args:
        step_description: Description of the test step

    Usage:
        @log_test_step("Login with valid credentials")
        def test_login(self):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = TestLogger.get_logger(func.__module__)
            logger.info(f"TEST STEP: {step_description}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"TEST STEP PASSED: {step_description}")
                return result
            except Exception as e:
                logger.error(f"TEST STEP FAILED: {step_description} - {str(e)}")
                raise
        return wrapper
    return decorator


def log_action(action_description: Optional[str] = None):
    """
    Decorator to log page actions.

    Args:
        action_description: Description of the action (optional)

    Usage:
        @log_action("Click login button")
        def click_login(self):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get logger from first argument (self) if it has logger attribute
            if len(args) > 0 and hasattr(args[0], 'logger'):
                logger = args[0].logger
            else:
                logger = TestLogger.get_logger(func.__module__)

            description = action_description or f"{func.__name__}"
            logger.debug(f"ACTION: {description}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"ACTION SUCCESS: {description}")
                return result
            except Exception as e:
                logger.error(f"ACTION FAILED: {description} - {str(e)}")
                raise
        return wrapper
    return decorator
