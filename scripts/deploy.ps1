param(
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

python scripts\validate_content.py
python scripts\security_audit.py

if ($DryRun) {
  Write-Output "Dry run complete. No deploy action was performed."
  exit 0
}

Write-Output "Local checks passed. Push to main to deploy through GitHub Pages."
