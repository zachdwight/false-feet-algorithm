#include "../src/amoeba_solver.h"
#include <iostream>
#include <vector>
#include <string>

// ============================================================================
// LLM REASONING ROBUSTNESS: Multi-Path Convergence Analysis
//
// Uses the Amoeba Algorithm to verify LLM reasoning quality:
// - Generate multiple independent reasoning paths for the same problem
// - Evaluate each path's internal consistency and strength
// - Use INVERSE resource allocation (give more scrutiny to weaker paths)
// - Check for convergence across paths → high confidence in reasoning
//
// This addresses: "How do I know my LLM's answer is actually robust?"
// Answer: When multiple independent reasoning approaches converge,
//         that's a strong signal of robustness.
// ============================================================================

Problem setup_llm_reasoning_robustness() {
    Problem problem;
    problem.title = "LLM Reasoning Robustness Analysis";
    problem.description = "Verify LLM answer quality through multi-path reasoning";
    problem.goal = "Achieve convergence across multiple independent reasoning paths";

    // ===== OPTIONS (Reasoning conclusions) =====
    // In this example, we're testing whether an LLM's conclusion "C" is robust
    problem.options = {
        Option{"conclusion_a", "Conclusion A",
               "Derived from step-by-step reasoning",
               "Direct logical progression from premises", 35},

        Option{"conclusion_b", "Conclusion B",
               "Derived from devil's advocate approach",
               "Refutation of opposing views", 40},

        Option{"conclusion_c", "Conclusion C",
               "Derived from constraint-based analysis",
               "Solution satisfying all constraints", 50},

        Option{"conclusion_d", "Conclusion D",
               "Derived from evidence-first analysis",
               "Supported by primary evidence", 45}
    };

    // ===== DATA POINTS (Reasoning quality indicators) =====

    problem.all_data.push_back(DataPoint{
        "path_step_by_step",
        "Step-by-step reasoning leads to C",
        "Logical progression through clear stages converges on C",
        {"conclusion_c"},
        {},
        5
    });

    problem.all_data.push_back(DataPoint{
        "path_devils_advocate",
        "Devil's advocate refutation supports C",
        "Opposing view fails under scrutiny, C remains standing",
        {"conclusion_c"},
        {},
        5
    });

    problem.all_data.push_back(DataPoint{
        "path_constraint_based",
        "Constraint satisfaction points to C",
        "All constraints analyzed; only C satisfies all requirements",
        {"conclusion_c"},
        {},
        5
    });

    problem.all_data.push_back(DataPoint{
        "path_evidence_first",
        "Evidence-first analysis supports C",
        "Primary evidence and data signals point to C",
        {"conclusion_c"},
        {"conclusion_a"},
        4
    });

    problem.all_data.push_back(DataPoint{
        "consistency_measure",
        "All paths show internal consistency",
        "No logical contradictions detected within reasoning chains",
        {"conclusion_c", "conclusion_b"},
        {},
        4
    });

    problem.all_data.push_back(DataPoint{
        "convergence_signal",
        "Multiple independent paths converge",
        "When weak paths are strengthened through iteration, all point to C",
        {"conclusion_c"},
        {"conclusion_a", "conclusion_b"},
        5
    });

    problem.all_data.push_back(DataPoint{
        "strength_reinforcement",
        "Weaker paths strengthen when scrutinized",
        "Inverse resource allocation forces weak reasoning to improve or fail",
        {"conclusion_c"},
        {},
        4
    });

    problem.all_data.push_back(DataPoint{
        "reasoning_robustness",
        "Answer robust under multi-path analysis",
        "Convergence across independent reasoning approaches signals robustness",
        {"conclusion_c"},
        {},
        5
    });

    return problem;
}

// ============================================================================
// MAIN: LLM Reasoning Robustness Verification
// ============================================================================

int main() {
    try {
        std::cout << "\n╔═══════════════════════════════════════════════════════════════════╗\n";
        std::cout << "║                                                                   ║\n";
        std::cout << "║      LLM REASONING ROBUSTNESS: Multi-Path Convergence Analysis    ║\n";
        std::cout << "║                    Using the Amoeba Algorithm                     ║\n";
        std::cout << "║                                                                   ║\n";
        std::cout << "╚═══════════════════════════════════════════════════════════════════╝\n";

        std::cout << "\n📊 SCENARIO:\n";
        std::cout << "An LLM has proposed an answer to a complex reasoning question.\n";
        std::cout << "We verify robustness by testing it through multiple independent\n";
        std::cout << "reasoning paths:\n\n";
        std::cout << "  1. Step-by-step logical progression\n";
        std::cout << "  2. Devil's advocate (refute the opposite)\n";
        std::cout << "  3. Constraint-based analysis\n";
        std::cout << "  4. Evidence-first evaluation\n\n";
        std::cout << "If all paths CONVERGE on the same answer → HIGH CONFIDENCE\n";
        std::cout << "We use INVERSE resource allocation to scrutinize weaker paths.\n\n";

        Problem problem = setup_llm_reasoning_robustness();
        AmoebaInvestigation solver(problem);
        solver.solve();

        std::cout << "\n📋 INTERPRETATION:\n";
        std::cout << "If the algorithm converges on a single conclusion, that reasoning\n";
        std::cout << "is robust. If paths diverge, the LLM's answer needs human review.\n\n";

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
        return 1;
    }

    return 0;
}
