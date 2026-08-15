#!/usr/bin/env python3
"""Register private longitudinal context paths without copying their contents."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib


ROLES = ("issues", "history", "formulation", "parts", "prompt")


def digest(path: pathlib.Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def describe(path: pathlib.Path) -> dict[str, object]:
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise FileNotFoundError(resolved)
    stat = resolved.stat()
    return {
        "path": str(resolved),
        "filename": resolved.name,
        "bytes": stat.st_size,
        "modified_at": dt.datetime.fromtimestamp(stat.st_mtime).astimezone().isoformat(timespec="seconds"),
        "sha256": digest(resolved),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for role in ROLES:
        parser.add_argument(f"--{role}", type=pathlib.Path)
    parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path("private/client-context.json"))
    args = parser.parse_args()

    supplied = {role: getattr(args, role) for role in ROLES if getattr(args, role) is not None}
    if not supplied:
        parser.error("Provide at least one context source")
    result = {
        "registered_at": dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds"),
        "privacy": "Local path index only. Never stage, commit, or upload this file.",
        "sources": {role: describe(path) for role, path in supplied.items()},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
