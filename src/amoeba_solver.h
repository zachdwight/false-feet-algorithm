#ifndef AMOEBA_SOLVER_H
#define AMOEBA_SOLVER_H

#include "amoeba_framework.h"
#include <iomanip>
#include <chrono>

// ============================================================================
// AMOEBA ALGORITHM SOLVER (Generic Implementation)
// ============================================================================

class AmoebaInvestigation {
public:
    AmoebaInvestigation(const Problem& problem)
        : problem(problem), max_iterations(15), pool_budget(20),
          proposal_budget_per_round(8), improvement_threshold(0.02f),
          starvation_rounds(3) {
        evaluator = std::make_unique<HypothesisEvaluator>();
    }

    void solve() {
        std::cout << "\n" << std::string(70, '=') << "\n";
        std::cout << "🧬 AMOEBA ALGORITHM SOLVER\n";
        std::cout << "Problem: " << problem.title << "\n";
        std::cout << "Goal: " << problem.goal << "\n";
        std::cout << std::string(70, '=') << "\n\n";

        std::cout << "Total options: " << problem.options.size() << "\n";
        std::cout << "Total data points: " << problem.all_data.size() << "\n\n";

        initialize_branches();

        int iteration = 0;
        while (iteration < max_iterations && !check_convergence()) {
            iteration++;

            std::cout << "📋 ROUND " << iteration << "\n";
            std::cout << std::string(70, '-') << "\n";

            // Phase A: Evaluation
            phase_evaluation();
            evaluate_branch();
            print_branch_scores();

            // Phase B: Resource Allocation
            phase_resource_allocation();

            // Phase C: Data Proposals & Pooling
            phase_data_gathering();
            print_data_pool();

            // Phase D: Starvation & Culling
            phase_starvation_culling();

            std::cout << "\n";
        }

        print_solution();
    }

private:
    const Problem& problem;
    std::vector<EvaluationBranch> branches;
    SharedDataPool data_pool;
    std::unique_ptr<HypothesisEvaluator> evaluator;

    int max_iterations;
    int pool_budget;
    int proposal_budget_per_round;
    float improvement_threshold;
    int starvation_rounds;

    // ========== PHASE A: Evaluation ==========
    void phase_evaluation() {
        for (auto& branch : branches) {
            if (branch.get_is_alive()) {
                branch.evaluate(data_pool);
            }
        }
    }

    void evaluate_branch() {
        for (auto& branch : branches) {
            if (branch.get_is_alive()) {
                float prev_score = branch.get_score();
                float new_score = evaluator->evaluate(branch, data_pool, problem);
                branch.set_score(new_score);

                if (new_score > prev_score + improvement_threshold) {
                    branch.reset_improvement_counter();
                    std::cout << "  ✨ Branch #" << branch.get_id()
                              << " made progress!\n";
                } else {
                    branch.increment_improvement_counter();
                }
            }
        }
    }

    void print_branch_scores() {
        std::cout << "\n  Hypothesis Scores:\n";
        for (const auto& branch : branches) {
            if (branch.get_is_alive()) {
                std::cout << "    Branch #" << branch.get_id()
                          << " (" << branch.get_hypothesis().chosen_option << "): "
                          << std::fixed << std::setprecision(2) << branch.get_score()
                          << "/1.00";
                if (branch.get_improvement_counter() > 0) {
                    std::cout << " [no progress x" << branch.get_improvement_counter() << "]";
                }
                std::cout << "\n";
            }
        }
    }

    // ========== PHASE B: Resource Allocation ==========
    void phase_resource_allocation() {
        // Rank branches by score
        std::vector<std::pair<float, int>> ranked;
        for (size_t i = 0; i < branches.size(); i++) {
            if (branches[i].get_is_alive()) {
                ranked.push_back({branches[i].get_score(), i});
            }
        }
        std::sort(ranked.rbegin(), ranked.rend());

        // Inverse allocation: weakest get more slots
        for (size_t rank = 0; rank < ranked.size(); rank++) {
            int idx = ranked[rank].second;
            int slots = std::max(1, proposal_budget_per_round - static_cast<int>(rank) * 2);
            branches[idx].set_proposal_slots(slots);
        }

        std::cout << "\n  Resource Allocation (inverse by rank):\n";
        for (size_t rank = 0; rank < ranked.size(); rank++) {
            int idx = ranked[rank].second;
            std::cout << "    Branch #" << branches[idx].get_id()
                      << " → " << branches[idx].get_proposal_slots() << " data slots\n";
        }
    }

    // ========== PHASE C: Data Gathering ==========
    void phase_data_gathering() {
        std::vector<std::string> proposals;

        for (auto& branch : branches) {
            if (branch.get_is_alive() && branch.get_proposal_slots() > 0) {
                std::vector<std::string> branch_proposals;
                branch.propose_data_to_examine(problem, branch_proposals);
                proposals.insert(proposals.end(),
                               branch_proposals.begin(),
                               branch_proposals.end());
            }
        }

        // Deduplicate and add to pool (respecting budget)
        std::set<std::string> unique_proposals(proposals.begin(), proposals.end());
        int slots_available = pool_budget - data_pool.size();

        std::cout << "\n  Data Gathering:\n";
        std::cout << "    Proposals: " << unique_proposals.size() << "\n";
        std::cout << "    Pool space: " << slots_available << "/" << pool_budget << "\n";

        int added = 0;
        for (const auto& data_id : unique_proposals) {
            if (added >= slots_available) break;

            for (const auto& data : problem.all_data) {
                if (data.id == data_id) {
                    data_pool.add_data(data);
                    std::cout << "    + Added: " << data.title << "\n";
                    added++;
                    break;
                }
            }
        }
    }

    void print_data_pool() {
        std::cout << "\n  Current Data Pool (" << data_pool.size()
                  << "/" << pool_budget << "):\n";
        for (const auto& data : data_pool.get_all()) {
            std::cout << "    • " << data.title << "\n";
        }
    }

    // ========== PHASE D: Starvation & Culling ==========
    void phase_starvation_culling() {
        std::cout << "\n  Starvation Check:\n";
        for (auto& branch : branches) {
            if (branch.get_is_alive()) {
                if (branch.get_improvement_counter() >= starvation_rounds) {
                    int new_slots = std::max(0, branch.get_proposal_slots() - 1);
                    branch.set_proposal_slots(new_slots);

                    if (new_slots == 0) {
                        branch.set_alive(false);
                        std::cout << "    ☠️  Branch #" << branch.get_id()
                                  << " starved to death (option: "
                                  << branch.get_hypothesis().chosen_option << ")\n";
                    } else {
                        std::cout << "    📉 Branch #" << branch.get_id()
                                  << " losing resources (" << new_slots << " left)\n";
                    }
                }
            }
        }
    }

    // ========== Convergence Check ==========
    bool check_convergence() {
        std::vector<std::string> answers;
        for (const auto& branch : branches) {
            if (branch.get_is_alive() && !branch.get_hypothesis().chosen_option.empty()) {
                answers.push_back(branch.get_hypothesis().chosen_option);
            }
        }

        if (answers.size() < 2) return false;  // Need at least 2 branches to converge

        std::string first = answers[0];
        bool all_same = std::all_of(answers.begin(), answers.end(),
                                   [&first](const std::string& a) { return a == first; });

        if (all_same) {
            std::cout << "\n🎯 CONVERGENCE ACHIEVED!\n";
            std::cout << "All surviving branches agree: " << first << " is the answer!\n";
            return true;
        }

        return false;
    }

    // ========== Solution Output ==========
    void print_solution() {
        std::cout << "\n" << std::string(70, '=') << "\n";
        std::cout << "🔎 ANALYSIS COMPLETE\n";
        std::cout << std::string(70, '=') << "\n\n";

        std::vector<EvaluationBranch*> survivors;
        for (auto& branch : branches) {
            if (branch.get_is_alive()) {
                survivors.push_back(&branch);
            }
        }

        if (survivors.empty()) {
            std::cout << "All hypotheses were eliminated. Inconclusive result.\n";
            return;
        }

        std::string conclusion = survivors[0]->get_hypothesis().chosen_option;

        std::cout << "💼 CONCLUSION:\n";
        std::cout << "Selected option: " << conclusion << "\n\n";

        std::cout << "📖 Supporting Data:\n";
        for (const auto& survivor : survivors) {
            const auto& hyp = survivor->get_hypothesis();
            std::cout << "\nBranch #" << survivor->get_id() << " reasoning:\n";
            std::cout << "  • Option: " << hyp.chosen_option << "\n";
            std::cout << "  • Rationale: " << hyp.reasoning << "\n";
            std::cout << "  • Data point count: " << hyp.supporting_data.size() << "\n";

            std::cout << "  • Supporting data:\n";
            for (const auto& data_id : hyp.supporting_data) {
                if (data_pool.has_data(data_id)) {
                    const auto& data = data_pool.get_data(data_id);
                    std::cout << "      ✓ " << data.title << " ("
                              << data.description << ")\n";
                }
            }
        }

        std::cout << "\n" << std::string(70, '=') << "\n";
        std::cout << "Problem solved by the Amoeba Algorithm\n";
        std::cout << "Survivors: " << survivors.size() << " reasoning branches\n";
        std::cout << std::string(70, '=') << "\n\n";
    }

    void initialize_branches() {
        for (int i = 0; i < 4; i++) {
            branches.emplace_back(i, problem);
        }
        std::cout << "🧬 Spawned " << branches.size()
                  << " evaluation branches\n\n";
    }
};

#endif // AMOEBA_SOLVER_H
