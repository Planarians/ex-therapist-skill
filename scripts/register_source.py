#!/usr/bin/env python3
"""Register authorized private source metadata without copying its contents."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib


KINDS = {"transcript", "note", "export", "public-writing", "image", "pdf"}


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=pathlib.Path)
    parser.add_argument("--kind", required=True, choices=sorted(KINDS))
    parser.add_argument("--rights", required=True, help="Your brief authority-to-process statement")
    parser.add_argument("--purpose", default="private reflection and style calibration")
    parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path("private/sources.jsonl"))
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "registered_at": dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds"),
        "filename": source.name,
        "extension": source.suffix.lower(),
        "kind": args.kind,
        "bytes": source.stat().st_size,
        "sha256": sha256(source),
        "rights": args.rights,
        "purpose": args.purpose,
        "contents_copied": False,
    }
    with args.output.open("a", encoding="utf-8", newline="\n") as destination:
        destination.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
