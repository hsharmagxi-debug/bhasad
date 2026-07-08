#!/usr/bin/env python3
"""Update YouTube video descriptions from a JSON mapping."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

SCOPES = ["https://www.googleapis.com/auth/youtube"]
TOKEN_URI = "https://oauth2.googleapis.com/token"
FOOTER = "\n\n---\nMore from Bhasad: https://bhasad.org"


def load_descriptions(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8") as handle:
        raw = json.load(handle)

    if not isinstance(raw, dict):
        raise ValueError("descriptions file must contain a JSON object")

    descriptions: dict[str, str] = {}
    for video_id, description in raw.items():
        if video_id.startswith("_"):
            continue
        if not isinstance(description, str):
            raise ValueError(f"description for {video_id} must be a string")
        descriptions[video_id] = description.strip()
    return descriptions


def credentials_from_env():
    from google.oauth2.credentials import Credentials

    client_id = os.environ.get("YT_CLIENT_ID")
    client_secret = os.environ.get("YT_CLIENT_SECRET")
    refresh_token = os.environ.get("YT_REFRESH_TOKEN")

    missing = [
        name
        for name, value in {
            "YT_CLIENT_ID": client_id,
            "YT_CLIENT_SECRET": client_secret,
            "YT_REFRESH_TOKEN": refresh_token,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(f"missing required YouTube secret(s): {', '.join(missing)}")

    return Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri=TOKEN_URI,
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES,
    )


def build_description(description: str) -> str:
    cleaned = description.strip()
    if "https://bhasad.org" not in cleaned:
        cleaned = f"{cleaned}{FOOTER}"
    if len(cleaned) > 5000:
        raise ValueError("YouTube descriptions must be 5000 characters or fewer")
    return cleaned


def fetch_video_snippet(youtube: Any, video_id: str) -> dict[str, Any] | None:
    response = youtube.videos().list(part="snippet", id=video_id).execute()
    items = response.get("items", [])
    if not items:
        return None
    return items[0]["snippet"]


def update_video_description(youtube: Any, video_id: str, description: str) -> None:
    snippet = fetch_video_snippet(youtube, video_id)
    if snippet is None:
        raise RuntimeError(f"video not found or inaccessible: {video_id}")

    snippet["description"] = description
    youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": snippet,
        },
    ).execute()


def run(descriptions_path: Path, dry_run: bool) -> int:
    descriptions = load_descriptions(descriptions_path)
    planned = {
        video_id: build_description(description)
        for video_id, description in descriptions.items()
        if description
    }

    skipped = [video_id for video_id, description in descriptions.items() if not description]
    for video_id in skipped:
        print(f"SKIP {video_id}: empty description")

    if not planned:
        print("No non-empty descriptions to update.")
        return 0

    for video_id, description in planned.items():
        print(f"{'DRY-RUN' if dry_run else 'UPDATE'} {video_id}: {len(description)} characters")

    if dry_run:
        return 0

    from googleapiclient.discovery import build

    youtube = build("youtube", "v3", credentials=credentials_from_env())
    for video_id, description in planned.items():
        update_video_description(youtube, video_id, description)
        print(f"UPDATED {video_id}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--descriptions",
        type=Path,
        default=Path("scripts/descriptions.json"),
        help="Path to the video ID to description JSON file.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print planned updates without calling YouTube.")
    args = parser.parse_args()

    try:
        return run(args.descriptions, args.dry_run)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
