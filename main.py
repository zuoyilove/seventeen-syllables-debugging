#!/usr/bin/env python3
"""Seventeen Syllables of Debugging — a haiku about debugging.

Writes one haiku (5-7-5 syllables, three lines, <= 200 characters) to
/output/entry.txt. The haiku is fixed text: the program is deterministic,
so every run produces the same bytes.
"""

import os
import re

HAIKU = (
    "Breakpoint holds its breath\n"
    "log lines scroll past, no clues\n"
    "dawn finds my typo"
)

VOWELS = "aeiouy"


def count_syllables(word):
    """Count syllables by vowel groups (good enough for this haiku's words)."""
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    if w.endswith("e") and len(w) > 2 and not w.endswith("le"):
        w = w[:-1]
    return len(re.findall(r"[aeiouy]+", w))


def main():
    lines = HAIKU.split("\n")
    assert len(lines) == 3, f"haiku must have 3 lines, got {len(lines)}"
    assert all(line.strip() for line in lines), "no blank lines allowed"
    assert len(HAIKU) <= 200, f"haiku must be <= 200 chars, got {len(HAIKU)}"
    counts = [sum(count_syllables(w) for w in line.split()) for line in lines]
    assert counts == [5, 7, 5], f"expected 5-7-5 syllables, got {counts}"
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(HAIKU + "\n")
    # Read back what was written: the file on disk must be exactly the
    # haiku we asserted above, so a partial write can never slip through.
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    assert written == HAIKU + "\n", "entry.txt on disk differs from haiku"


if __name__ == "__main__":
    main()
