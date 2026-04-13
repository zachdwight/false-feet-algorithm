"""
Evaluation branch classes for the False Feet Algorithm.

Each branch represents an independent reasoning path that evaluates a hypothesis
(Option) against available evidence in the SharedDataPool.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass, field
from false_feet_algorithm.core.problem import Option, DataPoint, SharedDataPool


@dataclass
class BranchState:
    """Internal state of a branch during algorithm execution."""
    option: Option
    score: float = 0.0
    proposal_slots: int = 0
    improvement_counter: int = 0  # Increments when branch doesn't improve
    is_alive: bool = True
    iteration_created: int = 0
    last_improvement_iteration: int = 0
    proposed_data_ids: List[str] = field(default_factory=list)


class EvaluationBranch:
    """
    Base implementation of an evaluation branch.

    A branch maintains an independent hypothesis (Option) and evaluates it
    against available evidence. The solver orchestrates multiple branches
    competing to find the best solution.

    Attributes:
        branch_id: Unique identifier for this branch
        option: The hypothesis this branch is evaluating
        state: Current state of the branch
    """

    def __init__(self, branch_id: int, option: Option):
        """
        Initialize a branch.

        Args:
            branch_id: Unique ID for this branch (usually assigned by solver)
            option: The Option (hypothesis) this branch represents
        """
        self.branch_id = branch_id
        self.option = option
        self.state = BranchState(
            option=option,
            score=option.initial_score / 100.0,  # Normalize to 0-1
            iteration_created=0
        )

    def evaluate(self, data_pool: SharedDataPool) -> float:
        """
        Evaluate the hypothesis given current evidence.

        This method should:
        1. Examine relevant data points in the pool
        2. Update the branch's score based on how well evidence supports the hypothesis
        3. Return the new score (0.0 to 1.0)

        Base implementation: Returns current score unchanged.
        Override in subclasses for domain-specific evaluation logic.

        Args:
            data_pool: The shared pool of evidence

        Returns:
            Score after evaluation (0.0 to 1.0)
        """
        return self.state.score

    def propose_data(self, data_pool: SharedDataPool) -> List[str]:
        """
        Propose new data points to investigate.

        This method should return a list of data point IDs that this branch
        thinks would be useful to add to the evidence pool. The solver will
        deduplicate proposals and add them to the pool.

        Base implementation: Returns empty list (no proposals).
        Override in subclasses for domain-specific proposal logic.

        Args:
            data_pool: The current shared pool of evidence

        Returns:
            List of proposed data point IDs
        """
        return []

    def get_summary(self) -> str:
        """Get a human-readable summary of this branch's state."""
        return (
            f"Branch {self.branch_id}: {self.option.name} "
            f"(score={self.state.score:.3f}, alive={self.state.is_alive})"
        )

    def get_score(self) -> float:
        """Get the current score of this branch."""
        return self.state.score

    def set_score(self, score: float) -> None:
        """Update the branch's score."""
        if not (0.0 <= score <= 1.0):
            raise ValueError(f"Score must be 0.0-1.0, got {score}")
        self.state.score = score

    def is_alive(self) -> bool:
        """Check if this branch is still active."""
        return self.state.is_alive

    def increment_improvement_counter(self) -> None:
        """Increment the starvation counter (used during culling phase)."""
        self.state.improvement_counter += 1

    def reset_improvement_counter(self) -> None:
        """Reset the starvation counter (called when branch improves)."""
        self.state.improvement_counter = 0

    def kill(self) -> None:
        """Mark this branch as dead (culled from the investigation)."""
        self.state.is_alive = False


class BaseBranch(EvaluationBranch, ABC):
    """
    Abstract base class for domain-specific branch implementations.

    Users should subclass this to implement custom evaluation and proposal logic
    for their specific problem domain.

    Example:
        class MedicalDiagnosisBranch(BaseBranch):
            def evaluate(self, data_pool):
                # Custom medical reasoning
                pass

            def propose_data(self, data_pool):
                # Suggest next diagnostic tests
                pass
    """

    @abstractmethod
    def evaluate(self, data_pool: SharedDataPool) -> float:
        """
        Evaluate the hypothesis with domain-specific logic.

        Subclasses must implement this method.
        """
        pass

    @abstractmethod
    def propose_data(self, data_pool: SharedDataPool) -> List[str]:
        """
        Propose new data points with domain-specific logic.

        Subclasses must implement this method.
        """
        pass
