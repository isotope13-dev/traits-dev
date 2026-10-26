# PATTERN_RULES = [
from collections import namedtuple
Rule = namedtuple("Rule", ["id", "detector", "severity", "pattern", "description", "confidence"])
DownloadRunPayload = "download"
