"""Check the supported observations and preserve each consuming attack rule."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--baseline', type=Path)
parser.add_argument('--scratch', required=True)
args = parser.parse_args()
here = Path(__file__).resolve().parent
root = here.parents[1]
opcode = 'metadata/binary/instruction/opcode::repeated-rdtscp-byte-pattern'
setup = 'micro-behaviors/fs/path/application/executable::hyphenated-setup-exe-name'
auto = 'objectives/execution/autoinstall/manager-package::download-manager-auto-installer'
xor = 'objectives/anti-static/obfuscation/name-mangling/variables::javascript-hex-variables-with-xor'
drive = 'micro-behaviors/communications/http/services/google::googleapis-drive'
moves = {
    'micro-behaviors/time/query::rdtscp': opcode,
    'micro-behaviors/process/create/launch::temp-setup-output-name': setup,
    'objectives/anti-static/obfuscation/eval/loader::javascript-fragmented-xor-obfuscation': xor,
    'objectives/exfiltration/cloud/object-store::gdrive-api': drive,
}
cases = {
    'native-opcodes.exe': ([opcode], [setup, auto, loader]),
    'single-opcode.exe': ([], [opcode]),
    'data-opcodes.exe': ([], [opcode]),
    'setup-name-only.exe': ([setup], [auto, loader]),
    'download-launch.exe': ([setup, auto], [loader]),
    'download-no-name.exe': ([], [setup, auto]),
    'analysis-catalog.exe': ([opcode], [auto]),
    'xor-names.js': ([xor], []),
    'xor-readable.js': ([], [xor]),
    'hex-names.js': ([], [xor]),
    'drive-client.py': ([drive], ['objectives/exfiltration/cloud/object-store::gdrive-api']),
}

def scan(traits, paths):
    result = subprocess.run([args.cleave, '--traits-dir', str(traits), '--format', 'json',
                             *map(str, paths)], check=True, capture_output=True, text=True)
    reports = {}
    pending = result.stdout
    decoder = json.JSONDecoder()
    while pending.strip():
        data, end = decoder.raw_decode(pending.lstrip())
        pending = pending.lstrip()[end:]
        for file in data.get('files', []):
            reports[Path(file['path']).name] = {trait['id'] for trait in file.get('traits', [])}
    return reports

with tempfile.TemporaryDirectory(prefix='observations-', dir=args.scratch) as directory:
    paths = []
    for name in cases:
        dest = Path(directory)/name
        shutil.copyfile(here/name, dest)
        paths.append(dest)
    current = scan(root, paths)
    original = scan(args.baseline, paths) if args.baseline else None
    for name, (matched, absent) in cases.items():
        ids = current[name]
        assert set(matched) <= ids, (name, 'missing', set(matched)-ids)
        assert not set(absent) & ids, (name, 'unexpected', set(absent)&ids)
        if original is not None:
            remapped = {moves.get(trait, trait) for trait in original[name]}
            assert remapped == ids, (name, 'coverage changed', remapped-ids, ids-remapped)
        print('PASS', name)
