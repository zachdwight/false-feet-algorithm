"""
Clinical Diagnosis Example for the False Feet Algorithm.

This example demonstrates how to use the Amoeba algorithm for medical
differential diagnosis. A patient presents with a constellation of symptoms,
and we evaluate competing diagnoses using clinical evidence.

Case Study: A 55-year-old patient with fatigue, weight gain, cold intolerance, and dry skin.
Differential diagnoses: Hypothyroidism, Depression, Anemia

The algorithm uses clinical reasoning to evaluate which diagnosis is most consistent
with the available test results and clinical findings.
"""

import logging
from false_feet_algorithm.core import (
    Problem,
    Option,
    DataPoint,
    BaseBranch,
    BaseEvaluator,
    AmoebaInvestigation,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)


class ClinicalFindingScore:
    """Helper to score clinical findings."""

    # Likelihood ratios for common findings
    # (Real values would come from medical literature)
    LIKELIHOOD_RATIOS = {
        # Hypothyroidism
        "elevated_tsh": {"hypothyroidism": 8.0, "depression": 0.8, "anemia": 0.5},
        "low_t4": {"hypothyroidism": 10.0, "depression": 0.3, "anemia": 0.5},
        "fatigue": {"hypothyroidism": 4.0, "depression": 6.0, "anemia": 5.0},
        "weight_gain": {"hypothyroidism": 8.0, "depression": 3.0, "anemia": 0.3},
        "cold_intolerance": {"hypothyroidism": 9.0, "depression": 1.0, "anemia": 0.5},
        "dry_skin": {"hypothyroidism": 7.0, "depression": 1.5, "anemia": 0.5},
        "constipation": {"hypothyroidism": 5.0, "depression": 2.0, "anemia": 0.5},

        # Depression
        "depressed_mood": {"depression": 10.0, "hypothyroidism": 2.0, "anemia": 0.5},
        "sleep_disturbance": {"depression": 6.0, "hypothyroidism": 3.0, "anemia": 4.0},
        "anhedonia": {"depression": 9.0, "hypothyroidism": 1.0, "anemia": 0.5},
        "normal_tsh": {"depression": 4.0, "hypothyroidism": 0.1, "anemia": 5.0},

        # Anemia
        "low_hemoglobin": {"anemia": 15.0, "hypothyroidism": 0.5, "depression": 0.5},
        "low_ferritin": {"anemia": 10.0, "hypothyroidism": 0.3, "depression": 0.3},
        "pallor": {"anemia": 8.0, "hypothyroidism": 1.0, "depression": 0.5},
        "dyspnea_on_exertion": {"anemia": 6.0, "hypothyroidism": 2.0, "depression": 3.0},
    }


class MedicalDiagnosisBranch(BaseBranch):
    """
    Custom branch for medical diagnosis.

    This branch evaluates a diagnostic hypothesis by:
    1. Examining available test results and clinical findings
    2. Computing likelihood ratios for the diagnosis
    3. Computing a probability using Bayesian reasoning
    """

    def evaluate(self, data_pool) -> float:
        """
        Evaluate the hypothesis (diagnosis) using available evidence.

        Uses likelihood ratios and Bayesian reasoning to score the diagnosis.
        """
        supporting = data_pool.get_supporting_data(self.option.id)
        contradicting = data_pool.get_contradicting_data(self.option.id)

        if not supporting and not contradicting:
            return self.option.initial_score / 100.0

        # Calculate likelihood ratio product
        lr_product = 1.0

        for finding in supporting:
            # Each supporting finding increases the likelihood
            lr_product *= 2.0  # Simple multiplier; real would use actual LRs

        for finding in contradicting:
            # Each contradicting finding decreases the likelihood
            lr_product *= 0.3  # Reduces likelihood ratio

        # Convert to probability (simplified Bayesian)
        base_probability = self.option.initial_score / 100.0
        adjusted_probability = base_probability * lr_product / (1.0 + lr_product)

        # Clamp to 0-1
        score = min(1.0, max(0.0, adjusted_probability))
        self.set_score(score)

        return score

    def propose_data(self, data_pool) -> list[str]:
        """
        Propose the next most useful diagnostic tests.

        Returns ordered list of test IDs to investigate next.
        """
        diagnosis = self.option.id

        # Define what tests to suggest for each diagnosis
        test_proposals = {
            "hypothyroidism": [
                "tsh_test",
                "free_t4_test",
                "antibody_test",
                "metabolic_panel",
            ],
            "depression": [
                "phq9_screening",
                "tsh_test",  # Rule out medical causes
                "vitamin_b12",
                "thyroid_antibodies",
            ],
            "anemia": [
                "cbc_test",
                "iron_studies",
                "b12_folate",
                "blood_smear",
            ],
        }

        # Return tests not yet done
        proposed = []
        for test_id in test_proposals.get(diagnosis, []):
            if not data_pool.has_data(test_id):
                proposed.append(test_id)

        return proposed[:self.state.proposal_slots]


class MedicalEvaluator(BaseEvaluator):
    """
    Custom evaluator using medical reasoning.

    Scores diagnoses based on:
    - Clinical likelihood (base rate)
    - Supporting vs contradicting findings
    - Consistency with patient presentation
    """

    def evaluate(self, branch, data_pool) -> float:
        """Evaluate using medical knowledge."""
        supporting = data_pool.get_supporting_data(branch.option.id)
        contradicting = data_pool.get_contradicting_data(branch.option.id)

        # Clinical likelihood scoring
        # More supporting evidence = higher likelihood
        if not supporting and not contradicting:
            return 0.5  # Neutral with no evidence

        support_count = len(supporting)
        contradiction_count = len(contradicting)
        total_findings = support_count + contradiction_count

        if total_findings == 0:
            return 0.5

        # Score based on evidence ratio
        likelihood = support_count / total_findings

        # Weight by clinical importance
        # (In reality, would weight each finding differently)
        weighted_score = likelihood * 0.8 + 0.2  # Include base rate

        return min(1.0, max(0.0, weighted_score))


def run_clinical_example():
    """Run the clinical diagnosis example."""

    # Create the problem
    problem = Problem(
        title="Differential Diagnosis: Fatigue",
        description="55-year-old with fatigue, weight gain, cold intolerance, dry skin",
        goal="Identify the primary diagnosis"
    )

    # Define differential diagnoses
    problem.add_option(Option(
        id="hypothyroidism",
        name="Hypothyroidism",
        rationale="Classic presentation: fatigue, weight gain, cold intolerance, dry skin",
        initial_score=40
    ))

    problem.add_option(Option(
        id="depression",
        name="Depression",
        rationale="Fatigue is primary symptom; can cause weight gain and anhedonia",
        initial_score=35
    ))

    problem.add_option(Option(
        id="anemia",
        name="Anemia",
        rationale="Fatigue is chief complaint; weight gain less common",
        initial_score=25
    ))

    # Define clinical findings and test results
    # Findings strongly supporting hypothyroidism
    problem.add_data_point(DataPoint(
        id="fatigue",
        title="Chief Complaint: Fatigue",
        description="Patient reports persistent fatigue for 3 months",
        supports=["hypothyroidism", "depression", "anemia"],
        contradicts=[],
        priority=5
    ))

    problem.add_data_point(DataPoint(
        id="weight_gain",
        title="Weight Gain",
        description="10 kg weight gain over 3 months despite normal appetite",
        supports=["hypothyroidism"],
        contradicts=["depression", "anemia"],
        priority=5
    ))

    problem.add_data_point(DataPoint(
        id="cold_intolerance",
        title="Cold Intolerance",
        description="Patient complains of feeling cold, wears heavy clothing indoors",
        supports=["hypothyroidism"],
        contradicts=["depression", "anemia"],
        priority=4
    ))

    problem.add_data_point(DataPoint(
        id="dry_skin",
        title="Dry Skin",
        description="Generalized dry skin and coarse hair noted on exam",
        supports=["hypothyroidism"],
        contradicts=["depression", "anemia"],
        priority=3
    ))

    problem.add_data_point(DataPoint(
        id="constipation",
        title="Constipation",
        description="Patient reports constipation, 1-2 bowel movements per week",
        supports=["hypothyroidism"],
        contradicts=["depression", "anemia"],
        priority=3
    ))

    # Test results
    problem.add_data_point(DataPoint(
        id="tsh_test",
        title="TSH Level: Elevated",
        description="TSH 12.5 mIU/L (normal <4.5)",
        supports=["hypothyroidism"],
        contradicts=["depression"],
        priority=5
    ))

    problem.add_data_point(DataPoint(
        id="free_t4",
        title="Free T4: Low",
        description="Free T4 0.8 ng/dL (normal 0.8-1.8), borderline low",
        supports=["hypothyroidism"],
        contradicts=["depression"],
        priority=4
    ))

    problem.add_data_point(DataPoint(
        id="cbc_normal",
        title="Complete Blood Count: Normal",
        description="Hemoglobin 13.5 g/dL, no anemia",
        supports=["depression", "hypothyroidism"],
        contradicts=["anemia"],
        priority=4
    ))

    problem.add_data_point(DataPoint(
        id="mood_assessment",
        title="Mood Assessment: Euthymic",
        description="Patient denies depressed mood, enjoys activities, good sleep",
        supports=["hypothyroidism", "anemia"],
        contradicts=["depression"],
        priority=4
    ))

    # Run the solver with custom branch and evaluator
    logger.info("Starting clinical differential diagnosis...")
    logger.info("=" * 60)

    solver = AmoebaInvestigation(
        problem,
        max_iterations=20,
        max_pool_size=100,
        starvation_threshold=10,
        evaluator=MedicalEvaluator(),
        branch_class=MedicalDiagnosisBranch,
    )

    result = solver.solve()

    logger.info("=" * 60)
    if result:
        logger.info(f"DIAGNOSIS: {result.name}")
        logger.info(f"Confidence: {result.initial_score}%")
        logger.info(f"\nSupporting Evidence:")
        for ev_id in solver.get_supporting_evidence():
            ev = solver.data_pool.get_data(ev_id)
            if ev:
                logger.info(f"  ✓ {ev.title}: {ev.description}")
    else:
        logger.warning("Could not reach diagnostic consensus")

    # Show final branch scores
    logger.info(f"\nFinal Scores:")
    for branch in solver.get_branches():
        status = "alive" if branch.is_alive() else "culled"
        logger.info(f"  {branch.option.name}: {branch.get_score():.3f} ({status})")


if __name__ == "__main__":
    run_clinical_example()
