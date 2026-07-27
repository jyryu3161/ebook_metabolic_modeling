#!/usr/bin/env python3
"""Generate every chapter infographic spec sequentially and summarize failures."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Spec files or directories; defaults to specs/.",
    )
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
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


def main() -> int:
    args = parse_args()
    specs = collect_specs(args.paths)
    if not specs:
        print("No JSON specs found.", file=sys.stderr)
        return 1

    failures: list[Path] = []
    for index, spec in enumerate(specs, 1):
        print(f"[{index}/{len(specs)}] {spec.relative_to(ROOT)}", flush=True)
        command = [sys.executable, str(ROOT / "gen_one.py"), str(spec)]
        if args.force:
            command.append("--force")
        if args.dry_run:
            command.append("--dry-run")
        completed = subprocess.run(command, cwd=ROOT, check=False)
        if completed.returncode:
            failures.append(spec)

    if failures:
        print("Failed specs:", file=sys.stderr)
        for spec in failures:
            print(f"- {spec.relative_to(ROOT)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
