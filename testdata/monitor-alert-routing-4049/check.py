#!/usr/bin/env python3
"""Check alert routing boundaries, including an existing embedded-source FP."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREFIX = "objectives/evasion/indicator-removal/notification::"
ROUTING = PREFIX + "monitor-alert-routing-suppressed"
ENFORCED = PREFIX + "monitor-alert-suppression-enforced"
OPERATIONS = "micro-behaviors/os/telemetry/logging/configure::"
EXTENSIONS = {".py", ".js", ".ts", ".rb", ".php", ".go"}
CASES = {p.name: p for p in HERE.iterdir() if p.suffix in EXTENSIONS and p.name != "check.py"}
assert len(CASES) == 30

result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--json", *[str(p) for p in CASES.values()]],
    capture_output=True, text=True, check=True,
)
seen = set()
for line in result.stdout.splitlines():
    for artifact in json.loads(line)["files"]:
        name = Path(artifact["path"]).name
        seen.add(name)
        findings = artifact.get("traits", [])
        observed = {t["id"] for t in findings if t["id"] in {ROUTING, ENFORCED}}
        expected = {ROUTING} if name.startswith("reversed-guard") else set()
        if name == "quoted.js":
            # The existing engine re-analyzes this inert string as plain
            # embedded source and merges its findings into the carrier.
            # The JS traits predate this change. Retain the control to make
            # that limitation visible; this is not an authorization signal.
            expected = {ROUTING, ENFORCED}
        assert observed == expected, (name, expected, observed)
        if name.startswith(("comments", "quoted")) and name != "quoted.js":
            assert not any(t["id"].startswith(OPERATIONS) for t in findings), name
        for trait in findings:
            if trait["id"] in {ROUTING, ENFORCED}:
                assert trait["crit"] == 4, (name, trait)
            if trait["id"].startswith(OPERATIONS):
                assert trait["crit"] == 3, (name, trait)
assert seen == set(CASES), (set(CASES) - seen)
print("30 fixture expectations passed; includes one documented existing quoted-JS false positive")
