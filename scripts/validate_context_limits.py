#!/usr/bin/env python3
"""Validate GitHub Copilot instruction file token limits.

Based on official GitHub Copilot and LLM provider documentation.
Cross-platform script (Windows/Linux/macOS).
"""

import argparse
import fnmatch
import subprocess
import sys
from pathlib import Path
from statistics import quantiles
from typing import Any, NamedTuple

# =============================================================================
# LLM Provider Configurations
# =============================================================================
# Context windows are from official provider documentation (December 2025).
# Instruction limits are 4% of context window (middle of 3-5% recommended range).
# Reference: https://docs.github.com/copilot/reference/ai-models/supported-models
#
# File patterns are based on GitHub Copilot agent instructions documentation:
# - CLAUDE.md: Anthropic Claude models
# - GEMINI.md: Google Gemini models
# - AGENTS.md, .github/copilot-instructions.md: Default (any model)
# =============================================================================
LLM_PROVIDERS: dict[str, dict[str, Any]] = {
    "anthropic": {
        "display_name": "Anthropic Claude",
        "file_patterns": ["CLAUDE.md"],
        "context_window_tokens": 200_000,  # Claude Sonnet 4/4.5, Opus 4/4.5, Haiku 4.5
        "instruction_limit_pct": 4,  # 4% of context window
    },
    "google": {
        "display_name": "Google Gemini",
        "file_patterns": ["GEMINI.md"],
        "context_window_tokens": 1_048_576,  # Gemini 2.5/3 Pro
        "instruction_limit_pct": 4,  # 4% of context window
    },
    "openai": {
        "display_name": "OpenAI GPT",
        "file_patterns": ["GPT.md", "OPENAI.md"],
        "context_window_tokens": 1_047_576,  # GPT-4.1
        "instruction_limit_pct": 4,  # 4% of context window
    },
    "xai": {
        "display_name": "xAI Grok",
        "file_patterns": ["GROK.md", "XAI.md"],
        "context_window_tokens": 1_000_000,  # Grok Code Fast 1
        "instruction_limit_pct": 4,  # 4% of context window
    },
    "default": {
        "display_name": "Default (Copilot)",
        "file_patterns": [
            "AGENTS.md",
            ".github/copilot-instructions.md",
            ".github/instructions/*.instructions.md",
            ".github/prompts/*.prompt.md",
            ".github/agents/*.agent.md",
        ],
        # Use most conservative limit (Claude's 200K) for generic files
        "context_window_tokens": 200_000,
        "instruction_limit_pct": 4,  # 4% of context window
    },
}


def get_provider_for_file(file_path: Path) -> str:
    """Detect LLM provider from filename pattern.

    Args:
        file_path: Path to the instruction file.

    Returns:
        Provider key (e.g., 'anthropic', 'google', 'default').
    """
    filename = file_path.name
    rel_path = str(file_path).replace("\\", "/")

    for provider_key, config in LLM_PROVIDERS.items():
        if provider_key == "default":
            continue  # Check default last
        for pattern in config["file_patterns"]:
            if fnmatch.fnmatch(filename, pattern) or fnmatch.fnmatch(rel_path, pattern):
                return provider_key

    return "default"


def get_provider_token_limit(provider_key: str) -> int:
    """Get instruction token limit for a provider.

    Args:
        provider_key: Provider key (e.g., 'anthropic', 'google').

    Returns:
        Token limit for instruction files (4% of context window).
    """
    config = LLM_PROVIDERS.get(provider_key, LLM_PROVIDERS["default"])
    context_tokens = config["context_window_tokens"]
    limit_pct = config["instruction_limit_pct"]
    return context_tokens * limit_pct // 100


class ValidationResult(NamedTuple):
    """Result of validating a single file."""

    path: str
    char_count: int
    token_count: int
    token_limit: int
    provider: str
    status: str  # "ok", "info", "warning", "error"


class CategoryResult(NamedTuple):
    """Result of validating a category budget."""

    category_name: str
    total_chars: int
    budget: int
    status: str  # "ok", "info", "warning", "error"


class BaselineStats(NamedTuple):
    """Statistics computed from baseline (reference branch) files."""

    q1: float
    q3: float
    iqr: float
    lower_fence: float
    upper_fence: float
    file_count: int


def get_changed_files(ref_branch: str, repo_root: Path) -> list[Path]:
    """Get list of files changed between ref_branch and HEAD.

    Args:
        ref_branch: Reference branch to compare against (e.g., 'origin/main').
        repo_root: Root directory of the repository.

    Returns:
        List of Paths for files that are new or modified in HEAD vs ref_branch.
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{ref_branch}...HEAD"],
            capture_output=True,
            text=True,
            cwd=repo_root,
            check=True,
        )
        changed = []
        for line in result.stdout.strip().split("\n"):
            if line:
                changed.append(repo_root / line)
        return changed
    except subprocess.CalledProcessError:
        return []


def get_file_content_from_branch(file_path: str, branch: str, repo_root: Path) -> str | None:
    """Read file content from a specific git branch without checkout.

    Args:
        file_path: Path relative to repo root (e.g., '.github/instructions/foo.md').
        branch: Git branch or ref to read from (e.g., 'origin/main').
        repo_root: Root directory of the repository.

    Returns:
        File content as string, or None if file doesn't exist on that branch.
    """
    try:
        result = subprocess.run(
            ["git", "show", f"{branch}:{file_path}"],
            capture_output=True,
            text=True,
            cwd=repo_root,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return None


def get_baseline_file_sizes(
    patterns: list[str],
    ref_branch: str,
    repo_root: Path,
) -> dict[str, list[tuple[str, int]]]:
    """Get file sizes from reference branch for baseline calculation.

    Args:
        patterns: List of glob patterns to match (e.g., '.github/instructions/*.md').
        ref_branch: Reference branch to read files from.
        repo_root: Root directory of the repository.

    Returns:
        Dict mapping pattern to list of (file_path, char_count) tuples.
    """
    # Get list of files on the reference branch using git ls-tree
    try:
        result = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", ref_branch],
            capture_output=True,
            text=True,
            cwd=repo_root,
            check=True,
        )
        all_files = result.stdout.strip().split("\n")
    except subprocess.CalledProcessError:
        return {}

    baseline_files: dict[str, list[tuple[str, int]]] = {}

    for pattern in patterns:
        baseline_files[pattern] = []
        for file_path in all_files:
            # Match pattern using Path matching
            if Path(file_path).match(pattern.lstrip("*").lstrip("/")):
                content = get_file_content_from_branch(file_path, ref_branch, repo_root)
                if content is not None:
                    baseline_files[pattern].append((file_path, len(content)))

    return baseline_files


def compute_baseline_stats(
    file_sizes: list[int],
    iqr_multiplier: float = 1.5,
) -> BaselineStats | None:
    """Compute baseline statistics (Q1, Q3, IQR, fences) from file sizes.

    Args:
        file_sizes: List of character counts from baseline files.
        iqr_multiplier: IQR multiplier for fences (1.5=mild, 3=extreme).

    Returns:
        BaselineStats with computed values, or None if insufficient data.
    """
    if len(file_sizes) < 4:
        return None

    q1, _, q3 = quantiles(file_sizes, n=4)
    iqr = q3 - q1

    if iqr == 0:
        return None

    lower_fence = q1 - iqr_multiplier * iqr
    upper_fence = q3 + iqr_multiplier * iqr

    return BaselineStats(
        q1=q1,
        q3=q3,
        iqr=iqr,
        lower_fence=lower_fence,
        upper_fence=upper_fence,
        file_count=len(file_sizes),
    )


def load_config(config_path: Path) -> dict[str, int | float]:
    """Load configuration from copilot-limits.conf."""
    config = {}
    if not config_path.exists():
        print(f"ERROR: Configuration file not found: {config_path}")
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                value = value.strip()
                # Parse as float if contains decimal point, else int
                if "." in value:
                    config[key.strip()] = float(value)
                else:
                    config[key.strip()] = int(value)
    return config


def get_char_count(file_path: Path) -> int:
    """Get character count of a file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            return len(f.read())
    except (OSError, UnicodeDecodeError):
        return 0


def estimate_tokens(char_count: int, chars_per_token: int = 4) -> int:
    """Estimate token count from character count.

    Args:
        char_count: Number of characters.
        chars_per_token: Average characters per token (default: 4 for English/code).

    Returns:
        Estimated number of tokens, rounded up.
    """
    if char_count == 0:
        return 0
    # Use ceiling division to round up
    return (char_count + chars_per_token - 1) // chars_per_token


def find_files(root: Path, pattern: str) -> list[Path]:
    """Find files matching a glob pattern or exact path."""
    # Check if it's an exact file path first
    exact_path = root / pattern
    if exact_path.is_file():
        return [exact_path]
    # Otherwise use glob
    return list(root.glob(pattern))


def validate_file(
    file_path: Path,
    chars_per_token: int,
    info_pct: int,
    warn_pct: int,
) -> ValidationResult:
    """Validate a single file against its provider-specific token limit.

    Args:
        file_path: Path to the file to validate.
        chars_per_token: Characters per token for estimation.
        info_pct: Percentage of limit for INFO status.
        warn_pct: Percentage of limit for WARN status.

    Returns:
        ValidationResult with provider-specific token limit applied.
    """
    char_count = get_char_count(file_path)
    token_count = estimate_tokens(char_count, chars_per_token)

    provider = get_provider_for_file(file_path)
    token_limit = get_provider_token_limit(provider)

    info_threshold = token_limit * info_pct // 100
    warn_threshold = token_limit * warn_pct // 100

    if token_count > token_limit:
        status = "error"
    elif token_count > warn_threshold:
        status = "warning"
    elif token_count > info_threshold:
        status = "info"
    else:
        status = "ok"

    return ValidationResult(
        path=str(file_path),
        char_count=char_count,
        token_count=token_count,
        token_limit=token_limit,
        provider=provider,
        status=status,
    )


OutlierResult = tuple[list[int], list[int]]


def detect_outliers(file_sizes: list[int], iqr_multiplier: float = 1.5) -> OutlierResult:
    """Detect files that are statistical outliers using IQR method.

    Uses Tukey's fences: values outside Q1 - k*IQR or Q3 + k*IQR are outliers.
    More robust than stddev method as it's not affected by extreme values.

    Args:
        file_sizes: List of character counts for files in a category.
        iqr_multiplier: IQR multiplier for fences (1.5=mild, 3=extreme).

    Returns:
        Tuple of (lower_outlier_indices, upper_outlier_indices).
    """
    if len(file_sizes) < 4:
        # Need at least 4 points for meaningful quartiles
        return [], []

    # Get quartiles using Python stdlib (returns [Q1, Q2, Q3] for n=4)
    q1, _, q3 = quantiles(file_sizes, n=4)
    iqr = q3 - q1

    if iqr == 0:
        return [], []  # All files clustered, no outliers

    lower_fence = q1 - iqr_multiplier * iqr
    upper_fence = q3 + iqr_multiplier * iqr

    lower_outliers = [i for i, size in enumerate(file_sizes) if size < lower_fence]
    upper_outliers = [i for i, size in enumerate(file_sizes) if size > upper_fence]

    return lower_outliers, upper_outliers


def calculate_effective_limit(budget: int, file_count: int, min_limit: int = 0) -> int:
    """Calculate effective per-file limit based on category budget and file count.

    Args:
        budget: Total character budget for the category.
        file_count: Number of files in the category.
        min_limit: Minimum per-file limit (optional floor).

    Returns:
        Effective per-file character limit.
    """
    if file_count <= 0:
        return budget
    effective = budget // file_count
    return max(effective, min_limit) if min_limit > 0 else effective


def validate_category(
    category_name: str,
    total_chars: int,
    budget: int,
    info_threshold_percent: int,
    warn_threshold_percent: int,
) -> CategoryResult:
    """Validate a category's total character count against its budget.

    Args:
        category_name: Name of the category (e.g., "path_instructions").
        total_chars: Sum of all file character counts in this category.
        budget: Maximum allowed characters for this category.
        info_threshold_percent: Percentage of budget for INFO status.
        warn_threshold_percent: Percentage of budget for WARN status.

    Returns:
        CategoryResult with status: ok, info, warning, or error.
    """
    info_threshold = budget * info_threshold_percent // 100
    warn_threshold = budget * warn_threshold_percent // 100

    if total_chars > budget:
        status = "error"
    elif total_chars > warn_threshold:
        status = "warning"
    elif total_chars > info_threshold:
        status = "info"
    else:
        status = "ok"

    return CategoryResult(
        category_name=category_name,
        total_chars=total_chars,
        budget=budget,
        status=status,
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate GitHub Copilot instruction file character limits.",
    )
    parser.add_argument(
        "--compare-to",
        metavar="BRANCH",
        help="Compare changed files against baseline from BRANCH (e.g., origin/main)",
    )
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()

    script_dir = Path(__file__).parent
    config_path = script_dir / "copilot-context-health.conf"
    repo_root = script_dir.parent

    config = load_config(config_path)
    info_pct = int(config.get("INFO_THRESHOLD_PERCENT", 50))
    warn_pct = int(config.get("WARN_THRESHOLD_PERCENT", 75))
    chars_per_token = int(config.get("CHARS_PER_TOKEN", 4))

    # File patterns to check (limits are now determined by LLM_PROVIDERS)
    file_checks = [
        ("Repository Instructions", ".github/copilot-instructions.md"),
        ("Path-Specific Instructions", ".github/instructions/**/*.instructions.md"),
        ("Prompt Files", ".github/prompts/**/*.prompt.md"),
        ("Custom Agents", ".github/agents/**/*.agent.md"),
        ("Multi-Agent Workspace", "AGENTS.md"),
        ("Multi-Agent Workspace", "CLAUDE.md"),
        ("Multi-Agent Workspace", "GEMINI.md"),
        ("Multi-Agent Workspace", "GPT.md"),
        ("Multi-Agent Workspace", "GROK.md"),
    ]

    # Get patterns for baseline comparison
    instruction_patterns = [pattern for _, pattern in file_checks]

    print("Validating GitHub Copilot instruction file token limits...")
    print("Provider limits: 4% of context window (Claude: 8K, Gemini: 42K, GPT: 42K)")
    if args.compare_to:
        print(f"Baseline comparison mode: comparing to {args.compare_to}")
    print("=" * 70)

    errors, warnings, current_section = 0, 0, ""
    section_total_tokens, section_files = 0, 0
    overall_total_tokens, overall_files = 0, 0
    category_totals: dict[str, int] = {}  # Now stores tokens, not chars
    category_files: dict[str, list[tuple[Path, int]]] = {}  # (path, tokens)

    for section, pattern in file_checks:
        files = find_files(repo_root, pattern)

        for file_path in files:
            if section != current_section:
                # Store previous section total for budget validation
                if current_section:
                    prev_total = category_totals.get(current_section, 0)
                    category_totals[current_section] = prev_total + section_total_tokens
                    if section_files > 1:
                        print(f"  --- {section_total_tokens} tokens ({section_files} files)")
                print(f"\n{section}:")
                current_section = section
                section_total_tokens, section_files = 0, 0

            result = validate_file(file_path, chars_per_token, info_pct, warn_pct)
            tok, lim = result.token_count, result.token_limit
            provider_name = LLM_PROVIDERS[result.provider]["display_name"]
            section_total_tokens += tok
            section_files += 1
            overall_total_tokens += tok
            overall_files += 1

            # Track for outlier detection (now using tokens)
            if section not in category_files:
                category_files[section] = []
            category_files[section].append((file_path, tok))

            if result.status == "error":
                print(f"  ERROR: {result.path} exceeds limit")
                print(f"    Tokens: {tok} / {lim} ({tok - lim} over) [{provider_name}]")
                print("    Fix: Split content into multiple files or reduce text")
                errors += 1
            elif result.status == "warning":
                print(f"  WARN: {result.path} approaching limit")
                print(f"    Tokens: {tok} / {lim} ({lim - tok} remaining) [{provider_name}]")
                print("    Action: Review content; consider splitting soon")
                warnings += 1
            elif result.status == "info":
                print(f"  INFO: {result.path} ({tok} / {lim} tokens) [{provider_name}]")
            else:
                print(f"  OK: {result.path} ({tok} / {lim} tokens) [{provider_name}]")

    # Store last section total
    if current_section:
        prev_total = category_totals.get(current_section, 0)
        category_totals[current_section] = prev_total + section_total_tokens
        if section_files > 1:
            print(f"  --- {section_total_tokens} tokens ({section_files} files)")

    # Outlier analysis using IQR method (now using tokens)
    iqr_multiplier = config.get("OUTLIER_IQR_MULTIPLIER", 1.5)
    outlier_found = False

    if args.compare_to:
        # Baseline comparison mode: compute stats from reference branch, validate changed files
        print(f"\nOutlier Analysis (baseline from {args.compare_to}):")
        changed_files = get_changed_files(args.compare_to, repo_root)
        changed_set = {str(p) for p in changed_files}

        # Get baseline file sizes from reference branch
        baseline_data = get_baseline_file_sizes(instruction_patterns, args.compare_to, repo_root)

        # Build mapping: pattern -> baseline stats
        baseline_stats: dict[str, BaselineStats | None] = {}
        for pattern in instruction_patterns:
            sizes = [size for _, size in baseline_data.get(pattern, [])]
            baseline_stats[pattern] = compute_baseline_stats(sizes, iqr_multiplier)

        # Check each changed file against its category's baseline
        for category, files_list in category_files.items():
            # Find matching pattern for this category
            cat_pattern = None
            for section, pattern in file_checks:
                if section == category:
                    cat_pattern = pattern
                    break

            if not cat_pattern:
                continue

            stats = baseline_stats.get(cat_pattern)
            if not stats:
                ref = args.compare_to
                print(f"  {category}: Insufficient baseline data (need 4+ files on {ref})")
                continue

            for path, tokens in files_list:
                if str(path) not in changed_set:
                    continue  # Only check changed files

                q1_val, q3_val = int(stats.q1), int(stats.q3)
                baseline_info = f"Baseline: {stats.file_count} files, Q1={q1_val}, Q3={q3_val}"
                if tokens < stats.lower_fence:
                    outlier_found = True
                    print(f"  OUTLIER: {path.name} ({tokens} tokens)")
                    print(f"    Below lower fence: {stats.lower_fence:.0f} tokens")
                    print(f"    {baseline_info}")
                elif tokens > stats.upper_fence:
                    outlier_found = True
                    print(f"  OUTLIER: {path.name} ({tokens} tokens)")
                    print(f"    Above upper fence: {stats.upper_fence:.0f} tokens")
                    print(f"    {baseline_info}")

        if not outlier_found:
            print("  No outliers in changed files")
    else:
        # Standard mode: compute stats from current branch files
        print(f"\nOutlier Analysis (IQR method, {iqr_multiplier}x multiplier):")
        for category, files_list in category_files.items():
            if len(files_list) < 4:
                continue  # Need at least 4 files for IQR
            token_sizes = [tokens for _, tokens in files_list]
            lower_outliers, upper_outliers = detect_outliers(token_sizes, iqr_multiplier)
            median_tokens = sorted(token_sizes)[len(token_sizes) // 2]
            for idx in lower_outliers:
                outlier_found = True
                path, tokens = files_list[idx]
                diff = tokens - median_tokens
                print(f"  {category}: {path.name} ({tokens} tokens, {diff:+d} vs median) [LOW]")
            for idx in upper_outliers:
                outlier_found = True
                path, tokens = files_list[idx]
                diff = tokens - median_tokens
                print(f"  {category}: {path.name} ({tokens} tokens, {diff:+d} vs median) [HIGH]")
        if not outlier_found:
            print("  No outliers detected")

    print("\n" + "=" * 70)
    print(f"Overall: {overall_total_tokens} tokens across {overall_files} files")
    print(f"Summary: {errors} error(s), {warnings} warning(s)")

    if errors > 0:
        print("Validation failed!")
        return 1

    print("Validation passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
