# AMOEBA ALGORITHM - VISUAL ARCHITECTURE & EXECUTION TRACE

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    AMOEBA INVESTIGATION                         │
└─────────────────────────────────────────────────────────────────┘

                          ┌──────────────────┐
                          │  Query/Problem   │
                          │  (Mystery Case)  │
                          └────────┬─────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │   SPAWN N BRANCHES       │
                    │  (4 Different theories) │
                    └────────────┬─────────────┘
                                 │
                ┌────────────────┼────────────────┐
                │                │                │
                ▼                ▼                ▼
          ┌────────┐        ┌────────┐       ┌────────┐
          │Branch 0│        │Branch 1│       │Branch 2│  ...
          │Theory: │        │Theory: │       │Theory: │
          │Butler  │        │Driver  │       │Nephew  │
          │Score:? │        │Score:? │       │Score:? │
          └────┬───┘        └────┬───┘       └────┬───┘
               │                 │                │
               └─────────────────┼────────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │  SHARED EVIDENCE POOL       │
                  │  (All branches see this!)   │
                  │  • Fingerprints             │
                  │  • Witness testimony       │
                  │  • Bank deposits           │
                  │  • Handwriting analysis    │
                  │  [Grows as rounds progress]│
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────┐
                  │    EVALUATOR             │
                  │  Scores each branch on:  │
                  │  - Evidence support      │
                  │  - Motive plausibility   │
                  │  - Consistency          │
                  └──────────┬───────────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
                ▼            ▼            ▼
            Branch 0:   Branch 1:   Branch 2:
            Score 0.77  Score 0.45  Score 0.35
                │            │            │
                └────────────┼────────────┘
                             │
                  ┌──────────▼──────────┐
                  │ RESOURCE ALLOCATION │
                  │ (Inverse by rank!)  │
                  │ Strong:  2 slots    │
                  │ Medium:  4 slots    │
                  │ Weak:    8 slots    │◄─── KEY INNOVATION
                  └──────────┬──────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
                ▼            ▼            ▼
            Branch 0     Branch 1     Branch 2
            Proposes 2   Proposes 4   Proposes 8
            new clues    new clues    new clues
                │            │            │
                └────────────┼────────────┘
                             │
                  ┌──────────▼──────────┐
                  │  SHARED POOL        │
                  │  (Grows & Updates)  │
                  │  Budget: 20 max     │
                  │  Current: 13        │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │  STARVATION CHECK    │
                  │  Branches that don't │
                  │  improve lose slots  │
                  │  gradually starve    │
                  └──────────┬───────────┘
                             │
                  ┌──────────▼──────────┐
                  │ CONVERGENCE CHECK   │
                  │ All survivors agree?│
                  │ → YES: SOLVED! ✓    │
                  │ → NO: Next round    │
                  └─────────────────────┘
```

---

## Execution Flow: Round-by-Round Trace

### INITIALIZATION
```
Mystery: "The Vanished Necklace"
Suspects: 4 (Butler, Driver, Nephew, Maid)
Evidence: 13 total clues
Branches: 4 investigative threads

Branch #0 → investigates BUTLER first
Branch #1 → investigates DRIVER first
Branch #2 → investigates NEPHEW first
Branch #3 → investigates MAID first

Shared Pool: EMPTY
```

---

### ROUND 1: Initial Investigation

```
┌─ PHASE A: Investigation ──────────────────────┐
│ Each branch reasons with empty pool           │
│                                               │
│ Branch 0: "Butler is suspicious" (Theory)    │
│ Branch 1: "Driver is suspicious" (Theory)    │
│ Branch 2: "Nephew is suspicious" (Theory)    │
│ Branch 3: "Maid is suspicious" (Theory)      │
└───────────────────────────────────────────────┘

┌─ PHASE B: Evaluation ─────────────────────────┐
│ Evaluator scores each theory (on heuristics) │
│                                               │
│ Branch 0 (Butler):  0.55 ✨ Progress!        │
│ Branch 1 (Driver):  0.55 ✨ Progress!        │
│ Branch 2 (Nephew):  0.35 ✨ Progress!        │
│ Branch 3 (Maid):    0.40 ✨ Progress!        │
│                                               │
│ Improvement Counter: All reset to 0          │
└───────────────────────────────────────────────┘

┌─ PHASE C: Resource Allocation ────────────────┐
│ Rank by score (descending):                   │
│ 1. Branch 0 (Butler, 0.55)    →  2 slots     │
│ 1. Branch 1 (Driver, 0.55)    →  2 slots     │ (tied)
│ 3. Branch 3 (Maid, 0.40)      →  4 slots     │
│ 4. Branch 2 (Nephew, 0.35)    →  8 slots     │◄ MOST
│                                               │
│ (Inverse: weakest gets most)                 │
└───────────────────────────────────────────────┘

┌─ PHASE D: Evidence Gathering ─────────────────┐
│ Butler branch proposes (2 slots):              │
│   • "Fingerprints on jewelry case"            │
│   • "Witness: butler in garden at midnight"  │
│                                               │
│ Driver branch proposes (2 slots):             │
│   • "Driver's theft conviction"               │
│   • "Vehicle logs"                            │
│                                               │
│ Maid branch proposes (4 slots):               │
│   • "Maid employed 15 years spotless"         │
│   • "Maid's sister confirms alibi"            │
│   • "Maid rejected by butler drama"           │
│   • "Butler's romantic advances rejection"    │
│                                               │
│ Nephew branch proposes (8 slots):             │
│   • "Nephew's gambling debts"                 │
│   • "Security guard reports (no exit)"        │
│   • "Jewelry box key missing"                 │
│   • "Butler's suspicious savings increase"    │
│   • "Handwriting analysis on butler"          │
│   • "Nephew at hotel with accomplice"         │
│   • "Butler's opportunity (key access)"       │
│   • "Motivation: resentment over wages"       │
│                                               │
│ Total Proposals: 16 unique items              │
│ Shared Pool: EMPTY (0/20)                     │
│ Add to pool: min(16, 20) = 16? NO - add top  │
│ Pool Budget: 20 max                           │
│ Added: 9 best proposals                       │
│                                               │
│ NEW SHARED POOL (9/20):                       │
│ 1. Fingerprints on jewelry case               │
│ 2. Witness: butler in garden                  │
│ 3. Driver's theft conviction                  │
│ 4. Maid employed 15 years spotless            │
│ 5. Maid's sister alibi                        │
│ 6. Nephew's gambling debts                    │
│ 7. Security guard: no exits                   │
│ 8. Jewelry box key missing                    │
│ 9. Handwriting analysis (butler matches note)│
│                                               │
│ (All branches now see these 9 clues)          │
└───────────────────────────────────────────────┘

┌─ PHASE E: Starvation & Culling ───────────────┐
│ Check improvement_counter >= 3?                │
│ All branches: counter = 0 (just reset)        │
│ No starvation yet                             │
└───────────────────────────────────────────────┘

┌─ CONVERGENCE CHECK ───────────────────────────┐
│ Branch 0: Butler  (has evidence)              │
│ Branch 1: Driver  (has evidence)              │
│ Branch 2: Nephew  (has evidence)              │
│ Branch 3: Maid    (has evidence)              │
│                                               │
│ All have suspects ≠ CONVERGED                 │
│ Continue to next round...                     │
└───────────────────────────────────────────────┘
```

---

### ROUND 2: Evidence Refinement

```
┌─ PHASE A: Investigation (with 9 clues) ──────┐
│ Branch 0 now sees: butler fingerprints,       │
│                    witness testimony,          │
│                    handwriting analysis,       │
│                    key missing, etc.           │
│ → Confidence in BUTLER increases!             │
│                                               │
│ Branch 1 now sees: driver exonerated by       │
│                    security (didn't leave),    │
│                    outside town               │
│ → Confidence in DRIVER drops!                 │
│ → May switch to BUTLER (if evidence strong)   │
│                                               │
│ Branch 2 (Nephew) and 3 (Maid):               │
│ → Evidence shows they weren't there           │
│ → Both losing confidence                      │
└───────────────────────────────────────────────┘

┌─ PHASE B: Evaluation ─────────────────────────┐
│ Branch 0 (Butler):  0.55 → 0.77 ✨ Progress! │
│ Branch 1 (Driver):  0.55 → 0.45 ✗ Decline    │
│ Branch 2 (Nephew):  0.35 → 0.38 ✗ Minimal   │
│ Branch 3 (Maid):    0.40 → 0.35 ✗ Decline    │
│                                               │
│ Improvement tracking:                         │
│ B0: 0 (improved!) → Reset to 0               │
│ B1: 1 (no improvement)                        │
│ B2: 1 (no improvement)                        │
│ B3: 1 (no improvement)                        │
└───────────────────────────────────────────────┘

┌─ PHASE C: Resource Allocation ────────────────┐
│ Rank by score (descending):                   │
│ 1. Branch 0 (Butler, 0.77)    →  2 slots     │
│ 2. Branch 2 (Nephew, 0.38)    →  4 slots     │
│ 3. Branch 3 (Maid, 0.35)      →  6 slots     │
│ 4. Branch 1 (Driver, 0.45)    →  4 slots     │
│                                               │
│ (Weak branches get more chances)              │
└───────────────────────────────────────────────┘

┌─ PHASE D: Evidence Gathering ─────────────────┐
│ Proposals: 16 new clues offered              │
│ Pool budget: 20 - 9 = 11 remaining           │
│ Add: 11 new clues (fill remaining space)     │
│                                               │
│ UPDATED POOL (20/20 - FULL):                  │
│ [Previous 9 items] +                          │
│ • Vehicle logs (driver was in village)        │
│ • Nephew seen at hotel with accomplice       │
│ • Butler's increased savings deposits         │
│ • Maid's 15-year spotless record             │
│ • Security footage analysis                   │
│ • Handwriting match to ransom note            │
│ • Motive: butler's low wages & resentment    │
│ • Opportunity: butler had key access          │
│ • Timeline: butler was in garden at theft     │
│ • Financial: butler recently gained funds     │
│ • Driver exonerated: was elsewhere            │
└───────────────────────────────────────────────┘

┌─ PHASE E: Starvation & Culling ───────────────┐
│ B0: improved! counter = 0 (still alive)      │
│ B1: no improve! counter = 1                   │
│ B2: no improve! counter = 1                   │
│ B3: no improve! counter = 1                   │
│ (No deaths yet)                               │
└───────────────────────────────────────────────┘

┌─ CONVERGENCE CHECK ───────────────────────────┐
│ Branch 0: Butler   (0.77 confidence)          │
│ Branch 1: Driver   (0.45 confidence)          │
│ Branch 2: Nephew   (0.38 confidence)          │
│ Branch 3: Maid     (0.35 confidence)          │
│                                               │
│ NOT converged (different suspects)            │
│ Continue...                                   │
└───────────────────────────────────────────────┘
```

---

### ROUND 3: Weak Branch Adaptation

```
┌─ PHASE B: Evaluation ─────────────────────────┐
│ Pool now complete with exonerating evidence  │
│ for Driver, Maid                              │
│                                               │
│ Branch 0 (Butler):  0.77 → 0.85 ✨ STRONG!  │
│ Branch 1 (Driver):  0.45 → 0.25 ☠️ Failing │
│ Branch 2 (Nephew):  0.38 → 0.42 ✓ Slightly  │
│ Branch 3 (Maid):    0.35 → 0.15 ☠️ Collapse │
│                                               │
│ Branch 1&3: improvement_counter = 2          │
└───────────────────────────────────────────────┘

┌─ PHASE C: Resource Allocation ────────────────┐
│ 1. Branch 0 (Butler, 0.85)    →  1 slot      │
│ 2. Branch 2 (Nephew, 0.42)    →  3 slots     │
│ 3. Branch 1 (Driver, 0.25)    →  5 slots     │
│ 4. Branch 3 (Maid, 0.15)      →  7 slots     │
│                                               │
│ Maid theory given MAXIMUM chance to defend! │
└───────────────────────────────────────────────┘

┌─ PHASE E: Starvation & Culling ───────────────┐
│ B0: improved → counter = 0 ✓                  │
│ B1: 2 rounds no improve → counter = 2        │
│ B2: 1 round no improve → counter = 1         │
│ B3: 2 rounds no improve → counter = 2        │
│ (Still alive but weakening)                  │
└───────────────────────────────────────────────┘

┌─ CONVERGENCE CHECK ───────────────────────────┐
│ Still 4 different theories → NOT converged    │
│ Continue...                                   │
└───────────────────────────────────────────────┘
```

---

### ROUND 4: Convergence!

```
┌─ PHASE B: Evaluation ─────────────────────────┐
│ Evidence is overwhelming for butler           │
│ Multiple exonerating pieces for others        │
│                                               │
│ Branch 0 (Butler):  0.85 → 0.92 ✨ SOLID!   │
│ Branch 1 (Driver):  0.25 → 0.15 ☠️ Critical│
│ Branch 2 (Nephew):  0.42 → 0.58 ✓ Better    │
│ Branch 3 (Maid):    0.15 → 0.10 ☠️ Dying    │
│                                               │
│ Branches 1&3: counter = 3 → STARVATION       │
└───────────────────────────────────────────────┘

┌─ PHASE E: Starvation & Culling ───────────────┐
│ B0: improved → counter = 0 ✓ ALIVE           │
│ B1: 3 rounds no improve → STARVES            │
│     proposal_slots = 0 → ☠️ DEAD             │
│ B2: improved → counter = 0 ✓ ALIVE           │
│ B3: 3 rounds no improve → STARVES            │
│     proposal_slots = 0 → ☠️ DEAD             │
│                                               │
│ Survivors: B0 (Butler), B2 (Nephew)          │
└───────────────────────────────────────────────┘

┌─ Phase A: Next Investigation (with survivors)┐
│ B0: "Definitely BUTLER"                       │
│ B2: Evidence points to... "BUTLER"            │
│     (Nephew theory finally abandoned)         │
│                                               │
│ Both now suspect: BUTLER                      │
└───────────────────────────────────────────────┘

┌─ CONVERGENCE CHECK ───────────────────────────┐
│ Branch 0: BUTLER  (0.92 confidence)           │
│ Branch 2: BUTLER  (switched from Nephew)      │
│                                               │
│ ALL SURVIVORS AGREE: BUTLER IS GUILTY! ✨    │
│                                               │
│ 🎯 CONVERGENCE ACHIEVED IN ROUND 4!          │
│                                               │
│ Confidence: VERY HIGH                         │
│ Reason: Multiple independent paths            │
│         converged despite different routes    │
└───────────────────────────────────────────────┘
```

---

## Key Metrics Throughout Investigation

```
TIMELINE OF CONVERGENCE:

Round 1: Exploration
  Survivors: 4/4
  Theories: Butler, Driver, Nephew, Maid
  Pool: 9/20
  Status: Divergent

Round 2: Refinement
  Survivors: 4/4
  Theories: Butler, Driver, Nephew, Maid
  Pool: 20/20 (FULL)
  Status: Still divergent but evidence clear

Round 3: Adaptation
  Survivors: 4/4
  Weak theories losing confidence
  Pool: 20/20
  Status: Weak theories starving

Round 4: CONVERGENCE
  Survivors: 2/4 (Driver & Maid dead)
  Theories: ALL BUTLER
  Pool: 20/20 (full)
  Status: ✅ SOLVED

Evidence Trail:
  • Fingerprints → incriminates Butler
  • Witness → incriminates Butler
  • Handwriting → incriminates Butler
  • Deposits → incriminates Butler
  • Key access → incriminates Butler
  • Security footage → exonerates Driver
  • Alibi → exonerates Maid
  • Timeline → exonerates Nephew (mostly)
```

---

## Why Multiple Convergence is Robust

```
SCENARIO A: Single Path
  Theory: "Driver did it"
  Confidence: ???
  Problem: Only one voice, may be wrong
  
SCENARIO B: All Paths Agree
  Path 1: Started thinking Nephew
         Found evidence → switched to Butler
  Path 2: Started thinking Maid
         Found evidence → switched to Butler
  Path 3: Started thinking Driver
         Found evidence → switched to Butler
  Path 4: Started thinking Butler
         Stayed confident
  
  Result: BUTLER
  Confidence: VERY HIGH
  Why: Each path independently arrived at same answer
       despite starting from different assumptions!
```

---

## The Innovation in One Picture

```
TRADITIONAL:                          AMOEBA:

Strong Theory                         Weak Theory ← Resources
   ↓ (gets resources)                    ↓ (forced to prove)
Wins                                 Gets evidence
                                        ↓
                                      Improves or dies
                                      
Result: One winner                   Result: If weak survives,
        (but fragile)                        it converges
                                           (very robust!)
```

---

**This architecture embodies the principle: 
"True consensus emerges when weak theories are given fair chances to prove themselves."** 🧬

