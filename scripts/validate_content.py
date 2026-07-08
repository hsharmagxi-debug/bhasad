#!/usr/bin/env python3
"""Validate public content before deploy."""

from __future__ import annotations

import sys
from pathlib import Path

PUBLIC_EXTENSIONS = {".html", ".css", ".js", ".md", ".json"}
SKIP_DIRS = {".git", ".venv", "__pycache__"}
DEVANAGARI_START = 0x0900
DEVANAGARI_END = 0x097F


def iter_public_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in PUBLIC_EXTENSIONS:
            yield path


def has_devanagari(text: str) -> bool:
    return any(DEVANAGARI_START <= ord(char) <= DEVANAGARI_END for char in text)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    failures: list[str] = []

    for path in iter_public_files(root):
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root)
        if has_devanagari(text):
            failures.append(f"{relative}: contains Devanagari text")

    index_path = root / "index.html"
    if index_path.exists() and "https://bhasad.org" not in index_path.read_text(encoding="utf-8"):
        failures.append("index.html: missing https://bhasad.org link")

    if failures:
        print("Content validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Content validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
