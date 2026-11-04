#!/usr/bin/env python3
"""Check triage wording/flow boundaries without executing sample code."""
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
        "hostile": [
            "aliased-collector.js", "aliased-encoded-collector.js",
            "withdrawn-release.registry.json",
        ],
        "notable": [
            "unrelated-curl.js", "get-with-unrelated-post.js", "custom-request.js",
            "holder-string/package.json", "holder-object/package.json",
            "unavailable-release.registry.json", "holder-release.registry.json",
            "manifest-wrapper.tgz", "empty-export-wrapper.tgz",
        ],
    }
    reports = {}
    for level, names in cases.items():
        for name in names:
            path = root / "testdata" / level / "generated/probable-hostile-improve" / name
            result = subprocess.run(
                [args.cleave, "--traits-dir", str(root), "--json", str(path)],
                check=True, capture_output=True, text=True, cwd=root,
            )
            report = json.loads(result.stdout)
            findings = {t["id"]: t for f in report["files"] for t in f.get("traits", [])}
            reports[name] = findings
            hostile = [t["id"] for t in findings.values() if t["crit"] == 5]
            assert bool(hostile) == (level == "hostile"), (name, hostile)
    collector = "micro-behaviors/communications/http/request/configuration::node-post-host-from-curl-response"
    assert collector in reports["aliased-collector.js"]
    for name in ["unrelated-curl.js", "get-with-unrelated-post.js", "custom-request.js"]:
        assert collector not in reports[name], name
    holder = "metadata/package/freeform::npm-security-holder-package"
    for name in ["holder-string/package.json", "holder-object/package.json"]:
        assert holder in reports[name], name
    withdrawn = "objectives/supply-chain/security-hold::registry-security-withdrawn-package-coordinate"
    assert withdrawn in reports["withdrawn-release.registry.json"]
    for name in ["unavailable-release.registry.json", "holder-release.registry.json"]:
        assert withdrawn not in reports[name], name
    for name in ["manifest-wrapper.tgz", "empty-export-wrapper.tgz"]:
        assert not [t["id"] for t in reports[name].values() if t["crit"] >= 4], name
        assert "metadata/package/dependencies/source::npm-https-runtime-dependency" in reports[name]
    print(f"Probable-hostile improvements: {len(reports)} static regressions passed.")


if __name__ == "__main__":
    main()
