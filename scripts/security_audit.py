#!/usr/bin/env python3
"""Lightweight repository security audit for automation workflows."""

from __future__ import annotations

import re
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "__pycache__"}
SECRET_PATTERNS = {
    "generic api key": re.compile(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
    "github token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    "google client secret": re.compile(r"GOCSPX-[A-Za-z0-9_-]+"),
    "private key": re.compile(r"-----BEGIN (RSA |OPENSSH |EC |)PRIVATE KEY-----"),
}


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    findings: list[str] = []

    for path in iter_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = path.relative_to(root)
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{relative}: possible {label}")

    if findings:
        print("Security audit failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("Security audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
