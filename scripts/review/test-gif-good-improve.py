#!/usr/bin/env python3
"""Static archive-parity, stage-delay and neutral-format regression controls.

Requires the recovered sample work directory recorded by GIF triage. Samples
are only read, modified, archived and scanned; no sample code is executed.
"""
import argparse
import io
import json
import os
from pathlib import Path
import struct
import subprocess
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
FAMILY = 'well-known/malware/rat/miniduke::command-backdoor'
SOCKET = 'objectives/execution/payload/image-map::encrypted-socket-buffer-execution'
MASK = 'objectives/evasion/masquerade/image::gif-conceals-xor-pe'
DELAY = 'objectives/anti-analysis/timing/evasion::repeated-buffer-transform-before-transfer'
NRV = 'metadata/encoded-payload/nrv2b-8'


def objects(text):
    decoder = json.JSONDecoder()
    offset = 0
    while offset < len(text):
        while offset < len(text) and text[offset].isspace():
            offset += 1
        if offset == len(text):
            break
        value, offset = decoder.raw_decode(text, offset)
        yield value


def zip_bytes(data, member='images/cache.dat'):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(member, data)
    return out.getvalue()


def tar_bytes(data, member='images/cache.dat'):
    out = io.BytesIO()
    with tarfile.open(fileobj=out, mode='w:gz') as archive:
        info = tarfile.TarInfo(member)
        info.size = len(data)
        archive.addfile(info, io.BytesIO(data))
    return out.getvalue()


def literal_nrv(data):
    """Literal-only NRV2B-8 control stream, followed by its end marker."""
    out = bytearray()
    count = flag = 0

    def bit(value):
        nonlocal count, flag
        if count == 0:
            flag = len(out)
            out.append(0)
        out[flag] |= value << (7 - count)
        count = (count + 1) % 8

    for byte in data:
        bit(1)
        out.append(byte)
    bit(0)
    for shift in reversed(range(24)):
        bit((0x1000002 >> shift) & 1)
        bit(int(shift == 0))
    out.append(0xff)
    return bytes(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--triage-work', required=True, type=Path)
    parser.add_argument('--work-dir', required=True, type=Path)
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    samples = args.work_dir / 'controls'
    samples.mkdir(exist_ok=True)
    cases = {}

    def add(name, data, required=(), forbidden=(), neutral=False):
        cases[name] = dict(required=list(required), forbidden=list(forbidden), neutral=neutral)
        (samples / name).write_bytes(data)

    rows = [r for r in json.loads((args.triage_work / 'decoded-payloads.json').read_text())
            if r['period'] == 8]
    big = None
    for row in rows:
        pe = Path(row['path']).read_bytes()
        name = row['source_sha256'][:12]
        second = SOCKET if len(pe) < 20000 else FAMILY
        observations = [second]
        if second == FAMILY:
            big = pe
            observations += [DELAY,
                             'micro-behaviors/process/enumerate/psapi::psapi-enumeration-api-profile',
                             'micro-behaviors/process/enumerate/psapi::psapi-library-api-name-profile']
        else:
            observations += ['micro-behaviors/crypto/provider/cryptoapi::capi-key-setup-api-profile',
                             'micro-behaviors/crypto/provider/cryptoapi::capi-buffer-crypto-api-reference',
                             'micro-behaviors/crypto/provider/cryptoapi::capi-key-buffer-api-profile',
                             'micro-behaviors/crypto/provider/cryptoapi::capi-hash-decrypt-api-profile']
        add(name + '-direct.exe', pe, observations)
        add(name + '-member.zip', zip_bytes(pe), observations)
        add(name + '-member.tar.gz', tar_bytes(pe), observations)
        add(name + '-nested.zip', zip_bytes(tar_bytes(pe), 'assets/images.tar.gz'), observations)
    relocations = json.loads((args.triage_work / 'relocations.json').read_text())
    for row in relocations:
        data = Path(row['target']).read_bytes()
        second = SOCKET if len(data) < 20000 else FAMILY
        add(row['sha256'][:12] + '-carrier.zip', zip_bytes(data), [MASK, second])

    assert big is not None
    counter = bytes.fromhex('817de420a10700')
    transfer = bytes.fromhex('8d05d0784400ffe0')
    assert big.count(counter) == big.count(transfer) == 1
    add('count-threshold-variant.exe', big.replace(counter, bytes.fromhex('817de4') + struct.pack('<I', 20000)), [DELAY])
    add('short-count.exe', big.replace(counter, bytes.fromhex('817de4') + struct.pack('<I', 3)), forbidden=[DELAY])
    add('different-transfer-buffer.exe', big.replace(transfer, bytes.fromhex('8d05d1784400ffe0')), forbidden=[DELAY])
    add('different-counter-slot.exe', big.replace(counter, bytes.fromhex('817de020a10700')), forbidden=[DELAY])
    invalid_call = bytearray(big)
    loop_start = big.index(counter) - 18
    struct.pack_into('<i', invalid_call, loop_start + 47, 0x7f000000)
    add('transform-target-outside-code.exe', bytes(invalid_call), forbidden=[DELAY])
    # Remove execute permission from the .data section holding the output.
    nonexec = bytearray(big)
    pe_offset = struct.unpack_from('<I', nonexec, 0x3c)[0]
    sections = struct.unpack_from('<H', nonexec, pe_offset + 6)[0]
    opt_size = struct.unpack_from('<H', nonexec, pe_offset + 20)[0]
    for index in range(sections):
        at = pe_offset + 24 + opt_size + index * 40
        address = struct.unpack_from('<I', nonexec, at + 12)[0]
        size = struct.unpack_from('<I', nonexec, at + 8)[0]
        if address <= 0x478d0 < address + size:
            flags = struct.unpack_from('<I', nonexec, at + 36)[0]
            struct.pack_into('<I', nonexec, at + 36, flags & ~0x20000000)
    add('output-not-executable.exe', bytes(nonexec), forbidden=[DELAY])

    benign = (ROOT.parent / 'cleave/src/extractors/testdata/hex-rc4-benign-pe.bin').read_bytes()
    packed = literal_nrv(benign)
    benign_packed = benign + struct.pack('<I', len(packed)) + packed
    add('neutral-packed.exe', benign_packed, [NRV], neutral=True)
    add('neutral-packed.zip', zip_bytes(benign_packed), [NRV], neutral=True)
    add('neutral-packed.tar.gz', tar_bytes(benign_packed), [NRV], neutral=True)
    add('neutral-plain.exe', benign, forbidden=[NRV, DELAY], neutral=True)

    env = {**os.environ, 'CLEAVE_TRAITS_DIR': str(ROOT), 'SCAN_NO_ANALYSIS_CACHE': '1',
           'FILEFACTS_CACHE': '0', 'STNG_STRING_CACHE': '0', 'CLEAVE_SKIP_CACHE': '1'}
    proc = subprocess.run([os.environ.get('ATOMSCAN', str(ROOT.parent / 'scan/target/release/atomscan')),
                           '--no-update', '--analyze', 'local', '--mode', 'slow', '--follow=none',
                           '--format=json', str(samples)], text=True, capture_output=True, env=env, timeout=300)
    (args.work_dir / 'scan.log').write_text(proc.stderr)
    assert proc.returncode in (0, 1), proc.stderr
    assert 'could not parse' not in proc.stderr and 'skipped ' not in proc.stderr, proc.stderr
    found = {}
    summaries = []
    for result in objects(proc.stdout):
        files = result.get('raw', {}).get('files', [])
        if not files:
            continue
        root = files[0]
        name = Path(root['path']).name
        if name not in cases:
            continue
        found[name] = root
        summaries.append({'name': name, 'traits': root.get('traits', []),
                          'children': [{'path': f['path'], 'type': f['type']} for f in files[1:]]})
    checks = []
    for name, case in cases.items():
        assert name in found, name
        traits = found[name].get('traits', [])
        ids = {t['id'] for t in traits}
        checks.append({'case': name, 'missing': sorted(set(case['required']) - ids),
                       'unexpected': sorted(set(case['forbidden']) & ids),
                       'unexpected_flags': [t['id'] for t in traits if t.get('crit', 0) >= 4] if case['neutral'] else []})
    (args.work_dir / 'checks.json').write_text(json.dumps(checks, indent=2))
    (args.work_dir / 'summaries.json').write_text(json.dumps(summaries, indent=2))
    failures = [c for c in checks if c['missing'] or c['unexpected'] or c['unexpected_flags']]
    assert not failures, json.dumps(failures, indent=2)
    print(f'{len(checks)} static GIF improvement controls passed')


if __name__ == '__main__':
    main()
