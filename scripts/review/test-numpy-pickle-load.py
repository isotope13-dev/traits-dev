#!/usr/bin/env python3
"""Check explicit NumPy pickle loading and its basic boundaries."""

import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))
RULE = "micro-behaviors/data/serialize/unsafe::numpy-load-with-pickle-enabled"

with tempfile.TemporaryDirectory() as temp:
    for name, source, expected in (
        ("enabled", "import numpy as np\nnp.load(path, allow_pickle=True)\n", True),
        ("disabled", "import numpy as np\nnp.load(path, allow_pickle=False)\n", False),
        ("other_receiver", "import numpy as np\nother.load(path, allow_pickle=True)\n", False),
        ("no_import", "np.load(path, allow_pickle=True)\n", False),
    ):
        path = Path(temp) / f"{name}.py"
        path.write_text(source)
        result = subprocess.run(
            [CLEAVE, "--traits-dir", str(ROOT), "--all-files", "--format=json", str(path)],
            check=True, capture_output=True, text=True,
            env={**os.environ, "CLEAVE_SKIP_CACHE": "1"},
        )
        report = json.loads(result.stdout)
        found = any(t["id"] == RULE for f in report["files"] for t in f.get("traits", []))
        assert found == expected, (name, found)

print("NumPy pickle load boundaries passed")
