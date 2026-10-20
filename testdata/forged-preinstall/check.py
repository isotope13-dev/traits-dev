"""Check feed samples and cleave fixture controls without executing specimens.

Usage: python3 check.py SAMPLE_ROOT CLEAVE_FIXTURE_ROOT [CLEAVE]
"""
import json
from pathlib import Path
import subprocess
import sys

samples, controls = map(Path, sys.argv[1:3])
cleave = sys.argv[3] if len(sys.argv) > 3 else "cleave"
tls = "micro-behaviors/process/deploy::unverified-curl-temp-interpreter-cluster"
hidden = "micro-behaviors/process/daemonize/detach::nohup-curl-download-output-suppressed"
temp = "micro-behaviors/process/create/shell/command-string::exec-temp-unix-path"
retired = "objectives/command-and-control/dropper/node-bootstrap::exec-temp-unix-path"


def reports(root):
    result = subprocess.run(
        [cleave, "--traits-dir", str(Path(__file__).resolve().parents[2]),
         "--format", "jsonl", str(root)],
        check=True, capture_output=True, text=True,
    )
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    while remaining:
        report, offset = decoder.raw_decode(remaining)
        remaining = remaining[offset:].lstrip()
        yield from report["files"]


seen = set()
for report in reports(samples):
    name = Path(report["path"]).name
    seen.add(name)
    traits = {item["id"] for item in report.get("traits", [])}
    assert {tls, hidden} <= traits, (name, traits)
    assert retired not in traits, (name, "retired capability still fires")
    if name in {"loader-v1.js", "loader-v2.js"}:
        assert temp in traits, (name, "moved capability lost")
assert len(seen) == 6, seen

expected = {
    "insecure-download-only.sh": set(),
    "verified-background.sh": {hidden},
    "visible-insecure.sh": {tls},
    "daemon-no-fetch.py": set(),
    "logs-visible.sh": {tls},
    "separated-operations.sh": set(),
    "data-path.sh": set(),
    "no-tls-bypass.py": set(),
    "other-command-k.sh": set(),
    "exec-without-temp.js": set(),
    "temp-reference.js": set(),
}
seen_controls = set()
for report in reports(controls):
    name = Path(report["path"]).name
    seen_controls.add(name)
    traits = {item["id"] for item in report.get("traits", [])}
    assert traits & {tls, hidden} == expected[name], (name, traits)
    if name == "exec-without-temp.js":
        assert temp not in traits
    if name == "temp-reference.js":
        assert temp in traits
assert seen_controls == expected.keys(), seen_controls
print(f"Passed: {len(seen)} samples, {len(seen_controls)} controls")
