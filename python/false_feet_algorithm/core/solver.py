"""
Main solver orchestrator for the False Feet Algorithm.

AmoebaInvestigation implements the 6-phase loop that orchestrates multiple
independent branches competing to find the best solution.
"""

import logging
from typing import List, Optional, Type
from false_feet_algorithm.core.problem import Problem, Option, SharedDataPool
from false_feet_algorithm.core.branch import EvaluationBranch
from false_feet_algorithm.core.evaluator import HypothesisEvaluator

logger = logging.getLogger(__name__)


class AmoebaInvestigation:
    """
    Main solver implementing the False Feet Algorithm.

    The algorithm runs iteratively through 6 phases:
    1. Investigation - Branches evaluate current evidence
    2. Evaluation - All branches scored
    3. Resource Allocation - Weakest branches get more proposal slots (inverse ranking)
    4. Evidence Gathering - Branches propose new data to investigate
    5. Starvation & Culling - Non-improving branches are removed
    6. Convergence Check - Stop if all branches agree or max iterations reached

    The key innovation: weak branches get MORE resources (proposal slots),
    forcing them to improve or die off. When multiple independent paths
    converge on the same answer despite different starting assumptions,
    this provides a robust confidence signal.
    """

    def __init__(
        self,
        problem: Problem,
        max_iterations: int = 100,
        max_pool_size: int = 500,
        starvation_threshold: int = 5,
        evaluator: Optional[HypothesisEvaluator] = None,
        branch_class: Optional[Type[EvaluationBranch]] = None,
    ):
        """
        Initialize the solver.

        Args:
            problem: The problem to solve
            max_iterations: Maximum iterations (default 100)
            max_pool_size: Maximum evidence points in pool (default 500)
            starvation_threshold: Iterations before branch starves (default 5)
            evaluator: Custom evaluator (default HypothesisEvaluator)
            branch_class: Custom branch class (default EvaluationBranch)
        """
        is_valid, error_msg = problem.validate()
        if not is_valid:
            raise ValueError(f"Invalid problem: {error_msg}")

        self.problem = problem
        self.max_iterations = max_iterations
        self.max_pool_size = max_pool_size
        self.starvation_threshold = starvation_threshold

        # Initialize evaluator
        self.evaluator = evaluator or HypothesisEvaluator()

        # Initialize branch class
        self.branch_class = branch_class or EvaluationBranch

        # Initialize data pool
        self.data_pool = SharedDataPool()
        for data_point in problem.data_points:
            self.data_pool.add_data(data_point)

        # Initialize branches (one per option)
        self.branches: List[EvaluationBranch] = []
        for idx, option in enumerate(problem.options):
            branch = self.branch_class(idx, option)
            branch.state.iteration_created = 0
            self.branches.append(branch)

        # Tracking
        self.iteration = 0
        self.conclusion: Optional[Option] = None
        self.supporting_evidence: List[str] = []

    def solve(self) -> Optional[Option]:
        """
        Run the Amoeba algorithm until convergence or max iterations.

        Returns:
            The winning Option if converged, None if no clear winner
        """
        logger.info(f"Starting Amoeba investigation with {len(self.branches)} branches")

        for self.iteration in range(self.max_iterations):
            logger.debug(f"--- Iteration {self.iteration} ---")

            # Phase A: Investigation
            self._phase_investigation()

            # Phase B: Evaluation
            self._phase_evaluation()

            # Phase C: Resource Allocation
            self._phase_resource_allocation()

            # Phase D: Evidence Gathering
            self._phase_evidence_gathering()

            # Phase E: Starvation & Culling
            self._phase_starvation_culling()

            # Phase F: Convergence Check
            converged, winner = self._phase_convergence_check()
            if converged:
                self.conclusion = winner
                logger.info(f"Converged on {winner.name} after {self.iteration + 1} iterations")
                self._determine_supporting_evidence()
                return winner

            # Status update
            alive_count = sum(1 for b in self.branches if b.is_alive())
            logger.info(f"Iteration {self.iteration}: {alive_count} branches alive, "
                       f"pool size: {self.data_pool.size()}")

        logger.warning(f"Max iterations ({self.max_iterations}) reached without convergence")
        # Return the highest-scoring option
        alive_branches = [b for b in self.branches if b.is_alive()]
        if alive_branches:
            winner = max(alive_branches, key=lambda b: b.get_score())
            self.conclusion = winner.option
            logger.info(f"Best option: {winner.option.name} (score: {winner.get_score():.3f})")
            self._determine_supporting_evidence()
            return winner.option

        return None

    def _phase_investigation(self) -> None:
        """Phase A: Each branch evaluates the current evidence pool."""
        for branch in self.branches:
            if not branch.is_alive():
                continue
            try:
                score = branch.evaluate(self.data_pool)
                branch.set_score(score)
                logger.debug(f"{branch.get_summary()}")
            except Exception as e:
                logger.error(f"Error evaluating branch {branch.branch_id}: {e}")
                branch.kill()

    def _phase_evaluation(self) -> None:
        """Phase B: Evaluate all branches using the evaluator."""
        for branch in self.branches:
            if not branch.is_alive():
                continue
            try:
                score = self.evaluator.evaluate(branch, self.data_pool)
                branch.set_score(score)
                logger.debug(f"Evaluator: {branch.get_summary()}")
            except Exception as e:
                logger.error(f"Error in evaluator for branch {branch.branch_id}: {e}")
                branch.kill()

    def _phase_resource_allocation(self) -> None:
        """
        Phase C: Allocate proposal slots (inverse ranking).

        Weakest branches get MORE slots, forcing them to propose more evidence.
        This is the key innovation of the algorithm.
        """
        alive_branches = [b for b in self.branches if b.is_alive()]
        if not alive_branches:
            return

        # Sort by score (ascending - weakest first)
        sorted_branches = sorted(alive_branches, key=lambda b: b.get_score())

        # Allocate slots inversely: weakest gets most
        for rank, branch in enumerate(sorted_branches):
            # Allocation formula: weakest (rank 0) gets most slots
            max_slots = len(sorted_branches)
            slots = max_slots - rank
            branch.state.proposal_slots = max(1, slots)
            logger.debug(f"Branch {branch.branch_id}: {slots} proposal slots")

    def _phase_evidence_gathering(self) -> None:
        """
        Phase D: Branches propose new evidence to add to the pool.

        Proposals are deduplicated before adding to the pool.
        """
        all_proposals = {}  # Dict to avoid duplicates: data_id -> DataPoint

        for branch in self.branches:
            if not branch.is_alive() or branch.state.proposal_slots <= 0:
                continue

            try:
                proposed_ids = branch.propose_data(self.data_pool)
                # Take only up to proposal_slots
                proposed_ids = proposed_ids[: branch.state.proposal_slots]
                logger.debug(f"Branch {branch.branch_id} proposed: {proposed_ids}")
                # Note: In real usage, these would be actual DataPoint objects
                # For this base implementation, we assume IDs refer to known data points
                branch.state.proposed_data_ids.extend(proposed_ids)
            except Exception as e:
                logger.error(f"Error in proposal phase for branch {branch.branch_id}: {e}")

        # In a real scenario, branches would propose new DataPoint objects
        # and we'd add them here. This base implementation mainly tracks proposals.

    def _phase_starvation_culling(self) -> None:
        """
        Phase E: Remove branches that aren't improving.

        Branches that don't improve for starvation_threshold iterations are killed.
        """
        for branch in self.branches:
            if not branch.is_alive():
                continue

            # Check if this branch improved
            old_score = branch.state.score
            # Re-evaluate to see if it improved
            try:
                new_score = self.evaluator.evaluate(branch, self.data_pool)
                improvement = new_score - old_score

                if improvement > 0.001:  # Small improvement threshold
                    branch.reset_improvement_counter()
                    branch.set_score(new_score)
                else:
                    branch.increment_improvement_counter()
                    if branch.state.improvement_counter >= self.starvation_threshold:
                        branch.kill()
                        logger.debug(f"Culled branch {branch.branch_id} (no improvement)")
            except Exception as e:
                logger.error(f"Error in culling phase for branch {branch.branch_id}: {e}")
                branch.kill()

    def _phase_convergence_check(self) -> tuple[bool, Optional[Option]]:
        """
        Phase F: Check if all alive branches agree on the same option.

        Returns:
            Tuple of (converged, winning_option)
        """
        alive_branches = [b for b in self.branches if b.is_alive()]

        if not alive_branches:
            return False, None

        if len(alive_branches) == 1:
            # Only one branch left
            return True, alive_branches[0].option

        # Check if all alive branches support the same option
        first_option = alive_branches[0].option
        all_agree = all(b.option == first_option for b in alive_branches)

        if all_agree:
            return True, first_option

        return False, None

    def _determine_supporting_evidence(self) -> None:
        """Collect evidence that supports the conclusion."""
        if not self.conclusion:
            return

        supporting = self.data_pool.get_supporting_data(self.conclusion.id)
        self.supporting_evidence = [d.id for d in supporting]

    def get_conclusion(self) -> Optional[Option]:
        """Get the algorithm's conclusion."""
        return self.conclusion

    def get_supporting_evidence(self) -> List[str]:
        """Get IDs of evidence supporting the conclusion."""
        return self.supporting_evidence

    def get_branches(self) -> List[EvaluationBranch]:
        """Get all branches."""
        return self.branches

    def get_alive_branches(self) -> List[EvaluationBranch]:
        """Get all alive branches."""
        return [b for b in self.branches if b.is_alive()]

    def get_data_pool(self) -> SharedDataPool:
        """Get the shared evidence pool."""
        return self.data_pool
