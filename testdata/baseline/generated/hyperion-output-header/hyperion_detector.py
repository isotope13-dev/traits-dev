"""Recognize Python sources that still carry an obfuscator banner.

Hyperion prepends a fixed dunder header to everything it emits. Packers that
strip it leave no banner, so a miss here says nothing about the body.
"""
import re

HYPERION_HEADER = re.compile(r"__obfuscator__ = 'Hyperion'")
HYPERION_AUTHORS = "__authors__ = ('billythegoat356', 'BlueRed')"


def is_hyperion(source: str) -> bool:
    """Report whether the Hyperion header survives in source."""
    return bool(HYPERION_HEADER.search(source)) or HYPERION_AUTHORS in source


def banner_lines(source: str) -> list[str]:
    """Return the header lines that identify Hyperion output."""
    return [line for line in source.splitlines() if is_hyperion(line)]
