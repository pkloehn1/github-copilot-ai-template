"""Main entry point for context validation."""

import sys
from pathlib import Path

from .config import LLM_PROVIDERS, load_config, parse_args
from .utils import find_files
from .validator import validate_file


def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Determine script directory relative to this file
    # This file is in scripts/context_validator/main.py
    # We want scripts/copilot-context-health.conf
    package_dir = Path(__file__).parent
    scripts_dir = package_dir.parent
    config_path = scripts_dir / "copilot-context-health.conf"
    repo_root = scripts_dir.parent

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

    print("Validating GitHub Copilot instruction file token limits...")
    print("Provider limits: 4% of context window (Claude: 8K, Gemini: 42K, GPT: 42K)")
    if args.compare_to:
        print(f"Baseline comparison mode: comparing to {args.compare_to}")
    print("=" * 70)

    errors, warnings, current_section = 0, 0, ""
    section_total_tokens, section_files = 0, 0
    overall_total_tokens, overall_files = 0, 0
    category_totals: dict[str, int] = {}  # Now stores tokens, not chars

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

            status_icon = "[OK]"
            if result.status == "error":
                status_icon = "[ERR]"
                errors += 1
            elif result.status == "warning":
                status_icon = "[WARN]"
                warnings += 1
            elif result.status == "info":
                status_icon = "[INFO]"

            rel_path = Path(result.path).relative_to(repo_root)
            print(
                f"  {status_icon} {str(rel_path):<50} "
                f"{tok:>5} / {lim:>5} tokens ({result.char_count:>6} chars) "
                f"[{provider_name}]"
            )

    # Print final section total
    if current_section:
        if section_files > 1:
            print(f"  --- {section_total_tokens} tokens ({section_files} files)")

    print("=" * 70)
    print(f"Total: {overall_total_tokens} tokens across {overall_files} files")

    if errors > 0:
        print(f"\nFAILED: Found {errors} files exceeding token limits.")
        return 1
    if warnings > 0:
        print(f"\nWARNING: Found {warnings} files approaching token limits.")
    else:
        print("\nSUCCESS: All files within token limits.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
