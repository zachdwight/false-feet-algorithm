# 🧬 False Feet Algorithm
## Novel Approach to Problem-Solving Through Inverse Resource Allocation

> *"When weak theories are given fair chances, convergence becomes a signal of robustness, not just luck."*

---

## 🎯 What Is This?

The **False Feet Algorithm** is a novel architecture for solving complex problems through **adaptive multi-branch reasoning** with **inverse resource allocation**. 

Instead of giving more resources to strong branches (traditional approach), this algorithm gives **more resources to weak branches** — forcing them to either improve or naturally die off. When multiple independent reasoning paths converge on the same answer despite starting with different hypotheses, that's a **very robust signal** of correctness.

The name comes from the biological metaphor: **amoebas use temporary "false feet" (pseudopodia) to explore and move.** These exploratory structures are not the final form — they're intermediate scaffolding that gets discarded. Similarly, this algorithm generates temporary reasoning branches that either converge to a solution or starve.

---

## 🚀 Quick Start

### Try It Now (30 seconds)

```bash
# Compile
g++ -std=c++17 -O2 src/poirot_main.cpp -o solver

# Run (solves "The Vanished Necklace" mystery)
./solver
```

**Output:** 4 investigative branches compete to solve a Hercule Poirot-style mystery. They converge on the guilty party in ~2 rounds. ✅

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

### Source Code (`src/`)
- **poirot_mystery.h** — Core data structures (Evidence, Suspect, Branch, Pool, Evaluator)
- **poirot_solver.h** — Main algorithm (6 phases, helper functions)
- **poirot_main.cpp** — Mystery scenario + entry point

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
| **Lines of Code** | ~850 |
| **Documentation** | ~9,000 lines |
| **Header Files** | 2 |
| **Implementation Files** | 1 |
| **Test Case Suspects** | 4 |
| **Test Case Clues** | 13 |
| **Parallel Branches** | 4 |
| **Compile Time** | < 1 second |
| **Runtime** | < 1 second |
| **Executable Size** | 90 KB |

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

