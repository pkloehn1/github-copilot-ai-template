<#
.SYNOPSIS
    Runs Super-Linter locally using Docker.
.DESCRIPTION
    This script pulls the Super-Linter image and runs it against the current repository,
    using the configuration defined in .github/super-linter.env.
.EXAMPLE
    .\scripts\local-super-linter.ps1
#>

$ErrorActionPreference = "Stop"

# Get the repository root
$RepoRoot = git rev-parse --show-toplevel
if (-not $RepoRoot) {
    Write-Error "Could not find repository root. Are you in a git repository?"
    exit 1
}

# Path to the env file
$EnvFile = Join-Path $RepoRoot ".github\super-linter.env"
$EnvArgs = @()

# Load configuration
if (Test-Path $EnvFile) {
    Write-Host "Loading configuration from $EnvFile..."
    $Lines = Get-Content $EnvFile
    foreach ($Line in $Lines) {
        $Line = $Line.Trim()
        # Skip comments and empty lines
        if ([string]::IsNullOrWhiteSpace($Line) -or $Line.StartsWith("#")) {
            continue
        }

        # Split into Key=Value
        if ($Line -match "^([^=]+)=(.*)$") {
            $Key = $matches[1]
            $Value = $matches[2]
            $EnvArgs += "-e"
            $EnvArgs += "$Key=$Value"
        }
    }
}

# Run Docker
Write-Host "Running Super-Linter..."
$DockerArgs = @(
    "run", "--rm",
    "-e", "RUN_LOCAL=true",
    "-v", "$($RepoRoot):/tmp/lint"
) + $EnvArgs + @("super-linter/super-linter:v7")

# Print the command for debugging
# Write-Host "docker $DockerArgs"

& docker $DockerArgs
