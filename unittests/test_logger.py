"""
Unit tests for TestLogger class.
Tests logging functionality and logger creation.
"""
import unittest
import logging
from pathlib import Path
from utils.logger import TestLogger, LoggerMixin


class TestTestLogger(unittest.TestCase):
    """Test suite for TestLogger class."""

    def test_get_logger_returns_logger_instance(self):
        """Test that get_logger returns a logging.Logger instance."""
        logger = TestLogger.get_logger('test_logger')
        self.assertIsInstance(logger, logging.Logger)

    def test_get_logger_returns_same_instance_for_same_name(self):
        """Test that get_logger returns the same instance for the same name."""
        logger1 = TestLogger.get_logger('test_logger_same')
        logger2 = TestLogger.get_logger('test_logger_same')
        self.assertIs(logger1, logger2)

    def test_get_logger_creates_different_instances_for_different_names(self):
        """Test that get_logger creates different instances for different names."""
        logger1 = TestLogger.get_logger('test_logger_1')
        logger2 = TestLogger.get_logger('test_logger_2')
        self.assertIsNot(logger1, logger2)

    def test_logger_has_correct_level(self):
        """Test that logger has the correct logging level."""
        logger = TestLogger.get_logger('test_logger_level', log_level='DEBUG')
        self.assertEqual(logger.level, logging.DEBUG)

    def test_logger_has_handlers(self):
        """Test that logger has at least one handler."""
        logger = TestLogger.get_logger('test_logger_handlers')
        self.assertGreater(len(logger.handlers), 0)

    def test_logger_has_console_handler(self):
        """Test that logger has a console handler."""
        logger = TestLogger.get_logger('test_logger_console')
        has_console_handler = any(
            isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
            for h in logger.handlers
        )
        self.assertTrue(has_console_handler)

    def test_logger_has_file_handler(self):
        """Test that logger has a file handler."""
        logger = TestLogger.get_logger('test_logger_file')
        has_file_handler = any(
            isinstance(h, logging.FileHandler)
            for h in logger.handlers
        )
        self.assertTrue(has_file_handler)

    def test_logs_directory_created(self):
        """Test that logs directory is created in project root."""
        TestLogger.get_logger('test_logger_dir')
        logs_dir = Path(__file__).parent.parent / 'logs'
        self.assertTrue(logs_dir.exists())
        self.assertTrue(logs_dir.is_dir())

    def test_set_level_changes_logger_level(self):
        """Test that set_level changes the logger's level."""
        logger_name = 'test_logger_set_level'
        logger = TestLogger.get_logger(logger_name, log_level='INFO')
        self.assertEqual(logger.level, logging.INFO)

        TestLogger.set_level(logger_name, 'ERROR')
        self.assertEqual(logger.level, logging.ERROR)


class TestLoggerMixin(unittest.TestCase):
    """Test suite for LoggerMixin class."""

    def test_logger_mixin_provides_logger_property(self):
        """Test that LoggerMixin provides a logger property."""
        class TestClass(LoggerMixin):
            pass

        obj = TestClass()
        self.assertTrue(hasattr(obj, 'logger'))

    def test_logger_mixin_returns_logger_instance(self):
        """Test that LoggerMixin returns a logging.Logger instance."""
        class TestClass(LoggerMixin):
            pass

        obj = TestClass()
        self.assertIsInstance(obj.logger, logging.Logger)

    def test_logger_mixin_logger_named_after_class(self):
        """Test that logger is named after the class."""
        class MyTestClass(LoggerMixin):
            pass

        obj = MyTestClass()
        self.assertEqual(obj.logger.name, 'MyTestClass')

    def test_logger_mixin_returns_same_logger_instance(self):
        """Test that multiple calls return the same logger instance."""
        class TestClass(LoggerMixin):
            pass

        obj = TestClass()
        logger1 = obj.logger
        logger2 = obj.logger
        self.assertIs(logger1, logger2)


if __name__ == '__main__':
    unittest.main()
