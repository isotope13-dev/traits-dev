"""Check the NBNS spoof loop without the reflection half.

The triaged relay skeleton poisons name resolution (NBNS answer bytes,
transaction-ID walk, paired brute-force loops, socket send) without the
local SMB reflection half, so it must read suspicious, never hostile.
Controls are synthetic variants, not sample bytes.

- positive-spoof-loop.ps1: same technique with renamed loop variables
  and a while-loop shape fires nbns-poisoning-loop (suspicious) while
  nbns-poisoning-for-ntlm-reflection stays absent.
- negative-probe-loop.ps1: paired loops and a send over a generic probe
  packet (no NBNS bytes, no transaction-ID assignments) fires neither.
"""
import json
import pathlib
import shutil
import subprocess
import tempfile

root = pathlib.Path(__file__).resolve().parents[3]
fixtures = pathlib.Path(__file__).resolve().parent
# Staged into a fresh temp dir before scanning: any path under this repo's
# own testdata/ tree matches the harness test-presence markers, which
# correctly suppress this rule's legs. The committed bytes are the test;
# the temp location is just scaffolding.
with tempfile.TemporaryDirectory(prefix="nbns-") as stage:
    for control in ("positive-spoof-loop.ps1", "negative-probe-loop.ps1"):
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
        reports[pathlib.Path(item["path"]).name] = item["traits"]

loop = "objectives/credential-access/capture/network::nbns-poisoning-loop"
reflection = "objectives/credential-access/capture/network::nbns-poisoning-for-ntlm-reflection"


def has(name, rule_id):
    return rule_id in {t["id"] for t in reports[name]}


def hot(name):
    return [t["id"] for t in reports[name] if t["crit"] >= 4]


assert has("positive-spoof-loop.ps1", loop), "positive"
assert not has("positive-spoof-loop.ps1", reflection), "boundary"
assert not has("negative-probe-loop.ps1", loop), "negative"
assert not has("negative-probe-loop.ps1", reflection), "negative"
print("PASS: spoof loop is suspicious without the reflection half")
