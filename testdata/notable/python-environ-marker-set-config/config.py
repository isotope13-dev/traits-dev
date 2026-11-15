import os

PREFIXES = ("APP_", "CONFIG_")
settings = {}
for name, value in os.environ.items():
    if any(prefix in name.upper() for prefix in PREFIXES):
        settings[name] = value
