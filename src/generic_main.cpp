#include "amoeba_solver.h"

// ============================================================================
// EXAMPLE PROBLEM: Product Recommendation System
// This example shows how to use the Amoeba Algorithm for any hypothesis
// evaluation problem - not just mysteries!
// ============================================================================

Problem setup_product_recommendation() {
    Problem problem;
    problem.title = "Best Product for Customer";
    problem.description = "Evaluate which product best fits customer needs";
    problem.goal = "Identify the product that satisfies the most important requirements";

    // ===== OPTIONS (Products to evaluate) =====
    problem.options = {
        Option{"product_a", "Premium Pro",
               "High performance, many features, top-tier quality",
               "For power users and professionals", 50},

        Option{"product_b", "Budget Basic",
               "Affordable, reliable, covers core needs",
               "For cost-conscious consumers", 40},

        Option{"product_c", "Eco Green",
               "Sustainable materials, eco-friendly production",
               "For environmentally conscious buyers", 35},

        Option{"product_d", "Custom Lite",
               "Lightweight, portable, single-purpose focused",
               "For mobile and travel use cases", 45}
    };

    // ===== DATA POINTS (Customer requirements/feedback) =====

    problem.all_data.push_back(DataPoint{
        "data_1",
        "Customer needs portability",
        "Customer frequently travels and needs lightweight gear",
        {"product_d"},  // supports
        {"product_a"},  // contradicts
        5
    });

    problem.all_data.push_back(DataPoint{
        "data_2",
        "Customer has tight budget",
        "Budget constraint of $200 maximum",
        {"product_b", "product_d"},
        {"product_a"},
        5
    });

    problem.all_data.push_back(DataPoint{
        "data_3",
        "Eco-conscious values",
        "Customer emphasizes sustainability in all purchases",
        {"product_c"},
        {},
        4
    });

    problem.all_data.push_back(DataPoint{
        "data_4",
        "Needs advanced features",
        "Customer uses professional tools and advanced workflows",
        {"product_a"},
        {"product_b", "product_d"},
        4
    });

    problem.all_data.push_back(DataPoint{
        "data_5",
        "Product A has excellent reviews",
        "95% customer satisfaction rating and industry awards",
        {"product_a"},
        {},
        4
    });

    problem.all_data.push_back(DataPoint{
        "data_6",
        "Product B widely available",
        "In stock at all retailers, same-day delivery options",
        {"product_b"},
        {},
        3
    });

    problem.all_data.push_back(DataPoint{
        "data_7",
        "Product C high cost",
        "Premium pricing due to sustainable sourcing",
        {},
        {"product_c", "product_b"},
        4
    });

    problem.all_data.push_back(DataPoint{
        "data_8",
        "Product D limited features",
        "Single-purpose, cannot expand with add-ons",
        {},
        {"product_a"},
        3
    });

    problem.all_data.push_back(DataPoint{
        "data_9",
        "Customer values durability",
        "Wants product that lasts 5+ years without replacement",
        {"product_a", "product_c"},
        {"product_b"},
        5
    });

    problem.all_data.push_back(DataPoint{
        "data_10",
        "Support and warranty excellent for Premium Pro",
        "5-year warranty, 24/7 support included",
        {"product_a"},
        {},
        4
    });

    return problem;
}

// ============================================================================
// ALTERNATIVE EXAMPLE: Medical Diagnosis
// Shows how the framework adapts to different domains
// ============================================================================

Problem setup_medical_diagnosis() {
    Problem problem;
    problem.title = "Patient Diagnosis";
    problem.description = "Evaluate diagnostic hypotheses based on patient symptoms";
    problem.goal = "Identify the most likely diagnosis given available clinical data";

    // ===== OPTIONS (Possible diagnoses) =====
    problem.options = {
        Option{"diagnosis_a", "Condition A",
               "Common presentation, well-established treatment",
               "Most frequent diagnosis in patient demographics", 45},

        Option{"diagnosis_b", "Condition B",
               "Rare but serious, requires immediate intervention",
               "Life-threatening if missed, excellent prognosis with early treatment", 30},

        Option{"diagnosis_c", "Condition C",
               "Chronic manageable disease, lifestyle modifications help",
               "Affects quality of life significantly if untreated", 35},

        Option{"diagnosis_d", "Benign finding",
               "Not a disease, explains symptoms through other factors",
               "Common in this patient demographic, excellent prognosis", 40}
    };

    // ===== DATA POINTS (Clinical findings) =====
    problem.all_data.push_back(DataPoint{
        "finding_1",
        "Lab test positive for marker X",
        "Elevated level indicates Condition A pathology",
        {"diagnosis_a"},
        {"diagnosis_d"},
        5
    });

    problem.all_data.push_back(DataPoint{
        "finding_2",
        "Imaging shows pattern consistent with B",
        "Specific radiological sign seen only in Condition B",
        {"diagnosis_b"},
        {},
        5
    });

    problem.all_data.push_back(DataPoint{
        "finding_3",
        "Patient reports symptom started gradually",
        "Gradual onset more consistent with Condition C",
        {"diagnosis_c"},
        {"diagnosis_b"},
        4
    });

    problem.all_data.push_back(DataPoint{
        "finding_4",
        "Vital signs all normal",
        "Rules out acute/life-threatening conditions",
        {"diagnosis_d", "diagnosis_c"},
        {"diagnosis_b"},
        5
    });

    problem.all_data.push_back(DataPoint{
        "finding_5",
        "Environmental exposure history",
        "Patient exposed to trigger for Condition A",
        {"diagnosis_a"},
        {},
        3
    });

    problem.all_data.push_back(DataPoint{
        "finding_6",
        "Family history of Condition C",
        "Genetic predisposition increases probability",
        {"diagnosis_c"},
        {},
        4
    });

    return problem;
}

// ============================================================================
// MAIN: Generic Amoeba Algorithm Solver
// ============================================================================

int main() {
    try {
        std::cout << "\n╔═══════════════════════════════════════════════════════════════════╗\n";
        std::cout << "║                                                                   ║\n";
        std::cout << "║     AMOEBA ALGORITHM - Generic Hypothesis Evaluation Framework    ║\n";
        std::cout << "║              Multi-Branch Reasoning with Convergence              ║\n";
        std::cout << "║                                                                   ║\n";
        std::cout << "╚═══════════════════════════════════════════════════════════════════╝\n";

        // Choose which problem to solve
        std::cout << "\nSelect a problem:\n";
        std::cout << "1. Product Recommendation (default)\n";
        std::cout << "2. Medical Diagnosis\n";
        std::cout << "\nUsing: Product Recommendation\n\n";

        Problem problem = setup_product_recommendation();
        // Uncomment below to try medical diagnosis instead:
        // Problem problem = setup_medical_diagnosis();

        AmoebaInvestigation solver(problem);
        solver.solve();

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
        return 1;
    }

    return 0;
}
