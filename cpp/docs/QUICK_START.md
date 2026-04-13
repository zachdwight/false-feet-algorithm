# AMOEBA ALGORITHM - QUICK START GUIDE

## The Core Idea (in Pictures)

```
TRADITIONAL SEARCH:               AMOEBA ALGORITHM:
      
      [Branch A]                    [Weak  ] ← Gets MORE resources
         ↓                          [Weak  ] ← Competing
      [Branch B]                    [Strong] ← Gets LESS resources
         ↓
      Single path                   All share evidence pool
      to answer                     Multiple paths converge
                                    on same answer = CONFIDENCE
```

---

## The 6 Phases (Each Round)

### PHASE A: Investigation
```
Branch 0: "Maybe it's the butler..."
Branch 1: "Could be the driver..."
Branch 2: "What about the nephew..."
Branch 3: "The maid seems suspicious..."

All branches think in parallel with current evidence
```

### PHASE B: Evaluation
```
Evaluator scores each theory:
  Branch 0 (butler):  0.55/1.00 ← Decent
  Branch 1 (driver):  0.45/1.00 ← Weak
  Branch 2 (nephew):  0.35/1.00 ← Very weak
  Branch 3 (maid):    0.40/1.00 ← Weak
```

### PHASE C: Resource Allocation (THE KEY INNOVATION)
```
Instead of giving strongest MORE resources:
  
  Weakest (nephew):   8 evidence slots   ← "Here, prove your theory!"
  Weak (maid):        6 evidence slots   ← "Try harder"
  Weak (driver):      4 evidence slots   ← "You can do it"
  Strong (butler):    2 evidence slots   ← "You don't need help"
  
The weak get STARVING BONUS to catch up!
```

### PHASE D: Evidence Gathering & Pooling
```
Butler branch proposes:     "Fingerprints match butler!"
Driver branch proposes:     "Driver was out of town!"
Nephew branch proposes:     "Nephew had gambling debts!"
Maid branch proposes:       "Maid's alibi checks out!"

All proposals go into SHARED POOL:
┌─────────────────────────────────┐
│ Shared Evidence Pool (9/20):    │
│ • Fingerprints (butler)         │
│ • Witness testimony (butler)    │
│ • Debts (nephew)                │
│ • Vehicle logs (driver away)    │
│ • Alibi (maid clear)            │
│ ...                             │
└─────────────────────────────────┘

ALL BRANCHES NOW SEE THIS EVIDENCE
(Level playing field, different reasoning)
```

### PHASE E: Starvation & Culling
```
Round 1: No improvement
  Nephew proposal slots: 8 → 7
  
Round 2: Still no improvement
  Nephew proposal slots: 7 → 6
  
Round 3: Still stuck
  Nephew proposal slots: 6 → 5
  
Round 4: Still failing
  Nephew proposal slots: 5 → 0 ☠️  DEAD (starvation)
```

### Convergence Check
```
Branch 0 conclusion: BUTLER is guilty
Branch 1 conclusion: BUTLER is guilty
Branch 2 conclusion: BUTLER is guilty
Branch 3 conclusion: ☠️ (starved to death)

🎯 ALL SURVIVORS AGREE: BUTLER DID IT!
Convergence achieved → HIGH CONFIDENCE
```

---

## Why This Works Better

### Traditional Tree Search
```
Explore ALL possibilities
Cost: Exponential 💥
Time: Slow ⏱️
Wasteful: Many dead branches
```

### Amoeba Algorithm
```
Explore COMPETITIVELY
  - Strong theories get less help
  - Weak theories get chances
  - Mutually exclusive theories eliminate each other
  - Multiple convergence = robust answer

Cost: Polynomial 📊
Time: Faster ⏱️
Efficient: Weak theories die naturally
Robust: Multiple paths agree
```

---

## Real Example: The Mystery

```
THE CASE:
Lady Pembroke's diamond necklace stolen!
4 suspects, 13 pieces of evidence

INITIAL SUSPICION (before investigation):
  Butler:    45% suspicious (low wages, access)
  Nephew:    35% suspicious (gambling debts)
  Maid:      25% suspicious (jealousy)
  Driver:    60% suspicious (past theft record)  ← HIGHEST

INVESTIGATION ROUND 1-2:
Evidence emerges:
  • Butler's fingerprints on case ← Implicates butler
  • Butler's recent bank deposits ← Implicates butler
  • Witness saw butler at night ← Implicates butler
  • Handwriting matches ransom note ← Implicates butler
  
CONVERGENCE:
  All 4 branches now agree: BUTLER IS GUILTY
  (despite driver being most suspicious initially!)

CONFIDENCE: VERY HIGH
  - Multiple independent investigations converged
  - Not just "strongest theory won"
  - Weak theories were given chances, eliminated by evidence
```

---

## The Algorithm in Code (Simplified)

```cpp
while (not_converged && rounds < max) {
    
    // Phase A: Each branch reasons
    for (auto branch : branches) {
        branch.investigate(evidence_pool);
    }
    
    // Phase B: Score each theory
    for (auto branch : branches) {
        branch.score = evaluator.evaluate(branch);
    }
    
    // Phase C: Inverse allocation (KEY!)
    // Weakest branch gets most proposal slots
    allocate_inversely_by_score(branches);
    
    // Phase D: Gather evidence (shared pool)
    proposals = collect_proposals(branches);
    add_to_shared_pool(proposals, max_budget);
    
    // Phase E: Starvation
    for (auto branch : branches) {
        if (no_improvement) {
            branch.proposal_slots--;
            if (branch.proposal_slots == 0) {
                branch.die();
            }
        }
    }
    
    // Convergence?
    if (all_survivors_agree_on_suspect()) {
        return SOLVED;
    }
}
```

---

## Complexity Comparison

```
PROBLEM: Find answer in large dataset

BRUTE FORCE:
  Try all possibilities
  Time: O(2^n)  😱
  
HEURISTIC SEARCH (A*, Beam Search):
  Smart branch pruning
  Time: O(n^2) or O(n log n)
  Problem: Still may miss good paths
  
AMOEBA ALGORITHM:
  Competitive evolution
  Time: O(T × N × L)  where:
    T = rounds to convergence
    N = number of branches
    L = reasoning path length
  Result: O(polynomial)
  Benefit: Multiple paths agree = robust
```

---

## Key Properties

```
✅ DIVERSITY MAINTAINED
   Weak branches kept alive → different perspectives

✅ RESOURCE EFFICIENT
   Dead branches don't waste computation long

✅ ROBUST CONVERGENCE
   Multiple paths must agree → high confidence

✅ INTERPRETABLE
   Can trace which evidence led to answer

✅ TRAINABLE
   Self-supervised from convergence outcomes

✅ DOMAIN-AGNOSTIC
   Works for any problem with evidence/reasoning
```

---

## Metrics During Investigation

```
After Round 1:
  Branches alive: 4/4
  Evidence pool: 9/20
  Average score: 0.55
  Confidence: LOW (unclear)

After Round 2:
  Branches alive: 3/4  (nephew starving)
  Evidence pool: 13/20
  Average score: 0.72
  Confidence: MEDIUM (narrowing)

After Round 3:
  Branches alive: 1/3  (nephew dead, driver starving)
  Evidence pool: 16/20
  Average score: 0.85
  Confidence: HIGH (converging)

CONVERGENCE (Round 2):
  Branches alive: 3/3
  All agree on: BUTLER
  Confidence: VERY HIGH
  Supporting evidence count: 5 pieces
```

---

## When to Use Amoeba Algorithm

### GOOD FOR:
- Problems with multiple reasonable approaches
- Cases where evidence gradually clarifies
- Situations needing interpretability
- Systems where you want robust convergence
- Tasks with limited computational budget

### NOT IDEAL FOR:
- Single correct path (no benefit from diversity)
- Exhaustive search needed (algorithms already optimal)
- Real-time systems (multiple rounds add latency)
- Problems with no clear evidence

---

## Running the Prototype

### Step 1: Compile
```bash
g++ -std=c++17 -O2 poirot_main.cpp -o poirot_solver
```

### Step 2: Run
```bash
./poirot_solver
```

### Step 3: Watch the Investigation
```
Round 1: Branches form initial theories, propose evidence
Round 2: Evidence pool grows, theories refine
Round 3: Weak theories starving, strong theories gaining
Round 4: CONVERGENCE! Multiple paths agree on culprit
```

---

## What Makes This Novel?

| Feature | Traditional | Amoeba |
|---------|-------------|--------|
| **Weak branches** | Eliminated quickly | Given extra resources |
| **Resource allocation** | Uniform or greedy | Inverse-by-rank |
| **Evidence** | Cached at start | Shared pool, grows |
| **Training** | Supervised, expensive | Self-supervised |
| **Robustness** | Single path | Multiple converged |

---

## Example: Mystery Converges in 2 Rounds

```
START (No evidence):
  Butler (45):    Initial suspicion
  Nephew (35):
  Maid (25):
  Driver (60):    Most suspicious! ← WRONG

ROUND 1:
  Fingerprints surface → Butler +40 points
  Witness testimony → Butler +35 points
  Deposits noted → Butler +25 points
  Driver cleared → Driver -50 points
  
ROUND 2:
  All branches now point to: BUTLER
  Different evidence, same conclusion
  🎯 CONVERGENCE
```

**Result:** Despite driver being most suspicious initially, 
butler converges due to strong evidence. Robust!

---

## The Aha Moment

```
"Wait, why is the weak theory getting more resources??"

Answer: Because it NEEDS them to catch up!

Like a handicap system:
  Strong golfer: No handicap needed
  Weak golfer: Extra strokes to compete

In investigation:
  Strong theory: "I'm confident, investigate what I suggest"
  Weak theory: "I'm struggling, let me propose more angles"

Result: If both survive to convergence → ROBUST SIGNAL
```

---

## Next Steps

1. **Read the code** — Start with `poirot_mystery.h` (clean, documented)
2. **Run it** — See the algorithm work on the mystery
3. **Modify it** — Change suspects, evidence, weights
4. **Adapt it** — Apply to your own domain
5. **Train it** — Implement neural evaluator (in formal spec)

---

**The Amoeba Algorithm: When weak theories are given a fair chance,
convergence becomes a signal of robustness, not just luck.** 🧬🔍

