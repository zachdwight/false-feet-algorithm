# False Feet Algorithm (AKA Amoeba)
## Novel Approach to Problem-Solving Through Inverse Resource Allocation

> *"When weak theories are given fair chances, convergence becomes a signal of robustness, not just luck."*

---

## 🎯 What Is This?

The **False Feet Algorithm** is a cool architecture for solving complex problems through **adaptive multi-branch reasoning** with **inverse resource allocation**. 

Instead of giving more resources to strong branches (traditional approach), this algorithm gives **more resources to weak branches** — forcing them to either improve or naturally die off. When multiple independent reasoning paths converge on the same answer despite starting with different hypotheses, that's a **very robust signal** of correctness.

The name comes from the biological metaphor: **amoebas use temporary "false feet" (pseudopodia) to explore and move.** These exploratory structures are not the final form — they're intermediate scaffolding that gets discarded. Similarly, this algorithm generates temporary reasoning branches that either converge to a solution or starve.

---

## 🚀 Quick Start

### Option 1: Mystery Solver (Original)

```bash
# Compile the mystery solver
make build

# Run (solves "The Vanished Necklace" mystery)
make run
```

**Output:** 4 investigative branches compete to solve a Hercule Poirot-style mystery. Converges in ~2 rounds. ✅

### Option 2: Generic Framework (New!)

```bash
# Compile the generic version
make generic

# Run (solves product recommendation problem)
make run-generic
```

**Output:** 4 evaluation branches compete to find the best product. Framework works for ANY hypothesis evaluation problem!

### Read the Overview (5 minutes)

Start with [`docs/QUICK_START.md`](docs/QUICK_START.md) for visual introduction.

---

## 🔑 Core Innovation

```
TRADITIONAL SEARCH          FALSE FEET ALGORITHM
───────────────────────────────────────────────────
Strong branch               Weak branch
   ↓ (more resources)         ↓ (MORE resources)
Dominates                   Must prove itself or die
                           
Result: Single path         Result: Multiple converged
        (fragile)                   (robust)
```

### The Key Insight

In traditional algorithms:
- Strong candidates get more resources
- Single winner emerges
- Problem: If that winner is wrong, system fails

With False Feet Algorithm:
- Weak candidates get resources to catch up
- Multiple theories survive and explore differently
- All survivors see same evidence (shared pool)
- **When they converge, answer is very robust**

---

## 📊 How It Works (6 Phases Per Round)

```
PHASE A: Investigation
  └─ Each branch reasons using shared evidence pool

PHASE B: Evaluation  
  └─ Score each theory (likelihood of correctness)

PHASE C: Resource Allocation (INVERSE by rank)
  └─ Weakest branch → Most proposal slots
  └─ Strongest branch → Fewest slots

PHASE D: Evidence Gathering & Pooling
  └─ Branches propose new evidence/documents
  └─ Shared pool grows (budgeted, immutable)

PHASE E: Starvation & Culling
  └─ Branches with no improvement gradually starve
  └─ Proposal slots decrease each round
  └─ When slots = 0, branch dies naturally

CONVERGENCE CHECK
  └─ Do all survivors agree on answer?
  └─ YES → SOLVED (with high confidence)
  └─ NO → Repeat until convergence or timeout
```

---

## 📦 What's Included

### Mystery Solver (Domain-Specific)
- **src/poirot_mystery.h** — Mystery-specific structures (Evidence, Suspect, Branch, Pool, Evaluator)
- **src/poirot_solver.h** — Mystery investigation algorithm
- **src/poirot_main.cpp** — "The Vanished Necklace" scenario

### Generic Framework (Reusable for Any Domain)
- **src/amoeba_framework.h** — Generic data structures (DataPoint, Option, Problem, EvaluationBranch, HypothesisEvaluator)
- **src/amoeba_solver.h** — Generic Amoeba Algorithm solver
- **src/generic_main.cpp** — Examples: Product Recommendation & Medical Diagnosis

### Documentation (`docs/`)
- **QUICK_START.md** — Visual introduction with diagrams
- **EXECUTION_TRACE.md** — Detailed round-by-round walkthrough
- **amoeba_algorithm_spec.md** — Formal specification (pseudocode, loss functions, training)
- **INDEX.md** — File guide and learning paths

### Examples (`examples/`)
- **poirot_solver** — Pre-compiled demo

---

## 🎓 Learn More

### For Intuition (15 minutes)
Read [`docs/QUICK_START.md`](docs/QUICK_START.md) — Visual diagrams and examples

### For Implementation (1 hour)
1. Read [`docs/EXECUTION_TRACE.md`](docs/EXECUTION_TRACE.md)
2. Study `src/poirot_mystery.h` (data structures)
3. Study `src/poirot_solver.h` (algorithm)

### For Research (4+ hours)
Read [`docs/amoeba_algorithm_spec.md`](docs/amoeba_algorithm_spec.md) — Full formal specification including:
- Complete pseudocode
- Self-supervised training procedure
- Complexity analysis (O-notation)
- Loss functions & hyperparameters
- Failure mode analysis

### For Benchmarking & Comparison
Read [`docs/BENCHMARKS.md`](docs/BENCHMARKS.md) — Comprehensive performance analysis:
- Comparison to Greedy, Beam Search, and Uniform Parallel methods
- Convergence speed and accuracy metrics across problem difficulties
- Evidence efficiency analysis
- Real-world application scenarios
- When to use False Feet vs simpler alternatives

---

## 🧪 The Test Case: Poirot Mystery

**Scenario:** "The Vanished Necklace"
- **Victim:** Lady Pembroke  
- **Crime:** Theft of priceless diamond necklace
- **Suspects:** 4 (Butler, Driver, Nephew, Maid)
- **Clues:** 13 pieces of evidence
- **Branches:** 4 parallel investigations
- **Solution:** All converge on Butler (correct!) ✅

**Why this works as a test case:**
- Deterministic (same result each time)
- Interpretable (can see reasoning)
- Realistic (multiple theories, evidence refinement)
- Visual (good demo output)

---

## 📈 Algorithm Properties

| Property | Details |
|----------|---------|
| **Time Complexity** | O(T × N × L) where T=rounds, N=branches, L=reasoning length |
| **Space Complexity** | O(N × L + B × D) where B=budget, D=doc size |
| **Convergence** | Monotonic improvement, bounded by T_max |
| **Robustness** | Multiple paths converge = high confidence |
| **Scalability** | Polynomial (not exponential) |
| **Training** | Self-supervised via convergence outcomes |

---

## 🔬 Comparison to Baselines

| Aspect | LLM | Tree Search | False Feet |
|--------|-----|-------------|-----------|
| **Search Type** | Feed-forward | Exhaustive | Adaptive competition |
| **Resource Allocation** | Uniform | Uniform | **Inverse (weak favored)** |
| **Data Integration** | Cached | Per-branch | **Shared pool** |
| **Convergence Signal** | None | Coverage | **Agreement** |
| **Training** | Supervised | Outcome-only | **Self-supervised** |
| **Speed** | Fast | Slow | Medium |
| **Robustness** | Low | Medium | **High** |

---

## 🛠️ Building & Running

### Prerequisites
- C++17 compiler (g++, clang, MSVC)
- Standard library only (no dependencies)

### Compile
```bash
g++ -std=c++17 -O2 src/poirot_main.cpp -o solver
```

### Run
```bash
./solver
```

### Expected Output
```
🔍 HERCULE POIROT'S MYSTERY SOLVER 🔍
Case: The Vanished Necklace
Victim: Lady Pembroke
Crime: Theft of the priceless Maharaja Diamond Necklace

🧬 Spawned 4 investigative branches

📋 ROUND 1
  [Investigation, evaluation, allocation, gathering, starvation]
  
📋 ROUND 2
  [Evidence pool grows, theories refine]

🎯 CONVERGENCE ACHIEVED!
All surviving branches agree: butler is guilty!

💼 VERDICT: butler
📖 Supporting Evidence: [5 pieces listed with details]
```

**Runtime:** < 1 second

---

## 🎯 Using the Generic Framework

**The generic framework is domain-agnostic and ready to use for any hypothesis evaluation problem!**

### How It Works

Replace mystery-specific concepts with your own:

| Mystery | Generic | Your Domain |
|---------|---------|------------|
| Evidence | DataPoint | Requirement, Feature, Symptom |
| Suspect | Option | Product, Diagnosis, Recipe |
| Investigation | Evaluation | Analysis, Assessment |

### Quick Example: Product Recommendation

```cpp
// Define your problem
Problem problem;
problem.title = "Best Product for Customer";
problem.goal = "Find optimal product given constraints";

// Add options to evaluate
problem.options = {
    Option{"product_a", "Premium Pro", "For power users", "top-tier quality", 50},
    Option{"product_b", "Budget Basic", "For cost-conscious", "affordable", 40}
};

// Add data points that support/contradict options
problem.all_data.push_back(DataPoint{
    "data_1",
    "Customer needs portability",
    "Lightweight is critical",
    {"product_b"},        // supports lightweight product
    {"product_a"},        // contradicts heavy premium product
    5                     // priority
});

// Run the algorithm
AmoebaInvestigation solver(problem);
solver.solve();
```

All 4 evaluation branches compete, share data, and converge on best product! ✅

### Other Examples Included

See `src/generic_main.cpp` for:
- **Product Recommendation** — Find best product for customer needs
- **Medical Diagnosis** — Identify most likely diagnosis from symptoms

### Create Your Own

1. Define your `Option` candidates
2. Define your `DataPoint` evidence/requirements
3. Create a `Problem` with them
4. Run `AmoebaInvestigation solver(problem); solver.solve();`

---

## 🎨 Customization

### Change the Mystery
Edit `setup_mystery()` in `src/poirot_main.cpp`:
```cpp
mystery.suspects.push_back(Suspect{
  "id", "Name", "Motive", "Opportunity"
});

mystery.all_evidence.push_back(Evidence{
  "id", "Title", "Description",
  {"incriminates_id"}, {"exonerates_id"}, priority
});
```

### Change Algorithm Parameters
Edit `MysteryInvestigation` in `src/poirot_solver.h`:
```cpp
max_iterations = 20;              // More rounds
pool_budget = 50;                 // Larger pool
proposal_budget_per_round = 10;   // More proposals
improvement_threshold = 0.01;     // Stricter
starvation_rounds = 5;            // Longer grace period
```

### Change Evaluator Scoring
Modify `MysteryEvaluator` in `src/poirot_mystery.h`:
```cpp
float evaluate_evidence_support() { ... }
float evaluate_motive() { ... }
float evaluate_consistency() { ... }
```

---

## 📚 Apply to Other Domains

The algorithm is **domain-agnostic**. Examples:

### Recipe/Meal Planner
- **Evidence:** Ingredients, nutrition facts, preparation time
- **Branches:** Different meal theories
- **Convergence:** "This recipe works best given constraints"

### Product Recommender
- **Evidence:** Product features, user requirements, reviews
- **Branches:** Different product theories
- **Convergence:** "This product best fits your needs"

### QA/Retrieval System
- **Evidence:** Document relevance, semantic similarity
- **Branches:** Different answer hypotheses
- **Convergence:** "This answer is most correct"

---

## 🧠 Training (Self-Supervised)

The formal specification includes a complete training procedure:

### Phase 0: Warm Start
Use hand-crafted heuristic evaluator
```
score = 0.5 * coherence(τ) 
      + 0.3 * relevance(τ, q)
      + 0.2 * consistency(τ, 𝒫)
```

### Phase 1: Self-Supervised Learning
Run tree search on (query, correct_answer) pairs. Loss:
```
LOSS = -log(score_of_correct_survivors)
     + log(score_of_incorrect_survivors)
     + penalty_for_wasted_branches

Backprop through entire search to refine evaluator
```

See [`docs/amoeba_algorithm_spec.md`](docs/amoeba_algorithm_spec.md) Section 4 for complete procedure.

---

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| **Lines of Code** | ~1,500 (mystery + generic) |
| **Documentation** | ~9,000 lines |
| **Header Files** | 4 (2 mystery-specific, 2 generic) |
| **Implementation Files** | 2 (poirot_main + generic_main) |
| **Mystery Test Case** | 4 suspects, 13 clues |
| **Generic Examples** | 2 (product recommendation, medical diagnosis) |
| **Parallel Branches** | 4 |
| **Compile Time** | < 1 second |
| **Runtime** | < 1 second |
| **Executable Size** | ~100 KB (each) |

---

## 🔍 Key Files Explained

### `src/poirot_mystery.h` (11 KB)
Core data structures:
- `Evidence` — Clues with incriminations/exonerations
- `Suspect` — Suspects with motive and opportunity
- `InvestigativeBranch` — One investigation hypothesis
- `SharedEvidencePool` — Evidence all branches see
- `MysteryEvaluator` — Scores theories

### `src/poirot_solver.h` (12 KB)
Main algorithm with 6 phases:
- `phase_investigation()` — Branches think
- `phase_evaluation()` — Score theories
- `phase_resource_allocation()` — Inverse by rank
- `phase_evidence_gathering()` — Shared pool updates
- `phase_starvation_culling()` — Weak branches die
- `check_convergence()` — Did we solve it?

### `src/poirot_main.cpp` (6.6 KB)
Mystery scenario:
- 4 suspects with motives
- 13 clues with relationships
- Main entry point
- Console output

---

## 🎯 Next Steps

### Try It
```bash
git clone <this-repo>
cd false-feet-algorithm
g++ -std=c++17 -O2 src/poirot_main.cpp -o solver
./solver
```

### Understand It
1. Read `docs/QUICK_START.md`
2. Read `docs/EXECUTION_TRACE.md`
3. Study `src/poirot_mystery.h`
4. Study `src/poirot_solver.h`

### Extend It
- Change the mystery scenario
- Apply to new domains
- Implement neural evaluator
- Benchmark against baselines
- Publish research

### Research/Publish
1. Read `docs/amoeba_algorithm_spec.md`
2. Implement neural training (Section 4)
3. Run benchmarks
4. Write paper!

---

## 🤝 Contributing

Ideas for extensions:

- **New domains:** Implement for recipes, products, QA systems
- **Neural evaluator:** Learnable scoring function
- **Benchmarking:** Compare to LLMs, tree search, other baselines
- **Optimization:** Parallel branch execution, caching, GPU support
- **Visualization:** Web interface, interactive demos
- **Research:** Analyze convergence properties, write papers

---

## 📝 Citation

If you use this in research:

```bibtex
@software{false_feet_2026,
  title={False Feet Algorithm: Inverse Resource Allocation for Robust Convergence},
  author={Dwight, Zach},
  year={2026},
  url={https://github.com/zachdwight/false-feet-algorithm}
}
```

---

## 📖 Reading Guide

**Quick (30 min):** `QUICK_START.md` → Run solver → Output

**Standard (2 hr):** README → All docs → Study code

**Deep (4+ hr):** All docs → Code line-by-line → Modify & test

**Research (1 day):** Everything + `amoeba_algorithm_spec.md` → Implement training → Benchmark

---

## ❓ FAQ

**Q: What makes this different from beam search?**  
A: Inverse resource allocation + shared pool + self-supervised training. See comparison table.

**Q: Can I use this in production?**  
A: It's a prototype. Needs: (1) neural evaluator, (2) benchmarking, (3) optimization.

**Q: Can I apply this to [my domain]?**  
A: Yes! Replace Evidence/Suspect with your domain concepts.

**Q: How do I train the evaluator?**  
A: See Section 4 of `docs/amoeba_algorithm_spec.md`.

**Q: Why C++?**  
A: Fast, clean, no external dependencies. Easy to port to Python/Rust.

---

## 📄 License

Open source - free to use, modify, and distribute.

---

## 🙏 Acknowledgments

Developed through collaborative exploration of biological metaphors applied to algorithm design. Inspired by the adaptive behavior of amoebas and the reasoning patterns in Hercule Poirot mysteries.

---

**Ready to solve mysteries with parallel reasoning branches?** 🔍🧬

Start with: [`docs/QUICK_START.md`](docs/QUICK_START.md)

