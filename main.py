#!/usr/bin/env python3
"""Worst Monday One-Liners v3 — writes the winning one-liner to entry.txt.

Deterministic, Python stdlib only. No network, no randomness, no I/O
outside the chosen output directory.
"""

import os
import sys

ENTRY = (
    "The Monday update promised 'stability improvements.' "
    "Now I'm stably broken until Friday \u2014 and the patch notes "
    "say 'known issue: Monday.'"
)


def resolve_output_dir():
    """Fallback chain: env vars, then /output, ./output, then cwd."""
    for var in ("OUTPUT_DIR", "_OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        value = os.environ.get(var)
        if value:
            return value
    for candidate in ("/output", "./output"):
        if os.path.isdir(candidate):
            return candidate
    return os.getcwd()


def main():
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    # Gate validation: 1-140 chars, single line, UTF-8.
    if not 1 <= len(ENTRY) <= 140:
        print(f"entry length {len(ENTRY)} out of range 1-140", file=sys.stderr)
        return 1
    if "\n" in ENTRY or "\r" in ENTRY:
        print("entry must be a single line", file=sys.stderr)
        return 1
    data = ENTRY.encode("utf-8")

    # Write WITHOUT a trailing newline: the entry is exactly the line.
    with open(path, "wb") as f:
        f.write(data)

    # Read back and verify byte-exact, then text-exact with no trailing newline.
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        print("verification failed: entry.txt does not match", file=sys.stderr)
        return 1
    if written.endswith(b"\n") or written.endswith(b"\r"):
        print("verification failed: entry.txt has a trailing newline", file=sys.stderr)
        return 1
    if written.decode("utf-8") != ENTRY:
        print("verification failed: decoded text does not match", file=sys.stderr)
        return 1
    print(f"wrote {path} ({len(ENTRY)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
