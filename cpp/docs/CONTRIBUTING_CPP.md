# Contributing to False Feet Algorithm

Thank you for your interest in contributing! This document outlines how to get involved.

## Ways to Contribute

### 1. Apply to New Domains
- Recipe/meal planning
- Product recommendation
- QA/document retrieval
- Math/logic puzzles
- Historical event analysis
- Any problem with evidence and reasoning

See examples in `examples/` and documentation in `docs/`.

### 2. Improve Implementation
- Add neural evaluator (see `docs/amoeba_algorithm_spec.md` Section 4)
- Optimize performance (parallel execution, caching)
- Improve memory efficiency
- Add GPU support

### 3. Benchmarking & Research
- Compare against LLMs, tree search, other baselines
- Analyze convergence properties
- Test on real-world datasets
- Publish findings

### 4. Documentation
- Add tutorials for new domains
- Create more examples
- Improve clarity
- Add diagrams and visualizations

### 5. Bug Reports & Features
- Report issues or unexpected behavior
- Suggest algorithm improvements
- Request features

## Getting Started

### Setup
```bash
git clone https://github.com/zachdwight/false-feet-algorithm.git
cd false-feet-algorithm
g++ -std=c++17 -O2 src/poirot_main.cpp -o solver
./solver
```

### Project Structure
```
false-feet-algorithm/
├── src/                    # C++ source code
│   ├── poirot_mystery.h    # Data structures
│   ├── poirot_solver.h     # Algorithm
│   └── poirot_main.cpp     # Demo scenario
├── docs/                   # Documentation
│   ├── QUICK_START.md      # Visual intro
│   ├── EXECUTION_TRACE.md  # Walkthrough
│   ├── INDEX.md            # Guide
│   └── amoeba_algorithm_spec.md  # Formal spec
├── examples/               # Pre-compiled demos
├── tests/                  # Test cases (add here!)
└── README.md              # Project overview
```

## Code Style

### C++ (src/)
- **Standard:** C++17
- **Naming:** snake_case for functions, UPPER_CASE for constants
- **Comments:** Document complex logic, explain WHY not just WHAT
- **Headers:** Use guards, keep dependencies minimal
- **Example:**
```cpp
// Calculate the score for a theory
// Takes into account evidence, motive, and consistency
float evaluate_theory(const Theory& theory, 
                     const SharedEvidencePool& pool) {
    // ... implementation
}
```

### Documentation (docs/)
- Use Markdown with clear headings
- Include code examples where relevant
- Add diagrams for complex concepts
- Link between related documents

### Commit Messages
```
Short description (50 chars max)

Longer description explaining:
- What changed and why
- Any breaking changes
- References to issues

Example:
  Add neural evaluator training

  Implements self-supervised training procedure
  from Section 4 of algorithm spec. Uses
  convergence outcomes as training signal.
  
  Fixes #42, relates to #15
```

## Adding a New Domain

### Steps

1. **Create a new file** in `examples/` (or new folder)
   ```
   examples/recipe_planner/
   ├── recipe_solver.h
   ├── recipe_main.cpp
   └── README.md (explain the domain)
   ```

2. **Define domain concepts** replacing Evidence/Suspect:
   ```cpp
   struct Recipe { ... }
   struct Ingredient { ... }
   class RecipeSolver { ... }
   ```

3. **Implement evaluator** for your domain:
   ```cpp
   class RecipeEvaluator {
       float evaluate(const Recipe& recipe) {
           // Score based on:
           // - Ingredient availability
           // - Nutritional value
           // - Preparation time
       }
   };
   ```

4. **Test thoroughly** with your domain data

5. **Document it** with:
   - README explaining the domain
   - Example usage
   - Sample output

6. **Submit** (see below)

## Submitting Contributions

### Small Changes (typos, docs)
1. Fork the repo
2. Create a branch: `git checkout -b fix/typo-in-docs`
3. Make changes
4. Commit: `git commit -am 'Fix typo in QUICK_START.md'`
5. Push: `git push origin fix/typo-in-docs`
6. Create Pull Request

### New Features (domains, improvements)
1. Fork the repo
2. Create branch: `git checkout -b feature/recipe-planner`
3. Implement thoroughly
4. Add tests (in `tests/`)
5. Document (in `docs/` or example README)
6. Test: `g++ -std=c++17 -O2 src/*.cpp -o test && ./test`
7. Commit with clear message
8. Push and create Pull Request with:
   - What you added
   - Why it matters
   - How to use it
   - Any limitations

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New domain/example
- [ ] Algorithm improvement
- [ ] Documentation
- [ ] Bug fix
- [ ] Performance improvement

## How to Test
Steps to verify the change works

## Documentation
- [ ] Updated relevant docs
- [ ] Added code comments
- [ ] Added examples

## Related Issues
Fixes #123
```

## Testing

### Run the Demo
```bash
g++ -std=c++17 -O2 src/poirot_main.cpp -o solver
./solver
```

### Expected Output
- All branches should investigate
- Evidence pool should grow
- Weak branches should be allocated more slots
- Eventually converge to butler as guilty

### For New Domains
Create test cases that verify:
1. ✅ Algorithm converges
2. ✅ Solution is correct
3. ✅ Weak theories get chances
4. ✅ Resource allocation is inverse
5. ✅ Shared pool works correctly

## Documentation Standards

### For Code
- Every class should have brief comment explaining purpose
- Complex functions should have comments explaining algorithm
- Use `//` for single line, `/* */` for blocks

### For Markdown
```markdown
# Main Title
## Section
### Subsection

**Bold** for emphasis
`code` for inline
\`\`\`cpp
// Code blocks
\`\`\`

Use bullet points for lists
- Item 1
- Item 2
```

## Areas We Need Help With

1. **Neural Evaluator** — Implement learnable scoring (see spec Section 4)
2. **GPU Acceleration** — Parallelize branch execution
3. **Benchmarking** — Compare against LLMs, tree search
4. **New Domains** — Recipe planner, QA system, etc.
5. **Visualization** — Web UI showing investigation progress
6. **Python Port** — Rewrite in Python with PyTorch

## Questions?

- Check documentation first: `docs/INDEX.md`
- Review existing examples: `examples/`
- Read the algorithm spec: `docs/amoeba_algorithm_spec.md`
- Open a discussion issue

## Code of Conduct

- Be respectful and inclusive
- Assume good intent
- Focus on the code, not the person
- Help others learn

---

**Thanks for contributing to the False Feet Algorithm! 🧬**
