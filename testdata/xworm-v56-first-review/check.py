#!/usr/bin/env python3
"""Check static matcher controls; never execute the specimen or its CIL."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLIP = 'objectives/impact/crypto-manipulation/clipboard::managed-wallet-regex-clipboard-replacement'
HOSTILE = 'objectives/impact/crypto-manipulation/clipboard::managed-backdoor-wallet-clipboard-replacement'
REPORT = 'micro-behaviors/communications/messaging/send::managed-telegram-host-report-construction'
SHA = '53e2f4a1c8fb9fb860718f2ce08381e2b0d70310018055f4d1382a4674a13af3'


def variants(blob):
    result = {'original.exe': (blob, True, True)}
    for name, old, new in [
        ('no-write', b'SetText\0', b'GetText\0'),
        ('no-listener', b'AddClipboardFormatListener\0', b'BadClipboardFormatListener\0'),
    ]:
        assert old in blob and len(old) == len(new)
        result[name + '.exe'] = (blob.replace(old, new), False, True)
    changed = blob
    for old, new in [('\\b(bc1|[13])', '\\b(foo|[ab])'), ('\\b(0x)', '\\b(xx)')]:
        assert old.encode('utf-16le') in changed
        changed = changed.replace(old.encode('utf-16le'), new.encode('utf-16le'))
    result['no-wallet-patterns.exe'] = (changed, False, True)
    # Same CIL pattern as the rule, with field-token relations intact.
    swap = re.compile(
        rb'\x7e...\x04\x7e...\x04\x6f...\x0a\x2d.'
        rb'\x7e...\x04\x7e...\x04\x7e...\x04\x6f...\x0a'
        rb'[\x0a-\x0d][\x06-\x09]\x28...\x0a\x28...\x06', re.S)
    matches = list(swap.finditer(blob))
    assert len(matches) == 3
    changed = bytearray(blob)
    for match in matches:
        # Change replacement target without changing its preceding Contains test.
        changed[match.start() + 28] ^= 0x01
    result['different-destination.exe'] = (bytes(changed), False, True)
    changed = bytearray(blob)
    position = blob.index(b'currentClipboard')
    changed[position + len(b'current') - 1] = 0
    result['standalone-type-name.exe'] = (bytes(changed), True, True)
    for name, old, new in [
        ('no-user-getter', b'get_UserName\0', b'get_TypeName\0'),
        ('no-os-getter', b'get_OSFullName\0', b'get_XXFullName\0'),
        ('no-text-carrier', '&text='.encode('utf-16le'), '&xxxx='.encode('utf-16le')),
    ]:
        assert old in blob and len(old) == len(new)
        result[name + '.exe'] = (blob.replace(old, new), True, False)
    request = list(re.finditer(
        rb'\x11.\x1b[\x06-\x09]\xa2\x11.\x28...\x0a\x6f...\x0a\x26', blob, re.S))
    assert len(request) == 1
    for name, offset, value in [('unrelated-report-local', 3, 7), ('no-client-call', 12, 0x28)]:
        changed = bytearray(blob)
        changed[request[0].start() + offset] = value
        result[name + '.exe'] = (bytes(changed), True, False)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('sample', type=Path)
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    blob = args.sample.read_bytes()
    assert hashlib.sha256(blob).hexdigest() == SHA
    cases = variants(blob)
    with tempfile.TemporaryDirectory(dir=args.scratch, prefix='xworm-static-') as tmp:
        paths = []
        expected = {}
        for name, (content, clip, report) in cases.items():
            path = Path(tmp) / name
            path.write_bytes(content)
            paths.append(path)
            expected[str(path)] = (clip, report)
        for name in ['clipboard-manager.exe', 'clipboard-keylogger.exe']:
            path = ROOT / 'testdata/stranded-additional-behaviors' / name
            paths.append(path)
            expected[str(path)] = (False, False)
        run = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--json', *map(str, paths)],
                             capture_output=True, text=True)
        assert run.returncode in (0, 1), run.stderr
        assert not run.stderr.strip(), run.stderr
        reports = {}
        # Unicode NEL in binary evidence is not a JSONL separator.
        for line in run.stdout.split('\n'):
            if line:
                for file in json.loads(line)['files']:
                    reports[file['path']] = {t['id'] for t in file.get('traits', [])}
        for path, (clip, report) in expected.items():
            got = reports[path]
            assert (CLIP in got) == clip, path
            assert (HOSTILE in got) == clip, path
            assert (REPORT in got) == report, path
        print(f'{len(expected) * 3} assertions passed across {len(expected)} static controls')


if __name__ == '__main__':
    main()
