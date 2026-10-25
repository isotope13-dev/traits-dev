#!/usr/bin/env python3
"""Scan static controls outside testdata; never execute fixture code.

Usage: python3 check.py /absolute/scratch/directory
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

here = Path(__file__).resolve().parent
root = here.parents[2]
scratch = Path(sys.argv[1]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
controls = scratch / "controls"
controls.mkdir(exist_ok=True)
fixtures = {
    name: here / name for name in (
        "decode-print.py", "encoded-descriptor-shell.py",
        "unrelated-registry-write.py", "normal-typelib-registration.py",
        "typelib-setvalueex.py", "keytar-calls.js", "other-password-api.js",
        "source-labels.js", "mirc-reg-file.mrc",
    )
}
fixtures.update({
    "descriptor-shell.py": root / "testdata/hostile/python-descriptor-shell.py",
    "typelib-visible.ps1": root / "testdata/triage/fallout-runtime-review/typelib-visible.ps1",
    "typelib-no-write.ps1": root / "testdata/triage/fallout-runtime-review/typelib-no-write.ps1",
    "typelib-read.py": root / "testdata/triage/python-pipe-com-review/typelib-read.py",
})
for name, source in fixtures.items():
    shutil.copyfile(source, controls / name)
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
     "--format", "jsonl", str(controls)],
    capture_output=True, text=True, check=True,
    env=dict(os.environ, CLEAVE_VALIDATE="0"),
)
(scratch / "controls.jsonl").write_text(result.stdout)
seen = {}
for line in result.stdout.splitlines():
    report = json.loads(line)
    name = Path(report["files"][0]["path"]).name
    seen[name] = {
        trait["id"]: trait["crit"]
        for file in report["files"] for trait in file.get("traits", [])
    }
assert seen.keys() == fixtures.keys(), (seen.keys(), fixtures.keys())
com = "objectives/persistence/system/registry/com-hijack::typelib-scriptlet-hijack"
reverse_shell = "objectives/command-and-control/reverse-shell/fd-redirect::python-socket-fileno-shell"
for name in ("typelib-visible.ps1", "typelib-setvalueex.py"):
    assert seen[name].get(com) == 5, name
for name in ("descriptor-shell.py", "encoded-descriptor-shell.py"):
    assert seen[name].get(reverse_shell) == 5, name
for name in (
    "decode-print.py", "normal-typelib-registration.py",
    "unrelated-registry-write.py", "typelib-no-write.ps1", "typelib-read.py",
    "other-password-api.js", "source-labels.js", "mirc-reg-file.mrc",
):
    assert not any(crit >= 4 for crit in seen[name].values()), name
for operation in ("get", "replace", "delete"):
    trait = f"micro-behaviors/os/security/credential-manager::keytar-{operation}-password"
    assert seen["keytar-calls.js"].get(trait) == 3, trait
    assert trait not in seen["other-password-api.js"], trait
for suffix in ("registry-file-header", "executable-registry-value"):
    trait = f"micro-behaviors/fs/write/content::mirc-stages-{suffix}"
    assert seen["mirc-reg-file.mrc"].get(trait) == 3, trait
print(f"Passed {len(fixtures)} static controls: retained attacks and benign near misses")
