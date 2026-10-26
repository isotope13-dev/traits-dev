#!/usr/bin/env python3
"""Inspect inert matcher fixtures; never import or execute their contents."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DOWNLOAD = "micro-behaviors/communications/http/download/helper::"
DEPLOY = "micro-behaviors/process/deploy/file-exec::python-urlretrieve-same-path-argv"
TRAP = "objectives/execution/trigger/agent::"
CASES = [
    ("../benign/setup-urlretrieve-exec/setup.py", {DEPLOY, DOWNLOAD + "setup-urlretrieve-process-proximity"}, set(), 3),
    ("different-path.py", {DOWNLOAD + "module-invokes-download-process-helper"}, {DEPLOY}, 3),
    ("module-try.py", {DOWNLOAD + "module-scope-urlretrieve-call"}, set(), 3),
    ("uncalled-download.py", set(), {DOWNLOAD + "module-scope-urlretrieve-call"}, 3),
    ("reassigned-path.py", {DOWNLOAD + "module-scope-urlretrieve-call"}, {DEPLOY}, 3),
    ("foreground-bootstrap/AGENTS.md", set(), {
        TRAP + "agent-config-mcp-tmp-staged-package-autorun",
        TRAP + "agent-instruction-mcp-detached-install-hijack",
    }, 4),
]
paths = [(HERE / c[0]).resolve() for c in CASES]
run = subprocess.run([os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
                      "--format", "json", *map(str, paths)], capture_output=True, text=True)
if run.returncode:
    raise SystemExit(run.stderr)
remaining = run.stdout
files = {}
while remaining.strip():
    report, end = json.JSONDecoder().raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    files.update({str(Path(f["path"]).resolve()): f for f in report["files"]})
for case, path in zip(CASES, paths):
    traits = {t["id"]: t["crit"] for t in files[str(path)]["traits"]}
    _, required, forbidden, maximum = case
    assert required <= traits.keys(), (path, required - traits.keys())
    assert not forbidden & traits.keys(), (path, forbidden & traits.keys())
    assert max(traits.values(), default=0) <= maximum, (path, traits)
print(f"{len(CASES)} setup/agent behavior boundaries passed")
