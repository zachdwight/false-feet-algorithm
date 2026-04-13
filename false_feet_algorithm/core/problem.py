"""
Core problem definition classes for the False Feet Algorithm.

This module contains the data structures for defining a problem that the
Amoeba solver can work with: Problems, Options (hypotheses), DataPoints (evidence),
and the SharedDataPool that manages evidence across all branches.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Set
from enum import Enum


@dataclass
class Option:
    """
    Represents a candidate solution or hypothesis in the problem.

    Attributes:
        id: Unique identifier for this option
        name: Human-readable name of the hypothesis
        rationale: Initial reasoning or justification for this option
        initial_score: Starting confidence score (0-100)
    """
    id: str
    name: str
    rationale: str = ""
    initial_score: float = 50.0

    def __post_init__(self):
        if not (0 <= self.initial_score <= 100):
            raise ValueError(f"initial_score must be 0-100, got {self.initial_score}")


@dataclass
class DataPoint:
    """
    Represents a piece of evidence or information relevant to the problem.

    Attributes:
        id: Unique identifier for this data point
        title: Short name of the evidence
        description: Detailed description of what this evidence shows
        supports: List of Option IDs this evidence supports
        contradicts: List of Option IDs this evidence contradicts
        priority: Importance level (1-5, where 5 is highest)
    """
    id: str
    title: str
    description: str = ""
    supports: List[str] = field(default_factory=list)
    contradicts: List[str] = field(default_factory=list)
    priority: int = 3  # Default to medium priority (1-5 scale)

    def __post_init__(self):
        if not (1 <= self.priority <= 5):
            raise ValueError(f"priority must be 1-5, got {self.priority}")
        # Convert to lists if needed
        if isinstance(self.supports, set):
            self.supports = list(self.supports)
        if isinstance(self.contradicts, set):
            self.contradicts = list(self.contradicts)


class SharedDataPool:
    """
    Centralized repository of evidence accessible to all branches.

    This pool prevents duplication and ensures all branches work with the same
    evidence. DataPoints can only be added, not removed.
    """

    def __init__(self):
        self._data_points: dict[str, DataPoint] = {}

    def add_data(self, data_point: DataPoint) -> bool:
        """
        Add a data point to the pool.

        Args:
            data_point: DataPoint to add

        Returns:
            True if added, False if already exists (by ID)
        """
        if data_point.id in self._data_points:
            return False
        self._data_points[data_point.id] = data_point
        return True

    def has_data(self, data_id: str) -> bool:
        """Check if a data point exists in the pool."""
        return data_id in self._data_points

    def get_data(self, data_id: str) -> Optional[DataPoint]:
        """Retrieve a specific data point by ID."""
        return self._data_points.get(data_id)

    def get_all(self) -> List[DataPoint]:
        """Get all data points in the pool."""
        return list(self._data_points.values())

    def size(self) -> int:
        """Return the number of data points in the pool."""
        return len(self._data_points)

    def get_supporting_data(self, option_id: str) -> List[DataPoint]:
        """Get all data points that support a specific option."""
        return [dp for dp in self._data_points.values() if option_id in dp.supports]

    def get_contradicting_data(self, option_id: str) -> List[DataPoint]:
        """Get all data points that contradict a specific option."""
        return [dp for dp in self._data_points.values() if option_id in dp.contradicts]


@dataclass
class Problem:
    """
    Container for a problem to be solved by the Amoeba algorithm.

    Attributes:
        title: Problem title
        description: Problem description
        goal: What we're trying to determine
        options: List of candidate solutions to evaluate
        data_points: List of initial evidence
    """
    title: str
    description: str = ""
    goal: str = ""
    options: List[Option] = field(default_factory=list)
    data_points: List[DataPoint] = field(default_factory=list)

    def add_option(self, option: Option) -> None:
        """Add an option to the problem."""
        if any(o.id == option.id for o in self.options):
            raise ValueError(f"Option with id '{option.id}' already exists")
        self.options.append(option)

    def add_data_point(self, data_point: DataPoint) -> None:
        """Add a data point to the problem."""
        if any(d.id == data_point.id for d in self.data_points):
            raise ValueError(f"DataPoint with id '{data_point.id}' already exists")
        self.data_points.append(data_point)

    def validate(self) -> tuple[bool, str]:
        """
        Validate the problem structure.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.options:
            return False, "Problem must have at least one option"

        # Check for duplicate IDs
        option_ids = [o.id for o in self.options]
        if len(option_ids) != len(set(option_ids)):
            return False, "Duplicate option IDs"

        data_ids = [d.id for d in self.data_points]
        if len(data_ids) != len(set(data_ids)):
            return False, "Duplicate data point IDs"

        # Check that references are valid
        valid_option_ids = set(option_ids)
        for data in self.data_points:
            for opt_id in data.supports + data.contradicts:
                if opt_id not in valid_option_ids:
                    return False, f"DataPoint references invalid option ID: {opt_id}"

        return True, ""

    def get_option(self, option_id: str) -> Optional[Option]:
        """Get an option by ID."""
        for opt in self.options:
            if opt.id == option_id:
                return opt
        return None
