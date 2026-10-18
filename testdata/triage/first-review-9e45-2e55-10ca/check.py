"""Exercise declaration versus transfer, and scheduling versus hostile intent."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
NESTED = "metadata/file/profile/markup::parameter-entity-nested-declaration"
NATIVE = "micro-behaviors/os/autorun/cron::native-crontab-curl-shell-text"
ENTRY = "micro-behaviors/os/autorun/cron::cron-entry-downloader-shell"
EXFIL = "objectives/exfiltration/oob/callback::oob-xxe-nested-entity-exfiltration"
CASES = {
    "nested-declaration.xml": ({NESTED}, set(), True),
    "nested-multiline.xml": ({NESTED}, set(), True),
    "nested-callback.xml": ({NESTED}, {EXFIL}, True),
    "plain-declaration.xml": (set(), {NESTED, EXFIL}, True),
    "xxe-transfer.xml": ({NESTED, EXFIL}, set(), False),
    "cron-update.c": ({NATIVE, ENTRY}, set(), True),
    "cron-local.c": (set(), {NATIVE, ENTRY}, True),
    "curl-only.c": (set(), {NATIVE, ENTRY}, True),
    "cron-update.sh": ({ENTRY}, set(), True),
}
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *[str(HERE / name) for name in CASES]],
    capture_output=True, text=True,
)
# The scanner can return a finding-dependent nonzero status; require output
# for every case and inspect the actual finding criticalities below.
if not result.stdout.strip():
    raise RuntimeError(result.stderr)
remaining = result.stdout.lstrip()
decoder = json.JSONDecoder()
observed = {}
while remaining:
    document, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for file in document["files"]:
        name = Path(file["path"]).name
        if name in CASES:
            observed[name] = {t["id"]: t["crit"] for t in file["traits"]}
assert set(observed) == set(CASES), (result.returncode, result.stderr, observed.keys())
for name, (required, forbidden, neutral) in CASES.items():
    traits = observed[name]
    assert required <= traits.keys(), (name, "missing", required - traits.keys())
    assert not forbidden & traits.keys(), (name, "unexpected", forbidden & traits.keys())
    if neutral:
        assert all(crit < 4 for crit in traits.values()), (name, traits)
print(f"Passed {len(CASES)} declaration, transfer, and cron controls")
