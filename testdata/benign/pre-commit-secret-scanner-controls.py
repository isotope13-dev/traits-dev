#!/usr/bin/env python3
"""Benign fixture: a pre-commit secret scanner.

Scans staged files for provider token formats and blocks the commit on a
hit. Install with: cp scanner.py .git/hooks/pre-commit
"""
import re
import subprocess
import sys

SECRET_PATTERNS = [
    ("GitHub PAT (ghp_)", re.compile(r"\bghp_[A-Za-z0-9]{36,}\b")),
    ("GitHub fine-grained PAT (github_pat_)", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b")),
    ("GitLab PAT (glpat-)", re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b")),
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("PyPI token (pypi-)", re.compile(r"\bpypi-[A-Za-z0-9_-]{20,}\b")),
]


def staged_files():
    out = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        text=True,
    )
    return [line.strip() for line in out.splitlines() if line.strip()]


def main():
    hits = 0
    for path in staged_files():
        with open(path, errors="replace") as fh:
            for lineno, line in enumerate(fh, start=1):
                for name, pattern in SECRET_PATTERNS:
                    if pattern.search(line):
                        print("%s:%d: %s" % (path, lineno, name))
                        hits += 1
    if hits:
        print("blocking the commit: %d secret(s) found" % hits)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
