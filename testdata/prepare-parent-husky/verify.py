"""Check Husky prepare exclusions without hiding additional shell commands.

Usage: python3 testdata/prepare-parent-husky/verify.py <scratch-directory>
"""

import json
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
PREFIX = "objectives/supply-chain/install-hook/project-rewrite::"
ESCAPE = PREFIX + "prepare-parent-directory-escape"
INSTALL = "objectives/execution/autoinstall/package::script-npm-install-prepare"

# These scripts are analyzed as data and are never executed.
CASES = {
    "single-parent": ("cd .. && husky install ui/.husky", False, False),
    "two-parents": ("cd ../.. && husky install packages/lib/.husky", False, False),
    "three-parents": ("cd ../../.. && husky install modules/ui/.husky", False, False),
    "quoted-parent": ('cd "../.." && husky install ui/.husky', False, False),
    "windows-parent": (r"pushd ..\.. && husky install ui/.husky", False, False),
    "npx": ("cd ../.. && npx husky install ui/.husky", False, False),
    "default-directory": ("cd ../.. && husky install", False, False),
    "bare-husky": ("cd ../.. && husky", False, False),
    "appended-install": (
        "cd ../.. && husky install ui/.husky && npm install injected-package", True, True),
    "prepended-install": (
        "cd ../.. && npm install injected-package && husky install ui/.husky", True, True),
    "appended-node": ("cd ../.. && husky install ui/.husky && node helper.js", True, False),
    "semicolon": ("cd ../.. && husky install ui/.husky;node helper.js", True, False),
    "pipeline": ("cd ../.. && husky install ui/.husky|node helper.js", True, False),
    "background": ("cd ../.. && husky install ui/.husky&node", True, False),
    "substitution": ("cd ../.. && husky install $(node helper.js)", True, False),
    "backticks": ("cd ../.. && husky install `node helper.js`", True, False),
    "windows-variable": ("cd ../.. && husky install %HOOK_DIR%", True, False),
    "windows-delayed-variable": ("cd ../.. && husky install !HOOK_DIR!", True, False),
    "redirection": ("cd ../.. && husky install ui/.husky>output", True, False),
    "plain-injection": ("cd ../.. && npm install injected-package", True, True),
}


def main():
    dest = Path(sys.argv[1]).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    for name, (script, _, _) in CASES.items():
        folder = dest / name
        folder.mkdir(exist_ok=True)
        (folder / "package.json").write_text(json.dumps({"scripts": {"prepare": script}}))

    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "json", str(dest)],
        env=dict(os.environ, CLEAVE_VALIDATE="0"),
        text=True, capture_output=True, check=True)
    # Directory scans emit one JSON report per artifact, possibly concatenated.
    decoder = json.JSONDecoder()
    reports = []
    remaining = result.stdout.strip()
    while remaining:
        report, end = decoder.raw_decode(remaining)
        reports.append(report)
        remaining = remaining[end:].lstrip()
    findings = {Path(f["path"]).parent.name: {t["id"] for t in f.get("traits", [])}
                for report in reports for f in report["files"]
                if Path(f["path"]).name == "package.json"}
    for name, (_, escape, install) in CASES.items():
        ids = findings[name]
        assert (ESCAPE in ids) == escape, (name, "escape", sorted(ids))
        assert (INSTALL in ids) == install, (name, "package install", sorted(ids))
        print("PASS", name)


if __name__ == "__main__":
    main()
