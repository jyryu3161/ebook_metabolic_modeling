#!/usr/bin/env python3
"""Check that every numbered textbook section contains enough visualizations."""

from __future__ import annotations

import argparse
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
HTML_IMAGE = re.compile(r"<img\b", re.IGNORECASE)
MERMAID_FENCE = re.compile(r"^```mermaid\s*$", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--minimum", type=int, default=2)
    parser.add_argument(
        "--chapter",
        type=int,
        action="append",
        help="Validate only this chapter number; repeat for multiple chapters.",
    )
    return parser.parse_args()


def chapter_number(path: Path) -> int:
    return int(path.parent.name.split("-", 1)[1])


def section_number(path: Path) -> int:
    return int(path.stem)


def main() -> int:
    args = parse_args()
    section_files = sorted(
        ROOT.glob("chapter-*/[0-9][0-9].md"),
        key=lambda path: (chapter_number(path), section_number(path)),
    )
    if args.chapter:
        selected = set(args.chapter)
        section_files = [
            path for path in section_files if chapter_number(path) in selected
        ]
    if not section_files:
        raise SystemExit("No numbered section files matched the requested chapters.")
    failures: list[tuple[Path, int]] = []
    total = 0
    for path in section_files:
        text = path.read_text(encoding="utf-8")
        count = (
            len(MARKDOWN_IMAGE.findall(text))
            + len(HTML_IMAGE.findall(text))
            + len(MERMAID_FENCE.findall(text))
        )
        total += count
        if count < args.minimum:
            failures.append((path, count))

    if failures:
        for path, count in failures:
            print(
                f"{path.relative_to(ROOT)}: {count} visualizations; "
                f"minimum is {args.minimum}"
            )
        print(
            f"FAIL: {len(failures)} of {len(section_files)} numbered sections "
            "are below the visualization minimum."
        )
        return 1
    print(
        f"PASS: {len(section_files)} numbered sections contain at least "
        f"{args.minimum} visualizations each ({total} total)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
