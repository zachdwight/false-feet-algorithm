"""
False Feet Algorithm core framework.

This module contains all the core classes needed to define and solve problems
using the Amoeba algorithm.
"""

from false_feet_algorithm.core.problem import (
    Problem,
    Option,
    DataPoint,
    SharedDataPool,
)
from false_feet_algorithm.core.branch import (
    EvaluationBranch,
    BaseBranch,
    BranchState,
)
from false_feet_algorithm.core.evaluator import (
    HypothesisEvaluator,
    BaseEvaluator,
)
from false_feet_algorithm.core.solver import AmoebaInvestigation

__all__ = [
    "Problem",
    "Option",
    "DataPoint",
    "SharedDataPool",
    "EvaluationBranch",
    "BaseBranch",
    "BranchState",
    "HypothesisEvaluator",
    "BaseEvaluator",
    "AmoebaInvestigation",
]
