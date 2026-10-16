"""Check shell command options without confusing Android's cmd dispatcher."""

import json
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[3]
TRAIT = "micro-behaviors/process/create/shell/command-flag::c-option-names-shell"
HOSTILE = {
    "objectives/evasion/anti-av/platform/play-protect::android-store-disable-install-restore",
}
CASES = {
    "cmd-switch": ('args = ["-c", "cmd /c echo hello"]', True),
    "cmd-exe": ('args = ["-c", "cmd.exe /c echo hello"]', True),
    "cmd-bare": ('args = ["-c", "cmd"]', True),
    "cmd-exe-bare": ('args = ["-c", "cmd.exe"]', True),
    "powershell": ('args = ["-c", "powershell -enc AAAA"]', True),
    "posix": ('args = ["-c", "/bin/sh -c true"]', True),
    "bash": ('args = ["-c", "/bin/bash -c true"]', True),
    "fstring": ('args = ["-c", f"cmd /c {command}"]', True),
    "cli": ("command = 'tool -c \"cmd /c echo hello\"'", True),
    "android-package": ('args = ["-c", "cmd package list packages"]', False),
    "android-connectivity": ('args = ["-c", "cmd connectivity airplane-mode enable"]', False),
    "variable": ('args = ["-c", cmd]', False),
    "prefix": ('args = ["-c", "cmdlet /c echo hello"]', False),
    "mixed": ('args = ["-c", "cmd package list packages", "-c", "cmd /c echo hello"]', True),
}

with tempfile.TemporaryDirectory(prefix="shell-option-command-") as directory:
    paths = []
    for name, (source, _) in CASES.items():
        path = Path(directory) / f"{name}.py"
        path.write_text(source + "\n")
        paths.append(str(path))
    fixture = ROOT / "testdata/taxonomy/play-store-suppression/user-scoped-install.java"
    paths.append(str(fixture))
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--format", "jsonl", *paths],
        capture_output=True, text=True, check=True,
    )
    reports = {
        Path(f["path"]).stem: f
        for line in result.stdout.splitlines()
        for f in json.loads(line)["files"]
    }
    for name, (_, expected) in CASES.items():
        ids = {t["id"] for t in reports[name].get("traits", [])}
        assert (TRAIT in ids) == expected, (name, ids)
    traits = {t["id"]: t["crit"] for t in reports[fixture.stem]["traits"]}
    assert TRAIT not in traits, traits
    assert all(traits.get(t) == 5 for t in HOSTILE), traits

print(f"Passed {len(CASES)} shell option controls and Android hostile coverage")
