#!/usr/bin/env python3
"""Check reference-only classification and preserved geo attack consumers."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
base = Path(__file__).resolve().parent
neutral = "micro-behaviors/communications/http/ip-discovery::multi-public-geo-api-references"
gate = "objectives/anti-analysis/geofencing/network::geo-api-target-country-gate"
wallet = "objectives/exfiltration/stealer/wallet::wallet-phrase-geo-text-exfiltration"
generated = "objectives/exfiltration/stealer/wallet::generated-wallet-phrase-geo-export"
cases = [
    (base / "service-catalog.js", {neutral}, {gate}, True),
    (base / "one-primary-service.js", set(), {neutral, gate}, True),
    (base / "country-gate.js", {neutral, gate}, set(), False),
    (root / "testdata/benign/site-rank-table-fp.js", set(), {neutral, gate}, True),
    (root / "testdata/triage/intensive-second-review/wallet-export.js",
     {wallet, generated}, set(), False),
    (root / "testdata/triage/intensive-second-review/wallet-renamed-export.js",
     {wallet, generated}, set(), False),
    (root / "testdata/triage/intensive-second-review/wallet-local.js",
     set(), {wallet, generated}, True),
]
for path, required, forbidden, benign in cases:
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root), "--json", str(path)],
        check=True, text=True, capture_output=True,
    )
    report = json.loads(result.stdout)
    findings = {t["id"]: t for f in report["files"] for t in f["traits"]}
    assert required <= findings.keys(), (path, "missing", required - findings.keys())
    assert not forbidden & findings.keys(), (path, "unexpected", forbidden & findings.keys())
    if neutral in findings:
        assert findings[neutral]["crit"] == 3, (path, findings[neutral])
    if gate in findings:
        assert findings[gate]["crit"] == 5, (path, findings[gate])
    if benign:
        assert not [t for t in findings.values() if t["crit"] >= 4], path
    print("PASS", path.relative_to(root))
