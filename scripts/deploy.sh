#!/usr/bin/env bash
set -euo pipefail

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
fi

python scripts/validate_content.py
python scripts/security_audit.py

if [[ "$DRY_RUN" == "true" ]]; then
  echo "Dry run complete. No deploy action was performed."
  exit 0
fi

echo "Local checks passed. Push to main to deploy through GitHub Pages."
