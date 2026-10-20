#!/usr/bin/env python3
"""Exercise native task/exfil rules without executing or committing a specimen.

Usage: python3 run_cases.py SAMPLE --work-dir SCRATCH [--cleave cleave]
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

PARSER = argparse.ArgumentParser(description=__doc__)
PARSER.add_argument("sample", type=Path)
PARSER.add_argument("--work-dir", required=True, type=Path)
PARSER.add_argument("--cleave", default="cleave")
ARGS = PARSER.parse_args()
ROOT = Path(__file__).resolve().parents[3]
DATA = ARGS.sample.read_bytes()
assert hashlib.sha256(DATA).hexdigest() == (
    "39c02cc43c456424cee291e821d9cb73775df4c67a2159e591891cefc15fcf59"
)
EXFIL = "objectives/exfiltration/stealer/file::native-declared-stealer-file-upload"
TASK = "objectives/command-and-control/backdoor/tasking/http::native-stealer-locker-command-interface"
CASES = [
    ("renamed", [], {EXFIL, TASK}),
    ("ordinary-uploader", [(b"X-Stealer-Upload", b"X-Archive-Upload"),
                           (b"!stealer", b"!collect"),
                           (b"!winlocker", b"!displayxx")], set()),
    ("no-theft-header", [(b"X-Stealer-Upload", b"X-Archive-Upload")], set()),
    ("no-lock-task", [(b"!winlocker", b"!displayxx")], {EXFIL}),
    ("no-file-read", [(b"ReadFile\0", b"ReadFyle\0")], {TASK}),
    ("no-command-export", [(b"ExecuteSpecialCommand", b"ExecuteSpecialUtility")], {EXFIL}),
]
ARGS.work_dir.mkdir(parents=True, exist_ok=True)
RESULTS = []
for name, edits, expected in CASES:
    data = DATA
    for old, new in edits:
        assert len(old) == len(new) and old in data
        data = data.replace(old, new)
    path = ARGS.work_dir / (name + ".dll")
    path.write_bytes(data)
    result = subprocess.run(
        [ARGS.cleave, "--traits-dir", str(ROOT), "--format", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    report = json.loads(result.stdout)
    traits = report["files"][0]["traits"]
    observed = {t["id"] for t in traits} & {EXFIL, TASK}
    assert observed == expected, (name, observed, expected)
    if name in ("ordinary-uploader", "no-theft-header"):
        assert not [t for t in traits if t["crit"] == 5], name
    RESULTS.append({"case": name, "matched": sorted(observed)})
    print("PASS", name, flush=True)
(ARGS.work_dir / "results.json").write_text(json.dumps(RESULTS, indent=2) + "\n")
