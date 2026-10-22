#!/usr/bin/env python3
"""Static byte mutations and benign controls. Never executes any PE."""
import argparse
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CONNECT = 'micro-behaviors/communications/socket/connect::winsock-client-ordinal-api-set'
RUN = 'micro-behaviors/os/registry/write::x86-windows-logon-run-value-write'
PERSIST = 'objectives/persistence/login/registry/autostart::msmp-state-loader-windows-run-persistence'
DELETE = 'objectives/evasion/self-delete/file/script::x86-queried-path-retry-delete-formatter'
SCSI = 'micro-behaviors/fs/disk/raw::x86-scsi-write10-passthrough-setup'
ZIP = 'metadata/binary/resource/embedded-media::encrypted-zip-rsrc-pe'
FAMILY = 'well-known/malware/trojan/urelas::urelas-msmp-state-storage-profile'
FALLBACK = 'well-known/malware/trojan/urelas::urelas-complemented-state-loader'
RETIRED = {'well-known/malware/trojan/urelas::urelas-card-game-spy-loader',
           'well-known/malware/trojan/elex/worm/elex-loader::elex-golfupdate-remote-thread-injection'}


def patch(data, off, value):
    b = bytearray(data)
    struct.pack_into('<I', b, off, value)
    return bytes(b)


def documents(text):
    dec = json.JSONDecoder()
    while text.strip():
        obj, end = dec.raw_decode(text.lstrip())
        text = text.lstrip()[end:]
        yield obj


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sample', type=Path, required=True)
    ap.add_argument('--scratch-dir', type=Path, required=True)
    ap.add_argument('--fixtures-dir', type=Path, required=True)
    ap.add_argument('--cleave', default='cleave')
    args = ap.parse_args()
    original = args.sample.read_bytes()
    all_expected = {CONNECT, RUN, PERSIST, DELETE, SCSI, ZIP, FAMILY}
    cases = [('original', original, all_expected, {FALLBACK})]
    renamed = original
    for a, b in [('HGDraw.dll', 'Renamed.xx'), ('golfinfo.ini', 'abcdefgh.ini'),
                 ('golfset.ini', 'abcdefg.ini')]:
        a, b = a.encode('utf-16le'), b.encode('utf-16le')
        assert len(a) == len(b) and a in renamed
        renamed = renamed.replace(a, b)
    renamed = renamed.replace(b'_uinsey.bat', b'_rename.bat')
    cases.append(('renamed-artifacts', renamed, all_expected - {FAMILY} | {FALLBACK}, {FAMILY}))
    cases += [
        ('other-dll-owns-ordinals', patch(original, 0x35920+12, 0x3620a), {RUN, DELETE, SCSI, ZIP}, {CONNECT, FAMILY, PERSIST}),
        ('wrong-ordinal-lookup-pointer', patch(original, 0x35920, 0x35da5), {RUN, DELETE}, {CONNECT, FAMILY, PERSIST}),
        ('wrong-open-api', patch(original, 0x2057, 0x42b004), {CONNECT, DELETE}, {RUN, PERSIST}),
        ('wrong-write-api', patch(original, 0x2090, 0x42b004), {CONNECT, DELETE}, {RUN, PERSIST}),
        ('wrong-run-value-pointer', patch(original, 0x2089, 0x432f18), {CONNECT, DELETE}, {RUN, PERSIST}),
        ('different-query-buffer', patch(original, 0x33ab, 0x110), {CONNECT, RUN}, {DELETE}),
        ('different-delete-buffer', patch(original, 0x3483, 0x130), {CONNECT, RUN}, {DELETE}),
        ('wrong-delete-template', patch(original, 0x348c, 0x439551), {CONNECT, RUN}, {DELETE}),
    ]
    b = bytearray(original); b[0x207a] = 0x1c
    cases.append(('different-registry-handle', bytes(b), {CONNECT, DELETE}, {RUN, PERSIST}))
    b = bytearray(original); b[0x41d3] = 0x28
    cases.append(('scsi-read10-near-miss', bytes(b), {CONNECT, RUN, DELETE}, {SCSI}))
    b = original.replace(b'MSMP', b'ABCD')
    cases.append(('no-state-validation', b, {CONNECT, RUN, DELETE}, {FAMILY, FALLBACK, PERSIST}))
    b = bytearray(original); b[0x3f0d6] = 8
    cases.append(('unencrypted-resource', bytes(b), {CONNECT, RUN, DELETE}, {ZIP}))
    # Preserve every ZIP byte and section; remove only its resource-directory
    # membership. A signature in .text is not a resource by itself.
    import pefile
    pe = pefile.PE(data=original)
    pe.DIRECTORY_ENTRY_RESOURCE.entries[0].directory.entries[1].directory.entries[0].data.struct.OffsetToData = 0x3f000
    pe.DIRECTORY_ENTRY_RESOURCE.entries[0].directory.entries[1].directory.entries[0].data.struct.Size = 205
    b = pe.write()
    cases.append(('zip-outside-resource', b, {CONNECT, RUN, DELETE}, {ZIP}))
    spec = importlib.util.spec_from_file_location('inert', ROOT/'testdata/native-post-graft-review/run_cases.py')
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    literals = b'VirtualAllocEx\0WriteProcessMemory\0CreateRemoteThread\0AttachDllToProcess: CreateRemoteThread\0'
    for s in ['golfinfo.ini', 'golfset.ini', 'HGDraw.dll']:
        literals += s.encode('utf-16le') + b'\0\0'
    inert = bytes(mod.pe(b'\xc3', literals)) + b'\0'*32768
    cases.append(('inert-api-and-artifact-names', inert, set(), {FAMILY, FALLBACK, RUN, PERSIST, DELETE, SCSI}))
    fake_resource = mod.pe(b'\xc3', bytes.fromhex('50 4b 03 04 14 00 09 00 08 00'))
    fake_resource[0x1a0:0x1a8] = b'.rsrc\0\0\0'
    fake_resource.extend(b'\0'*4096)
    cases.append(('rsrc-label-without-resource-directory', bytes(fake_resource), set(), {ZIP, RUN, PERSIST, DELETE, FAMILY, FALLBACK}))
    # Valid ordinary Winsock client imports retain the existing notable signal;
    # a different library's identical ordinals must not acquire that signal.
    def ordinal_pe(owner):
        b = mod.pe(b'\xc3', b'')
        struct.pack_into('<II', b, 0x98+104, 0x2000, 40)
        struct.pack_into('<IIIII', b, 0x400, 0x20d0, 0, 0, 0x2080, 0x20d0)
        b[0x480:0x48b] = owner
        b[0x4a0:0x4ab] = b'WS2_32.dll\0'
        for i, n in enumerate([16,19,3,4,23]):
            struct.pack_into('<I', b, 0x4d0+i*4, 0x80000000 | n)
        return bytes(b)
    cases += [('ordinary-network-client', ordinal_pe(b'WS2_32.dll\0'), {CONNECT}, {RUN, PERSIST, DELETE, FAMILY, FALLBACK}),
              ('other-network-library', ordinal_pe(b'OTHERX.dll\0'), set(), {CONNECT, RUN, PERSIST, DELETE, FAMILY, FALLBACK})]
    with tempfile.TemporaryDirectory(dir=args.scratch_dir, prefix='controls-') as tmp:
        paths = []
        for name, data, _, _ in cases:
            p = Path(tmp)/(name+'.exe'); p.write_bytes(data); paths.append(p)
        fixtures = [p for p in args.fixtures_dir.iterdir() if not p.name.endswith('.json')]
        run = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--format', 'json',
                              *map(str, paths+fixtures)], capture_output=True, text=True)
        assert run.returncode == 0, run.stderr
        assert not any(x in run.stderr for x in ['Failed to load', 'skipped', 'failed to compile']), run.stderr
        reports = {Path(f['path']).name: f for d in documents(run.stdout) for f in d['files']}
        results = []
        for name, _, present, absent in cases:
            traits = reports[name+'.exe']['traits']; ids = {t['id'] for t in traits}
            assert present <= ids, (name, 'missing', present-ids)
            assert not (absent | RETIRED) & ids, (name, 'unexpected', (absent | RETIRED) & ids)
            if name in ['inert-api-and-artifact-names','ordinary-network-client','other-network-library']:
                assert not [t for t in traits if t['crit'] >= 4], (name, traits)
            results.append({'case': name, 'pass': True})
        for p in fixtures:
            ids = {t['id'] for t in reports[p.name]['traits']}
            expected = {PERSIST, 'well-known/malware/trojan/urelas::urelas-msmp-network-loader'}
            if p.name == 'run-relocated-value.exe':
                expected |= {ZIP, 'objectives/execution/payload/file-exec::self-deleting-complement-state-resource-loader'}
            assert expected <= ids, (p.name, expected-ids)
            results.append({'case': p.name, 'pass': True})
        print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
