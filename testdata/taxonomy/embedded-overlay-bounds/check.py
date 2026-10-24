"""Check reports from: cleave --format jsonl <this-directory>/*.exe"""
from pathlib import Path
import json, sys

TRAIT = "metadata/binary/layout/embedded::overlay-pe-section-beyond-eof"
expected = {"truncated-32.exe": True, "truncated-64.exe": True,
            "complete-32.exe": False, "complete-64.exe": False,
            "no-overlay.exe": False, "bad-signature.exe": False,
            "header-only.exe": False, "mapped-header.exe": False}
seen = set()
for line in Path(sys.argv[1]).read_text().splitlines():
    for file in json.loads(line)["files"]:
        name = Path(file["path"]).name
        if name not in expected:
            continue
        matched = any(t["id"] == TRAIT for t in file.get("traits", []))
        assert matched == expected[name], (name, matched, expected[name])
        seen.add(name)
assert seen == set(expected), ("missing controls", set(expected)-seen)
print(f"Passed {len(seen)} appended-PE boundary controls")
