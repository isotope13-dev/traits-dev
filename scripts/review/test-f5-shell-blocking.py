#!/usr/bin/env python3
"""Check F-5 findings and default-budget decisions in Scan.

Offline, each hostile fixture must carry its hostile trait and no control may
be blocked. Scan's static policy can allow a lone hostile trait, so blocking
is asserted only with --llm, the grader production blends in: then every
hostile fixture must block at budget 25 (and so at 250) and every control
must be allowed.
"""

import argparse
import json
import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
NETWORK = "objectives/execution/payload/interpreter-stdin/network/shell"
REVERSED = "objectives/execution/payload/script-eval/transformed/shell::js-reversed-command-runs-remote-shell"
CASES = {
    "hostile/raw-ip-postinstall/package.json": f"{NETWORK}::postinstall-raw-ip-fetch-into-shell",
    "hostile/raw-ip-preinstall/package.json": f"{NETWORK}::preinstall-raw-ip-fetch-into-shell",
    "hostile/raw-ip-exec.cjs": f"{NETWORK}::node-curl-pipe-shell-exec",
    "hostile/reversed-command.cjs": REVERSED,
    "hostile/reversed-wget-command.cjs": REVERSED,
    "suspicious/private-ip-postinstall/package.json": None,
    "suspicious/rustup-postinstall/package.json": None,
    "suspicious/rustup-exec.cjs": None,
    "notable/reversed-data.cjs": None,
    "notable/reversed-local-command.cjs": None,
}
DEFAULT_BUDGET = 25


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atomscan", default="atomscan")
    parser.add_argument("--llm", help="OpenAI-compatible grader URL; also asserts decisions")
    args = parser.parse_args()
    paths = {}
    for case, trait in CASES.items():
        severity, name = case.split("/", 1)
        path = ROOT / "testdata" / severity / "controls" / "f5-shell-blocking" / name
        paths[str(path)] = trait

    env = os.environ.copy()
    env.pop("SCAN_LLM", None)
    env.pop("SCAN_HOPPER", None)
    env.update(CLEAVE_TRAITS_DIR=str(ROOT), SCAN_NO_ANALYSIS_CACHE="1", CLEAVE_SKIP_CACHE="1")
    mode = ["--uplink", "false", "--no-update", "--llm", args.llm] if args.llm else ["--offline"]
    result = subprocess.run(
        [args.atomscan, *mode, "--mode", "slow", "--follow=none", "--format=json", "path", *paths],
        cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE,
    )
    # 0 benign, 1 hostile, 2 suspicious; 3 and 4 mean the scan proves nothing.
    if result.returncode not in (0, 1, 2):
        raise SystemExit(f"atomscan exited with status {result.returncode}")
    reports = {row["path"]: row for row in map(json.loads, result.stdout.splitlines())}
    if reports.keys() != paths.keys():
        raise SystemExit(f"Unexpected fixture paths: {reports.keys() ^ paths.keys()}")
    for path, trait in paths.items():
        report = reports[path]
        hostile = {finding["id"] for finding in report["findings"] if finding["crit"] == 5}
        fires_at = report["fires_at"]
        if trait is None:
            if hostile:
                raise SystemExit(f"{path}: expected no hostile findings, got {hostile}")
            if report["decision"] == "block":
                raise SystemExit(f"{path}: control blocked at fires_at={fires_at}")
        elif trait not in hostile:
            raise SystemExit(f"{path}: expected {trait}, got {hostile}")
        elif args.llm and not (0 <= fires_at <= DEFAULT_BUDGET and report["decision"] == "block"):
            raise SystemExit(f"{path}: expected a block at budget {DEFAULT_BUDGET}, got fires_at={fires_at}")
    print(f"Validated {len(paths)} F-5 fixtures with {'graded' if args.llm else 'local'} Scan")


if __name__ == "__main__":
    main()
