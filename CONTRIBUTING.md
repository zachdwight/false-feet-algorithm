# Contributing to False Feet Algorithm

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions.

## Getting Started

1. **Fork and clone** the repository
2. **Create a virtual environment**: `python -m venv venv && source venv/bin/activate`
3. **Install in development mode**: `pip install -e ".[dev,viz]"`
4. **Run tests**: `pytest`

## Making Changes

### Code Style

- Follow PEP 8
- Use type hints throughout
- Write clear docstrings for public APIs
- Keep functions focused and testable

### Testing

- Write tests for new functionality
- Maintain or improve test coverage
- Run tests before submitting: `pytest --cov`

```bash
# Run specific test
pytest false_feet_algorithm/tests/test_core.py::TestOption::test_create_option

# Run with coverage report
pytest --cov=false_feet_algorithm
```

### Commit Messages

- Use clear, descriptive commit messages
- Reference issues if applicable: "Fixes #123"
- Use present tense: "Add feature" not "Added feature"

## Documentation

- Update README.md if adding user-facing features
- Add docstrings to all public functions
- Update examples if behavior changes
- Consider adding/updating examples for new features

## Submitting Changes

1. Create a branch for your feature: `git checkout -b feature/my-feature`
2. Make your changes and commit
3. Push to your fork
4. Submit a pull request with a clear description

## Reporting Issues

- Check if the issue already exists
- Include steps to reproduce
- Provide example code if possible
- Specify Python version and OS

## Future Development Areas

- Performance optimizations for large-scale problems
- Advanced convergence detection strategies
- Integration with machine learning frameworks
- Extended visualization capabilities
- Multi-threaded branch evaluation

## Questions?

Open an issue or discussion on GitHub.

Happy contributing!
