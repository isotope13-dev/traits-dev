#!/usr/bin/env python3
"""Verify a quoted XXE example cannot hide active JavaScript execution."""
import lzma
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
TRAIT = "metadata/package/documentation/source::javascript-exported-documentation-records"
SOURCE = ROOT / "metadata/package/documentation/source/javascript-documentation-records.yaml"
FIXTURE = ROOT / "testdata/suspicious/generated/reduced/taxonomy/vsix-triage-2026-10-20/skill-content-catalog.js.xz"
CLEAVE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))

with lzma.open(FIXTURE, "rt", encoding="utf-8") as fixture:
    catalog = fixture.read()
needle = '"id": "arabic-localization",'
assert needle in catalog
nested = catalog.replace(needle, needle + ' "run": () => fetch("https://example.com"),', 1)
cases = [("catalog", catalog, True),
         ("top-level-call", catalog + '\nfetch("https://example.com");\n', False),
         ("nested-call", nested, False)]
with tempfile.TemporaryDirectory(prefix="xxe-doc-shape-") as tmp:
    root = Path(tmp)
    rules = root / "rules/metadata/package/documentation/source"
    rules.mkdir(parents=True)
    shutil.copyfile(SOURCE, rules / SOURCE.name)
    for name, source, expected in cases:
        sample = root / (name + ".js")
        sample.write_text(source, encoding="utf-8")
        result = subprocess.run([CLEAVE, "--disable", "yara", "--traits-dir", str(root / "rules"),
                                 "test-rules", "--rules", TRAIT, str(sample)],
                                text=True, capture_output=True, check=True)
        lines = result.stdout.splitlines()
        matched = any(line.startswith("MATCHED " + TRAIT + " ") for line in lines)
        if matched != expected:
            raise AssertionError(f"{name}: expected match={expected}\n{result.stdout}\n{result.stderr}")
print("XXE documentation shape: catalog accepted; active variants rejected")
