# False Feet Algorithm

> **Verify complex reasoning through multi-path convergence**
> 
> When your LLM, medical diagnosis, or decision system needs to be right—run it through multiple independent reasoning paths. When they converge, you have high confidence. When they diverge, you catch errors early.

A powerful algorithm for solving complex reasoning problems through competitive multi-branch investigation. Instead of giving resources to strong hypotheses, we give MORE to weak ones—forcing them to improve or fail. When multiple independent reasoning paths converge on the same answer despite different starting assumptions, that's a very robust signal.

## Why This Matters (2026)

**LLM Hallucinations:** Your language model sounds confident but might be completely wrong. You need proof, not just confidence.

**Medical Decisions:** Complex diagnoses require convergence across multiple specialist opinions before treatment.

**High-Stakes Analysis:** Financial decisions, policy recommendations, incident root causes—when you need certainty.

## Core Innovation

**Inverse Resource Allocation:** Instead of investing more in strong hypotheses, invest MORE in weak ones. Force weak reasoning paths to either strengthen or expose why they fail.

Result: Convergence is a robust signal. Divergence catches problems early.

## Examples

- **🔍 LLM Reasoning Robustness** — Verify multi-path convergence before acting on LLM outputs
- **🕵️ Mystery Solving** — Classic deduction through competitive hypothesis evaluation  
- **🏥 Clinical Diagnosis** — Multi-specialist convergence for high-confidence diagnosis

## Quick Start

### Python

```bash
cd python
pip install -e ".[viz]"

# Try it out
python -m false_feet_algorithm.examples.llm_reasoning_robustness
python -m false_feet_algorithm.examples.mystery_solving
python -m false_feet_algorithm.examples.clinical_diagnosis
```

### C++

```bash
cd cpp
g++ -std=c++17 -O2 src/poirot_main.cpp -o solver
./solver
```

## Documentation

- **Python:** `python/README.md` — API, examples, extensibility
- **C++:** `cpp/docs/QUICK_START.md` — Visual intro, execution traces, benchmarks

## Use Cases

### LLM Verification (Most Timely)
```python
# Problem: "How do I know this LLM answer is actually correct?"
# Solution: Run through multiple reasoning paths, verify convergence

investigator = LLMReasoningRobustness(problem)
result = investigator.run_investigation()

if result['confidence'] > 0.75:
    act_on_conclusion(result['conclusion'])
else:
    flag_for_human_review()
```

### Medical Diagnosis
Multiple diagnostic pathways (different specialists, test orders) that converge = higher confidence before treatment.

### Incident Root Cause Analysis
Multiple investigation teams starting from different hypotheses converge = robust root cause identification.

## Technical Overview

**6-Phase Iteration:**
1. **Investigation** — Branches evaluate current evidence
2. **Evaluation** — Score each hypothesis
3. **Resource Allocation** — INVERSE ranking (weakest gets scrutiny)
4. **Evidence Gathering** — Branches propose new data
5. **Starvation & Culling** — Non-improving branches die
6. **Convergence Check** — Did they agree?

## Implementations

| | Python | C++ |
|---|---|---|
| **Use Case** | Research, production, LLM applications | Performance-critical, benchmarks |
| **Setup** | `pip install` | `g++ compile` |
| **Extensibility** | Easy (subclass framework) | Moderate (templates) |
| **PyPI Ready** | ✅ Yes | ❌ No |

## License

MIT - See LICENSE file

Questions? Open an issue on GitHub.
