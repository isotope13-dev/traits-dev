#!/usr/bin/env python3
"""Check F-4 findings and pipeline verdicts in offline Scan."""

import argparse
import json
import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
SHELL = "objectives/execution/payload/script-eval/transformed/shell"
PIPELINE = f"{SHELL}::decoded-command-runs-remote-shell"
HTTP_PIPELINE = f"{SHELL}::decoded-http-command-runs-remote-shell"
POWERSHELL_PIPELINE = (
    "objectives/execution/payload/script-eval/network/decoded::"
    "powershell-launches-encoded-web-pipeline"
)
FETCH = f"{SHELL}::python-decoded-http-command"
EXEC = "objectives/anti-static/obfuscation/encoding/content::b64decode-exec"
CASES = {
    "hostile/base64-shell.tgz": PIPELINE,
    "hostile/base64-absolute-shell.py": PIPELINE,
    "hostile/hex-shell.py": PIPELINE,
    "hostile/go-base64.go": HTTP_PIPELINE,
    "hostile/go-hex.go": HTTP_PIPELINE,
    "hostile/node-base64.cjs": PIPELINE,
    "hostile/node-hex.ts": f"{SHELL}::program-decoded-remote-shell",
    "hostile/perl-base64.pl": HTTP_PIPELINE,
    "hostile/php-base64.php": HTTP_PIPELINE,
    "hostile/php-hex.php": HTTP_PIPELINE,
    "hostile/posix-base64.sh": f"{SHELL}::shell-decoded-remote-shell",
    "hostile/powershell-encoded-command.ps1": POWERSHELL_PIPELINE,
    "hostile/pwsh-encoded-command.ps1": POWERSHELL_PIPELINE,
    "hostile/ruby-base64.rb": PIPELINE,
    "suspicious/base64-http-fetch.py": FETCH,
    "suspicious/hex-http-fetch.py": FETCH,
    "suspicious/base64-exec.py": EXEC,
    "notable/base64-pipeline-data.py": None,
    "notable/base64-fetch-data.py": None,
    "notable/go-base64-data.go": None,
    "notable/node-base64-data.cjs": None,
    "notable/perl-unrelated-argument.pl": None,
    "notable/php-base64-data.php": None,
    "notable/powershell-encoded-data.ps1": None,
    "notable/powershell-comment.ps1": None,
    "notable/powershell-unrelated-command.ps1": None,
    "notable/ruby-base64-data.rb": None,
}
# Scan's default policy can allow even with one or more hostile static findings.
STATIC_ONLY = {
    "node-base64.cjs",
    "node-hex.ts",
    "powershell-encoded-command.ps1",
    "pwsh-encoded-command.ps1",
}
CRITICALITY = {"suspicious": 4, "hostile": 5}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atomscan", default="atomscan")
    args = parser.parse_args()
    paths = {}
    for case, trait in CASES.items():
        severity, name = case.split("/")
        path = ROOT / "testdata" / severity / "controls" / "f4-encoded-commands" / name
        paths[str(path)] = (severity, trait)

    env = os.environ.copy()
    env.pop("SCAN_LLM", None)
    env.pop("SCAN_HOPPER", None)
    env.update(CLEAVE_TRAITS_DIR=str(ROOT), SCAN_NO_ANALYSIS_CACHE="1", CLEAVE_SKIP_CACHE="1")
    result = subprocess.run(
        [args.atomscan, "--offline", "--mode", "slow",
         "--follow=none", "--format=json", "path", *paths],
        cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE,
    )
    if result.returncode not in (0, 1):
        raise SystemExit(f"atomscan exited with status {result.returncode}")
    reports = {row["path"]: row for row in map(json.loads, result.stdout.splitlines())}
    if reports.keys() != paths.keys():
        raise SystemExit(f"Unexpected fixture paths: {reports.keys() ^ paths.keys()}")
    for path, (severity, trait) in paths.items():
        report = reports[path]
        findings = {finding["id"]: finding["crit"] for finding in report["findings"]}
        if trait is None:
            if findings or report["severity"] != "benign":
                raise SystemExit(f"{path}: expected a benign data-only control")
        elif findings.get(trait) != CRITICALITY[severity]:
            raise SystemExit(f"{path}: expected {trait}, got {findings}")
        elif (
            severity == "hostile"
            and Path(path).name not in STATIC_ONLY
            and report["decision"] != "block"
        ):
            raise SystemExit(f"{path}: expected the remote shell pipeline to be blocked")
    print(f"Validated {len(paths)} F-4 fixtures with local Scan")


if __name__ == "__main__":
    main()
