# Changelog

All notable changes to the False Feet Algorithm Python implementation will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-13

### Added
- Initial Python port of False Feet Algorithm
- Core framework classes: `Problem`, `Option`, `DataPoint`, `SharedDataPool`
- `EvaluationBranch` and `BaseBranch` for custom domain logic
- `HypothesisEvaluator` and `BaseEvaluator` for custom scoring
- `AmoebaInvestigation` solver implementing 6-phase algorithm:
  - Investigation Phase
  - Evaluation Phase
  - Resource Allocation Phase (inverse ranking)
  - Evidence Gathering Phase
  - Starvation & Culling Phase
  - Convergence Check Phase
- Clinical diagnosis example with custom medical evaluator
- Mystery solving reference implementation
- 39 comprehensive tests (31 unit + 8 integration)
- Logging module with configurable levels
- Visualization tools (optional matplotlib support)
- Complete documentation with examples
- Type hints throughout codebase

### Features
- Generic, reusable framework for any hypothesis evaluation domain
- Clean Python API with subclassing for customization
- Configurable parameters: iterations, pool size, starvation threshold
- Optional visualization of branch survival and convergence
- Zero core dependencies (minimal stdlib only)

### Testing
- Unit tests for all core classes
- Integration tests for complete workflows
- Example tests demonstrating clinical and mystery solving
- 100% test pass rate

### Documentation
- README with quick start and architecture overview
- Docstrings for all public APIs
- Two fully worked examples (medical diagnosis, mystery solving)
- Contributing guidelines

---

## Upcoming

### [0.2.0] - Planned
- Enhanced convergence detection strategies
- Performance optimizations for large-scale problems
- Additional domain examples
- Extended visualization capabilities
- Integration with ML frameworks

### [0.3.0] - Planned
- Multi-threaded branch evaluation
- GPU acceleration
- Advanced statistical reporting
