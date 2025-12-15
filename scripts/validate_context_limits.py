#!/usr/bin/env python3
"""Validate GitHub Copilot instruction file token limits.

Wrapper script for the context_validator package.
"""

import sys
from pathlib import Path

# Add the scripts directory to sys.path so we can import the package
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from context_validator.main import main

if __name__ == "__main__":
    sys.exit(main())
