#!/bin/bash

# Run Super-Linter locally using Docker
# Usage: ./scripts/local-super-linter.sh

# Get the absolute path to the repository root
REPO_ROOT=$(git rev-parse --show-toplevel)

# Load configuration from .github/super-linter.env
ENV_FILE="$REPO_ROOT/.github/super-linter.env"
ENV_ARGS=""

if [ -f "$ENV_FILE" ]; then
    echo "Loading configuration from $ENV_FILE..."
    # Read the file, ignore comments and empty lines, and format as -e VAR=VAL
    while IFS='=' read -r key value; do
        if [[ $key =~ ^[^#]*$ ]] && [[ -n $key ]]; then
            ENV_ARGS="$ENV_ARGS -e $key=$value"
        fi
    done < "$ENV_FILE"
fi

# Run Super-Linter
echo "Running Super-Linter..."
docker run --rm \
    -e RUN_LOCAL=true \
    -v "$REPO_ROOT:/tmp/lint" \
    $ENV_ARGS \
    super-linter/super-linter:v7
