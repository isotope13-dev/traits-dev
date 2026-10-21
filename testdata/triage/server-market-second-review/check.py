"""Inert EA06 format and custom configuration controls; never run specimens."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess

from autoit_ripper import extract
from autoit_ripper.autoit_unpack import EA05_MAGIC
from autoit_ripper.utils import EA06Decryptor, crc_data

ROOT = Path(__file__).resolve().parents[3]
OLD = {
    'objectives/anti-static/obfuscation/payload/data-file::autoit-ea06-encrypted-ciphertext-blob',
    'objectives/command-and-control/dropper/staging/encrypted::encrypted-autoit-ea06-high-entropy-file',
    'objectives/command-and-control/dropper/staging/encrypted::autoit-a3x-encrypted-script-drop-stage',
}
HIGH = 'metadata/file/entropy::ea06-marker-high-entropy-data'
PEAK = 'metadata/file/entropy::ea06-marker-sustained-peak-entropy-data'
LARGE = 'metadata/lang/compiled::large-a3x-ea06-marker-data'
CONFIG = 'objectives/anti-static/obfuscation/encoding/arithmetic::nested-offset120-executable-config'
MAGIC = 'metadata/lang/compiled::autoit-ea06-magic-reference'


def token(opcode, value):
    return bytes([opcode]) + struct.pack('<I', len(value)) + b''.join(
        struct.pack('<H', ord(c) ^ len(value)) for c in value)


def benign_ea06():
    # A valid, non-compressed EA06 record: an inert variable and console output.
    literal = ''.join(hashlib.sha256(str(i).encode()).hexdigest() for i in range(700))
    tokens = (struct.pack('<I', 2) + token(0x33, 'reference') + b'\x41'
              + token(0x36, literal) + b'\x7f'
              + token(0x31, 'ConsoleWrite') + b'\x47'
              + token(0x36, 'format control') + b'\x48\x7f')
    d = EA06Decryptor()
    def string(s, keys):
        return struct.pack('<I', len(s) ^ keys[0]) + d.decrypt(s.encode('utf-16le'), len(s) + keys[1])
    data = (EA05_MAGIC + b'EA06' + bytes(16)
            + d.decrypt(b'FILE', d.au3_ResType)
            + string('>>>AUTOIT SCRIPT<<<', d.au3_ResSubType)
            + string('reference.au3', d.au3_ResName)
            + struct.pack('<BIII', 0, len(tokens) ^ d.au3_ResSize,
                          len(tokens) ^ d.au3_ResSize, crc_data(tokens) ^ d.au3_ResCrcCompressed)
            + bytes(16) + d.decrypt(tokens, d.au3_ResContent) + b'AU3!EA06')
    decoded = extract(data)
    assert decoded and decoded[0][1].decode().endswith('ConsoleWrite ( "format control" )\r\n')
    assert 'DllCall' not in decoded[0][1].decode()
    return data


def shifted(s):
    return bytes((b + 120) % 256 for b in s.encode())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--before', action='store_true')
    args = parser.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    benign = benign_ea06()
    config = bytes(128) + b'\\@/' + shifted('4\\@/T\\@/Service\\@/worker.exe\\@/0\\@/0') + b'\\@/none\\@/' + bytes(128)
    cases = [
        ('ordinary.bin', benign, {MAGIC, HIGH, PEAK}, {LARGE, CONFIG}),
        # The engine currently does not route opaque .a3x to data.
        ('ordinary.a3x', benign, set(), {MAGIC, HIGH, PEAK, LARGE, CONFIG}),
        ('bare-marker.bin', bytes(128) + b'AU3!EA06' + bytes(128),
         {'metadata/lang/compiled::autoit-ea06-magic-in-data'}, {HIGH, PEAK, LARGE, CONFIG}),
        ('nested-config.bin', config, {CONFIG}, {MAGIC, HIGH, PEAK, LARGE}),
        ('renamed-fields.bin', config.replace(shifted('worker.exe'), shifted('agent.exe')), {CONFIG}, set()),
        ('no-executable.bin', config.replace(shifted('.exe'), shifted('.txt')), set(), {CONFIG}),
        ('no-frame.bin', config.replace(b'\\@/', b'---'), set(), {CONFIG}),
        ('unencoded.bin', b'\\@/4\\@/T\\@/Service\\@/worker.exe\\@/0', set(), {CONFIG}),
    ]
    paths = []
    for name, data, _, _ in cases:
        path = args.scratch / name
        path.write_bytes(data)
        paths.append(str(path))
    p = subprocess.run(['cleave', '--traits-dir', str(ROOT), '--format', 'json', 'analyze', *paths],
                       capture_output=True, text=True, check=True)
    remaining = p.stdout
    files = {}
    decoder = json.JSONDecoder()
    while remaining.strip():
        report, offset = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[offset:]
        files.update({Path(f['path']).name: f for f in report['files']})
    results = []
    for name, _, yes, no in cases:
        traits = {t['id']: t['crit'] for t in files[name].get('traits', [])}
        if args.before:
            results.append({'case': name, 'old_hostile': sorted(OLD & traits.keys())})
        else:
            assert yes <= traits.keys(), (name, 'missing', yes - traits.keys())
            assert not (no | OLD) & traits.keys(), (name, 'unexpected', (no | OLD) & traits.keys())
            if name.startswith('ordinary'):
                assert all(crit < 4 for crit in traits.values()), (name, traits)
            results.append({'case': name, 'passed': True})
    (args.scratch / ('before.json' if args.before else 'after.json')).write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
