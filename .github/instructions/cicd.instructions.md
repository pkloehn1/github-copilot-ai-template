---
applyTo: ".github/workflows/**,.github/actions/**"
---

# CI/CD Instructions

Path-specific instructions for CI/CD workflow and action files.

## Workflow Architecture

Orchestrator workflows:

- MUST contain `uses:` only
- NEVER use `run:` or `shell:` directly in orchestrators
- Delegate logic to reusable workflows or composite actions

Reusable workflows:

- MUST use `workflow_call` trigger
- MUST encapsulate single responsibility
- MUST define clear inputs and outputs

Composite actions:

- MUST be thin wrappers calling scripts
- Logic belongs in `scripts/` directory

## Action Pinning

REQUIRE:

- MAJOR version pins only (@v4)
- SHA pins for third-party actions in security-sensitive workflows

NEVER:

- Pin to branches (@main, @master)
- Pin to minor/patch versions (@v4.1.2)

## Scripts as Source of Truth

REQUIRE:

- All logic in `scripts/` directory
- Platform-specific variants: `*.sh` (Linux), `*.ps1` (Windows)
- Workflows call scripts, not inline commands

## Validation

REQUIRE before merge:

- Workflow syntax validation (actionlint)
- Security scanning for secrets exposure
- Required status checks passing
