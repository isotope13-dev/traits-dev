#!/usr/bin/env python3
"""Check syntax observations without inferring theft or CI modification."""
import argparse
import json
from pathlib import Path
import subprocess
import shutil
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="cleave")
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
prefix = "metadata/lang/source/syntax/command::"
syntax = prefix + "curl-sensitive-variable-data-syntax"
token = prefix + "curl-token-variable-data-syntax"
key = prefix + "curl-key-auth-variable-data-syntax"
package = prefix + "curl-package-variable-data-syntax"
cases = {
    "token-body.sh": {token, syntax},
    "credential-body.sh": {key, syntax},
    "package-body.sh": {package, syntax},
    "documented-attack-table.sh": {token, syntax},
    "header-only.sh": set(),
    "public-body.sh": set(),
    "bind-port.sh": set(),
    "upstream-port.sh": set(),
    "separate-host-upload.sh": set(),
}
required_hostile = {
    "testdata/hostile/rule-query-performance/env-upload-positive.sh":
        {"objectives/exfiltration/stealer/env::env-secret-dump-piped-to-network-client"},
    "testdata/taxonomy/registry-second-review/environment-upload.sh":
        {"objectives/exfiltration/stealer/env::env-full-dump-piped-to-network-client"},
    str((fixtures / "combined-upload.sh").relative_to(root)):
        {"objectives/supply-chain/trojanized/ci-pipeline::codecov-style-attack",
         "objectives/exfiltration/stealer/env::env-secret-dump-piped-to-network-client"},
}
paths = [fixtures / name for name in cases] + [root / p for p in required_hostile]
# Analyze copies outside testdata: the original matchers deliberately exclude
# test/documentation roles inferred from test directories. These controls must
# exercise the command matcher, not pass because of their fixture path.
temporary = tempfile.TemporaryDirectory(prefix=".curl-variable-check-", dir=root)
original_paths = {p.resolve(): Path(temporary.name) / str(i) / p.name
                  for i, p in enumerate(paths)}
for original, copied in original_paths.items():
    copied.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(original, copied)
paths = list(original_paths.values())
result = subprocess.run(
    [args.cleave, "--traits-dir", str(root), "--format", "json", *map(str, paths)],
    check=True, capture_output=True, text=True,
)
assert not result.stderr.strip(), result.stderr
# The CLI can concatenate JSON objects without a newline between them.
decoder = json.JSONDecoder()
remaining = result.stdout
files = {}
while remaining.strip():
    remaining = remaining.lstrip()
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:]
    for file in report["files"]:
        files[Path(file["path"]).resolve()] = {
            t["id"]: t for t in file.get("traits", [])
        }
for name, expected in cases.items():
    traits = files[original_paths[(fixtures / name).resolve()]]
    observed = {t for t in traits if t.startswith(prefix + "curl-") and t.endswith("-syntax")}
    # Redundant grouping composites may be omitted from final presentation.
    assert expected - {syntax} <= observed <= expected, (name, observed, expected)
    assert all(traits[t]["crit"] == 3 for t in observed), (name, traits)
    assert not any(t["crit"] >= 4 for t in traits.values()), (name, traits)
for name, expected in required_hostile.items():
    traits = files[original_paths[(root / name).resolve()]]
    assert all(t in traits and traits[t]["crit"] == 5 for t in expected), (name, traits)
listener = "micro-behaviors/communications/http/server/listener::bind-port-3000"
assert listener in files[original_paths[(fixtures / "bind-port.sh").resolve()]]
assert listener not in files[original_paths[(fixtures / "upstream-port.sh").resolve()]]
hosting = "micro-behaviors/communications/http/services/file-hosting::"
assert hosting + "public-file-hosting-with-upload-evidence" in files[
    original_paths[(fixtures / "separate-host-upload.sh").resolve()]]
temporary.cleanup()
print(f"Passed {len(cases)} syntax controls and {len(required_hostile)} attack controls")
