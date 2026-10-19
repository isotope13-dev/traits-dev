#!/usr/bin/env python3
"""Check the memo-loader boundary and the provider-fragment correction."""
import argparse
import json
from pathlib import Path
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="cleave")
parser.add_argument("--fixtures", required=True, type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
result = subprocess.run(
    [args.cleave, "--traits-dir", str(root), "--format", "json", str(args.fixtures)],
    text=True, capture_output=True,
)
assert result.returncode == 0, result.stderr or result.stdout
assert not result.stderr.strip(), result.stderr
decoder = json.JSONDecoder()
remaining = result.stdout
files = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report["files"]:
        files[Path(file["path"]).name] = file["traits"]

expected = {
    "selector-display.py", "selector-decimal-display.py",
    "emoji-crypto.py", "selector-table-crypto.py",
    "memo-viewer.py", "memo-viewer.js", "ordinary-evaluator.js",
    "rpc-providers.js", "rpc-provider-only.js",
}
assert set(files) == expected, set(files)
for name, traits in files.items():
    convictions = {trait["id"] for trait in traits if trait["crit"] >= 4}
    # Preserve existing generic findings while asserting that the new
    # intent-specific detections do not convict these controls.
    wanted = {
        "ordinary-evaluator.js": {
            "objectives/supply-chain/hidden-payload/encoding::eval-atob"
        },
        "selector-decimal-display.py": {
            "objectives/anti-static/obfuscation/encoding/custom::unicode-codepoint-offset-decoder"
        },
    }.get(name, set())
    assert convictions == wanted, (name, convictions)

provider = "micro-behaviors/communications/blockchain/client::solana-signature-provider-fragments"
selector = "micro-behaviors/data/decode/custom::python-variation-selector-byte-decoder"
for name in ("selector-display.py", "selector-decimal-display.py"):
    assert selector in {t["id"] for t in files[name]}, name
assert provider in {t["id"] for t in files["rpc-providers.js"]}
assert provider not in {t["id"] for t in files["rpc-provider-only.js"]}
for name in ("rpc-providers.js", "rpc-provider-only.js"):
    assert not any("solana-get-transaction" in t["id"] for t in files[name])
print("Passed 9 controls: memo display, selector display, emoji/crypto, and RPC providers.")
