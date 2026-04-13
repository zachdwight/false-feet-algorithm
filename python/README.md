# False Feet Algorithm

> **Amoeba: Novel Multi-Branch Hypothesis Evaluation with Inverse Resource Allocation**

A powerful algorithm for solving complex reasoning problems through competitive multi-branch investigation. Instead of giving more resources to strong hypotheses, we give MORE to weak ones—forcing them to improve or die off. When multiple independent reasoning paths converge on the same answer, that's a very robust signal.

## 📦 Two Implementations

This repository contains **both C++ (original) and Python (new) implementations**:

### 🐍 **Python Version** (`python/`)
- **Pure Python**, minimal dependencies  
- Generic framework for any hypothesis evaluation problem
- Medical diagnosis and mystery solving examples
- 39 comprehensive tests (all passing)
- Visualization tools (optional matplotlib)
- **Ready for PyPI publication**

```bash
cd python
pip install -e .
python -m false_feet_algorithm.examples.mystery_solving
```

### ⚡ **C++ Version** (`cpp/`)
- High-performance reference implementation
- Original mystery solver ("The Vanished Necklace")
- Generic framework with benchmarks
- Full specification and execution traces

```bash
cd cpp
g++ -std=c++17 -O2 src/poirot_main.cpp -o solver
./solver
```

---

## 🎯 Core Innovation

**Instead of giving resources to strong hypotheses, we give MORE to weak ones.**

When weak branches are forced to improve or die off, and multiple independent reasoning paths converge on the same answer despite different starting assumptions—that's a highly robust signal.

### The 6-Phase Algorithm

Each iteration:
1. **Investigation** — Branches evaluate current evidence
2. **Evaluation** — Score each hypothesis (0-1)
3. **Resource Allocation** — **INVERSE ranking (weakest gets most slots!)**
4. **Evidence Gathering** — Branches propose new data to investigate
5. **Starvation & Culling** — Non-improving branches gradually die
6. **Convergence Check** — All agree? → SOLVED

---

## 🐍 Python Quick Start

```bash
cd python
pip install -e ".[viz]"

python -m false_feet_algorithm.examples.mystery_solving
python -m false_feet_algorithm.examples.clinical_diagnosis
```

### Extend for Your Domain

```python
from false_feet_algorithm.core import Problem, Option, DataPoint, BaseBranch, BaseEvaluator, AmoebaInvestigation

class YourBranch(BaseBranch):
    def evaluate(self, data_pool):
        # Your domain reasoning logic
        return score  # 0.0-1.0
    
    def propose_data(self, data_pool):
        # Suggest next evidence/tests
        return proposed_ids

class YourEvaluator(BaseEvaluator):
    def evaluate(self, branch, data_pool):
        # Your scoring logic
        return score

problem = Problem(title="Your Problem")
# ... add options and evidence ...

solver = AmoebaInvestigation(
    problem,
    branch_class=YourBranch,
    evaluator=YourEvaluator()
)
result = solver.solve()
```

---

## 📚 Documentation

### Python (`python/`)
- API docs in `false_feet_algorithm/core/`
- Examples in `false_feet_algorithm/examples/`
- Tests in `false_feet_algorithm/tests/`
- Full README in `python/README.md`

### C++ (`cpp/`)
- **QUICK_START.md** — Visual introduction (15 min)
- **EXECUTION_TRACE.md** — Detailed walkthrough (1 hour)
- **amoeba_algorithm_spec.md** — Full formal spec (4+ hours)
- **BENCHMARKS.md** — Performance analysis
- Source code in `src/`

---

## 🧪 Test Case: The Vanished Necklace

Both versions solve the classic mystery:
- **Problem:** Identify the culprit among 4 suspects
- **Evidence:** 13 pieces of investigative clues
- **Solution:** All branches converge on **Butler** ✅

Run it:
```bash
# Python
cd python && python -m false_feet_algorithm.examples.mystery_solving

# C++
cd cpp && g++ -std=c++17 -O2 src/poirot_main.cpp -o solver && ./solver
```

---

## 📦 Publishing (Python)

The Python implementation is ready for PyPI:

```bash
cd python
pip install build twine
python -m build
twine upload dist/*
```

Users can then install with:
```bash
pip install false-feet-algorithm
pip install false-feet-algorithm[viz]  # With visualization
```

---

## 📊 Quick Comparison

| Aspect | Python | C++ |
|--------|--------|-----|
| **Language** | Python 3.7+ | C++17 |
| **Speed** | Good | Excellent |
| **Setup** | `pip install` | `g++ compile` |
| **Extensibility** | Easy (subclass) | Moderate (templates) |
| **Dependencies** | Minimal (none core) | None |
| **Best For** | Research, production | Performance-critical |
| **PyPI Ready** | ✅ Yes | ❌ No |

---

## 🤝 Contributing

See CONTRIBUTING.md for development guidelines.

**Ways to contribute:**
- **Python:** New domains, improved evaluators, optimizations
- **C++:** Benchmarking, performance optimization, research
- **Both:** Examples, documentation, tutorials

---

## 📄 License

MIT License - see LICENSE file

---

**Next steps:**
1. **Python users:** `cd python && pip install -e ".[viz]"`
2. **C++ users:** `cd cpp && cat docs/QUICK_START.md`
3. **Researchers:** `cd cpp && cat docs/BENCHMARKS.md`

Questions? Open an issue on GitHub.
