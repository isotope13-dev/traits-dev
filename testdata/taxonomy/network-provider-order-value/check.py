#!/usr/bin/env python3
"""Check real registry registration/audit scripts and the media-list near miss."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TRAIT = "micro-behaviors/os/registry/keys/execution::network-provider-order-value"
CASES = {
    "ConfigureRegistrySettings.ps1": True,
    "Get-NetworkProviders.ps1": True,
    "registry-value.py": True,
    "registry-value.bat": True,
    "provider-list.js": False,
    "near-value.ps1": False,
}
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "jsonl", *(str(HERE / name) for name in CASES)],
    check=True, capture_output=True, text=True, timeout=180,
)
files = {Path(f["path"]).name: f
         for line in result.stdout.splitlines()
         for f in json.loads(line)["files"]}
for name, expected in CASES.items():
    ids = {trait["id"] for trait in files[name].get("traits", [])}
    assert (TRAIT in ids) == expected, (name, expected, sorted(ids))
    if name == "ConfigureRegistrySettings.ps1":
        # These consumers must still correlate the actual registration surface.
        for suffix in ["network-provider-path-and-value-references",
                       "network-provider-order-value-and-key-references"]:
            assert TRAIT.rsplit("::", 1)[0] + "::" + suffix in ids, suffix
print(f"PASS: {len(CASES)} ProviderOrder cases")
