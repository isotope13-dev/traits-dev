#!/usr/bin/env python3
"""Static triage regressions; never import or execute fixture code."""
import argparse
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="../cleave/target/release/cleave")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    cases = {
        "notable": ["referral.js", "campaign.js", "setup.py", "verified-host-census.js", "local-host-census.js"],
        "suspicious": ["credential-broker.js", "font_inventory.py", "zsh-escaped-prompt.tgz"],
        "hostile": ["cross-provider.js", "zsh-remote-prompt.tgz", "remote-host-census.js"],
    }
    paths = [root / "testdata" / level / "generated/probable-hostile-review" / name
             for level, names in cases.items() for name in names]
    result = subprocess.run(
        [args.cleave, "--traits-dir", str(root), "--json", *map(str, paths)],
        check=True, capture_output=True, text=True, cwd=root,
    )
    reports = {}
    for line in result.stdout.splitlines():
        report = json.loads(line)
        findings = {t["id"]: t for f in report["files"] for t in f.get("traits", [])}
        reports[Path(report["files"][0]["path"]).name] = findings
    assert len(reports) == len(paths), (len(reports), len(paths))
    for level, names in cases.items():
        for name in names:
            findings = reports[name]
            hostile = [t for t in findings.values() if t["crit"] == 5]
            suspicious = [t for t in findings.values() if t["crit"] == 4]
            if level == "hostile":
                assert hostile, (name, "missing hostile evidence")
            else:
                assert not hostile, (name, [t["id"] for t in hostile])
            if level == "suspicious":
                assert suspicious, (name, "lost meaningful warning")
    assert "objectives/execution/exploit/command-injection::json-text-command-substituting-zsh-prompt" in reports["zsh-remote-prompt.tgz"]
    assert "micro-behaviors/communications/http/request/body/credential::coding-agent-auth-json-http-upload" in reports["credential-broker.js"]
    assert "micro-behaviors/communications/url/query/tracking::tab-query-campaign-parameter-context" in reports["campaign.js"]
    assert "objectives/exfiltration/stealer/system-info/profile::shell-resolved-load-time-host-census-post" in reports["remote-host-census.js"]
    print(f"Probable-hostile triage: {len(paths)} static regressions passed.")


if __name__ == "__main__":
    main()
