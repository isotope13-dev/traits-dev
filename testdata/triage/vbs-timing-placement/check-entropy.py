#!/usr/bin/env python3
"""Keep real low-entropy PE coverage across resource-parser fallback."""
import argparse
import importlib.util
import json
from pathlib import Path
import struct
import subprocess

root = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('controls', root / 'testdata/taxonomy/reasoned-loader-review/check.py')
controls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controls)
parser = argparse.ArgumentParser()
parser.add_argument('--output-dir', required=True)
args = parser.parse_args()
out = Path(args.output_dir)
out.mkdir(parents=True, exist_ok=True)
ids = {
 'metadata/binary/code/entropy::code-entropy-near-zero',
 'metadata/binary/resource/size::oversized-low-entropy-rsrc',
 'metadata/binary/section/entropy::large-near-constant-rsrc-section',
 'metadata/binary/section/entropy::low-entropy-pe-resource-section',
}
for malformed in [False, True]:
    for low in [False, True]:
        code = bytes(65536) if low else bytes(range(256)) * 256
        resource = bytes(1048576) if low else bytes(range(256)) * 4096
        data = bytearray(controls.pe(code, resource))
        if malformed:
            # A resource-directory size rejected by the main parser, with
            # perfectly in-bounds section data whose entropy remains measurable.
            struct.pack_into('<II', data, 0x118 + 96 + 2 * 8, 0x12000, 0x1503200)
        path = out / f'low-{low}-malformed-{malformed}.exe'
        path.write_bytes(data)
        proc = subprocess.run(['cleave', '--traits-dir', str(root), '--format', 'json', str(path)],
                              capture_output=True, text=True, check=True)
        traits = json.loads(proc.stdout)['files'][0]['traits']
        found = {t['id'] for t in traits} & ids
        assert found == (ids if low else set()), (path.name, found)
        print('PASS', path.name)
