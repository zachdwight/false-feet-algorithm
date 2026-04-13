"""
Evaluator classes for scoring hypotheses in the False Feet Algorithm.

The HypothesisEvaluator provides a standard three-dimensional scoring model,
while BaseEvaluator allows customization for domain-specific scoring.
"""

from abc import ABC, abstractmethod
from typing import Tuple
from false_feet_algorithm.core.problem import Option, SharedDataPool
from false_feet_algorithm.core.branch import EvaluationBranch


class HypothesisEvaluator:
    """
    Standard three-dimensional hypothesis evaluator.

    Scores hypotheses across three weighted dimensions:
    - Data Support (40%): How much evidence backs this hypothesis
    - Rationale Strength (30%): Quality of reasoning/explanation
    - Consistency (30%): How internally coherent the hypothesis is

    All three scores are normalized to 0.0-1.0, then weighted and summed
    to produce a final score.
    """

    def __init__(
        self,
        data_support_weight: float = 0.4,
        rationale_weight: float = 0.3,
        consistency_weight: float = 0.3,
    ):
        """
        Initialize the evaluator with custom weights.

        Args:
            data_support_weight: Weight for data support dimension (default 0.4)
            rationale_weight: Weight for rationale strength dimension (default 0.3)
            consistency_weight: Weight for consistency dimension (default 0.3)

        Raises:
            ValueError: If weights don't sum to 1.0
        """
        total = data_support_weight + rationale_weight + consistency_weight
        if abs(total - 1.0) > 0.001:  # Allow small floating-point error
            raise ValueError(f"Weights must sum to 1.0, got {total}")

        self.data_support_weight = data_support_weight
        self.rationale_weight = rationale_weight
        self.consistency_weight = consistency_weight

    def evaluate(
        self, branch: EvaluationBranch, data_pool: SharedDataPool
    ) -> float:
        """
        Evaluate a branch's hypothesis using the three-dimensional model.

        Args:
            branch: The branch containing the hypothesis to evaluate
            data_pool: The shared pool of evidence

        Returns:
            Overall score (0.0-1.0)
        """
        data_support = self._evaluate_data_support(branch, data_pool)
        rationale = self._evaluate_rationale(branch, data_pool)
        consistency = self._evaluate_consistency(branch, data_pool)

        # Weighted sum
        final_score = (
            data_support * self.data_support_weight
            + rationale * self.rationale_weight
            + consistency * self.consistency_weight
        )

        return max(0.0, min(1.0, final_score))  # Clamp to 0-1

    def _evaluate_data_support(
        self, branch: EvaluationBranch, data_pool: SharedDataPool
    ) -> float:
        """
        Evaluate how much evidence supports this hypothesis.

        Base calculation: (supporting evidence count) / (total evidence count)
        Penalizes contradicting evidence.
        """
        if data_pool.size() == 0:
            return 0.5  # Neutral if no evidence yet

        supporting = data_pool.get_supporting_data(branch.option.id)
        contradicting = data_pool.get_contradicting_data(branch.option.id)

        support_score = len(supporting) / data_pool.size()
        contradiction_penalty = len(contradicting) / data_pool.size()

        return max(0.0, support_score - contradiction_penalty)

    def _evaluate_rationale(
        self, branch: EvaluationBranch, data_pool: SharedDataPool
    ) -> float:
        """
        Evaluate the quality and clarity of the hypothesis rationale.

        Base calculation: Length and presence of rationale.
        Override in subclasses for more sophisticated logic.
        """
        if not branch.option.rationale:
            return 0.3  # Low but not zero (hypothesis can be clarified)

        # Simple heuristic: longer rationale suggests more thought
        rationale_length = len(branch.option.rationale)
        return min(1.0, 0.3 + (rationale_length / 200.0))

    def _evaluate_consistency(
        self, branch: EvaluationBranch, data_pool: SharedDataPool
    ) -> float:
        """
        Evaluate the internal consistency of the hypothesis.

        Base calculation: checks for contradictions within the rationale.
        Override in subclasses for domain-specific consistency checks.
        """
        # Check if there's both supporting and contradicting evidence
        supporting = data_pool.get_supporting_data(branch.option.id)
        contradicting = data_pool.get_contradicting_data(branch.option.id)

        # If there's both support and contradiction, lower consistency
        if supporting and contradicting:
            consistency = 0.5  # Mixed evidence lowers consistency
        elif supporting:
            consistency = 0.8
        elif contradicting:
            consistency = 0.3
        else:
            consistency = 0.5  # Neutral

        return consistency


class BaseEvaluator(ABC):
    """
    Abstract base class for domain-specific evaluators.

    Users should subclass this to implement custom scoring logic
    tailored to their problem domain.

    The standard HypothesisEvaluator can be used as-is for many domains,
    but specialized domains may benefit from custom evaluation logic.

    Example:
        class MedicalEvaluator(BaseEvaluator):
            def evaluate(self, branch, data_pool):
                # Custom medical scoring logic
                return score
    """

    @abstractmethod
    def evaluate(
        self, branch: EvaluationBranch, data_pool: SharedDataPool
    ) -> float:
        """
        Evaluate a branch's hypothesis with domain-specific logic.

        Args:
            branch: The branch containing the hypothesis to evaluate
            data_pool: The shared pool of evidence

        Returns:
            Score (0.0-1.0)
        """
        pass
