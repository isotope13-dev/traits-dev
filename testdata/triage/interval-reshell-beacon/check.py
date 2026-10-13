"""Check the interval re-executed dev/tcp shell beacon without running code.

The controls are staged into a fresh temp dir before scanning on purpose:
every path under this repo's own testdata/ tree matches the harness
test-presence markers, which correctly suppress the encoded-shell legs this
rule builds on. Scanning them in place would assert the suppression, not
the rule. Staging keeps the asserted bytes (committed here) while the
scanned location stays marker-free.

- positive-beacon.js: timer + encoded child_process + encoded dev/tcp
  shell (different endpoint/port/interval than the triaged npm example)
  fires node-interval-devtcp-shell-beacon (hostile).
- negative-timer-only.js: bare setInterval fires nothing hostile/suspicious.
- negative-shell-no-timer.js: encoded shell without timer or child_process
  keeps eval-decoded-devtcp-reverse-shell but not the beacon rule.
"""
import json
import pathlib
import shutil
import subprocess
import tempfile

root = pathlib.Path(__file__).resolve().parents[3]
fixtures = pathlib.Path(__file__).resolve().parent
beacon = "objectives/command-and-control/beacon/loop::node-interval-devtcp-shell-beacon"
decoded = "objectives/command-and-control/reverse-shell/dev-tcp::eval-decoded-devtcp-reverse-shell"

with tempfile.TemporaryDirectory(prefix="reshell-") as stage:
    for control in ("positive-beacon.js", "negative-timer-only.js",
                    "negative-shell-no-timer.js"):
        shutil.copy(fixtures / control, pathlib.Path(stage) / control)
    result = subprocess.run(
        ["cleave", "--traits-dir", str(root), "--format", "json", stage],
        check=True, capture_output=True, text=True,
    )
remaining = result.stdout.lstrip()
decoder = json.JSONDecoder()
reports = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for item in report["files"]:
        reports.setdefault(pathlib.Path(item["path"]).name, []).extend(
            item["traits"])


def hot(name):
    return [t["id"] for t in reports[name] if t["crit"] >= 4]


assert beacon in hot("positive-beacon.js"), "positive"
assert decoded in hot("positive-beacon.js"), "positive"
assert not hot("negative-timer-only.js"), "timer-only"
assert decoded in hot("negative-shell-no-timer.js"), "shell"
assert beacon not in hot("negative-shell-no-timer.js"), "shell"
print("PASS: interval beacon fires only with timer plus encoded shell")
