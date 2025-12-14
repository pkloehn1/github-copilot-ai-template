---
applyTo: "**/*.py,**/*.sh,**/*.ps1,**/*.js,**/*.ts"
---

# Development Instructions

Path-specific instructions for application code files.

## Test-Driven Development

REQUIRE:

- Write tests before implementation
- Run tests to confirm they fail
- Implement minimal code to pass
- Refactor with passing tests

NEVER:

- Skip tests to meet deadlines
- Commit code without passing tests

## Git Workflow

REQUIRE:

- Conventional commit messages
- Feature branches for changes
- PR review before merge

Protected operations (user approval required):

- Push to remote
- Force push
- Branch deletion
- PR merge

## Code Quality

REQUIRE:

- Linting passes before commit
- Format validation (language-specific formatter)
- No hardcoded secrets or credentials

ENFORCE:

- Single responsibility per module
- Files under 500 lines
- Functions under 50 lines

## Documentation

REQUIRE:

- Docstrings for public functions
- Type hints where language supports
- README for modules with external interfaces

