#!/usr/bin/env bash
set -euo pipefail

DESCRIPTIONS="scripts/descriptions.json"
DRY_RUN=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --descriptions)
      DESCRIPTIONS="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --credentials)
      echo "--credentials is accepted for compatibility, but this stack uses YT_CLIENT_ID, YT_CLIENT_SECRET, and YT_REFRESH_TOKEN."
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

ARGS=(--descriptions "$DESCRIPTIONS")
if [[ "$DRY_RUN" == "true" ]]; then
  ARGS+=(--dry-run)
fi

python scripts/update_yt_desc.py "${ARGS[@]}"
