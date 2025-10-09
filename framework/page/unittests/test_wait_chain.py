"""
Unit tests for Chain of Responsibility wait strategies.

These tests don't require a browser - they test the wait chain logic.

Reference: https://refactoring.guru/design-patterns/chain-of-responsibility
"""
import pytest
from unittest.mock import Mock, MagicMock
from selenium.common.exceptions import TimeoutException
from framework.page.strategies import (
    VisibilityWaitStrategy,
    ClickableWaitStrategy,
    PresenceWaitStrategy,
    create_default_wait_chain,
)


class TestWaitStrategyChain:
    """Test Chain of Responsibility pattern in wait strategies."""

    def test_single_strategy_success(self):
        """Test that a single strategy can find an element."""
        # Create mock driver and element
        mock_driver = Mock()
        mock_element = Mock()
        locator = ("id", "test_element")

        # Create strategy
        strategy = VisibilityWaitStrategy()

        # Mock the internal wait to return element
        strategy._wait = Mock(return_value=mock_element)

        # Execute
        result = strategy.wait_for(mock_driver, locator, timeout=10)

        # Verify
        assert result == mock_element
        strategy._wait.assert_called_once_with(mock_driver, locator, 10)

    def test_strategy_chain_first_succeeds(self):
        """Test chain where first strategy succeeds."""
        mock_driver = Mock()
        mock_element = Mock()
        locator = ("id", "test")

        # Create chain
        strategy1 = VisibilityWaitStrategy()
        strategy2 = ClickableWaitStrategy()
        strategy3 = PresenceWaitStrategy()

        strategy1.set_next(strategy2).set_next(strategy3)

        # Mock first strategy to succeed
        strategy1._wait = Mock(return_value=mock_element)
        strategy2._wait = Mock(return_value=None)
        strategy3._wait = Mock(return_value=None)

        # Execute
        result = strategy1.wait_for(mock_driver, locator, timeout=10)

        # Verify
        assert result == mock_element
        strategy1._wait.assert_called_once()
        strategy2._wait.assert_not_called()  # Should not reach second
        strategy3._wait.assert_not_called()  # Should not reach third

    def test_strategy_chain_second_succeeds(self):
        """Test chain where first fails but second succeeds."""
        mock_driver = Mock()
        mock_element = Mock()
        locator = ("id", "test")

        # Create chain
        strategy1 = VisibilityWaitStrategy()
        strategy2 = ClickableWaitStrategy()
        strategy3 = PresenceWaitStrategy()

        strategy1.set_next(strategy2).set_next(strategy3)

        # Mock first to fail, second to succeed
        strategy1._wait = Mock(side_effect=TimeoutException())
        strategy2._wait = Mock(return_value=mock_element)
        strategy3._wait = Mock(return_value=None)

        # Execute
        result = strategy1.wait_for(mock_driver, locator, timeout=10)

        # Verify
        assert result == mock_element
        strategy1._wait.assert_called_once()
        strategy2._wait.assert_called_once()
        strategy3._wait.assert_not_called()  # Should not reach third

    def test_strategy_chain_all_fail(self):
        """Test chain where all strategies fail."""
        mock_driver = Mock()
        locator = ("id", "test")

        # Create chain
        strategy1 = VisibilityWaitStrategy()
        strategy2 = ClickableWaitStrategy()

        strategy1.set_next(strategy2)

        # Mock both to fail
        strategy1._wait = Mock(side_effect=TimeoutException())
        strategy2._wait = Mock(side_effect=TimeoutException())

        # Execute and verify exception
        with pytest.raises(TimeoutException) as exc_info:
            strategy1.wait_for(mock_driver, locator, timeout=10)

        assert "not found after trying all wait strategies" in str(exc_info.value)

    def test_default_wait_chain_creation(self):
        """Test that default wait chain is properly constructed."""
        chain = create_default_wait_chain()

        # Verify it's a VisibilityWaitStrategy
        assert isinstance(chain, VisibilityWaitStrategy)

        # Verify it has next strategies
        assert chain._next_strategy is not None
        assert isinstance(chain._next_strategy, ClickableWaitStrategy)
        assert chain._next_strategy._next_strategy is not None
        assert isinstance(chain._next_strategy._next_strategy, PresenceWaitStrategy)

    def test_strategy_can_handle_names(self):
        """Test that each strategy has descriptive name."""
        assert "Visibility" in VisibilityWaitStrategy().can_handle()
        assert "Clickable" in ClickableWaitStrategy().can_handle()
        assert "Presence" in PresenceWaitStrategy().can_handle()

    def test_chain_builder_pattern(self):
        """Test that set_next returns next strategy for chaining."""
        strategy1 = VisibilityWaitStrategy()
        strategy2 = ClickableWaitStrategy()
        strategy3 = PresenceWaitStrategy()

        # Chain using fluent interface
        result = strategy1.set_next(strategy2).set_next(strategy3)

        # Verify returns allow chaining
        assert result == strategy3
        assert strategy1._next_strategy == strategy2
        assert strategy2._next_strategy == strategy3


class TestWaitStrategyIntegration:
    """Integration tests for wait strategies."""

    def test_visibility_strategy_name(self):
        """Test visibility strategy identification."""
        strategy = VisibilityWaitStrategy()
        assert strategy.can_handle() == "Visibility Wait"

    def test_clickable_strategy_name(self):
        """Test clickable strategy identification."""
        strategy = ClickableWaitStrategy()
        assert strategy.can_handle() == "Clickable Wait"

    def test_presence_strategy_name(self):
        """Test presence strategy identification."""
        strategy = PresenceWaitStrategy()
        assert strategy.can_handle() == "Presence Wait"

    def test_chain_construction_fluent_interface(self):
        """Test building a chain with fluent interface."""
        # Build chain - keep reference to first strategy
        first_strategy = VisibilityWaitStrategy()
        first_strategy.set_next(ClickableWaitStrategy()).set_next(PresenceWaitStrategy())

        # Verify chain structure
        assert first_strategy._next_strategy is not None
        assert first_strategy._next_strategy._next_strategy is not None


@pytest.mark.parametrize("strategy_class,expected_name", [
    (VisibilityWaitStrategy, "Visibility Wait"),
    (ClickableWaitStrategy, "Clickable Wait"),
    (PresenceWaitStrategy, "Presence Wait"),
])
def test_strategy_names_parametrized(strategy_class, expected_name):
    """Parametrized test for strategy names."""
    strategy = strategy_class()
    assert strategy.can_handle() == expected_name
