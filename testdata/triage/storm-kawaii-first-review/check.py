#!/usr/bin/env python3
"""Focused controls: check.py <managed-stage> <Action.dll> <scratch-dir>."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
LOADER = 'objectives/execution/payload/module-load::substituted-hex-reflective-assembly-loader'
TASK = 'objectives/command-and-control/remote-command/tasking::managed-security-control-task-plugin'
CRASH = 'objectives/impact/system/crash::managed-shutdown-privilege-hard-error'
OLD = {
    'objectives/command-and-control/dropper/staging/runtime::vbnet-embedded-native-temp-dropper',
    'objectives/command-and-control/dropper/staging/managed::dotnet-bitmap-invokemember-packed-loader',
    'objectives/command-and-control/dropper/staging/managed::dotnet-vb-bitmap-memory-reflective-stager',
    'objectives/anti-static/obfuscation/steganography/image::dotnet-red-channel-stego-reflective-loader',
}
managed, plugin, dest = map(Path, sys.argv[1:])
dest.mkdir(parents=True, exist_ok=True)


def scan(name, blob):
    path = dest / name
    path.write_bytes(blob)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(path)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
        capture_output=True, check=True)
    report = json.loads(result.stdout)
    return {t['id'] for f in report['files'] for t in f.get('traits', [])}


def replace_once(blob, source, target):
    assert len(source) == len(target)
    assert blob.count(source) == 1, (source, blob.count(source))
    return blob.replace(source, target, 1)


blob = managed.read_bytes()
ids = scan('arbitrary-name.exe', blob)
assert LOADER in ids and not OLD.intersection(ids)
print('PASS managed stage: activation, no false bitmap/native attribution', flush=True)
encoded_magic = 'XD|5A|9}'.encode('utf-16le')
negative = replace_once(blob, encoded_magic, 'XD|00|9}'.encode('utf-16le'))
assert LOADER not in scan('missing-encoded-magic.exe', negative)
print('PASS encoded payload magic is required', flush=True)
negative = replace_once(blob, b'InvokeMember\0', b'InvokXMember\0')
assert LOADER not in scan('missing-invocation.exe', negative)
print('PASS reflective activation evidence is required', flush=True)

blob = plugin.read_bytes()
ids = scan('arbitrary-plugin.dll', blob)
assert TASK in ids and CRASH in ids
print('PASS task dispatcher and explicit fatal-error calls', flush=True)
negative = replace_once(blob, 'RegUserinit'.encode('utf-16le'),
                        'RegUseriniX'.encode('utf-16le'))
ids = scan('missing-task-verb.dll', negative)
assert TASK not in ids and CRASH in ids
print('PASS task vocabulary and crash are independent', flush=True)
# Option six is NtRaiseHardError's shutdown response. Alter only that
# argument in the recovered IL sequence; API names remain unchanged.
# Resolve the token rather than assuming a metadata-table row number.
import re
matches = list(re.finditer(rb'\x16\x16\x7e....\x1c\x12.\x28', blob, re.S))
assert len(matches) == 1
index = matches[0].start() + 7
assert blob[index] == 0x1c
negative = blob[:index] + b'\x16' + blob[index + 1:]
ids = scan('nonfatal-error-option.dll', negative)
assert CRASH not in ids and TASK in ids
print('PASS API references alone cannot establish fatal error', flush=True)
