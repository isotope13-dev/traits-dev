"""Check file-copy placement, application attribution and text cardinality."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
COPY = "micro-behaviors/fs/file/copy::applescript-duplicate-to-location"
REPLACE = "micro-behaviors/fs/file/copy::applescript-duplicate-replacing"
POSIX = "micro-behaviors/fs/file/copy::applescript-duplicate-posix-reference"
FINDER = "micro-behaviors/os/application/target::finder-applescript-target"
COUNT = "metadata/file/profile/string-population::ledger-live-product-at-least-four"
CASES = {
    "finder.applescript": ({COPY, FINDER}, {REPLACE, POSIX}),
    "other-app.applescript": ({COPY, REPLACE}, {FINDER}),
    "target-only.applescript": ({FINDER}, {COPY, REPLACE}),
    "posix-file.applescript": ({COPY, POSIX}, {FINDER}),
    "posix-folder.applescript": ({COPY, POSIX}, {FINDER}),
    "reference.applescript": (set(), {COPY, REPLACE, POSIX, FINDER}),
    "ledger-four.py": ({COUNT}, set()),
    "ledger-three.py": (set(), {COUNT}),
}
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "jsonl", *[str(HERE / name) for name in CASES]],
    check=True, capture_output=True, text=True,
)
seen = set()
checks = 0
for line in result.stdout.split("\n"):
    if not line.strip():
        continue
    for file in json.loads(line)["files"]:
        name = Path(file["path"]).name
        expected, absent = CASES[name]
        traits = {t["id"]: t for t in file["traits"]}
        assert expected <= traits.keys(), (name, expected - traits.keys())
        assert not absent & traits.keys(), (name, absent & traits.keys())
        assert not any(t["crit"] >= 4 for t in traits.values()), name
        assert not any(t.startswith("micro-behaviors/process/create/script/automation::finder-")
                       for t in traits), name
        seen.add(name)
        checks += 4
assert seen == CASES.keys()
print(f"{checks} checks passed across {len(seen)} fixtures")
