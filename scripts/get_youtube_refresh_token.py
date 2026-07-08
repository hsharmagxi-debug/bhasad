#!/usr/bin/env python3
"""Run a local OAuth flow and print YouTube GitHub secret values."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--credentials",
        type=Path,
        required=True,
        help="Path to the OAuth Desktop app credentials JSON downloaded from Google Cloud.",
    )
    args = parser.parse_args()

    flow = InstalledAppFlow.from_client_secrets_file(str(args.credentials), SCOPES)
    credentials = flow.run_local_server(port=0, prompt="consent")

    raw = json.loads(args.credentials.read_text(encoding="utf-8"))
    client_info = raw.get("installed") or raw.get("web") or {}

    print("Add these as GitHub Actions secrets:")
    print(f"YT_CLIENT_ID={client_info.get('client_id', '')}")
    print(f"YT_CLIENT_SECRET={client_info.get('client_secret', '')}")
    print(f"YT_REFRESH_TOKEN={credentials.refresh_token or ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
