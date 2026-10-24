#!/usr/bin/env python3
"""Run the review controls outside test paths that suppress loader findings."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
destination = Path(sys.argv[1]).resolve() / "cases"
destination.mkdir(parents=True, exist_ok=True)

node = "micro-behaviors/os/module/dynamic-load::"
theft = "objectives/exfiltration/stealer/dev-secret::"
locale = "metadata/lang/locale::russian-language-or-locale-reference"
gate = "objectives/anti-analysis/geofencing/timezone::js-russian-locale-timezone-gate"
prototype = "well-known/lib/web/client-side/prototype::"
header = "micro-behaviors/communications/http/header/"
apify = "metadata/lang/source/syntax/member::"

cases = {
    "computed-node.js": ({node + "node-computed-require-call"}, set()),
    "dynamic-node.js": ({node + "node-dynamic-require-call"}, set()),
    "module-computed.js": ({node + "node-computed-require-call"}, set()),
    "module-dynamic.js": ({node + "node-dynamic-require-call"}, set()),
    "typed-node.ts": ({node + "node-computed-require-call"}, set()),
    "browser-require.js": (set(), {node + "node-dynamic-require-call", node + "node-computed-require-call"}),
    "require-comments.js": (set(), {node + "node-dynamic-require-call", node + "node-computed-require-call"}),
    "russian-locale.js": ({locale}, {gate}),
    "russian-gate.js": ({locale, gate}, set()),
    "prototype-header.js": ({header + "custom::x-prototype-version-header"}, {prototype + "version-string", prototype + "header-x"}),
    "prototype-definition.js": ({prototype + "version-string"}, set()),
    "go-header.go": ({header + "content-type::go-content-type-set"}, set()),
    "github-media-type.js": ({header + "content-type::github-json-media-type"}, set()),
    "apify-references.js": ({apify + "apify-actor-init-method-reference", apify + "apify-actor-pushdata-method-reference", theft + "apify-sdk-method-hook"}, set()),
    "github-token-send.yml": ({theft + "github-actions-secret-theft", theft + "curl-github-token", theft + "github-token-exfil"}, set()),
    "github-token-auth.yml": (set(), {theft + "github-actions-secret-theft", theft + "curl-github-token"}),
    "github-reserved-collector.yml": ({"micro-behaviors/communications/http/request/credentials::secrets-in-http-body"}, {theft + "github-actions-secret-theft", theft + "curl-github-token"}),
    "github-tool-flag.yml": (set(), {theft + "github-actions-secret-theft", theft + "curl-github-token"}),
    "network-export.js": ({node + "node-computed-require-call", "objectives/exfiltration/stealer/env::js-hex-table-env-post"}, set()),
    "network-writer.js": ({node + "node-computed-require-call", "objectives/exfiltration/stealer/env::js-hex-table-env-post"}, set()),
}
external = {
    "github-reserved-collector.yml": "testdata/benign/github-actions-curl-token-exfil.yml",
    "github-tool-flag.yml": "testdata/benign/github-actions-curl-flag-token.yml",
    "network-export.js": "testdata/hostile/stranded-byte-review/direct-index.js",
    "network-writer.js": "testdata/hostile/stranded-current-review/writer-renamed.js",
}
for name in cases:
    source = ROOT / external[name] if name in external else HERE / name
    shutil.copyfile(source, destination / name)

result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", str(destination)],
    capture_output=True, text=True,
)
if result.returncode:
    raise RuntimeError(result.stderr)
found = {}
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
while remaining:
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for file in report.get("files", [report]):
        name = Path(file["path"]).name
        found.setdefault(name, set()).update(trait["id"] for trait in file.get("traits", []))
for name, (required, forbidden) in cases.items():
    actual = found.get(name, set())
    assert required <= actual, (name, "missing", required - actual)
    assert not forbidden & actual, (name, "unexpected", forbidden & actual)
print(f"{len(cases)} review controls passed")
