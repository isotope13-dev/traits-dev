#!/usr/bin/env python3
"""Generate a harmless pickle containing a small dict."""

from __future__ import annotations

import pickle
import sys
from pathlib import Path


def main(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {"message": "this sample does nothing", "version": 1}
    with target.open("wb") as f:
        pickle.dump(payload, f, protocol=4)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
