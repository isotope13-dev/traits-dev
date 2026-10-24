"""Static rule controls: never execute any fixture or specimen."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
QUERY = "micro-behaviors/os/security/keychain::chrome-generic-password-query"
PHISH = "objectives/credential-access/keychain/theft::password-phishing-chrome-keychain-query"
OPEN = "micro-behaviors/fs/file/open::node-open-sync"
KEY4 = "micro-behaviors/fs/path/password-store::python-key4-db-reference"
CONSUMER = "objectives/credential-access/theft/multi-store::macos-credential-store-targets"
CASES = {
    "chrome-query.sh": ({QUERY: 3}, [PHISH]),
    "chrome-single-quote.sh": ({QUERY: 3}, [PHISH]),
    "chrome-escaped.applescript": ({QUERY: 3}, [PHISH]),
    "chrome-consumer.sh": ({QUERY: 3, CONSUMER: 4}, [PHISH]),
    "other-service.sh": ({}, [QUERY, PHISH]),
    "phishing-query.applescript": ({QUERY: 3, PHISH: 5}, []),
    "phishing-only.applescript": ({}, [QUERY, PHISH]),
    "key4-reference.py": ({KEY4: 3}, ["micro-behaviors/fs/file/open::key4-db-path"]),
    "open-sync.js": ({OPEN: 3}, ["micro-behaviors/fs/read/file/handle::node-open-sync"]),
    "open-bare.js": ({OPEN: 3}, ["micro-behaviors/fs/read/file/handle::node-open-sync"]),
    "open-alias.js": ({OPEN: 3}, ["micro-behaviors/fs/read/file/handle::node-open-sync"]),
    "open-reference.js": ({}, [OPEN]),
    "open-and-read.js": ({OPEN: 3, "micro-behaviors/fs/read/file/full::read-node": 3}, []),
}
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *(str(HERE / name) for name in CASES)],
    capture_output=True, text=True, check=True,
)
assert not result.stderr.strip(), result.stderr
files = {}
remaining = result.stdout
while remaining.strip():
    report, end = json.JSONDecoder().raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report["files"]:
        files[Path(file["path"]).name] = {t["id"]: t for t in file.get("traits", [])}
checks = 0
for name, (present, absent) in CASES.items():
    actual = files[name]
    for trait, criticality in present.items():
        assert actual.get(trait, {}).get("crit") == criticality, (name, trait, actual)
        checks += 1
    for trait in absent:
        assert trait not in actual, (name, trait)
        checks += 1
# An open, including r+ or a read-only descriptor, does not establish a read.
for name in ("open-sync.js", "open-bare.js", "open-alias.js", "open-reference.js"):
    assert not any(t.startswith("micro-behaviors/fs/read/") for t in files[name]), name
    checks += 1
print(f"{checks} assertions passed across {len(CASES)} controls")
