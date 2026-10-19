#!/usr/bin/env python3
"""Reproduce this sample's containers offline; never execute its scripts/PEs."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("sample", type=Path)
parser.add_argument("output", type=Path)
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
source = args.sample.read_text()
values = {
    name: base64.b64decode(re.sub(r"\s", "", value))
    for name, value in re.findall(r"\$(\w+)\s*=\s*@'\s*\n(.*?)\n'@", source, re.S)
}
stage = subprocess.run(
    ["openssl", "enc", "-d", "-aes-256-cbc", "-K", values["cryptoKeyMaterial"].hex(),
     "-iv", values["initializationVector"].hex()],
    input=values["encryptedPayload"], capture_output=True, check=True,
).stdout
text = stage.decode("utf-8")
key = re.search(r'\$encryptionKey\s*=\s*"([^"]+)"', text)[1].encode()
cipher = base64.b64decode(re.search(r"\$encryptedPayload\s*=\s*'([^']+)'", text)[1])
launcher = base64.b64decode(bytes(c ^ key[i % len(key)] for i, c in enumerate(cipher)))
array = re.search(r"\[Byte\[\]\]\$payloadBytes\s*=\s*\(([^)]+)\)", text)[1]
payload = bytes(map(int, array.split(",")))
manifest = {}
for name, data in [("stage1.ps1", stage), ("launcher.dll", launcher), ("payload.exe", payload)]:
    (args.output / name).write_bytes(data)
    manifest[name] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
print(json.dumps(manifest, indent=2))
