# Repository Instructions

Repository-wide instructions for GitHub Copilot in this codebase.

## Architectural Constraints

ENFORCE precedence hierarchy: Standards -> Diagrams -> Workflows -> Style Guides -> Testing -> Implementations

REQUIRE:

- TDD-first development (write tests before implementation)
- Single source of truth (no duplicate definitions)
- Zero-tolerance security policies (no hardcoded secrets)

ENFORCE repository standards through layered validation:

- Pre-commit hooks (local validation)
- CI validators (automated checks)
- Human review gates (protected operations)

## CI/CD Architecture Standards

Orchestrator workflows:

- MUST contain `uses:` only
- NEVER use `run:` or `shell:` directly

Reusable workflows:

- MUST use `workflow_call`
- MUST encapsulate single responsibilities

Composite actions:

- MUST be thin wrappers calling scripts only

Scripts:

- ALWAYS the source of truth for logic
- Platform-specific: `scripts/*.sh` (Linux), `scripts/*.ps1` (Windows)

Action pinning:

- MUST use MAJOR version only (@v4)
- NEVER use branches or minor/patch pins

## Output Generation Standards

REQUIRE:

- File length under 500 lines
- Single responsibility per module
- Conventional commit messages with pre-commit validation

Response format:

- Table-based change summaries with status indicators
- Single-action command blocks for diagnostics
- Sequential chains preserved for workflows
- Token-efficient responses; favor links over repetition

## Quality Assurance Protocols

REQUIRE codebase-retrieval before edits to verify:

- File paths exist
- Function signatures match expectations
- API endpoints are valid
- Existing patterns in the codebase

NEVER fabricate:

- Code or configuration syntax
- API endpoints or URLs
- Version-specific features
- Package versions

REQUIRE pre-commit hooks before all commits:

- Linting validation
- Security scanning
- Format checking

ENFORCE:

- Greater than 80% code coverage for critical paths
- NEVER skip tests to meet deadlines
- Least-privilege access patterns

## Operational Boundaries

REQUIRE human approval for:

- Destructive operations (deletion, force-push)
- Production deployment
- Security configuration changes
- Control document modifications

REQUIRE rollback plans for all deployments with tested procedures.

NEVER:

- Log or expose secrets, credentials, PII
- Suggest overly permissive configurations
- Bypass validation steps

REQUIRE license compatibility checks before adding dependencies.

## Integration Standards

Git operations:

- REQUIRE conventional commits
- NEVER push to remote without user approval
- Check `git status --porcelain` for unintended deletions before commit

Testing:

- REQUIRE TDD-first (write tests before implementation)
- Run tests to confirm they fail before implementing
- Implement minimal code to pass tests
- Refactor with passing tests

Logging and monitoring:

- REQUIRE structured JSON logging
- Prometheus-compatible metrics where applicable

Environment promotion:

- dev -> staging -> production
- NEVER skip staging for production deployments

## Context Window Management

Be aware of instruction file character limits:

| File Type | Max Characters |
|-----------|----------------|
| Repository instructions | 8,000 |
| Path-specific instructions | 8,000 |
| Prompt files | 8,000 |
| Agent files | 30,000 |
| Code review | 4,000 |

Token allocation strategy:

- Reserve 10-15% for directives and rules
- Allocate 70-80% for codebase context and conversation
- Reserve 10-15% for output generation

WARN when context load approaches limits.

