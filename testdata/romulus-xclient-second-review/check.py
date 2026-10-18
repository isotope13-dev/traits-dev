"""Static-only positive/near-miss controls; never loads or executes samples.

The binary controls retain the input PE's table layout. They remove individual
evidence roles, or provide an imported registry writer plus elevation command.
No generated file is a runnable repair of the damaged client.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DEFAULT_SAMPLES = Path('/usr/local/var/cyclotron/tmp.noindex/cyclotron-e321d729/samples')
DOS = 'objectives/impact/dos/http::managed-threaded-incomplete-post-tasking'
UAC = 'objectives/privilege-escalation/elevation-control/uac-bypass/hijack::exefile-isolated-command-hijack'
OBF = 'objectives/anti-static/obfuscation/eval/scripting/decode::powershell-transformed-scriptblock-invocation'
ARCHIVE = 'micro-behaviors/data/archive/extract/password::sevenzip-password-extraction'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--samples', type=Path, default=DEFAULT_SAMPLES)
    args = parser.parse_args()
    specimens = {
        'routeA': ('0c6560390592/romulus_routeA_stager.ps1', '0c6560390592bd01268248e443e0a9f5625e5670d25437a7e99c61b23ebbda3a'),
        'routeB': ('5177fc69c566/romulus_routeB_stager.ps1', '5177fc69c566f053b1cfe56a0f6a9c7b02d8d3ef4c0605c40fa7d7b51ad1fdc0'),
        'client': ('b524ba48c3f5/embedded_xclient.exe', 'b524ba48c3f5bdf83887d5420471ea503248249df75abd34270472f75b2d93be'),
    }
    paths = {}
    for name, (relative, digest) in specimens.items():
        path = args.samples / relative
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest, path
        paths[name] = path
    original = paths['client'].read_bytes()

    with tempfile.TemporaryDirectory(prefix='romulus-controls-') as directory:
        tmp = Path(directory)

        def control(name, data):
            path = tmp / (name + '.exe')
            path.write_bytes(data)
            paths[name] = path

        control('renamed-client', original)
        old, new = 'StartDDos'.encode('utf-16le'), 'StartTask'.encode('utf-16le')
        assert original.count(old) == 1
        control('without-task', original.replace(old, new))
        header = 'Content-length:'.encode('utf-16le')
        assert original.count(header) == 1
        control('without-body-header', original.replace(header, 'Content-header:'.encode('utf-16le')))
        fanout = re.search(rb'\x06\x25\xfe\x07...\x06\x73...\x0a\x73...\x0a', original, re.S)
        assert fanout, 'CIL thread fan-out not found'
        data = bytearray(original)
        data[fanout.start() + 2:fanout.start() + 4] = b'\x00\x00'
        control('without-thread-fanout', data)

        # Build a positive UAC constituent control without executing the PE.
        # Redirect its single name thunk to a new IMAGE_IMPORT_BY_NAME record.
        import dnfile
        pe = dnfile.dnPE(data=original)
        data = bytearray(original)
        record_rva = 0x2704  # Already zeroed entry method; not executable CIL.
        record_offset = pe.get_offset_from_rva(record_rva)
        record = b'\0\0RegSetValueExA\0'
        data[record_offset:record_offset + len(record)] = record
        descriptor = pe.DIRECTORY_ENTRY_IMPORT[0]
        for rva in (descriptor.struct.OriginalFirstThunk, descriptor.struct.FirstThunk):
            struct.pack_into('<I', data, pe.get_offset_from_rva(rva), record_rva)
        overlay = max(s.PointerToRawData + s.SizeOfRawData for s in pe.sections)
        command = b'sdclt.exe /KickOffElev\0'
        data[overlay:overlay + len(command)] = command
        control('uac-constituents', data)
        data[overlay:overlay + len(command)] = b'\0' * len(command)
        control('uac-without-trigger', data)

        fixtures = list(HERE.glob('*.ps1'))
        result = subprocess.run(
            [args.cleave, '--traits-dir', str(ROOT), '--json',
             *map(str, paths.values()), *map(str, fixtures)],
            text=True, capture_output=True, check=True, timeout=180,
        )
        reports = {}
        for line in result.stdout.splitlines():
            for item in json.loads(line)['files']:
                reports[item['path']] = item
        def traits(path):
            return reports[str(path)].get('traits', [])
        def ids(path):
            return {t['id'] for t in traits(path)}

        for name in ('routeA', 'routeB'):
            ts = traits(paths[name])
            assert not [t for t in ts if t['crit'] == 5], name
            assert [t['id'] for t in ts if t['crit'] == 4] == [OBF], name
        for name in ('client', 'renamed-client'):
            assert DOS in ids(paths[name]), name
            assert 'well-known/malware/rat/xworm::xworm-classic-command-set' in ids(paths[name]), name
            assert UAC not in ids(paths[name]), name
        for name in ('without-task', 'without-body-header', 'without-thread-fanout'):
            assert DOS not in ids(paths[name]), name
        assert UAC in ids(paths['uac-constituents'])
        assert UAC not in ids(paths['uac-without-trigger'])
        for path in fixtures:
            ts = traits(path)
            assert not [t for t in ts if t['crit'] == 5], path
            suspicious = [t['id'] for t in ts if t['crit'] == 4]
            assert suspicious == ([OBF] if path.stem == 'transformed-invocation' else []), (path, suspicious)
        assert ARCHIVE in ids(HERE / 'quoted-extraction.ps1')
        assert ARCHIVE not in ids(HERE / 'unrelated-password-flags.ps1')
        assert not any('self-delete' in t['id'] for t in traits(HERE / 'unrelated-delete.ps1'))
        print(f'Passed {len(paths) + len(fixtures)} static sample and near-miss controls.')


if __name__ == '__main__':
    main()
