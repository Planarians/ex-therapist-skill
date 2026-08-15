#!/usr/bin/env python3
"""Write an explicitly private, evidence-limited mirror calibration note."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", required=True, help="The correction or observed pattern")
    parser.add_argument("--context", required=True, help="Why this correction was supplied")
    parser.add_argument("--confidence", choices=("tentative", "supported", "stable"), default="tentative")
    parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path("private/corrections.jsonl"))
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "recorded_at": dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds"),
        "text": args.text,
        "context": args.context,
        "confidence": args.confidence,
        "rule": "Private calibration only; do not treat as a claim about a real person's current inner state.",
    }
    with args.output.open("a", encoding="utf-8", newline="\n") as destination:
        destination.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
