#!/usr/bin/env python3
"""Ensure generated-looking paths alone do not establish SDK suppressor context."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent
MANIFEST = json.loads((BASE / "cases.json").read_text())
CLEAVE = shutil.which(sys.argv[1] if len(sys.argv) > 1 else str(ROOT.parent / "cleave/target/release/cleave"))
assert CLEAVE, "missing Cleave executable"
CMD = [str(Path(CLEAVE).resolve()), "--no-update-check", "--traits-dir", str(ROOT)]
ENV = {**os.environ, "CLEAVE_SKIP_CACHE": "1"}


def reports(text):
    dec = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        value, end = dec.raw_decode(text)
        yield from value["files"]
        text = text[end:]


def run_trace(path, ids):
    p = subprocess.run([*CMD, "--disable", "yara,radare2,upx", "test-rules", str(path), "--rules", ",".join(ids)],
                       text=True, capture_output=True, check=True, env=ENV)
    return p.stdout + p.stderr


with tempfile.TemporaryDirectory(prefix="tax-run-") as temp:
    root = Path(temp)
    source_paths = []
    expected_by_runtime = {}
    for i, case in enumerate(MANIFEST["fixtures"]):
        dest = root / f"{i:04d}" / case["runtime_path"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / case["path"], dest)
        source_paths.append(dest)
        expected_by_runtime[str(dest)] = case
    identity = MANIFEST["identity_control"]
    identity_dest = root / "identity" / identity["runtime_path"]
    identity_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / identity["path"], identity_dest)

    scan_paths = [*source_paths, identity_dest]
    scan = subprocess.run([*CMD, "--disable", "yara,radare2,upx", "--format", "json", *map(str, scan_paths)],
                          text=True, capture_output=True, check=True, env=ENV)
    by_path = {f["path"]: f for f in reports(scan.stdout)}

    for path in source_paths:
        case = expected_by_runtime[str(path)]
        file = by_path[str(path)]
        emitted = {t["id"] for t in file.get("traits", [])}
        if case["consumer_id"]:
            assert case["consumer_id"] in emitted, (case["case_id"], "consumer finding suppressed", file.get("supp"))
            assert not any(s.get("id") == case["consumer_id"] for s in file.get("supp", [])), \
                (case["case_id"], "consumer suppressed", file.get("supp"))
        else:
            trace = run_trace(path, [case["trace_rule"]])
            assert f"MATCHED {case['trace_rule']} (" in trace, (case["case_id"], "neutral field not recognized", trace)
        for rid in case.get("absent_ids", []):
            assert rid not in emitted, (case["case_id"], "schema/comment produced behavior finding", rid)
        assert "well-known/lib/network/getstream-stream-node::stream-node-sdk-official" not in emitted, \
            (case["case_id"], "path alone established SDK identity", emitted)

    identity_file = by_path[str(identity_dest)]
    identity_emitted = {t["id"] for t in identity_file.get("traits", [])}
    composite_id = "well-known/lib/network/getstream-stream-node::stream-node-sdk-official"
    for rid in identity["expected_matched"]:
        if rid == composite_id:
            continue  # Exception composites are tested through their debug trace below.
        assert rid in identity_emitted, ("package identity control", rid, identity_emitted)
    identity_trace = run_trace(identity_dest, [composite_id])
    assert f"MATCHED {composite_id} (" in identity_trace, ("package identity control", identity_trace)

print(f"GetStream generated-path controls passed: {len(MANIFEST['fixtures'])} source cases and one package-identity control")
