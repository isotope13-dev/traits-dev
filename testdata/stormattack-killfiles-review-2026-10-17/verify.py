"""Distinguish readable Chromium data from inaccessible-section stuffing."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
DECOY = 'objectives/anti-static/obfuscation/string/junking::chromium-decoy-stuffing'
HEADER = 'metadata/binary/layout/stub::upx-sections-without-early-magic'
TASKMGR = 'objectives/impact/degrade/application::autoit-disable-taskmgr-end-process'
REMOVED = 'objectives/anti-static/pack/upx::scrambled-upx-api-resolving-loader'
MARKERS = [b'example-cmdline.test', b'ui_test_utils::NavigateToURL',
           b'disabled-by-default-memory-infra', b'NotificationHelperMetrics']


def pe(sections, overlay=b''):
    """Small PE32 fixture with explicit file extents and memory access bits."""
    b = bytearray(0x400)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 0x3c, 0x80)
    b[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 0x84, 0x14c, len(sections), 0, 0, 0, 0xe0, 0x102)
    o = 0x98
    struct.pack_into('<H', b, o, 0x10b)
    struct.pack_into('<III', b, o + 16, 0x1000, 0x1000, 0x2000)
    struct.pack_into('<III', b, o + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<HH', b, o + 40, 4, 0)
    struct.pack_into('<HH', b, o + 48, 4, 0)
    struct.pack_into('<II', b, o + 56, (len(sections) + 1) * 0x1000, 0x400)
    struct.pack_into('<H', b, o + 68, 3)
    struct.pack_into('<IIIIII', b, o + 72, 0x100000, 0x1000, 0x100000, 0x1000, 0, 16)
    for i, (name, body, flags) in enumerate(sections):
        size = (len(body) + 0x1ff) & ~0x1ff
        at = len(b)
        struct.pack_into('<8sIIIIIIHHI', b, o + 0xe0 + i * 40,
                         name, len(body), (i + 1) * 0x1000, size, at, 0, 0, 0, 0, flags)
        b.extend(body.ljust(size, b'\0'))
    return bytes(b) + overlay


def main():
    readable, no_access = 0x40000040, 0
    text = (b'.text', b'\xc3' * 0x200, 0x60000020)
    corpus = b'\0'.join(MARKERS) + b'\0'
    cases = {
        'readable-chromium': (pe([text, (b'.rdata', corpus, readable)]), False),
        'inaccessible-chromium': (pe([text, (b'BlobData', corpus, no_access)]), True),
        'two-hidden-markers': (pe([text, (b'.rdata', corpus, readable),
                                    (b'BlobData', b'\0'.join(MARKERS[:2]), no_access)]), False),
        'overlay-only': (pe([text], corpus), False),
        'accessible-first-occurrences': (pe([text, (b'.rdata', corpus, readable),
                                            (b'BlobData', corpus, no_access)]), True),
        'upx-no-early-magic': (pe([(b'UPX0', b'\0' * 0x200, 0xe0000080),
                                   (b'UPX1', b'\xc3' * 0x200, 0xe0000040)]), False),
        'upx-with-early-magic': (pe([(b'UPX0', b'\0' * 0x200, 0xe0000080),
                                     (b'UPX1', b'UPX!' + b'\xc3' * 0x200, 0xe0000040)]), False),
    }
    cases.update({
        'taskmgr-disable': (b'ControlDisable ( "Windows Task Manager" , "" , "&End Process" )', False),
        'taskmgr-comment': (b'; ControlDisable ( "Windows Task Manager" , "" , "&End Process" )', False),
        'taskmgr-enable': (b'ControlEnable ( "Windows Task Manager" , "" , "&End Process" )', False),
        'ordinary-control-disable': (b'ControlDisable ( "My Application" , "" , "&End Process" )', False),
    })
    with tempfile.TemporaryDirectory(prefix='chromium-controls-', dir=ROOT / 'testdata') as tmp:
        paths = []
        for name, (data, _) in cases.items():
            p = Path(tmp) / (name + ('.exe' if data[:2] == b'MZ' else '.txt'))
            p.write_bytes(data)
            paths.append(str(p))
        cmd = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'jsonl', *paths]
        run = subprocess.run(cmd, text=True, capture_output=True, check=True)
        documents = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
        files = [f for doc in documents for f in doc.get('files', [doc])]
        data = documents
        results = []
        for f in files:
            name = Path(f['path']).stem
            if name not in cases:
                continue
            traits = {t['id']: t for t in f.get('findings', f.get('traits', []))}
            expected = cases[name][1]
            assert (DECOY in traits) == expected, (name, expected, list(traits))
            assert REMOVED not in traits, name
            assert (TASKMGR in traits) == (name == 'taskmgr-disable'), name
            if name.startswith('upx-'):
                assert (HEADER in traits) == (name == 'upx-no-early-magic'), name
                if HEADER in traits:
                    assert traits[HEADER]['crit'] in ['notable', 3], traits[HEADER]
            results.append({'case': name, 'decoy': expected, 'passed': True})
        assert len(results) == len(cases), (len(results), str(data)[:200])
        print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
