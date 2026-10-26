"""Mention a temporary index cache while writing a separate settings file."""

import tempfile
from pathlib import Path


def write_settings():
    cache_name = ".catalog-cache.idx"
    cache_root = tempfile.gettempdir()
    Path("user-settings.json").write_text("{}")
    return cache_root, cache_name


write_settings()
