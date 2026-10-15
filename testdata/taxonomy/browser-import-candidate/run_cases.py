#!/usr/bin/env python3
"""Run isolated browser-import candidate cases against Cleave."""
import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CASES = Path(__file__).with_name("cases.json")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="/home/t/cleave/target/release/cleave")
    args = parser.parse_args()
    cases = json.loads(CASES.read_text())["fixtures"]
    engine = shutil.which(args.cleave)
    if not engine:
        raise SystemExit(f"missing Cleave executable: {args.cleave}")
    command = [engine, "--no-update-check", "--traits-dir", str(ROOT),
               "--disable", "yara,radare2,upx", "--format", "json"]
    env = {**os.environ, "CLEAVE_SKIP_CACHE": "1"}
    with tempfile.TemporaryDirectory(prefix="tax-run-") as tmp:
        if any(word in Path(tmp).name.lower() for word in ("test", "case")):
            raise SystemExit("temporary fixture path contains a test marker")
        for case in cases:
            source = ROOT / case["path"]
            if case.get("execute_before_scan"):
                subprocess.run([os.environ.get("PYTHON", "python3"), str(source)],
                               check=True, capture_output=True, text=True, env=env)
            dest = Path(tmp) / source.name
            shutil.copy2(source, dest)
            report = subprocess.run([*command, str(dest)], capture_output=True,
                                    text=True, check=True, env=env)
            value = json.loads(report.stdout)["files"][0]
            ids = {finding["id"] for finding in value.get("traits", [])}
            for rid in case.get("required_emitted", []):
                assert rid in ids, (source.name, "missing", rid, sorted(ids))
            for rid in case.get("forbidden_emitted", []):
                assert rid not in ids, (source.name, "unexpected", rid)
            by_id = {finding["id"]: finding for finding in value.get("traits", [])}
            for rid in case.get("forbidden_mbc", []):
                assert by_id.get(rid, {}).get("mbc") != "B0028", \
                    (source.name, "unexpected MBC B0028", rid, by_id.get(rid))
            for prefix in case.get("forbidden_prefixes", []):
                assert not any(rid.startswith(prefix) for rid in ids), \
                    (source.name, "unexpected prefix", prefix,
                     sorted(rid for rid in ids if rid.startswith(prefix)))
    print(f"browser-import candidate checks passed: {len(cases)} specimens")


if __name__ == "__main__":
    main()
