#!/usr/bin/env python3
"""Static endpoint-triage controls for bytecode, score gates, and setup stages."""
import json
import os
from pathlib import Path
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[2]
TRAITS = Path(os.environ.get("TRAITS_DIR", ROOT))
ENGINE = shlex.split(os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave")))
GATE = "objectives/anti-analysis/sandbox-detect/script::python-sandbox-score-exit"
STAGE = "objectives/supply-chain/install-hook/setup::setup-base64-exec-with-socket-code-stage"
FILES = sorted(path for label in ("notable", "suspicious", "hostile")
               for path in (ROOT / "testdata" / label / "generated/python-improve").rglob("*")
               if path.is_file())
assert len(FILES) >= 6, "Missing focused controls"
for path in FILES:
    proc = subprocess.run([*ENGINE, "--traits-dir", str(TRAITS), "--format", "json", str(path)],
                          check=True, text=True, capture_output=True)
    report = json.loads(proc.stdout)["files"][0]
    traits = report.get("traits", [])
    ids = {trait["id"] for trait in traits}
    if "notable" in path.parts:
        assert not [t["id"] for t in traits if t["crit"] >= 4], (path, traits)
        assert GATE not in ids, path
    elif "suspicious" in path.parts:
        assert GATE in ids, (path, ids)
    else:
        assert STAGE in ids, (path, ids)
print(f"Python improvement regressions: {len(FILES)} static fixtures passed")
