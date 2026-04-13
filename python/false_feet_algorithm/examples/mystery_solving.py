"""
Classic Mystery Solving Example for the False Feet Algorithm.

This example demonstrates the algorithm solving a classic logic puzzle:
"The Case of the Vanished Necklace"

Four suspects, each with means, motive, and opportunity. Through
investigation and clue discovery, the algorithm converges on
the true culprit.
"""

import logging
from typing import List
from false_feet_algorithm.core import (
    Problem,
    Option,
    DataPoint,
    BaseBranch,
    BaseEvaluator,
    AmoebaInvestigation,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)


class InvestigationBranch(BaseBranch):
    """
    Custom branch for mystery solving.

    Investigates a suspect by:
    1. Examining evidence for/against them
    2. Assessing strength of motive and opportunity
    3. Scoring consistency with all clues
    """

    def evaluate(self, data_pool) -> float:
        """Evaluate how likely this suspect is guilty."""
        suspect_id = self.option.id

        supporting = data_pool.get_supporting_data(suspect_id)
        contradicting = data_pool.get_contradicting_data(suspect_id)

        if not supporting and not contradicting:
            return self.option.initial_score / 100.0

        # Simple scoring: more supporting clues, fewer contradictions
        support_weight = len(supporting) * 1.5
        contradiction_weight = len(contradicting) * 2.0

        total_weight = support_weight - contradiction_weight
        base_score = self.option.initial_score / 100.0

        # Normalize (keep in 0-1 range)
        if total_weight > 0:
            score = min(1.0, base_score + (total_weight / 10.0))
        else:
            score = max(0.0, base_score + (total_weight / 10.0))

        self.set_score(score)
        return score

    def propose_data(self, data_pool) -> List[str]:
        """Propose the next clue to investigate."""
        # Suggest clues that would distinguish between suspects
        clue_suggestions = {
            "alice": ["clue_alibi", "clue_motive_alice", "clue_fingerprint"],
            "bob": ["clue_location", "clue_motive_bob", "clue_witness"],
            "carol": ["clue_opportunity", "clue_motive_carol", "clue_timeline"],
            "diana": ["clue_suspicious", "clue_motive_diana", "clue_knowledge"],
        }

        proposed = []
        for clue_id in clue_suggestions.get(self.option.id, []):
            if not data_pool.has_data(clue_id):
                proposed.append(clue_id)

        return proposed[:self.state.proposal_slots]


class MysteryEvaluator(BaseEvaluator):
    """Evaluate guilt based on motive, means, and opportunity."""

    def evaluate(self, branch, data_pool) -> float:
        """Score based on evidence quality and consistency."""
        supporting = data_pool.get_supporting_data(branch.option.id)
        contradicting = data_pool.get_contradicting_data(branch.option.id)

        if not supporting and not contradicting:
            return 0.5

        # Weight evidence by priority (priority = importance)
        support_score = sum(d.priority for d in supporting) / 25.0  # Normalize
        contradiction_score = sum(d.priority for d in contradicting) / 25.0

        # Final score
        score = support_score / (support_score + contradiction_score + 0.1)
        return min(1.0, max(0.0, score))


def run_mystery_example():
    """Run the classic mystery solving example."""

    # Create the problem
    problem = Problem(
        title="The Case of the Vanished Necklace",
        description="A valuable diamond necklace vanished from the mansion. Four suspects.",
        goal="Identify the culprit"
    )

    # Define suspects (options)
    problem.add_option(Option(
        id="alice",
        name="Alice (The Maid)",
        rationale="Had access to all rooms, financial problems",
        initial_score=40
    ))

    problem.add_option(Option(
        id="bob",
        name="Bob (The Butler)",
        rationale="Guards the valuables, recently dismissed",
        initial_score=35
    ))

    problem.add_option(Option(
        id="carol",
        name="Carol (The Gardener)",
        rationale="Was in the mansion that day, needs money",
        initial_score=15
    ))

    problem.add_option(Option(
        id="diana",
        name="Diana (The Guest)",
        rationale="Visiting family member, strangers sometimes steal",
        initial_score=10
    ))

    # Define clues (data points)

    # Clues supporting Alice
    problem.add_data_point(DataPoint(
        id="clue_1",
        title="Maid's Access",
        description="Alice had a key to every room in the mansion",
        supports=["alice"],
        contradicts=["carol", "diana"],
        priority=4
    ))

    problem.add_data_point(DataPoint(
        id="clue_2",
        title="Financial Motive",
        description="Alice was behind on rent, gambling debts discovered",
        supports=["alice"],
        contradicts=["carol", "diana"],
        priority=5
    ))

    # Clues supporting Bob
    problem.add_data_point(DataPoint(
        id="clue_3",
        title="Security Knowledge",
        description="Bob knows security system codes and vulnerabilities",
        supports=["bob"],
        contradicts=[],
        priority=3
    ))

    problem.add_data_point(DataPoint(
        id="clue_4",
        title="Resentment",
        description="Bob was recently fired, has expressed bitterness",
        supports=["bob"],
        contradicts=["diana"],
        priority=4
    ))

    # Clues contradicting Alice
    problem.add_data_point(DataPoint(
        id="clue_5",
        title="Alibi - Witnessed",
        description="Multiple witnesses saw Alice in the kitchen all morning",
        supports=[],
        contradicts=["alice"],
        priority=5
    ))

    # Clues about location
    problem.add_data_point(DataPoint(
        id="clue_6",
        title="Theft Time Window",
        description="Necklace stolen between 10-11 AM when doors were locked",
        supports=["alice", "bob"],
        contradicts=["carol", "diana"],
        priority=4
    ))

    # The key clue
    problem.add_data_point(DataPoint(
        id="clue_7",
        title="Fingerprints Found",
        description="Fresh fingerprints on display case match Alice's records",
        supports=["alice"],
        contradicts=["bob", "carol", "diana"],
        priority=5
    ))

    # Run the solver
    logger.info("Investigating the vanished necklace...")
    logger.info("=" * 60)

    solver = AmoebaInvestigation(
        problem,
        max_iterations=30,
        max_pool_size=50,
        starvation_threshold=8,
        evaluator=MysteryEvaluator(),
        branch_class=InvestigationBranch,
    )

    result = solver.solve()

    logger.info("=" * 60)
    if result:
        logger.info(f"CULPRIT IDENTIFIED: {result.name}")
        logger.info(f"Initial suspicion level: {result.initial_score}%")
        logger.info("\nEvidence against the suspect:")
        for ev_id in solver.get_supporting_evidence():
            ev = solver.data_pool.get_data(ev_id)
            if ev:
                logger.info(f"  ✓ {ev.title}: {ev.description}")
    else:
        logger.warning("Investigation inconclusive")

    # Show final scores
    logger.info("\nFinal Suspicion Levels:")
    for branch in sorted(solver.get_branches(), key=lambda b: b.get_score(), reverse=True):
        status = "alive" if branch.is_alive() else "cleared"
        logger.info(f"  {branch.option.name}: {branch.get_score():.1%} ({status})")


if __name__ == "__main__":
    run_mystery_example()
