---
applyTo: "**/*.py"
---

# Python Development Instructions

These instructions apply to all Python files in the repository.
Source of truth: `docs/python-style-guide.md`

## Code Style & Formatting

**ENFORCE** via `ruff`:
- **Line Length**: 100 characters
- **Target Version**: Python 3.12+
- **Docstrings**: Google convention (`pydocstyle`)
- **Imports**: Sorted and organized (`isort` rules)
- **Formatting**: `ruff format` (Black-compatible)

**REQUIRE**:
- **Type Hints**: Mandatory for all function signatures and public variables.
- **Naming**:
  - `snake_case` for functions, variables, modules
  - `PascalCase` for classes, exceptions
  - `UPPER_CASE` for constants
- **Docstrings**: Mandatory for all modules, classes, and public functions.

## Testing

**REQUIRE**:
- Framework: `pytest`
- Location: `tests/` directory
- Naming: `test_*.py` files, `test_*` functions
- Coverage: Aim for >80% coverage

## Best Practices

**PREFER**:
- `pathlib.Path` over `os.path`
- f-strings over `.format()` or `%` formatting
- Context managers (`with` statements) for resource management
- Explicit imports over wildcard imports (`from module import *`)

**NEVER**:
- Use mutable default arguments (e.g., `def foo(x=[])`)
- Catch generic `Exception` without re-raising or logging
- Hardcode secrets or credentials
