#ifndef AMOEBA_FRAMEWORK_H
#define AMOEBA_FRAMEWORK_H

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
// GENERIC DATA POINT & OPTION
// ============================================================================

struct DataPoint {
    std::string id;
    std::string title;
    std::string description;
    std::vector<std::string> supports;      // option IDs this supports
    std::vector<std::string> contradicts;   // option IDs this contradicts
    int priority;  // 1-5, how important?
};

struct Option {
    std::string id;
    std::string name;
    std::string rationale;
    std::string context;
    int initial_score;  // 0-100
};

struct Problem {
    std::string title;
    std::string description;
    std::string goal;
    std::vector<Option> options;
    std::vector<DataPoint> all_data;
};

// ============================================================================
// SHARED DATA POOL
// ============================================================================

class SharedDataPool {
public:
    void add_data(const DataPoint& data) {
        if (pool.find(data.id) == pool.end()) {
            pool[data.id] = data;
        }
    }

    bool has_data(const std::string& id) const {
        return pool.find(id) != pool.end();
    }

    const DataPoint& get_data(const std::string& id) const {
        return pool.at(id);
    }

    std::vector<DataPoint> get_all() const {
        std::vector<DataPoint> result;
        for (const auto& p : pool) {
            result.push_back(p.second);
        }
        return result;
    }

    size_t size() const {
        return pool.size();
    }

private:
    std::map<std::string, DataPoint> pool;
};

// ============================================================================
// HYPOTHESIS/REASONING PATH
// ============================================================================

struct Hypothesis {
    std::string chosen_option;     // Which option is this branch pursuing?
    std::string reasoning;         // Why
    std::vector<std::string> supporting_data;  // Data IDs that support it
};

class EvaluationBranch {
public:
    EvaluationBranch(int id, const Problem& scenario)
        : branch_id(id), scenario(scenario), score(0.5f),
          proposal_slots(3), improvement_counter(0), is_alive(true) {}

    int get_id() const { return branch_id; }
    float get_score() const { return score; }
    int get_proposal_slots() const { return proposal_slots; }
    int get_improvement_counter() const { return improvement_counter; }
    bool get_is_alive() const { return is_alive; }
    const Hypothesis& get_hypothesis() const { return current_hypothesis; }

    void set_score(float s) { score = s; }
    void set_proposal_slots(int n) { proposal_slots = std::max(0, n); }
    void increment_improvement_counter() { improvement_counter++; }
    void reset_improvement_counter() { improvement_counter = 0; }
    void set_alive(bool a) { is_alive = a; }

    // Evaluation logic
    void evaluate(const SharedDataPool& pool) {
        if (current_hypothesis.chosen_option.empty()) {
            current_hypothesis.chosen_option = scenario.options[branch_id % scenario.options.size()].id;
        }
        analyze_data(pool);
        update_hypothesis(pool);
    }

    void propose_data_to_examine(
        const Problem& scenario,
        std::vector<std::string>& proposals) {

        std::set<std::string> already_have;
        for (const auto& d : current_hypothesis.supporting_data) {
            already_have.insert(d);
        }

        // Propose unchecked data related to chosen option
        for (const auto& data : scenario.all_data) {
            if (already_have.find(data.id) == already_have.end()) {
                for (const auto& support : data.supports) {
                    if (support == current_hypothesis.chosen_option) {
                        proposals.push_back(data.id);
                        break;
                    }
                }
            }
            if ((int)proposals.size() >= proposal_slots) break;
        }

        // If not enough proposals, add any unexplored data
        for (const auto& data : scenario.all_data) {
            if (already_have.find(data.id) == already_have.end() &&
                std::find(proposals.begin(), proposals.end(), data.id) == proposals.end()) {
                proposals.push_back(data.id);
                if ((int)proposals.size() >= proposal_slots) break;
            }
        }
    }

    std::string get_summary() const {
        return "Branch #" + std::to_string(branch_id) + " chose " +
               current_hypothesis.chosen_option + ": " +
               current_hypothesis.reasoning;
    }

private:
    int branch_id;
    const Problem& scenario;
    Hypothesis current_hypothesis;
    float score;
    int proposal_slots;
    int improvement_counter;
    bool is_alive;

    void analyze_data(const SharedDataPool& pool) {
        std::map<std::string, int> option_scores;

        for (const auto& option : scenario.options) {
            option_scores[option.id] = option.initial_score;
        }

        // Adjust scores based on data in pool
        for (const auto& data : pool.get_all()) {
            for (const auto& support : data.supports) {
                if (option_scores.find(support) != option_scores.end()) {
                    option_scores[support] += data.priority * 10;
                }
            }
            for (const auto& contra : data.contradicts) {
                if (option_scores.find(contra) != option_scores.end()) {
                    option_scores[contra] -= data.priority * 20;
                }
            }
        }

        // Only switch if significantly better (15+ points)
        int current_score = option_scores.count(current_hypothesis.chosen_option) ?
                           option_scores[current_hypothesis.chosen_option] : 0;

        std::string best_option = current_hypothesis.chosen_option;
        int best_score = current_score;

        for (const auto& p : option_scores) {
            if (p.second > best_score + 15) {
                best_score = p.second;
                best_option = p.first;
            }
        }

        if (!best_option.empty()) {
            current_hypothesis.chosen_option = best_option;
        }
    }

    void update_hypothesis(const SharedDataPool& pool) {
        current_hypothesis.supporting_data.clear();

        // Collect all data supporting current option
        for (const auto& data : pool.get_all()) {
            for (const auto& support : data.supports) {
                if (support == current_hypothesis.chosen_option) {
                    current_hypothesis.supporting_data.push_back(data.id);
                }
            }
        }

        // Find matching option for rationale
        for (const auto& option : scenario.options) {
            if (option.id == current_hypothesis.chosen_option) {
                current_hypothesis.reasoning = "Rationale: " + option.rationale +
                                              " | Context: " + option.context;
                break;
            }
        }
    }
};

// ============================================================================
// GENERIC EVALUATOR
// ============================================================================

class HypothesisEvaluator {
public:
    float evaluate(const EvaluationBranch& branch,
                   const SharedDataPool& pool,
                   const Problem& scenario) {

        const Hypothesis& hyp = branch.get_hypothesis();

        // Component 1: Data support (0-0.4)
        float data_score = evaluate_data_support(hyp, pool);

        // Component 2: Rationale strength (0-0.3)
        float rationale_score = evaluate_rationale(hyp, scenario);

        // Component 3: Consistency (0-0.3)
        float consistency_score = evaluate_consistency(hyp, pool);

        float total = data_score + rationale_score + consistency_score;
        return std::min(1.0f, total);
    }

private:
    float evaluate_data_support(const Hypothesis& hyp,
                               const SharedDataPool& pool) {
        if (hyp.supporting_data.empty()) return 0.1f;

        int strong_data = 0;
        for (const auto& data_id : hyp.supporting_data) {
            if (pool.has_data(data_id)) {
                const auto& data = pool.get_data(data_id);
                if (data.priority >= 4) strong_data++;
            }
        }

        float ratio = static_cast<float>(strong_data) / hyp.supporting_data.size();
        return 0.4f * ratio;
    }

    float evaluate_rationale(const Hypothesis& hyp,
                            const Problem& scenario) {
        // Generic evaluation based on rationale length/content
        if (hyp.reasoning.empty()) return 0.1f;

        // Longer, more detailed reasoning = stronger (simple heuristic)
        float detail_score = std::min(0.3f, hyp.reasoning.length() / 200.0f);
        return detail_score;
    }

    float evaluate_consistency(const Hypothesis& hyp,
                              const SharedDataPool& pool) {
        // Check if any data contradicts this option
        for (const auto& data : pool.get_all()) {
            for (const auto& contra : data.contradicts) {
                if (contra == hyp.chosen_option) {
                    return 0.05f;  // Heavily penalized if contradicted
                }
            }
        }
        return 0.3f;
    }
};

#endif // AMOEBA_FRAMEWORK_H
