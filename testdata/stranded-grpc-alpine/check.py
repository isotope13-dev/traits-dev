#!/usr/bin/env python3
"""Check an atomscan JSON stream: python3 check.py saved-report.json."""
import json
import pathlib
import sys
root = pathlib.Path(__file__).resolve().parent
expected = json.loads((root / "cases.json").read_text())
text = pathlib.Path(sys.argv[1]).read_text()
decoder = json.JSONDecoder()
files = {}
while text.strip():
    report, end = decoder.raw_decode(text.lstrip())
    text = text.lstrip()[end:]
    for file in report["raw"]["files"]:
        files[pathlib.Path(file["path"]).name] = {
            item["id"] for item in file.get("traits", [])
        }
for name, case in expected.items():
    assert name in files, f"missing scan: {name}"
    for trait in case.get("present", []):
        assert trait in files[name], f"{name}: missing {trait}"
    for trait in case.get("absent", []):
        assert trait not in files[name], f"{name}: unexpected {trait}"
print(f"{len(expected)} controls passed")
