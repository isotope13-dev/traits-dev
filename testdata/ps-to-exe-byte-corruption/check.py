"""Scan inert source fixtures; never execute their PowerShell content."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ENGINE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))
HOSTILE = {
    "objectives/impact/destroy/user-data::powershell-recursive-disk-byte-corruption",
    "objectives/impact/wipe/file/header::powershell-recursive-file-prefix-corruption",
    "objectives/impact/deface/wallpaper::powershell-file-corruptor-wallpaper-defacement",
}
TRANSFORM = "micro-behaviors/fs/write/file/transform::powershell-inplace-byte-increment"
results = []
for path in sorted(HERE.glob("*.ps1")):
    proc = subprocess.run(
        [ENGINE, "--traits-dir", str(ROOT), "--format", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    report = json.loads(proc.stdout)
    findings = [t for f in report["files"] for t in f.get("traits", [])]
    ids = {t["id"] for t in findings}
    hostile = {t["id"] for t in findings if t["crit"] == 5}
    if path.stem in {"corruptor", "renamed"}:
        assert HOSTILE <= hostile, (path.name, HOSTILE - hostile)
    else:
        assert not hostile, (path.name, hostile)
    expected_transform = path.stem in {"corruptor", "renamed", "single-file-transform"}
    assert (TRANSFORM in ids) == expected_transform, (path.name, ids)
    results.append({"file": path.name, "hostile": sorted(hostile), "inplace_transform": TRANSFORM in ids})
print(json.dumps(results, indent=2))
