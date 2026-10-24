#!/usr/bin/env python3
"""Scan controls under a neutral path so test-directory exclusions cannot hide failures."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="cleave")
parser.add_argument("--staging", type=Path, required=True)
args = parser.parse_args()
fixtures = Path(__file__).resolve().parent
root = fixtures.parents[2]
args.staging.mkdir(parents=True, exist_ok=True)
for source in fixtures.iterdir():
    if source.suffix in {".js", ".html"}:
        shutil.copyfile(source, args.staging / source.name)

query = "micro-behaviors/data/db/query::select-encrypted-key-field"
indexed = "metadata/lang/source/syntax/call/arguments::js-constructor-hex-indexed-arguments"
screen = "micro-behaviors/hardware/display/screen::browser-indexed-screen-dimension-field"
expected = {
    "encrypted-key-query.js": {query},
    "indexed-numeric-constructors.js": {indexed},
    "indexed-function-generation.js": {indexed, "micro-behaviors/metaprogramming/generation::function-ctor-call-expr-arg"},
    "plain-query-navigation.js": {"micro-behaviors/ui/window/navigation::browser-location-replace", "micro-behaviors/communications/http/url/query::browser-url-query-forwarding-loop"},
    "computed-query-navigation.js": {"micro-behaviors/communications/http/url/query::obfuscated-urlsearchparams-iteration"},
    "screen-properties.js": {screen},
    "layout-properties.js": set(),
    "database-oob.js": {query, "objectives/exfiltration/stealer/wallet::js-secret-database-rows-oob-exfil", "objectives/supply-chain/trojanized/package/exfil::npm-import-time-secret-database-exfil"},
    "turnstile-failure-redirect.html": {
        "objectives/credential-access/phishing/captcha::cloudflare-turnstile-phishing-page",
        "objectives/credential-access/phishing/landing::turnstile-encrypted-next-hop-redirect",
        "objectives/credential-access/phishing/landing::obfuscated-turnstile-expiry-decrypt-redirect",
    },
    "credential-sweep-function.js": {"objectives/credential-access/theft/multi-store::obfuscated-cloud-github-credential-sweep"},
    "self-defending-function.js": {"objectives/supply-chain/hidden-payload/eval::self-defending-string-table-function-loader"},
}
retired = {
    "objectives/collection/database/query::sql-selects-encrypted-key-fields",
    "objectives/anti-static/obfuscation/syntax::js-new-from-indexed-string-table",
    "objectives/anti-static/obfuscation/eval/function::string-table-function-constructor",
    "micro-behaviors/ui/window/navigation::obfuscated-query-navigation",
}
output = subprocess.run(
    [args.cleave, "--traits-dir", str(root), "--format", "json", str(args.staging)],
    check=True, capture_output=True, text=True,
).stdout
decoder = json.JSONDecoder()
reports = {}
while output.strip():
    report, end = decoder.raw_decode(output.lstrip())
    output = output.lstrip()[end:]
    reports.update({Path(f["path"]).name: f for f in report["files"]})
benign = set(expected) - {"database-oob.js", "turnstile-failure-redirect.html", "credential-sweep-function.js", "self-defending-function.js"}
for name, required in expected.items():
    traits = reports[name]["traits"]
    ids = {t["id"] for t in traits}
    assert required <= ids, (name, "missing", required - ids)
    assert not retired & ids, (name, "retired", retired & ids)
    if name in benign:
        assert not any(t["crit"] >= 4 for t in traits), (name, "unexpected suspicious finding")
    if name == "layout-properties.js":
        assert screen not in ids, (name, "screen-property false positive")
print(f"{len(expected)} controls passed; seven dependent hostile detections retained")
