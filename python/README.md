# False Feet Algorithm

> **Amoeba: Novel Multi-Branch Hypothesis Evaluation with Inverse Resource Allocation**

A Python library for solving complex reasoning problems through competitive multi-branch investigation. The algorithm forces weak hypotheses to strengthen or die off by allocating MORE resources to them, not less. When multiple independent reasoning paths converge on the same answer, that's a robust signal.

## Quick Start

```bash
pip install false-feet-algorithm
```

Run the examples:

```bash
python -m false_feet_algorithm.examples.mystery_solving
python -m false_feet_algorithm.examples.clinical_diagnosis
```

## How It Works

The 6-phase algorithm repeats until convergence:

1. **Investigation** — Branches evaluate current evidence
2. **Evaluation** — Score each hypothesis (0-1)
3. **Resource Allocation** — **INVERSE ranking (weakest gets most resources!)**
4. **Evidence Gathering** — Branches propose new evidence to test
5. **Starvation & Culling** — Non-improving branches die off
6. **Convergence Check** — All branches agree? → Problem solved

## Use It for Your Domain

Extend the framework with your own hypothesis evaluation logic:

```python
from false_feet_algorithm.core import Problem, Option, DataPoint, BaseBranch, BaseEvaluator, AmoebaInvestigation

class YourBranch(BaseBranch):
    def evaluate(self, data_pool):
        # Your domain-specific reasoning
        return score  # 0.0-1.0
    
    def propose_data(self, data_pool):
        # Suggest the next evidence to gather
        return proposed_evidence_ids

class YourEvaluator(BaseEvaluator):
    def evaluate(self, branch, data_pool):
        # Your scoring logic
        return score

# Set up the problem
problem = Problem(title="My Problem")
problem.add_option(Option("hypothesis_1"))
problem.add_option(Option("hypothesis_2"))
# ... add evidence ...

# Solve it
solver = AmoebaInvestigation(
    problem,
    branch_class=YourBranch,
    evaluator=YourEvaluator()
)
result = solver.solve()
print(f"Best hypothesis: {result.option.id}")
```

## Examples Included

- **Mystery Solving** — Classic logic puzzle (identify the culprit from clues)
- **Medical Diagnosis** — Differential diagnosis from symptoms and tests

## Visualization (Optional)

Install with visualization support:

```bash
pip install false-feet-algorithm[viz]
```

Then use the built-in plotting utilities to visualize algorithm convergence.

## Features

- ✅ Pure Python, minimal dependencies
- ✅ Generic framework for any hypothesis evaluation problem
- ✅ 39 comprehensive tests (Python 3.8+)
- ✅ Optional matplotlib visualization
- ✅ Well-documented API with examples

## Testing

```bash
pytest
```

## License

MIT License

## Learn More

For the complete algorithm specification and C++ reference implementation, see the [GitHub repository](https://github.com/zachdwight/false-feet-algorithm).
