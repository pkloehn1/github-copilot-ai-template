#!/usr/bin/env python3
"""
Cross-platform wrapper to run the local Super-Linter script from pre-commit.
"""
import os
import platform
import subprocess
import sys


def main():
    """Run the appropriate Super-Linter script based on the OS."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if platform.system() == "Windows":
        script_path = os.path.join(repo_root, "scripts", "local-super-linter.ps1")
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path]
    else:
        script_path = os.path.join(repo_root, "scripts", "local-super-linter.sh")
        cmd = ["bash", script_path]

    print(f"Running Super-Linter via {cmd[0]}...")

    try:
        # We ignore the arguments passed by pre-commit (filenames) because
        # the super-linter script runs on the repository context.
        # If we wanted to support file filtering, we'd need to modify the scripts
        # to accept file paths and pass them to super-linter (which is complex).
        result = subprocess.run(cmd, check=False)
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running Super-Linter: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
