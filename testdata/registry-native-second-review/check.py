#!/usr/bin/env python3
"""Byte-level admission and data-flow controls. Never executes a specimen."""
import argparse
import concurrent.futures
import importlib.util
import json
from pathlib import Path
import re
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
FIREFOX = 'objectives/credential-access/browser/firefox::packed-firefox-nss-login-decryptor'
CHROME = 'objectives/credential-access/browser/firefox::chrome-disguised-packed-firefox-decryptor'
FAMILY = 'well-known/malware/stealer/cosmicduke::packed-credential-stealer'
OLD_FAMILY = 'well-known/malware/stealer/cosmicduke::cosmicduke-builder-and-cipher-key'
STAGE = 'micro-behaviors/process/deploy/file-exec::x86-resource-buffer-stage-launch'
LOADER = 'objectives/execution/payload/file-exec::self-deleting-complement-state-resource-loader'
DELETE = 'objectives/evasion/self-delete/file/script::x86-module-path-retry-delete-batch'
RUN = 'micro-behaviors/os/registry/write::x86-windows-logon-run-value-write'
PERSIST = 'objectives/persistence/login/registry/autostart::msmp-state-loader-windows-run-persistence'
ZIP = 'metadata/binary/resource/embedded-media::encrypted-zip-rsrc-pe'
OLD_ZIP = 'micro-behaviors/data/embedded/payload/archive::encrypted-zip-rsrc-pe'


def replace(data, old, new):
    assert len(old) == len(new) and old in data
    return data.replace(old, new)


def patch(data, offset, value):
    result = bytearray(data)
    struct.pack_into('<I', result, offset, value)
    return bytes(result)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--samples-dir', type=Path, required=True)
    ap.add_argument('--scratch-dir', type=Path, required=True)
    ap.add_argument('--cleave', default='cleave')
    args = ap.parse_args()
    one = (args.samples_dir / '841e64fabd6d/no-family-corroboration.exe').read_bytes()
    two = (args.samples_dir / '30bb1fd1244c/no-chrome-identity.exe').read_bytes()
    three = (args.samples_dir / 'f6604fbf6ddd/run-hkey-near-miss.exe').read_bytes()
    cases = [
        ('no-family-evidence', one, {FIREFOX, CHROME}, {FAMILY}),
        ('no-chrome-evidence', two, {FIREFOX, FAMILY}, {CHROME}),
    ]
    for token in [b'NSS_Ini', b'SDR_Decrypt', b'select id, hostname, user']:
        changed = replace(two, token, b'X' * len(token))
        cases.append(('no-' + token[:6].decode().replace(' ', '_'), changed,
                      set(), {FIREFOX, CHROME, FAMILY}))
    match = re.search(rb'\x8b\x25....\x8b\x2d....\x8b\x0d....\x8b\x15....\x8b\x35....\x8b\x3d....\x8d\x05....\xff\xe0', two, re.DOTALL)
    assert match
    changed = bytearray(two)
    changed[match.end()-1] = 0xd0
    cases.append(('no-tail-handoff', bytes(changed), set(), {FIREFOX, FAMILY}))
    for token in [b'BotGenStudio', b'AdjustKernelTableFromSSDTSpace2']:
        cases.append(('one-corroborator-' + str(len(token)),
                      replace(two, token, b'X' * len(token)), {FIREFOX, FAMILY}, set()))
    # Reuse the existing non-executable two-section PE builder, then make its
    # code section UPX0 to exercise the family's actual matcher scope.
    spec = importlib.util.spec_from_file_location('controls', ROOT / 'testdata/native-post-graft-review/run_cases.py')
    controls = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(controls)
    inert = controls.pe(b'\xc3\0D:\\BotGenStudio\\bin\\bot.pdb\0AdjustKernelTableFromSSDTSpace2\0', b'')
    inert[0x178:0x180] = b'UPX0\0\0\0\0'
    inert.extend(b'\0' * (65536-len(inert)))
    cases.append(('inert-family-names', bytes(inert), set(), {FIREFOX, FAMILY, CHROME}))

    required = {STAGE, LOADER, DELETE, ZIP}
    cases.append(('loader-original', three, required, {RUN, PERSIST}))
    # Main flow starts at VA 0x40259a, raw offset 0x199a. Change relationships
    # rather than removing the file's unrelated resource and execution imports.
    stage = 0x199a
    cases += [
        ('different-launch-path', patch(three, stage+69, 0xfffffdcc), {ZIP, DELETE}, {STAGE, LOADER, RUN}),
        ('different-size-slot', patch(three, stage+28, 0xfffffdc4), {ZIP, DELETE}, {STAGE, LOADER, RUN}),
        ('unrelated-resource-call', patch(three, stage+11, 0), {ZIP, DELETE}, {STAGE, LOADER, RUN}),
        ('unrelated-preparation-call', patch(three, stage+41, 0), {ZIP, DELETE}, {STAGE, LOADER, RUN}),
        ('wrong-launch-api', patch(three, stage+78, 0x41c198), {ZIP, DELETE}, {STAGE, LOADER, RUN}),
        ('wrong-resource-api', patch(three, 0x1d74+27, 0x41c060), {ZIP, DELETE}, {STAGE, LOADER, RUN}),
        ('unrelated-store-call', patch(three, 0x1678+131, 0), {ZIP, DELETE}, {STAGE, LOADER, RUN}),
        ('wrong-write-api', patch(three, 0x7ffe+75, 0x41c070), {ZIP, DELETE}, {STAGE, LOADER, RUN}),
        ('without-encrypted-zip', replace(three, b'PK\x03\x04\x14\x00\x09\x00\x08\x00', b'PK\x03\x04\x14\x00\x08\x00\x08\x00'),
         {STAGE, DELETE}, {ZIP, LOADER, RUN}),
        ('without-state-magic', replace(three, b'MSMP', b'ABCD'), {STAGE, ZIP, DELETE}, {LOADER, RUN}),
        # The original opens into [ebp-0x1c40] but writes using [ebp-0x1c3c].
        ('corrected-run-handle', patch(three, 0x164c, 0xffffe3c0), required | {RUN, PERSIST}, set()),
    ]
    # The selected batch, helper, state and endpoint names cannot gate this.
    renamed = replace(three, b'_vslite.bat', b'_rename.bat')
    for old, new in [('HGDraw.dll', 'Rename.dll'), ('golfinfo.ini', 'abcdefgh.ini'), ('golfset.ini', 'abcdefg.ini')]:
        renamed = replace(renamed, old.encode('utf-16le'), new.encode('utf-16le'))
    cases.append(('renamed-artifacts', renamed, required, {RUN, PERSIST}))
    ordinal_ids = {
        4: 'micro-behaviors/communications/socket/connect::connect-api-ordinal',
        9: 'micro-behaviors/data/buffer/integer-codec::htons-api-ordinal',
        11: 'micro-behaviors/communications/ip/parse::inet-addr-api-ordinal',
        16: 'micro-behaviors/communications/socket/receive::recv-api-ordinal',
        19: 'micro-behaviors/communications/socket/send::send-api-ordinal',
        23: 'micro-behaviors/communications/socket/create::socket-api-ordinal',
        51: 'micro-behaviors/communications/dns/lookup::winsock-name-resolution-ordinal',
    }
    client = 'micro-behaviors/communications/socket/connect::winsock-client-ordinal-api-set'
    def ordinal_pe(owned, other):
        image = controls.pe(b'\xc3', b'')
        struct.pack_into('<II', image, 0x98+104, 0x2000, 60)
        for raw, thunk, name_rva, name, ordinals in [
            (0x400, 0x20d0, 0x2080, b'WS2_32.dll\0', owned),
            (0x414, 0x2120, 0x20a0, b'other.dll\0', other),
        ]:
            struct.pack_into('<IIIII', image, raw, thunk, 0, 0, name_rva, thunk)
            name_raw = 0x400+name_rva-0x2000
            image[name_raw:name_raw+len(name)] = name
            for n, ordinal in enumerate(ordinals):
                struct.pack_into('<I', image, 0x400+thunk-0x2000+n*4, 0x80000000 | ordinal)
        return bytes(image)
    all_ordinals = list(ordinal_ids)
    cases += [
        ('winsock-owned-ordinals', ordinal_pe(all_ordinals, [777]), set(ordinal_ids.values()) | {client}, set()),
        ('other-dll-ordinals', ordinal_pe([115], all_ordinals), set(), set(ordinal_ids.values()) | {client}),
        ('only-connect-owned', ordinal_pe([4], all_ordinals[1:]), {ordinal_ids[4]}, set(ordinal_ids.values()) - {ordinal_ids[4]} | {client}),
    ]
    tracked = {FIREFOX, CHROME, FAMILY, STAGE, LOADER, DELETE, RUN, PERSIST, ZIP} | set(ordinal_ids.values()) | {client}
    with tempfile.TemporaryDirectory(prefix='registry-native-', dir=args.scratch_dir) as temporary:
        def run(case):
            name, data, present, absent = case
            path = Path(temporary, name + '.exe')
            path.write_bytes(data)
            p = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--format', 'json', str(path)],
                               capture_output=True, text=True, check=True)
            assert not any(s in p.stderr for s in ['Failed to load traits', 'skipped', 'failed to compile']), p.stderr
            report = json.loads(p.stdout)
            ids = {t['id'] for f in report['files'] for t in f.get('traits', [])}
            assert present <= ids, (name, 'missing', present-ids)
            assert not absent & ids, (name, 'unexpected', absent & ids)
            assert not {OLD_FAMILY, OLD_ZIP} & ids
            if name == 'inert-family-names':
                high = [t for f in report['files'] for t in f.get('traits', []) if t['crit'] >= 4]
                assert not high, high
            return {'case': name, 'pass': True, 'tracked': sorted(ids & tracked)}
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            for result in pool.map(run, cases):
                print(json.dumps(result), flush=True)


if __name__ == '__main__':
    main()
