import os
from pathlib import Path
FIXTURE_VERSION=Path(__file__).with_name("VERSION").read_text() if Path(__file__).with_name("VERSION").exists() else "unknown"
print(FIXTURE_VERSION)
