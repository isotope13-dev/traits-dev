#!/usr/bin/env python3
"""Static-only regressions for the October Python edge-case review."""
import json
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[2]
TRAITS = Path(os.environ.get("TRAITS_DIR", ROOT))
ENGINE = shlex.split(os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave")))
FILES = sorted(
    path
    for label in ("baseline", "notable", "suspicious", "hostile")
    for path in (ROOT / "testdata" / label / "generated/python-bad-triage").glob("*")
    if path.is_file()
)
def scan(path):
    result = subprocess.run(
        [*ENGINE, "--traits-dir", str(TRAITS), "--format", "json", str(path)],
        check=True, text=True, capture_output=True,
    )
    return path.name, json.loads(result.stdout)["files"][0]


with ThreadPoolExecutor(max_workers=3) as workers:
    REPORTS = dict(workers.map(scan, FILES))
EXPECTED = {
    "sandbox-archive-loader.py": {
        "objectives/command-and-control/dropper/staging/encoded/carrier::python-sandbox-gated-encrypted-archive-launcher",
        "objectives/anti-static/obfuscation/payload/encrypted::python-xor-archive-hidden-launcher",
        "objectives/anti-analysis/sandbox-detect/script::python-sandbox-score-exit",
    },
    "monitor-evasion-socket.py": {
        "objectives/command-and-control/backdoor/shell/socket::python-analysis-evading-socket-shell",
        "objectives/anti-analysis/debugger-detect/combined-checks::python-monitor-blacklist-immediate-exit",
    },
    "discord-channel-keylogger.pyc.xz": {
        "objectives/exfiltration/stealer/multi-item::pyc-discord-buffered-keystroke-exfiltration",
        "objectives/collection/multi-source::pyc-keylog-screen-clipboard-agent",
        "objectives/command-and-control/backdoor/control/discord::pyc-discord-keylogger-shell-agent",
    },
    "ioc-table-with-live-sabotage.py": {
        "objectives/impact/degrade/system/recovery::multi-mechanism-recovery-inhibition",
    },
    "compressed-received-code.py": {
        "objectives/command-and-control/remote-command/dispatch/eval::python-recv-result-code-exec",
    },
    "ip-range-gate.py": {
        "objectives/anti-analysis/geofencing/ip-range::operation-restricted-ip-range-message",
    },
}
assert len(REPORTS) == len(FILES), "A regression fixture was skipped"
for path in FILES:
    report = REPORTS[path.name]
    traits = report.get("traits", [])
    identifiers = {trait["id"] for trait in traits}
    missing = EXPECTED.get(path.name, set()) - identifiers
    assert not missing, f"{path.name}: missing {sorted(missing)}"
    if path.parts[-4] in ("notable", "baseline"):
        unexpected = [trait["id"] for trait in traits if trait["crit"] >= 4]
        assert not unexpected, f"{path.name}: unexpected risk findings {unexpected}"
print(f"Python triage regressions: {len(FILES)} static fixtures passed")
