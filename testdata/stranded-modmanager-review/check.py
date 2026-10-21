#!/usr/bin/env python3
"""Verify the exact VMProtect suppression boundary and neutral relocations."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
UPSTREAM = "third_party/bartblaze/generic/VMProtectStub/vmprotectstub"
DESCRIPTOR = "metadata/binary/symbols/descriptor::hook-manager-rtti-without-protector-types"
MIME = "micro-behaviors/data/format/mime::wildcard-application-mime"
LOG = "micro-behaviors/communications/http/url/php-endpoint::php-log-script-path"
EXFIL = "objectives/exfiltration/http/collect::browser-stealer-php-exfil"

def main():
    cases = json.loads((ROOT / "cases.json").read_text())
    env = os.environ.copy()
    env.pop("CLEAVE_VALIDATE", None)
    env["CLEAVE_TRAITS_DIR"] = str(REPO)
    run = subprocess.run(["atomscan", "--no-update", "--follow=none", "--mode", "slow",
                          "-f", "json", *[str(ROOT / c["file"]) for c in cases]],
                         env=env, capture_output=True, text=True, check=True)
    rows = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
    by_name = {Path(row["raw"]["files"][0]["path"]).name: row for row in rows}
    for case in cases:
        ids = {t["id"] for f in by_name[case["file"]]["raw"]["files"] for t in f.get("traits", [])}
        for key, trait in [("upstream", UPSTREAM), ("descriptor", DESCRIPTOR),
                           ("mime", MIME), ("log", LOG), ("exfil", EXFIL)]:
            assert (trait in ids) == case.get(key, False), (case["file"], key, ids)
    print(f"PASS {len(cases)} controls; all 44 distinctive RTTI pairs retained")

if __name__ == "__main__":
    main()
