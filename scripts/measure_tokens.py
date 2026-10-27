#!/usr/bin/env python3
"""Estimate context tokens with the project's documented conservative heuristic."""

from __future__ import annotations

import argparse
import math
from pathlib import Path


def estimate_tokens(text: str) -> int:
    """Count non-ASCII characters as one token and ASCII characters as 1/4 token."""
    ascii_chars = sum(ord(char) < 128 for char in text)
    non_ascii_chars = len(text) - ascii_chars
    return math.ceil(ascii_chars / 4 + non_ascii_chars)


def collect_files(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_dir():
            files.extend(sorted(p for p in path.rglob("*.md") if p.is_file()))
        elif path.is_file():
            files.append(path)
        else:
            raise FileNotFoundError(f"Path does not exist: {path}")
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Files or directories; directories load Markdown recursively")
    args = parser.parse_args()

    total = 0
    for path in collect_files(args.paths):
        tokens = estimate_tokens(path.read_text(encoding="utf-8"))
        total += tokens
        print(f"{tokens:>8}  {path}")
    print(f"{total:>8}  TOTAL")


if __name__ == "__main__":
    main()
