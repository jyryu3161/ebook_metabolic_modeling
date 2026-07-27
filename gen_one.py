#!/usr/bin/env python3
"""Generate one textbook infographic from a JSON spec with Gemini image models."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
from pathlib import Path
import sys
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
API_ROOT = "https://generativelanguage.googleapis.com/v1beta/models"
DEFAULT_MODELS = (
    "gemini-3-pro-image",
    "nano-banana-pro-preview",
    "gemini-3-pro-image-preview",
    "gemini-2.5-flash-image",
)
REDRAW_INSTRUCTION = """You are given the ORIGINAL textbook figure as a reference image. REDRAW it as a NEW flat vector infographic in the house style described above.
- PRESERVE the same information, overall structure/layout, data values, ordering and meaning, so it is clearly recognizable as the same figure.
- RE-EXPRESS every shape cleanly in the house style; do NOT copy the original's photographic/screenshot look, its colors, and DO NOT reproduce any logo, watermark, or source stamp from the original.
- Replace ALL text with the exact Korean (+English term) labels specified below, correctly spelled, fully legible, no gibberish.
- Keep the same composition/aspect so it reads as a faithful redraw, not a different figure.

=== THIS FIGURE (labels & content) ===
"""


class GenerationError(RuntimeError):
    """Raised when no requested model returns a usable image."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path, help="JSON spec from specs/chN/")
    parser.add_argument(
        "--model",
        action="append",
        dest="models",
        help="Model ID; repeat to override the default fallback order.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing output with the same filename.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and print the request summary without calling the API.",
    )
    return parser.parse_args()


def read_key() -> str:
    for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        value = os.environ.get(name, "").strip()
        if value:
            return value
    key_file = ROOT / "key.txt"
    if key_file.exists():
        value = key_file.read_text(encoding="utf-8").strip()
        if value:
            return value
    raise GenerationError(
        "Gemini API key missing. Set GEMINI_API_KEY or place key.txt in the project root."
    )


def load_spec(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ("name", "out_dir", "aspect", "size", "prompt")
    missing = [key for key in required if not data.get(key)]
    if missing:
        raise GenerationError(f"{path}: missing required fields: {', '.join(missing)}")
    if data["size"] not in {"1K", "2K", "4K"}:
        raise GenerationError(f"{path}: size must be 1K, 2K, or 4K")
    return data


def reference_part(path_value: str) -> dict[str, Any]:
    path = Path(path_value)
    if not path.is_absolute():
        path = ROOT / path
    if not path.is_file():
        raise GenerationError(f"Reference image not found: {path}")
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return {
        "inlineData": {
            "mimeType": mime,
            "data": base64.b64encode(path.read_bytes()).decode("ascii"),
        }
    }


def build_payload(spec: dict[str, Any], model: str) -> dict[str, Any]:
    style = (ROOT / "style_v2.txt").read_text(encoding="utf-8").strip()
    parts: list[dict[str, Any]] = []
    if spec.get("ref_image"):
        parts.append(reference_part(str(spec["ref_image"])))
        prompt = f"{style}\n\n{REDRAW_INSTRUCTION}{spec['prompt']}"
    else:
        prompt = f"{style}\n\n=== THIS FIGURE (labels & content) ===\n{spec['prompt']}"
    parts.append({"text": prompt})

    image_config: dict[str, str] = {"aspectRatio": str(spec["aspect"])}
    if model != "gemini-2.5-flash-image":
        image_config["imageSize"] = str(spec["size"])
    return {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": image_config,
        },
    }


def call_model(
    model: str, key: str, payload: dict[str, Any], attempts: int = 4
) -> dict[str, Any]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(
        f"{API_ROOT}/{model}:generateContent",
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": key,
        },
        method="POST",
    )
    for attempt in range(attempts):
        try:
            with urlopen(request, timeout=300) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if exc.code in {429, 500, 502, 503, 504} and attempt + 1 < attempts:
                time.sleep(2**attempt)
                continue
            raise GenerationError(
                f"{model}: HTTP {exc.code}: {detail[:500]}"
            ) from exc
        except (URLError, TimeoutError) as exc:
            if attempt + 1 < attempts:
                time.sleep(2**attempt)
                continue
            raise GenerationError(f"{model}: network error: {exc}") from exc
    raise GenerationError(f"{model}: exhausted retries")


def extract_image(response: dict[str, Any]) -> tuple[bytes, str]:
    candidates = response.get("candidates") or []
    for candidate in candidates:
        content = candidate.get("content") or {}
        for part in content.get("parts") or []:
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                return (
                    base64.b64decode(inline["data"]),
                    inline.get("mimeType") or inline.get("mime_type") or "image/jpeg",
                )
    feedback = response.get("promptFeedback") or response.get("prompt_feedback")
    raise GenerationError(f"API response contained no image. feedback={feedback!r}")


def output_path(spec: dict[str, Any], mime: str) -> Path:
    suffix = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
    }.get(mime, ".img")
    out_dir = Path(str(spec["out_dir"]))
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    return out_dir / f"{spec['name']}{suffix}"


def append_usage(
    out_dir: Path,
    spec_path: Path,
    model: str,
    response: dict[str, Any],
    image_path: Path,
) -> None:
    record = {
        "spec": str(spec_path),
        "model": model,
        "output": str(image_path.relative_to(ROOT)),
        "usageMetadata": response.get("usageMetadata")
        or response.get("usage_metadata")
        or {},
    }
    with (out_dir / "_usage.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> int:
    args = parse_args()
    spec_path = args.spec if args.spec.is_absolute() else ROOT / args.spec
    spec = load_spec(spec_path)
    models = tuple(args.models or DEFAULT_MODELS)
    if args.dry_run:
        print(
            json.dumps(
                {
                    "spec": str(spec_path.relative_to(ROOT)),
                    "name": spec["name"],
                    "models": models,
                    "aspect": spec["aspect"],
                    "size": spec["size"],
                    "has_reference": bool(spec.get("ref_image")),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    configured_out_dir = Path(str(spec["out_dir"]))
    if not configured_out_dir.is_absolute():
        configured_out_dir = ROOT / configured_out_dir
    existing = [
        path
        for path in configured_out_dir.glob(f"{spec['name']}.*")
        if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".img"}
    ]
    if existing and not args.force:
        names = ", ".join(str(path.relative_to(ROOT)) for path in existing)
        raise GenerationError(
            f"Output already exists: {names}. Use --force to replace it."
        )

    key = read_key()
    failures: list[str] = []
    for model in models:
        try:
            response = call_model(model, key, build_payload(spec, model))
            image, mime = extract_image(response)
            destination = output_path(spec, mime)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if args.force:
                for old_output in existing:
                    if old_output != destination:
                        old_output.unlink()
            destination.write_bytes(image)
            append_usage(destination.parent, spec_path, model, response, destination)
            print(
                json.dumps(
                    {
                        "ok": True,
                        "model": model,
                        "output": str(destination.relative_to(ROOT)),
                        "mimeType": mime,
                    },
                    ensure_ascii=False,
                )
            )
            return 0
        except GenerationError as exc:
            failures.append(str(exc))
    raise GenerationError("All models failed:\n- " + "\n- ".join(failures))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (GenerationError, json.JSONDecodeError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
