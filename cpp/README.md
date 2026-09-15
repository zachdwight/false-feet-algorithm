# False Feet Algorithm - C++ Implementation

> **Multi-branch hypothesis evaluation with inverse resource allocation**

A high-performance C++ implementation of the Amoeba Algorithm for solving complex reasoning problems through competitive multi-branch investigation.

## Quick Start

### Compile and Run

```bash
cd cpp

# Compile the Poirot mystery example
g++ -std=c++17 -O2 src/poirot_main.cpp -o poirot_solver
./poirot_solver

# Compile the generic product recommendation example
g++ -std=c++17 -O2 src/generic_main.cpp -o generic_solver
./generic_solver

# Compile the LLM reasoning robustness example
g++ -std=c++17 -O2 examples/llm_reasoning_robustness.cpp -o llm_solver
./llm_solver
```

## Examples Included

- **Mystery Solving** — Classic deduction puzzle (identify the culprit from clues)
- **Product Recommendation** — Evaluate products against customer requirements
- **LLM Reasoning Robustness** — Verify LLM answer quality by checking convergence across multiple independent reasoning paths (step-by-step, devil's advocate, constraint-based, evidence-first)

## How It Works

The 6-phase algorithm repeats until convergence:

1. **Investigation** — Branches evaluate current evidence
2. **Evaluation** — Score each hypothesis (0-1)
3. **Resource Allocation** — **INVERSE ranking (weakest gets most resources!)**
4. **Evidence Gathering** — Branches propose new evidence to test
5. **Starvation & Culling** — Non-improving branches die off
6. **Convergence Check** — All branches agree? → Problem solved

## Use It for Your Domain

Extend the framework with your own evaluation logic:

```cpp
#include "amoeba_solver.h"

// Set up your problem
Problem problem;
problem.title = "Your Problem";
problem.goal = "Your Goal";

// Add options (hypotheses to evaluate)
problem.options = {
    Option{"option_1", "Option A", "Description", "Context", 50},
    Option{"option_2", "Option B", "Description", "Context", 45}
};

// Add data points (evidence)
problem.all_data.push_back(DataPoint{
    "data_1",
    "Evidence title",
    "Description of evidence",
    {"option_1"},      // supports
    {"option_2"},      // contradicts
    5                  // weight
});

// Solve it
AmoebaInvestigation solver(problem);
solver.solve();
```

## Features

- ✅ Pure C++17, minimal dependencies
- ✅ Generic framework for any hypothesis evaluation problem
- ✅ High-performance for large problem spaces
- ✅ Clear visualized output during investigation
- ✅ Well-documented examples

## Testing

Run the benchmark suite to verify performance:

```bash
g++ -std=c++17 -O2 src/benchmark.cpp -o benchmark
./benchmark
```

## Performance Notes

- Single-threaded, deterministic algorithm
- Memory efficient: O(N × M) where N = options, M = data points
- Iteration count depends on convergence (typically 2-6 rounds)
- Scales well to 100+ options and 1000+ evidence points

## Documentation

- **Quick Start Guide** — `docs/QUICK_START.md` — Visual intro and conceptual overview
- **Root README** — See parent directory for algorithm overview

## License

MIT License

## Learn More

For the Python implementation, algorithm specification, and additional examples, see the [GitHub repository](https://github.com/zachdwight/false-feet-algorithm).
