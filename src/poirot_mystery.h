#ifndef POIROT_MYSTERY_H
#define POIROT_MYSTERY_H

#include <vector>
#include <string>
#include <map>
#include <set>
#include <memory>
#include <iostream>
#include <algorithm>
#include <cmath>
#include <random>

// ============================================================================
// MYSTERY EVIDENCE & SCENARIO
// ============================================================================

struct Evidence {
    std::string id;
    std::string title;
    std::string description;
    std::vector<std::string> incriminates;  // suspect IDs this points to
    std::vector<std::string> exonerates;    // suspect IDs this clears
    int priority;  // 1-5, how important is this clue?
};

struct Suspect {
    std::string id;
    std::string name;
    std::string motive;
    std::string opportunity;
    int suspicion_level;  // 0-100
};

struct MysteryScenario {
    std::string title;
    std::string victim;
    std::string crime;
    std::vector<Suspect> suspects;
    std::vector<Evidence> all_evidence;
};

// ============================================================================
// SHARED EVIDENCE POOL
// ============================================================================

class SharedEvidencePool {
public:
    void add_evidence(const Evidence& evidence) {
        if (pool.find(evidence.id) == pool.end()) {
            pool[evidence.id] = evidence;
        }
    }
    
    bool has_evidence(const std::string& id) const {
        return pool.find(id) != pool.end();
    }
    
    const Evidence& get_evidence(const std::string& id) const {
        return pool.at(id);
    }
    
    std::vector<Evidence> get_all() const {
        std::vector<Evidence> result;
        for (const auto& p : pool) {
            result.push_back(p.second);
        }
        return result;
    }
    
    size_t size() const {
        return pool.size();
    }
    
private:
    std::map<std::string, Evidence> pool;
};

// ============================================================================
// INVESTIGATIVE BRANCH (Reasoning Path)
// ============================================================================

struct Theory {
    std::string prime_suspect;      // Who they think did it
    std::string motive;             // Why
    std::vector<std::string> supporting_evidence;  // Evidence IDs that support
    std::string reasoning;          // How they arrived at this
};

class InvestigativeBranch {
public:
    InvestigativeBranch(int id, const MysteryScenario& scenario)
        : branch_id(id), scenario(scenario), score(0.5f),
          proposal_slots(3), improvement_counter(0), is_alive(true) {}
    
    int get_id() const { return branch_id; }
    float get_score() const { return score; }
    int get_proposal_slots() const { return proposal_slots; }
    int get_improvement_counter() const { return improvement_counter; }
    bool get_is_alive() const { return is_alive; }
    const Theory& get_theory() const { return current_theory; }
    
    void set_score(float s) { score = s; }
    void set_proposal_slots(int n) { proposal_slots = std::max(0, n); }
    void increment_improvement_counter() { improvement_counter++; }
    void reset_improvement_counter() { improvement_counter = 0; }
    void set_alive(bool a) { is_alive = a; }
    
    // Investigation logic
    void investigate(const SharedEvidencePool& pool) {
        // Build theory based on available evidence
        // If no theory yet, pick a unique suspect for this branch
        if (current_theory.prime_suspect.empty()) {
            // Each branch gets a different starting suspect hypothesis
            current_theory.prime_suspect = scenario.suspects[branch_id % scenario.suspects.size()].id;
        }
        analyze_evidence(pool);
        update_theory(pool);
    }
    
    void propose_evidence_to_investigate(
        const MysteryScenario& scenario,
        std::vector<std::string>& proposals) {
        
        // This branch proposes which pieces of evidence it wants to examine
        std::set<std::string> already_have;
        for (const auto& e : current_theory.supporting_evidence) {
            already_have.insert(e);
        }
        
        // Propose unchecked evidence related to prime suspect
        for (const auto& evidence : scenario.all_evidence) {
            if (already_have.find(evidence.id) == already_have.end()) {
                for (const auto& incrim : evidence.incriminates) {
                    if (incrim == current_theory.prime_suspect) {
                        proposals.push_back(evidence.id);
                        break;
                    }
                }
            }
            if (proposals.size() >= proposal_slots) break;
        }
        
        // If not enough proposals, add any unexplored evidence
        for (const auto& evidence : scenario.all_evidence) {
            if (already_have.find(evidence.id) == already_have.end() &&
                std::find(proposals.begin(), proposals.end(), evidence.id) == proposals.end()) {
                proposals.push_back(evidence.id);
                if (proposals.size() >= proposal_slots) break;
            }
        }
    }
    
    std::string get_reasoning_summary() const {
        std::string summary = "Branch #" + std::to_string(branch_id) + " suspects " +
                             current_theory.prime_suspect + " because: " +
                             current_theory.reasoning;
        return summary;
    }
    
private:
    int branch_id;
    const MysteryScenario& scenario;
    Theory current_theory;
    float score;
    int proposal_slots;
    int improvement_counter;
    bool is_alive;
    
    void analyze_evidence(const SharedEvidencePool& pool) {
        // Score each suspect based on available evidence
        std::map<std::string, int> suspect_scores;
        
        for (const auto& suspect : scenario.suspects) {
            suspect_scores[suspect.id] = suspect.suspicion_level;
        }
        
        // Adjust scores based on evidence in pool
        for (const auto& evidence : pool.get_all()) {
            for (const auto& incrim : evidence.incriminates) {
                if (suspect_scores.find(incrim) != suspect_scores.end()) {
                    suspect_scores[incrim] += evidence.priority * 10;
                }
            }
            for (const auto& exoner : evidence.exonerates) {
                if (suspect_scores.find(exoner) != suspect_scores.end()) {
                    suspect_scores[exoner] -= evidence.priority * 20;
                }
            }
        }
        
        // Only switch suspects if the new one is SIGNIFICANTLY better (by 15+ points)
        int current_score = suspect_scores.count(current_theory.prime_suspect) ? 
                           suspect_scores[current_theory.prime_suspect] : 0;
        
        std::string best_suspect = current_theory.prime_suspect;
        int best_score = current_score;
        
        for (const auto& p : suspect_scores) {
            if (p.second > best_score + 15) {  // Only switch with strong evidence
                best_score = p.second;
                best_suspect = p.first;
            }
        }
        
        if (!best_suspect.empty()) {
            current_theory.prime_suspect = best_suspect;
        }
    }
    
    void update_theory(const SharedEvidencePool& pool) {
        current_theory.supporting_evidence.clear();
        
        // Collect all evidence that supports current suspect
        for (const auto& evidence : pool.get_all()) {
            for (const auto& incrim : evidence.incriminates) {
                if (incrim == current_theory.prime_suspect) {
                    current_theory.supporting_evidence.push_back(evidence.id);
                }
            }
        }
        
        // Find matching suspect object for motive/opportunity
        for (const auto& suspect : scenario.suspects) {
            if (suspect.id == current_theory.prime_suspect) {
                current_theory.motive = suspect.motive;
                current_theory.reasoning = "Has motive (" + suspect.motive + 
                                          ") and opportunity (" + suspect.opportunity + ")";
                break;
            }
        }
    }
};

// ============================================================================
// EVALUATOR (Scores investigative theories)
// ============================================================================

class MysteryEvaluator {
public:
    float evaluate(const InvestigativeBranch& branch, 
                   const SharedEvidencePool& pool,
                   const MysteryScenario& scenario) {
        
        const Theory& theory = branch.get_theory();
        
        // Component 1: Evidence support (0-0.4)
        float evidence_score = evaluate_evidence_support(theory, pool);
        
        // Component 2: Motive plausibility (0-0.3)
        float motive_score = evaluate_motive(theory, scenario);
        
        // Component 3: Consistency (0-0.3)
        float consistency_score = evaluate_consistency(theory, pool);
        
        float total = evidence_score + motive_score + consistency_score;
        return std::min(1.0f, total);
    }
    
private:
    float evaluate_evidence_support(const Theory& theory,
                                   const SharedEvidencePool& pool) {
        if (theory.supporting_evidence.empty()) return 0.1f;
        
        int strong_evidence = 0;
        for (const auto& evi_id : theory.supporting_evidence) {
            if (pool.has_evidence(evi_id)) {
                const auto& evi = pool.get_evidence(evi_id);
                if (evi.priority >= 4) strong_evidence++;
            }
        }
        
        float ratio = static_cast<float>(strong_evidence) / theory.supporting_evidence.size();
        return 0.4f * ratio;
    }
    
    float evaluate_motive(const Theory& theory,
                         const MysteryScenario& scenario) {
        for (const auto& suspect : scenario.suspects) {
            if (suspect.id == theory.prime_suspect) {
                // Strong motive = higher score
                if (suspect.motive.find("hatred") != std::string::npos ||
                    suspect.motive.find("revenge") != std::string::npos) {
                    return 0.3f;
                } else if (suspect.motive.find("inheritance") != std::string::npos ||
                          suspect.motive.find("money") != std::string::npos) {
                    return 0.25f;
                } else {
                    return 0.15f;
                }
            }
        }
        return 0.1f;
    }
    
    float evaluate_consistency(const Theory& theory,
                              const SharedEvidencePool& pool) {
        // Check if any evidence contradicts this suspect
        for (const auto& evidence : pool.get_all()) {
            for (const auto& exoner : evidence.exonerates) {
                if (exoner == theory.prime_suspect) {
                    return 0.05f;  // Heavily penalized if suspect is exonerated
                }
            }
        }
        return 0.3f;
    }
};

#endif // POIROT_MYSTERY_H
