"""
False Feet Algorithm - A novel multi-branch hypothesis evaluation system.

The False Feet Algorithm (also called Amoeba) implements a unique approach
to hypothesis evaluation: instead of giving more resources to strong branches,
it gives more resources to weak branches, forcing them to improve or die off.

When multiple independent reasoning paths converge on the same answer despite
different starting assumptions, this provides a robust confidence signal.

Example:
    >>> from false_feet_algorithm.core import Problem, Option, DataPoint, AmoebaInvestigation
    >>>
    >>> # Define the problem
    >>> problem = Problem(title="Root cause analysis", goal="Find the bug")
    >>> problem.add_option(Option(id="opt1", name="Memory leak"))
    >>> problem.add_data_point(DataPoint(id="d1", title="Memory grows", supports=["opt1"]))
    >>>
    >>> # Solve
    >>> solver = AmoebaInvestigation(problem)
    >>> result = solver.solve()
    >>> print(f"Conclusion: {result.name}")
"""

__version__ = "0.1.0"
__author__ = "Zach Dwight"

from false_feet_algorithm.core import (
    Problem,
    Option,
    DataPoint,
    SharedDataPool,
    EvaluationBranch,
    BaseBranch,
    HypothesisEvaluator,
    BaseEvaluator,
    AmoebaInvestigation,
)

__all__ = [
    "Problem",
    "Option",
    "DataPoint",
    "SharedDataPool",
    "EvaluationBranch",
    "BaseBranch",
    "HypothesisEvaluator",
    "BaseEvaluator",
    "AmoebaInvestigation",
]
