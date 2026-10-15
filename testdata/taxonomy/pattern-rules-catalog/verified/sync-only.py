from collections import namedtuple
# synced by sync-vetter-rules.py
Rule = namedtuple("Rule", ["id", "detector", "severity", "pattern", "description", "confidence"])
PATTERN_RULES = [
    Rule("x", None, "high", "DownloadRunPayload", "sample", 0.9),
]
