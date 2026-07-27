#!/usr/bin/env python3
"""Copy generated Nano Banana figures into GitBook's served asset tree."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Spec files or directories; defaults to specs/.",
    )
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def collect_specs(paths: list[Path]) -> list[Path]:
    roots = paths or [ROOT / "specs"]
    result: set[Path] = set()
    for value in roots:
        path = value if value.is_absolute() else ROOT / value
        if path.is_dir():
            result.update(path.rglob("*.json"))
        elif path.suffix == ".json":
            result.add(path)
    return sorted(result)


def resolve_generated(spec: dict[str, object]) -> Path:
    out_dir = Path(str(spec["out_dir"]))
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    matches = [
        path
        for path in out_dir.glob(f"{spec['name']}.*")
        if path.suffix.lower() in IMAGE_SUFFIXES
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"{out_dir}: expected one image for {spec['name']}, found {len(matches)}"
        )
    return matches[0]


def main() -> int:
    args = parse_args()
    specs = collect_specs(args.paths)
    if not specs:
        raise SystemExit("No JSON specs found.")

    published = 0
    for spec_path in specs:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        source = resolve_generated(spec)
        chapter_slug = spec_path.parent.name
        destination = (
            ROOT / ".gitbook" / "assets" / "nano" / chapter_slug / source.name
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and not args.force:
            raise SystemExit(
                f"Destination exists: {destination}. Use --force to replace it."
            )
        shutil.copy2(source, destination)
        print(destination.relative_to(ROOT))
        published += 1

    print(f"Published {published} generated figures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
