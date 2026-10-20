#!/usr/bin/env python3
"""Check neutral placement, near misses, and component emission context."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
NAMES = [
    "metadata/package/documentation/claims::markdown-repeated-casino-terms",
    "micro-behaviors/communications/http/token-auth::access-token-camel-field",
    "metadata/file/profile/string-population::random-like-alphanumeric-literal-present",
]
RETIRED = {
    "objectives/anti-static/obfuscation/eval/require::blob-loader-basename",
    "objectives/supply-chain/hidden-payload/spam::readme-repeated-gambling-copy",
    "micro-behaviors/communications/http/device-code::access-token-camel-field",
    "micro-behaviors/os/env/gate::source-random-activation-literal",
}
CASES = {
    "Blob.js": set(),
    "other.js": set(),
    "token.js": {NAMES[1]},
    "ordinary-field.js": set(),
    "checksum.js": set(),
    "literal-boundaries.js": set(),
    "literal-and-env.js": {NAMES[2]},
    "sponsors.md": {NAMES[0]},
    "two-mentions.md": set(),
}
paths = [str(HERE / "fixtures" / name) for name in CASES]
p = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", "--min-crit", "component", *paths],
    text=True, capture_output=True,
)
assert p.returncode == 0, p.stderr
assert not p.stderr.strip(), p.stderr
decoder = json.JSONDecoder()
files = []
remaining = p.stdout.lstrip()
while remaining:
    report, end = decoder.raw_decode(remaining)
    files.extend(report["files"])
    remaining = remaining[end:].lstrip()
seen = set()
for f in files:
    name = Path(f["path"]).name
    if name not in CASES:
        continue
    seen.add(name)
    traits = {t["id"]: t for t in f.get("traits", [])}
    assert not RETIRED.intersection(traits), (name, RETIRED.intersection(traits))
    got = set(NAMES).intersection(traits)
    assert got == CASES[name], (name, got, CASES[name])
    assert not any(t["crit"] >= 5 for t in traits.values()), (name, "hostile")
    for key in got:
        assert traits[key]["crit"] == (1 if key == NAMES[2] else 3), (name, key)
assert seen == set(CASES), seen
print(f"Passed {len(CASES)} placement and near-miss controls.")
