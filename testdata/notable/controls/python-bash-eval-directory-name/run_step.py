import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run_step(step, repository):
    return subprocess.run(["bash", "-euo", "pipefail", "-c", step["run"]], cwd=repository / "eval",
                          env={**os.environ, "CI": "true"}, capture_output=True, text=True, timeout=60)
