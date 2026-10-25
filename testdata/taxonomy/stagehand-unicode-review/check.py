#!/usr/bin/env python3
"""Behavioral-rule regression controls; fixtures are never executed."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent
EMAIL = "objectives/evasion/anti-av/content::unicode-tag-spliced-financial-email"
SPLICE = "objectives/evasion/anti-av/content::unicode-tag-spliced-ascii-token"
AWS = "micro-behaviors/communications/http/services/aws::billing-get-credits-call"
MCP = "micro-behaviors/communications/mcp::mcp-initialize-result"
DROP = "objectives/execution/exploit/service-command-injection::mcp-config-test-payload-dropper"
WP = "objectives/command-and-control/backdoor/webshell/upload::wordpress-plugin-command-webshell-upload"
CDP = "micro-behaviors/communications/http/devtools/client::"
BROWSER = [CDP + x for x in ["cdp-runtime-run-if-waiting-reference", "cdp-storage-set-cookies-literal", "cdp-storage-clear-cookies-literal"]]
POLICY = "micro-behaviors/os/security/policy::chromium-client-phishing-detection-disable-option"
LABEL = "metadata/lang/source/naming/action::delete-file-name-literal"
ZIP = "micro-behaviors/data/format/mime::application-zip-mime"
CASES = [
    (BASE / "tag-spliced-offer.txt", [EMAIL, SPLICE], []),
    (BASE / "ordinary-offer.txt", [], [EMAIL, SPLICE]),
    (BASE / "legitimate-unicode-offer.txt", [], [EMAIL, SPLICE]),
    (BASE / "single-splice-offer.txt", [], [EMAIL, SPLICE]),
    (BASE / "vercel-credit-query.js", [], [AWS]),
    (BASE / "aws-command.js", ["micro-behaviors/communications/http/services/aws::billing-get-credits-js-command"], []),
    (ROOT / "testdata/telemetry-trait-precision/aws-billing-positive.py", [AWS], []),
    (ROOT / "testdata/benign/bedrock-billing-controls.py", [AWS], []),
    (ROOT / "testdata/taxonomy/virgil-telemetry-triage/private-getcredits-no-billing.js", [], [AWS]),
    (BASE / "runtime-descriptor.js", [], [MCP]),
    (BASE / "mcp-response.py", [MCP], [DROP]),
    (BASE / "mcp-staging.py", [MCP, DROP], []),
    (BASE / "browser-capabilities.js", BROWSER + [POLICY, LABEL, ZIP], ["metadata/package/testing/harness/node-inspector::node-inspector-session-api"]),
    (BASE / "browser-near-miss.js", [], BROWSER + [POLICY, LABEL, ZIP]),
    (BASE / "wordpress-upload.js", [WP, ZIP], []),
    (BASE / "ordinary-plugin-upload.js", [ZIP], [WP]),
    (ROOT / "testdata/benign/invisible-unicode-legit-uses.txt", [], [EMAIL, SPLICE]),
]

def check(case):
    path, required, forbidden = case
    # Scan copied bytes outside testdata: the source fixture path intentionally
    # suppresses evasion rules and is not the deployment context under test.
    with tempfile.TemporaryDirectory(prefix=".rule-controls-", dir=ROOT) as d:
        target = Path(d) / path.name
        target.write_bytes(path.read_bytes())
        r = subprocess.run([os.environ.get("CLEAVE", "cleave"), "--format", "json", str(target)],
            cwd=ROOT, env=dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT)),
            capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    ids = {t["id"] for f in j["files"] for t in f.get("traits", [])}
    errors = ["missing " + x for x in required if x not in ids]
    errors += ["unexpected " + x for x in forbidden if x in ids]
    return str(path.relative_to(ROOT)), errors

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(check, CASES))
    for name, errors in results:
        print(("FAIL" if errors else "PASS"), name, "; ".join(errors))
    raise SystemExit(any(e for _, e in results))
