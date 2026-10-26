from collections import namedtuple
TOOL_NAME = "yotta-vetter"
Rule = namedtuple("Rule", ["id", "detector", "severity", "pattern", "description", "confidence"])
PATTERN_RULES = [
    Rule("x", None, "high", "DownloadRunPayload", "sample", 0.9),
]
