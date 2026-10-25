"""Scan inert source fixtures; never execute their PowerShell content."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

from envelope import build

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ENGINE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))
HOSTILE = {
    "objectives/impact/destroy/user-data::powershell-recursive-disk-byte-corruption",
    "objectives/impact/destroy/user-data::powershell-recursive-file-prefix-corruption",
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
with tempfile.TemporaryDirectory(prefix="ps-to-exe-controls-") as directory:
    for seed, base in [(b"new seed", 0x180000000), (b"seed two", 0x240000000)]:
        path = Path(directory) / "ordinary.exe"
        path.write_bytes(build(seed, base))
        proc = subprocess.run(
            [ENGINE, "--traits-dir", str(ROOT), "--format", "json", str(path)],
            capture_output=True, text=True, check=True,
        )
        files = json.loads(proc.stdout)["files"]
        assert any(f["type"] == "powershell" for f in files), "benign resource was not decoded"
        alarms = [t["id"] for f in files for t in f.get("traits", []) if t["crit"] >= 4]
        assert not alarms, alarms
print("Two benign converter envelopes decoded without suspicious or hostile findings.")
