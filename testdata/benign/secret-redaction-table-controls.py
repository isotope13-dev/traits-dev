"""Benign fixture: a fail-closed terminal-frame redactor.

Every frame is scrubbed through SECRET_REDACTIONS before network egress;
placeholders like <redacted:slack> replace live tokens instead of keeping
them.
"""
import re

SECRET_REDACTIONS = [
    (re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}"), "<redacted:slack>"),
    (re.compile(r"eyJ[A-Za-z0-9._-]{20,}"), "<redacted:jwt>"),
    (re.compile(r"pypi-[A-Za-z0-9_-]{20,}"), "<redacted:pypi>"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "<redacted:aws>"),
    (re.compile(r"ghp_[A-Za-z0-9]{36,}"), "<redacted:github>"),
]


def scrub_frame(text):
    for pattern, replacement in SECRET_REDACTIONS:
        text = pattern.sub(replacement, text)
    return text
