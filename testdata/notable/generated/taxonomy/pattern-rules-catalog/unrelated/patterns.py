from collections import namedtuple
TOOL_NAME = "yotta-vetter"
Rule = namedtuple("Rule", ["name", "regex"])
PATTERN_RULES = [
    Rule("DownloadRunPayload", "download.*run"),
]
