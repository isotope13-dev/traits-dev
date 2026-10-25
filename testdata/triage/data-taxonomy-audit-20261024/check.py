#!/usr/bin/env python3
"""Run inert taxonomy controls and a real operation contrast.

Usage: CLEAVE=/path/to/cleave python3 testdata/triage/data-taxonomy-audit-20261024/check.py
"""
import json
import os
from pathlib import Path
import subprocess

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
CLEAVE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))


def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        doc, consumed = decoder.raw_decode(text)
        yield doc
        text = text[consumed:]


def main():
    expected = json.loads((BASE / "control-expectations.json").read_text())
    completed = subprocess.run(
        [CLEAVE, "--traits-dir", str(ROOT), "--format", "json", "analyze", str(BASE / "controls")],
        check=True, capture_output=True, text=True,
    )
    observed = list(documents(completed.stdout))
    files = {Path(f["path"]).name: f for d in observed for f in d.get("files", [])}
    mappings = json.loads((BASE / "migration.json").read_text())["mappings"]
    removed = {m["old"] for m in mappings if m["old"] != m["new"]}
    checks = 0
    for case in expected["cases"]:
        result = files[case["file"]]
        ids = {t["id"] for t in result.get("traits", [])}
        assert not ids & removed, (case["file"], "old IDs", ids & removed)
        for required in case.get("required", []):
            assert required in ids, (case["file"], "missing", required)
            checks += 1
        for prefix in case.get("required_prefixes", []):
            assert any(i.startswith(prefix) for i in ids), (case["file"], "missing prefix", prefix)
            checks += 1
        for prefix in case.get("forbidden_prefixes", []):
            assert not any(i.startswith(prefix) for i in ids), (case["file"], "unsupported claim", prefix)
            checks += 1
    (BASE / "post-observations.json").write_text(json.dumps(observed, indent=2) + "\n")
    print(f"Passed {checks} assertions across {len(expected['cases'])} controls")


if __name__ == "__main__":
    main()
