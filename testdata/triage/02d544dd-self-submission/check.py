"""Check the real sample, key variation, and negative decoder/identity controls."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
DECODER = 'micro-behaviors/data/decode/xor::x86-unrolled-byte-xor-to-stack'
CLR = 'micro-behaviors/process/interpreter/runtime/clr::clr-metahost-interface-guids'
IDENTITY = 'well-known/dual-use/transfer/rifaien::rifaien-self-submission-utility'
UPLOAD = 'micro-behaviors/communications/http/upload::module-path-multipart-upload-references'
FAILURE = 'metadata/binary/layout/compression::upx-decompression-failed'
OLD = {
    'anti-static/packer/upx/decompression-failed',
    'well-known/malware/worm/snojan::snojan-self-upload-worm',
    'objectives/exfiltration/http/upload::self-image-http-upload',
}
# Unrolled byte XORs. Vary the key independently of the load/store layout.
XOR = re.compile(rb'\x80[\xf1\xf2](.)', re.DOTALL)


def main():
    source = Path(sys.argv[1]).read_bytes()
    embedded = source.index(b'MZ', 512)
    # Restrict mutations to the recovered decoder's original on-disk bytes.
    begin = embedded + 0x1650 - 0xc00
    end = embedded + 0x17d5 - 0xc00
    decoder = source[begin:end]
    assert len(list(XOR.finditer(decoder))) >= 28
    changed = XOR.sub(lambda m: m[0][:2] + bytes([m[1][0] ^ 0x69]), decoder)
    no_xor = XOR.sub(lambda m: b'\x80' + bytes([m[0][1] - 0x28]) + m[1], decoder)
    # /6 XOR becomes /1 OR, preserving instruction sizes and other bytes.
    controls = {
        'original.exe': source,
        'changed-keys.exe': source[:begin] + changed + source[end:],
        'no-xor.exe': source[:begin] + no_xor + source[end:],
        'other-banner.exe': source.replace(b'rifaien yanje', b'utility yanje'),
        'other-guid.exe': source.replace(bytes.fromhex('8d1880928e0e6748b30c7fa83884e8de'), bytes(16)),
        'plain.exe': (ROOT / 'testdata/triage-sighted/plain.exe').read_bytes(),
    }
    with tempfile.TemporaryDirectory(prefix='submission-controls-') as scratch:
        paths = []
        for name, content in controls.items():
            path = Path(scratch) / name
            path.write_bytes(content)
            paths.append(str(path))
        process = subprocess.run([
            os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
            '--format', 'json', *paths,
        ], capture_output=True, text=True, check=True)
        reports = {}
        decoder_json = json.JSONDecoder()
        output = process.stdout.strip()
        while output:
            item, stop = decoder_json.raw_decode(output)
            for report in item['files']:
                reports[Path(report['path']).name] = {
                    trait['id']: trait for trait in report['traits']
                }
            output = output[stop:].strip()
    for name in controls:
        traits = reports[name]
        assert not OLD.intersection(traits), (name, OLD.intersection(traits))
        if name == 'plain.exe':
            assert not {DECODER, CLR, IDENTITY, UPLOAD, FAILURE}.intersection(traits)
            continue
        assert UPLOAD in traits, name
        assert FAILURE in traits and traits[FAILURE]['crit'] == 3, name
        assert (DECODER in traits) == (name != 'no-xor.exe'), name
        assert (CLR in traits) == (name != 'other-guid.exe'), name
        assert (IDENTITY in traits) == (name != 'other-banner.exe'), name
        assert not [t for t in traits.values() if t['crit'] == 5], name
    print(json.dumps({'cases': len(controls), 'failures': []}, indent=2))


if __name__ == '__main__':
    main()
