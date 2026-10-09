"""Run distinguishing controls without test-path suppressors."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

fixtures = Path(__file__).resolve().parent
repo = fixtures.parent.parent
scratch = Path(os.environ.get("TRIAGE_SCRATCH", "/usr/local/var/cyclotron/tmp.noindex/cyclotron-09e7a68e/scratch"))
checks = {
    ".claude/settings.json": ("objectives/execution/trigger/agent::agent-sessionstart-project-config-script", True),
    "saved-hooks.json": ("objectives/execution/trigger/agent::agent-sessionstart-project-config-script", False),
    "active-device.sh": ("objectives/impact/wipe/disk/device::dd-zero", True),
    "blocked-device.txt": ("objectives/impact/wipe/disk/device::dd-zero", False),
    "mixed-device.sh": ("objectives/impact/wipe/disk/device::dd-zero", True),
    "env-helper.py": ("micro-behaviors/os/env/enumerate::python-env-command-reference", True),
    "env-init.py": ("micro-behaviors/os/env/enumerate::python-env-command-reference", True),
    "env-mention.py": ("micro-behaviors/os/env/enumerate::python-env-command-reference", False),
    "token-code-literal.js": ("micro-behaviors/os/env/vcs::node-gh-token-code-literal", True),
}
with tempfile.TemporaryDirectory(prefix="drift-controls-", dir=scratch) as td:
    root = Path(td)
    for name in checks:
        dest = root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(fixtures / name, dest)
    result = subprocess.run([os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(repo), "--format", "json", str(root)], check=True, capture_output=True, text=True)
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    files = []
    while remaining:
        doc, end = decoder.raw_decode(remaining)
        files.extend(doc["files"])
        remaining = remaining[end:].lstrip()
    reports = {str(Path(f["path"]).relative_to(root)): f for f in files if "##" not in f["path"]}
    for name, (trait, expected) in checks.items():
        report = reports[name]
        matches = {t["id"]: t for t in report.get("traits", [])}
        assert (trait in matches) == expected, (name, trait, matches.keys())
        if trait.startswith("micro-behaviors/") and expected:
            assert matches[trait]["crit"] == 3, (name, matches[trait])
        if name == "token-code-literal.js":
            assert not any(t["crit"] >= 4 for t in matches.values()), matches
    print(f"Passed {len(checks)} controls")
