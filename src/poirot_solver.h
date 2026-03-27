#ifndef POIROT_SOLVER_H
#define POIROT_SOLVER_H

#include "poirot_mystery.h"
#include <iomanip>
#include <chrono>

// ============================================================================
// MYSTERY SOLVER (Amoeba Algorithm Implementation)
// ============================================================================

class MysteryInvestigation {
public:
    MysteryInvestigation(const MysteryScenario& scenario)
        : scenario(scenario), max_iterations(15), pool_budget(20),
          proposal_budget_per_round(8), improvement_threshold(0.02f),
          starvation_rounds(3) {
        evaluator = std::make_unique<MysteryEvaluator>();
    }
    
    void solve() {
        std::cout << "\n" << std::string(70, '=') << "\n";
        std::cout << "🔍 HERCULE POIROT'S MYSTERY SOLVER 🔍\n";
        std::cout << "Case: " << scenario.title << "\n";
        std::cout << "Victim: " << scenario.victim << "\n";
        std::cout << "Crime: " << scenario.crime << "\n";
        std::cout << std::string(70, '=') << "\n\n";
        
        std::cout << "Total suspects: " << scenario.suspects.size() << "\n";
        std::cout << "Total evidence: " << scenario.all_evidence.size() << "\n\n";
        
        initialize_branches();
        
        int iteration = 0;
        while (iteration < max_iterations && !check_convergence()) {
            iteration++;
            
            std::cout << "📋 ROUND " << iteration << "\n";
            std::cout << std::string(70, '-') << "\n";
            
            // Phase A: Investigation
            phase_investigation();
            
            // Phase B: Evaluation
            phase_evaluation();
            print_branch_scores();
            
            // Phase C: Resource Allocation
            phase_resource_allocation();
            
            // Phase D: Evidence Proposals & Pooling
            phase_evidence_gathering();
            print_evidence_pool();
            
            // Phase E: Starvation & Culling
            phase_starvation_culling();
            
            std::cout << "\n";
        }
        
        print_solution();
    }
    
private:
    const MysteryScenario& scenario;
    std::vector<InvestigativeBranch> branches;
    SharedEvidencePool evidence_pool;
    std::unique_ptr<MysteryEvaluator> evaluator;
    
    int max_iterations;
    int pool_budget;
    int proposal_budget_per_round;
    float improvement_threshold;
    int starvation_rounds;
    
    // ========== PHASE A: Investigation ==========
    void phase_investigation() {
        for (auto& branch : branches) {
            if (branch.get_is_alive()) {
                branch.investigate(evidence_pool);
            }
        }
    }
    
    // ========== PHASE B: Evaluation ==========
    void phase_evaluation() {
        for (auto& branch : branches) {
            if (branch.get_is_alive()) {
                float prev_score = branch.get_score();
                float new_score = evaluator->evaluate(branch, evidence_pool, scenario);
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
        std::cout << "\n  Theory Scores:\n";
        for (const auto& branch : branches) {
            if (branch.get_is_alive()) {
                std::cout << "    Branch #" << branch.get_id() 
                          << " (" << branch.get_theory().prime_suspect << "): "
                          << std::fixed << std::setprecision(2) << branch.get_score()
                          << "/1.00";
                if (branch.get_improvement_counter() > 0) {
                    std::cout << " [no progress x" << branch.get_improvement_counter() << "]";
                }
                std::cout << "\n";
            }
        }
    }
    
    // ========== PHASE C: Resource Allocation ==========
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
                      << " → " << branches[idx].get_proposal_slots() << " evidence slots\n";
        }
    }
    
    // ========== PHASE D: Evidence Gathering ==========
    void phase_evidence_gathering() {
        std::vector<std::string> proposals;
        
        for (auto& branch : branches) {
            if (branch.get_is_alive() && branch.get_proposal_slots() > 0) {
                std::vector<std::string> branch_proposals;
                branch.propose_evidence_to_investigate(scenario, branch_proposals);
                proposals.insert(proposals.end(), 
                               branch_proposals.begin(), 
                               branch_proposals.end());
            }
        }
        
        // Deduplicate and add to pool (respecting budget)
        std::set<std::string> unique_proposals(proposals.begin(), proposals.end());
        int slots_available = pool_budget - evidence_pool.size();
        
        std::cout << "\n  Evidence Gathering:\n";
        std::cout << "    Proposals: " << unique_proposals.size() << "\n";
        std::cout << "    Pool space: " << slots_available << "/" << pool_budget << "\n";
        
        int added = 0;
        for (const auto& evidence_id : unique_proposals) {
            if (added >= slots_available) break;
            
            bool found = false;
            for (const auto& evidence : scenario.all_evidence) {
                if (evidence.id == evidence_id) {
                    evidence_pool.add_evidence(evidence);
                    std::cout << "    + Added: " << evidence.title << "\n";
                    added++;
                    found = true;
                    break;
                }
            }
        }
    }
    
    void print_evidence_pool() {
        std::cout << "\n  Current Evidence Pool (" << evidence_pool.size() 
                  << "/" << pool_budget << "):\n";
        for (const auto& evidence : evidence_pool.get_all()) {
            std::cout << "    • " << evidence.title << "\n";
        }
    }
    
    // ========== PHASE E: Starvation & Culling ==========
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
                                  << " starved to death (theory: " 
                                  << branch.get_theory().prime_suspect << ")\n";
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
            if (branch.get_is_alive() && !branch.get_theory().prime_suspect.empty()) {
                answers.push_back(branch.get_theory().prime_suspect);
            }
        }
        
        if (answers.size() < 2) return false;  // Need at least 2 branches to converge
        
        std::string first = answers[0];
        bool all_same = std::all_of(answers.begin(), answers.end(),
                                   [&first](const std::string& a) { return a == first; });
        
        if (all_same) {
            std::cout << "\n🎯 CONVERGENCE ACHIEVED!\n";
            std::cout << "All surviving branches agree: " << first << " is guilty!\n";
            return true;
        }
        
        return false;
    }
    
    // ========== Solution Output ==========
    void print_solution() {
        std::cout << "\n" << std::string(70, '=') << "\n";
        std::cout << "🔎 INVESTIGATION COMPLETE\n";
        std::cout << std::string(70, '=') << "\n\n";
        
        std::vector<InvestigativeBranch*> survivors;
        for (auto& branch : branches) {
            if (branch.get_is_alive()) {
                survivors.push_back(&branch);
            }
        }
        
        if (survivors.empty()) {
            std::cout << "All theories were eliminated. Case inconclusive.\n";
            return;
        }
        
        std::string conclusion = survivors[0]->get_theory().prime_suspect;
        
        std::cout << "💼 VERDICT:\n";
        std::cout << "The guilty party is: " << conclusion << "\n\n";
        
        std::cout << "📖 Supporting Evidence:\n";
        for (const auto& survivor : survivors) {
            const auto& theory = survivor->get_theory();
            std::cout << "\nBranch #" << survivor->get_id() << " reasoning:\n";
            std::cout << "  • Suspect: " << theory.prime_suspect << "\n";
            std::cout << "  • Motive: " << theory.motive << "\n";
            std::cout << "  • Evidence count: " << theory.supporting_evidence.size() << "\n";
            
            std::cout << "  • Evidence details:\n";
            for (const auto& evi_id : theory.supporting_evidence) {
                if (evidence_pool.has_evidence(evi_id)) {
                    const auto& evi = evidence_pool.get_evidence(evi_id);
                    std::cout << "      ✓ " << evi.title << " (" 
                              << evi.description << ")\n";
                }
            }
        }
        
        std::cout << "\n" << std::string(70, '=') << "\n";
        std::cout << "Case solved by the Amoeba Investigation Algorithm\n";
        std::cout << "Survivors: " << survivors.size() << " theory branches\n";
        std::cout << std::string(70, '=') << "\n\n";
    }
    
    void initialize_branches() {
        for (int i = 0; i < 4; i++) {
            branches.emplace_back(i, scenario);
        }
        std::cout << "🧬 Spawned " << branches.size() 
                  << " investigative branches\n\n";
    }
};

#endif // POIROT_SOLVER_H
