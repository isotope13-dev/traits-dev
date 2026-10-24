"""Test original encrypted Mach-O bytes and bounded mutations; never run them."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("sample", type=Path)
parser.add_argument("scratch", type=Path)
args = parser.parse_args()
original = args.sample.read_bytes()
assert hashlib.sha256(original).hexdigest() == "8202c3887b75b107f76385fe36e7949860b7931cebd2c65899649556c37e30bc"
offsets, length = [0x4c90, 0x14de0], 37077


def transform(data):
    state, result = 0x11667, bytearray()
    for byte in data:
        result.append(byte ^ (state & 255))
        state = ((state * 0x3785) & 0xffffffff) % 35999
    return bytes(result)


plain = transform(original[offsets[0]:offsets[0] + length])
assert plain == transform(original[offsets[1]:offsets[1] + length])
variants = {
    "original": (plain, True),
    "renamed-handlers": (re.sub(rb"\b([fpvr])[0-9]{19}\b", lambda m: m[0][:1] + b"1" + m[0][2:], plain), True),
    "without-masked-dialog": (plain.replace(b"hidden answer", b"xxxxxx xxxxxx"), False),
    "without-password-validation": (plain.replace(b"dscl . authonly", b"xxxx . xxxxxxxx"), False),
    "without-file-reads": (plain.replace(b" to read ", b" to xxxx "), False),
    "without-extension-ids": (re.sub(rb"[a-p]{32}", lambda m: b"z" * 32, plain), False),
    "without-extension-stores": (plain.replace(b"Local Extension Settings", b"x" * 24).replace(b"IndexedDB", b"x" * 9), False),
}
args.scratch.mkdir(parents=True, exist_ok=True)
for name, (source, _) in variants.items():
    assert len(source) == length, name
    result = bytearray(original)
    encoded = transform(source)
    for offset in offsets:
        result[offset:offset + length] = encoded
    (args.scratch / (name + ".macho")).write_bytes(result)

root = Path(__file__).resolve().parents[2]
rule = "objectives/credential-access/wallet/extension::validated-password-wallet-extension-read-profile"
paths = [args.scratch / (name + ".macho") for name in variants]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root), "--json"] + list(map(str, paths)),
    capture_output=True, text=True,
)
assert result.returncode in (0, 1), result.stderr
remaining, found = result.stdout, {}
while remaining.strip():
    report, end = json.JSONDecoder(strict=False).raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report["files"]:
        found[Path(file["path"]).stem] = {trait["id"] for trait in file.get("traits", [])}
for name, (_, expected) in variants.items():
    assert (rule in found[name]) == expected, (name, expected, found[name])
    print(name, "matched" if expected else "not matched", flush=True)
print("7 encrypted-native controls passed")
