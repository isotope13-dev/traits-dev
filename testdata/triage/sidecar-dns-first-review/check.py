"""Behavioral rule controls; specimen code is never executed."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import re
from pathlib import Path
import shutil
import subprocess
import tarfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--archive", type=Path, required=True)
parser.add_argument("--dll-one", type=Path, required=True)
parser.add_argument("--dll-two", type=Path, required=True)
parser.add_argument("--work-dir", type=Path, required=True)
args = parser.parse_args()
args.work_dir.mkdir(parents=True, exist_ok=True)
fixture_dir = Path(__file__).parent
crypto = "micro-behaviors/crypto/decrypt::node-aes-gcm-hex-input-and-tag-slice"
tag = "micro-behaviors/crypto/decrypt::auth-tag-sliced-from-buffer"
hex_input = "micro-behaviors/data/decode/hex::node-update-with-hex-buffer"
shell = "micro-behaviors/process/create/shell/command-string::gyp-source-command-with-shell-operators"
packed = "objectives/anti-static/obfuscation/encoding/numeric::charcode-packed-numeric-source"
brotli = "micro-behaviors/data/decompress/brotli::node-brotli-decompress-function"
erase = "objectives/evasion/indicator-removal/structure::x86-erase-pe-dos-signatures"
hook = "objectives/supply-chain/hidden-payload/native-extension::gyp-runs-obfuscated-entry-dropper"
execute = "objectives/execution/payload/file-exec::node-gcm-sidecar-decrypt-exec"
encrypted = "objectives/anti-static/obfuscation/payload/encrypted::packed-dropper-decrypts-inline-stage"
results = []
jobs = []

def check(path, expected, name=None):
    jobs.append((path, expected, name))

def evaluate(path, expected, name=None):
    name = name or path.name
    output = subprocess.run(
        ["cleave", "--traits-dir", ".", "test-rules", str(path),
         "--rules", ",".join(expected)],
        capture_output=True, text=True, check=True)
    log = output.stdout + output.stderr
    assert "validation failed" not in log and "Warning: Rule" not in log, log
    actual = {
        rule: any(line.startswith("MATCHED " + rule + " ")
                  for line in output.stdout.splitlines())
        for rule in expected
    }
    (args.work_dir / (name + ".log")).write_text(log)
    assert actual == expected, (name, actual, expected, log)
    results.append({"case": name, "matched": actual})

# Copy out of fixture directories: path-based test exclusions must not decide
# whether an application record or harmless packer receives an attack label.
for filename in ["decrypt-data.js", "generate-sources.gyp", "packed-add.js",
                 "brotli-alias.js", "brotli-mention.js", "chacha-record.js"]:
    shutil.copyfile(fixture_dir / filename, args.work_dir / filename)
check(args.work_dir / "decrypt-data.js",
      {crypto: True, tag: True, hex_input: True, execute: False, encrypted: False})
check(args.work_dir / "chacha-record.js", {tag: True, crypto: False})
check(args.work_dir / "generate-sources.gyp", {shell: True, hook: False})
check(args.work_dir / "packed-add.js", {packed: True, encrypted: False, execute: False})
check(args.work_dir / "brotli-alias.js", {brotli: True})
check(args.work_dir / "brotli-mention.js", {brotli: False})
# Retain existing positives outside this batch, including an actual staged-code
# fixture and an independent ordinary decompressor.
for filename in [
    "testdata/triage/betterbird-review/sidecar-loader.js",
    "testdata/triage/betterbird-review/unrelated-transform.js",
    "testdata/taxonomy/decompression/decompress.js",
]:
    check(Path(filename), {brotli: True}, filename.replace("/", "_"))
# test-rules evaluates each queried rule at the target type; file-scoped JS
# rules are checked on the actual member, while the archive hook spans files.
with tarfile.open(args.archive) as archive:
    member = archive.extractfile("package/index.js")
    index = args.work_dir / "index.js"
    index.write_bytes(member.read())
check(index, {crypto: True, packed: True, encrypted: True})
# The debug command projects symbols from its exact target. Test execution
# sinks on the real decoded source; normal atomscan pools decoded descendants.
source = index.read_text()
numbers = re.search(r"\[([0-9,]+)\]\.map", source).group(1)
shift = int(re.search(r'\.join\(""\),([0-9]+)\)', source).group(1))
stage = "".join(chr(int(number)) for number in numbers.split(","))
def unshift(match):
    c = match.group(0)
    origin = 65 if c <= "Z" else 97
    return chr((ord(c) - origin + shift) % 26 + origin)
stage = re.sub("[a-zA-Z]", unshift, stage)
decoded = args.work_dir / "decoded-loader.js"
decoded.write_text(stage)
check(decoded, {crypto: True, execute: True, brotli: True})
check(args.archive, {hook: True})
for index, sample in enumerate([args.dll_one, args.dll_two], 1):
    check(sample, {erase: True}, "dll-" + str(index))
    original = sample.read_bytes()
    # Removing any one of the signature/pointer writes must defeat erasure
    # recognition. The original executable bytes remain available as positives.
    variants = [
        bytes.fromhex("8B 45 08 8B 4D 08 03 48 3C 89 4D F8 8B 55 F8 C7 02 00 00 00 00 33 C0 8B 4D 08 66 89 01 8B 55 08 C7 42 3C 00 00 00 00"),
        bytes.fromhex("8B 4D 08 8B 55 08 03 51 3C 89 55 F8 8B 45 F8 C7 00 00 00 00 00 33 C9 8B 55 08 66 89 0A 8B 45 08 C7 40 3C 00 00 00 00"),
    ]
    signature = variants[index - 1]
    assert original.count(signature) >= 1
    for offset, length in [(15, 6), (26, 3), (32, 7)]:
        mutated = signature[:offset] + b"\x90" * length + signature[offset + length:]
        destination = args.work_dir / f"dll-{index}-missing-write-{offset}.dll"
        destination.write_bytes(original.replace(signature, mutated))
        check(destination, {erase: False})
with ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(lambda job: evaluate(*job), jobs))
print(json.dumps(sorted(results, key=lambda case: case["case"]), indent=2))
