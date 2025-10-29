"""
Data Loader Utility for Test Data.

Provides functionality to load and parse JSON test data files for data-driven testing.
This enables separation of test data from test logic, making tests more maintainable.

Usage:
    >>> from utils.data_loader import TestDataLoader
    >>>
    >>> # Load all happy path scenarios
    >>> data = TestDataLoader.load_leave_period_data("happy_path_scenarios")
    >>>
    >>> # Load with filtering by tags
    >>> smoke_tests = TestDataLoader.load_leave_period_data("happy_path_scenarios", tags=["smoke"])
    >>>
    >>> # Load and convert to pytest parametrize format
    >>> params = TestDataLoader.to_pytest_params(data, ["start_month", "expected_end_month"])
"""

import json
from pathlib import Path
from typing import Any


class TestDataLoader:
    """
    Utility class for loading JSON-based test data files.

    This class provides methods to load test data from JSON files and convert
    them into formats suitable for pytest parametrization.
    """

    # Base directory for test data files
    DATA_DIR = Path(__file__).parent.parent / "tests" / "data"

    @classmethod
    def load_json_file(cls, filename: str) -> dict[str, Any]:
        """
        Load a JSON file from the test data directory.

        Args:
            filename: Name of the JSON file (e.g., "leave_period_test_data.json")

        Returns:
            Dictionary containing the parsed JSON data

        Raises:
            FileNotFoundError: If the JSON file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON

        Example:
            >>> data = TestDataLoader.load_json_file("leave_period_test_data.json")
            >>> print(data.keys())
            dict_keys(['happy_path_scenarios', 'edge_cases', 'all_months'])
        """
        file_path = cls.DATA_DIR / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Test data file not found: {file_path}\nExpected location: {cls.DATA_DIR}",
            )

        with open(file_path, encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)
            return data

    @classmethod
    def load_leave_period_data(
        cls,
        scenario_type: str,
        tags: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Load Leave Period test data from JSON file.

        Args:
            scenario_type: Type of scenarios to load (e.g., "happy_path_scenarios",
                          "edge_cases", "all_months", "validation_scenarios")
            tags: Optional list of tags to filter scenarios (e.g., ["smoke"])

        Returns:
            List of test data dictionaries matching the criteria

        Example:
            >>> # Load all happy path scenarios
            >>> scenarios = TestDataLoader.load_leave_period_data("happy_path_scenarios")
            >>> len(scenarios)
            4
            >>>
            >>> # Load only smoke test scenarios
            >>> smoke = TestDataLoader.load_leave_period_data(
            ...     "happy_path_scenarios",
            ...     tags=["smoke"]
            ... )
            >>> len(smoke)
            2
        """
        data = cls.load_json_file("leave_period_test_data.json")
        scenarios: list[dict[str, Any]] = data.get(scenario_type, [])

        # Filter by tags if provided
        if tags:
            filtered_scenarios: list[dict[str, Any]] = [
                scenario
                for scenario in scenarios
                if any(tag in scenario.get("tags", []) for tag in tags)
            ]
            return filtered_scenarios

        return scenarios

    @classmethod
    def to_pytest_params(
        cls,
        data: list[dict[str, Any]],
        fields: list[str],
        id_field: str = "id",
    ) -> list[Any]:
        """
        Convert test data to pytest parametrize format.

        Args:
            data: List of test data dictionaries
            fields: List of field names to extract from each dictionary
            id_field: Field to use for test ID (default: "id")

        Returns:
            List of tuples suitable for pytest.mark.parametrize

        Example:
            >>> data = [
            ...     {"id": "test1", "month": "January", "expected": "December"},
            ...     {"id": "test2", "month": "June", "expected": "May"}
            ... ]
            >>> params = TestDataLoader.to_pytest_params(data, ["month", "expected"])
            >>> params
            [
                pytest.param("January", "December", id="test1"),
                pytest.param("June", "May", id="test2")
            ]
        """
        import pytest

        params = []
        for item in data:
            values = tuple(item.get(field) for field in fields)
            test_id = item.get(id_field, "")
            params.append(pytest.param(*values, id=test_id))

        return params

    @classmethod
    def get_scenario_by_id(
        cls,
        scenario_type: str,
        scenario_id: str,
    ) -> dict[str, Any] | None:
        """
        Get a specific test scenario by its ID.

        Args:
            scenario_type: Type of scenarios to search in
            scenario_id: Unique ID of the scenario

        Returns:
            Dictionary containing the scenario data, or None if not found

        Example:
            >>> scenario = TestDataLoader.get_scenario_by_id(
            ...     "happy_path_scenarios",
            ...     "calendar_year"
            ... )
            >>> scenario["start_month"]
            'January'
        """
        scenarios = cls.load_leave_period_data(scenario_type)
        for scenario in scenarios:
            if scenario.get("id") == scenario_id:
                return scenario
        return None

    @classmethod
    def get_all_scenario_ids(cls, scenario_type: str) -> list[str]:
        """
        Get list of all scenario IDs for a given type.

        Args:
            scenario_type: Type of scenarios

        Returns:
            List of scenario IDs

        Example:
            >>> ids = TestDataLoader.get_all_scenario_ids("edge_cases")
            >>> print(ids)
            ['february_last_day', 'mid_month_june', 'last_day_december', ...]
        """
        scenarios = cls.load_leave_period_data(scenario_type)
        return [scenario.get("id", "") for scenario in scenarios]

    @classmethod
    def validate_test_data(cls, filename: str) -> tuple[bool, list[str]]:
        """
        Validate test data file structure and content.

        Args:
            filename: Name of the JSON file to validate

        Returns:
            Tuple of (is_valid, list_of_errors)

        Example:
            >>> is_valid, errors = TestDataLoader.validate_test_data(
            ...     "leave_period_test_data.json"
            ... )
            >>> if not is_valid:
            ...     print("Validation errors:", errors)
        """
        errors = []

        try:
            data = cls.load_json_file(filename)
        except FileNotFoundError as e:
            return False, [str(e)]
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON format: {e}"]

        # Validate required keys
        required_keys = ["happy_path_scenarios", "edge_cases", "all_months"]
        for key in required_keys:
            if key not in data:
                errors.append(f"Missing required key: {key}")

        # Validate scenario structure
        for scenario_type, scenarios in data.items():
            if not isinstance(scenarios, list):
                errors.append(f"{scenario_type} should be a list")
                continue

            for idx, scenario in enumerate(scenarios):
                if not isinstance(scenario, dict):
                    errors.append(f"{scenario_type}[{idx}] should be a dictionary")
                    continue

                # Check for required fields
                if "id" not in scenario:
                    errors.append(f"{scenario_type}[{idx}] missing 'id' field")

        return len(errors) == 0, errors
