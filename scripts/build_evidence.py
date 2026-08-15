#!/usr/bin/env python3
"""Create a local, reviewable evidence report from authorized text sources."""

from __future__ import annotations

import argparse
import json
import pathlib
import re


AI_HEADING = re.compile(r"^#{1,3}\s*(?:ai|gpt\d*|gemini|claude|summary|总结|分析)", re.IGNORECASE)


def remove_ai_sections(text: str) -> str:
    kept: list[str] = []
    for line in text.splitlines():
        if AI_HEADING.match(line.strip()):
            break
        kept.append(line)
    return "\n".join(kept)


def inspect(path: pathlib.Path, max_questions: int) -> dict[str, object]:
    text = remove_ai_sections(path.read_text(encoding="utf-8-sig", errors="replace"))
    blocks = [re.sub(r"\s+", " ", item).strip() for item in re.split(r"\n\s*\n", text)]
    blocks = [item for item in blocks if item]
    return {
        "file": path.name,
        "characters": len(text),
        "blocks": len(blocks),
        "question_candidates": [item for item in blocks if "?" in item or "？" in item][:max_questions],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path("private/evidence.json"))
    parser.add_argument("--max-questions", type=int, default=100)
    args = parser.parse_args()

    report = {"sources": [inspect(path, args.max_questions) for path in args.source]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
