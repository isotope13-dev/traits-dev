"""Check declaration binding, encoding variants, and manifest-name placement."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
ENGINE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
NO_CODE = 'metadata/package/runtime::android-manifest-no-dex-code'
SPLIT = 'metadata/package/files/mobile-package::android-manifest-config-split'
NO_EXTRACT = 'metadata/package/config::android-manifest-no-native-extraction'
NAME = 'metadata/file/naming::android-manifest-basename'
EXAMPLE = 'metadata/package/testing/presence/manifest::android-example-manifest'
DECLARATIONS = {NO_CODE, SPLIT, NO_EXTRACT}


def axml(root, root_attrs, child, child_attrs, utf8):
    """Build small AXML with string and typed boolean attributes."""
    strings = ['android', 'http://schemas.android.com/apk/res/android', root, child]
    for attrs in (root_attrs, child_attrs):
        for name, value in attrs:
            strings.extend([name, str(value).lower()])
    strings = list(dict.fromkeys(strings))
    index = {s: n for n, s in enumerate(strings)}
    pool, offsets = b'', []
    for s in strings:
        offsets.append(len(pool))
        if utf8:
            encoded = s.encode()
            assert len(encoded) < 128
            pool += bytes([len(s), len(encoded)]) + encoded + b'\0'
        else:
            pool += struct.pack('<H', len(s)) + s.encode('utf-16le') + b'\0\0'
    pool += b'\0' * (-len(pool) % 4)
    pool_start = 28 + 4 * len(strings)
    chunks = struct.pack('<HH6I', 1, 28, pool_start + len(pool), len(strings), 0,
                         0x100 if utf8 else 0, pool_start, 0)
    chunks += struct.pack('<' + 'I' * len(offsets), *offsets) + pool
    nil = 0xffffffff

    def namespace(kind):
        return struct.pack('<HH5I', kind, 16, 24, 0, nil, 0, 1)

    def start(element, attrs):
        records = b''
        for name, value in attrs:
            is_bool = isinstance(value, bool)
            raw = nil if is_bool else index[str(value).lower()]
            typed = int(value) if is_bool else raw
            records += struct.pack('<IIIHBBI', 1 if name not in ('split', 'package') else nil,
                                   index[name], raw, 8, 0, 0x12 if is_bool else 3, typed)
        return (struct.pack('<HH5I6H', 0x102, 16, 36 + len(records), 0, nil,
                            nil, index[element], 20, 20, len(attrs), 0, 0, 0) + records)

    def end(element):
        return struct.pack('<HH5I', 0x103, 16, 24, 0, nil, nil, index[element])

    chunks += namespace(0x100) + start(root, root_attrs) + start(child, child_attrs)
    chunks += end(child) + end(root) + namespace(0x101)
    return struct.pack('<HHI', 3, 8, 8 + len(chunks)) + chunks


def scan(path):
    result = subprocess.check_output([ENGINE, '--traits-dir', str(ROOT), '--min-crit', 'baseline', '--format', 'json',
                                      str(path)], env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    return json.loads(result)['files'][0]['traits']


cases = [
    ('language-utf16', 'manifest', [('split', 'config.en')], 'application',
     [('hasCode', False), ('extractNativeLibs', False)], False, DECLARATIONS),
    ('abi-utf8', 'manifest', [('split', 'config.arm64_v8a')], 'application',
     [('extractNativeLibs', False), ('hasCode', False)], True, DECLARATIONS),
    ('unrelated-false', 'manifest', [('split', 'feature')], 'application',
     [('hasCode', True), ('extractNativeLibs', True), ('enabled', False)], False, set()),
    ('wrong-element', 'manifest', [('label', 'config.en')], 'meta-data',
     [('hasCode', False), ('extractNativeLibs', False)], True, set()),
    ('layout', 'LinearLayout', [('split', 'config.en'), ('layout_width', 'match_parent'),
                              ('layout_height', 'match_parent')],
     'TextView', [('hasCode', False), ('extractNativeLibs', False)], False, set()),
]
with tempfile.TemporaryDirectory(prefix='android-manifest-check-') as temp:
    for label, root, root_attrs, child, child_attrs, utf8, expected in cases:
        path = Path(temp) / label / 'AndroidManifest.xml'
        path.parent.mkdir()
        path.write_bytes(axml(root, root_attrs, child, child_attrs, utf8))
        findings = scan(path)
        ids = {item['id'] for item in findings}
        assert ids & DECLARATIONS == expected, (label, ids & DECLARATIONS, expected)
        assert not any(item['crit'] >= 4 for item in findings), (label, findings)
    path = Path(temp) / 'examples' / 'AndroidManifest.xml'
    path.parent.mkdir()
    path.write_bytes(axml('manifest', [], 'application', [], False))
    # The emitted example composite requires the relocated filename atom.
    # JSON output can omit baseline constituents when notable traits match.
    assert EXAMPLE in {item['id'] for item in scan(path)}
print('Passed 6 AXML cases: UTF-8/UTF-16, reordered attributes, binding near misses, layout near miss, example context.')
