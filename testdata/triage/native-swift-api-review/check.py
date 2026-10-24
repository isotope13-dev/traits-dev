#!/usr/bin/env python3
"""Check native API coverage without building or executing the Swift fixtures."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EVAL = "micro-behaviors/process/interpreter/eval/indirect::"
SYNTAX = "metadata/lang/source/syntax/call/invocation::"
AUDIO = "micro-behaviors/hardware/input/audio::"
CAPABILITIES = {
    EVAL + "swift-webkit-javascript-evaluation",
    EVAL + "swift-javascriptcore-script-evaluation",
    AUDIO + "swift-avaudio-recorder-construction",
    AUDIO + "swift-audio-session-record-permission",
}
SYNTAX_IDS = {
    SYNTAX + "swift-evaluate-javascript-method-call",
    SYNTAX + "swift-evaluate-script-method-call",
}
OTHER = {
    "micro-behaviors/crypto/hash/digest::sha256",
    "micro-behaviors/crypto/hash/digest::sha512",
    "micro-behaviors/os/random/crypto::secrandomcopybytes",
    "micro-behaviors/data/decompress/zlib::inflate",
}
paths = [HERE / name for name in (
    "api-calls.swift", "names-only.swift", "unrelated-methods.swift"
)]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *map(str, paths)],
    text=True, capture_output=True, check=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout
observations = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for entry in report["files"]:
        observations[Path(entry["path"]).name] = {
            trait["id"] for trait in entry.get("traits", [])
        }

assert CAPABILITIES | SYNTAX_IDS | OTHER <= observations["api-calls.swift"]
assert not (CAPABILITIES | SYNTAX_IDS) & observations["names-only.swift"]
assert SYNTAX_IDS <= observations["unrelated-methods.swift"]
assert not CAPABILITIES & observations["unrelated-methods.swift"]
print("PASS: native calls, inert references, and unrelated receivers")
