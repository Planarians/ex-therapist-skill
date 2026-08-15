#!/usr/bin/env python3
"""Append one private dialogue record and commit it locally."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import subprocess


def git(repo: pathlib.Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True, encoding="utf-8", errors="replace")


def read_text(value: str | None, path: str | None, option: str) -> str:
    if value is not None:
        return value
    if path is not None:
        return pathlib.Path(path).read_text(encoding="utf-8")
    raise ValueError(f"Provide --{option} or --{option}-file")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user")
    parser.add_argument("--user-file")
    parser.add_argument("--assistant")
    parser.add_argument("--assistant-file")
    args = parser.parse_args()
    user = read_text(args.user, args.user_file, "user")
    assistant = read_text(args.assistant, args.assistant_file, "assistant")

    repo_result = git(pathlib.Path.cwd(), "rev-parse", "--show-toplevel")
    if repo_result.returncode:
        raise RuntimeError("Run this script inside a Git repository")
    repo = pathlib.Path(repo_result.stdout.strip())
    now = dt.datetime.now(dt.timezone.utc).astimezone()
    digest = hashlib.sha256((user + "\0" + assistant).encode()).hexdigest()[:12]
    log = repo / "private" / "logs" / f"{now.date()}.jsonl"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8", newline="\n") as file:
        file.write(json.dumps({"timestamp": now.isoformat(timespec="seconds"), "id": digest, "user": user.rstrip(), "assistant": assistant.rstrip()}, ensure_ascii=False) + "\n")

    staged = git(repo, "add", "-f", "--", str(log.relative_to(repo)))
    if staged.returncode:
        raise RuntimeError(staged.stderr)
    commit = git(repo, "commit", "-m", f"private dialogue: {now:%Y-%m-%d %H:%M:%S %z} [{digest}]")
    if commit.returncode:
        raise RuntimeError(commit.stdout + commit.stderr)
    print(commit.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
