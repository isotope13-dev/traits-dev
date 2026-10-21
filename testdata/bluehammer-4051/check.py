#!/usr/bin/env python3
"""Check BlueHammer source reconstructions and independent benign boundaries."""
import argparse
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
RACE = 'objectives/privilege-escalation/exploit/race-condition::defender-update-sam-link-race'
SWAP = 'objectives/credential-access/registry::offline-sam-read-password-replacement'
HTTP = 'micro-behaviors/communications/http/client/initialize::viem-http-rpc-transport'
URLS = 'micro-behaviors/communications/http/url/rpc::multiple-rpc-provider-urls'

# Materialize controls in the cleave fixture tree supplied by the caller.
# Keep the recipe here so a clean cleave checkout can reproduce the checks.
CONTROLS = {
    'updater.py': '''def update(rpc, kernel, staged, done, ov):
    uuid = "c503f532-443a-4c69-8300-ccd1fbdb3839"
    endpoint = "IMpService77BDAF73-B396-481F-9042-AD358843EC24"
    kernel.DeviceIoControl(staged, 0x90008, None, 0, None, 0, done, ov)
    rpc.RpcStringBindingComposeW(uuid, "ncalrpc", None, endpoint, None, None)
''',
    'offline-backup.py': r'''def inspect(offreg, file, hive, key, data, size):
    path = r"C:\Windows\System32\config\SAM"
    offreg.OROpenHiveByHandle(file, hive)
    offreg.OROpenKey(hive, r"SAM\Domains\Account\Users\000003E9", key)
    offreg.ORGetValue(key, None, "V", None, data, size)
''',
    'password-change.py': '''def change(samlib, user, old_hash, new_hash):
    return samlib.SamiChangePasswordUser(user, old_hash, new_hash)
''',
    'prose.py': r'''# DeviceIoControl(staged, 0x90008, 0, 0, 0, 0, 0, 0)
# NtCreateSymbolicLinkObject and WDUpdateDirectory.
# c503f532-443a-4c69-8300-ccd1fbdb3839
# IMpService77BDAF73-B396-481F-9042-AD358843EC24
# C:\Windows\System32\config\SAM
# SAM\Domains\Account\Users
# OROpenHiveByHandle(file, hive), ORGetValue(key, 0, "V", 0, data, size)
# SamiChangePasswordUser(user, old_hash, new_hash)
pass
''',
    'wrong-control-code.py': r'''def io(kernel, nt, h, attrs, target):
    uuid = "c503f532-443a-4c69-8300-ccd1fbdb3839"
    endpoint = "IMpService77BDAF73-B396-481F-9042-AD358843EC24"
    name = "WDUpdateDirectory"
    path = r"C:\Windows\System32\config\SAM"
    kernel.DeviceIoControl(h, 0x90018, None, 0, None, 0, None, None)
    nt.NtCreateSymbolicLinkObject(None, 0x10000000, attrs, target)
''',
    'rpc-http-placement.js': '''const config = { transport: http(rpcUrl) };
const rpc = ['https://one.example.test', 'https://two.example.test'];
''',
    'rpc-http-nearmiss.js': '''const config = { transport: http(cacheDirectory) };
const pages = ['https://one.example.test', 'https://two.example.test'];
''',
}
CONTROLS['unused-numeric-code.py'] = CONTROLS['wrong-control-code.py'].replace(
    '0x90018', '17').replace('    uuid =', '    unrelated_constant = 0x90008\n    uuid =')


def decode_stream(text):
    decoder = json.JSONDecoder()
    position = 0
    while position < len(text):
        if text[position].isspace():
            position += 1
            continue
        value, position = decoder.raw_decode(text, position)
        yield value


def scan(cleave, path):
    result = subprocess.run([cleave, '--traits-dir', str(ROOT), '--format', 'json',
                             str(path)], capture_output=True, text=True, check=True)
    for report in decode_stream(result.stdout):
        yield from report.get('files', [])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--samples', type=Path, required=True)
    parser.add_argument('--fixtures', type=Path, required=True)
    args = parser.parse_args()
    args.fixtures.mkdir(parents=True, exist_ok=True)
    for name, source in CONTROLS.items():
        (args.fixtures / name).write_text(source)
    samples = list(scan(args.cleave, args.samples))
    assert len(samples) == 3, len(samples)
    results = []
    for file in samples:
        traits = {t['id']: t for t in file.get('traits', [])}
        assert traits[RACE]['crit'] == 5, file['path']
        assert traits[SWAP]['crit'] == 5, file['path']
        hostile = [t['id'] for t in traits.values() if t['crit'] == 5]
        assert len(hostile) >= 2, file['path']
        results.append({'file': Path(file['path']).name, 'hostile': hostile})
    controls = list(scan(args.cleave, args.fixtures))
    assert len(controls) == 8, len(controls)
    for file in controls:
        traits = {t['id']: t for t in file.get('traits', [])}
        assert not [t for t in traits.values() if t['crit'] >= 4], file['path']
        if Path(file['path']).name == 'rpc-http-placement.js':
            assert HTTP in traits and URLS in traits, file['path']
        if Path(file['path']).name == 'rpc-http-nearmiss.js':
            assert HTTP not in traits and URLS not in traits, file['path']
    print(json.dumps({'samples': results, 'controls_passed': len(controls)}, indent=2))


if __name__ == '__main__':
    main()
