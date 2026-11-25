"""Synthetic near-miss fixture: the marker literal without any model call.

No API client or chat-completions call is present, so the composite must not
fire. The marker alone is only a notable observation.
"""

PROBE_MARKER = "GODMODE:ENABLED...LOVE PLINY"


def label(name):
    return f"{PROBE_MARKER} {name}"
