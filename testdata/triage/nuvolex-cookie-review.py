"""Static controls for name-only evidence and wave-input enumeration.

Usage: python3 testdata/triage/nuvolex-cookie-review.py SCRATCH_DIRECTORY
Generated PE fixtures return immediately and are never executed.
"""
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BINARY_NAME = 'metadata/binary/symbols/name::decryptdata-name-reference'
SOURCE_NAME = 'metadata/file/function::csharp-decryptdata-declaration'
AUDIO = 'micro-behaviors/hardware/input/audio::wavein-device-count-reference'
OLD = 'micro-behaviors/crypto/decrypt::decryptdata-method-name'


def main():
    dest = Path(sys.argv[1]).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    build_pe = runpy.run_path(str(ROOT / 'testdata/managed-records-review/verify.py'))['build_pe']
    build_rtti = runpy.run_path(str(ROOT / 'testdata/taxonomy/iot-gh0st-reasoned-review/check.py'))['pe']
    cases = [
        ('name.exe', build_pe(['DecryptData']), {BINARY_NAME}),
        ('name.dll', build_pe(['DecryptData']), {BINARY_NAME}),
        ('name-near-miss.exe', build_pe(['DecryptDatabase']), set()),
        ('audio.exe', build_pe(['waveInGetNumDevs']), {AUDIO}),
        ('audio-near-miss.exe', build_pe(['waveOutGetNumDevs']), set()),
        ('name.cs', b'class Example { void DecryptData() {} }', {SOURCE_NAME}),
        ('name-near-miss.cs', b'class Example { void DecryptDatabase() {} }', set()),
        ('name-string.cs', b'class Example { string label = "DecryptData"; }', set()),
    ]
    descriptors = {
        'ckeyboard-manager': 'CKeyboardManager', 'cscreen-manager': 'CScreenManager',
        'cshell-manager': 'CShellManager', 'ckernel-manager': 'CKernelManager',
        'ctcp-socket': 'CTcpSocket', 'cmanager': 'CManager',
        'csystem-manager': 'CSystemManager', 'cfile-manager': 'CFileManager',
        'cscreen-spy': 'CScreenSpy', 'cdialupass': 'CDialupass',
    }
    rtti_ids = {'metadata/binary/symbols/descriptor::rtti-' + key for key in descriptors}
    for key, name in descriptors.items():
        cases.append((key + '.dll', build_rtti([name.encode()]),
                      {'metadata/binary/symbols/descriptor::rtti-' + key}))
    cases.append(('rtti-near-miss.dll', build_rtti([b'CKeyboardManagerOther']), set()))
    cases.append(('rtti-wrong-section.dll', build_rtti([b'CKeyboardManager']).replace(
        b'.data\x00\x00\x00', b'.rdata\x00\x00'), set()))
    for name, content, _ in cases:
        (dest / name).write_bytes(content)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--disable', 'radare2,third-party', '--format', 'json',
         *[str(dest / name) for name, _, _ in cases]],
        capture_output=True, text=True)
    (dest / 'controls.json').write_text(result.stdout)
    (dest / 'controls.stderr').write_text(result.stderr)
    assert result.returncode == 0, result.stderr
    files, remaining = [], result.stdout.strip()
    decoder = json.JSONDecoder()
    while remaining:
        report, consumed = decoder.raw_decode(remaining)
        files.extend(report['files'])
        remaining = remaining[consumed:].lstrip()
    for name, _, expected in cases:
        matches = [f for f in files if Path(f['path']).name == name]
        assert len(matches) == 1, (name, matches)
        traits = {t['id']: t for t in matches[0].get('traits', [])}
        assert OLD not in traits, name
        assert not any(t.startswith('metadata/binary/symbols/name::rtti-') for t in traits), name
        assert set(traits).intersection({BINARY_NAME, SOURCE_NAME, AUDIO} | rtti_ids) == expected, name
        # A helper name or a device-count API does not establish hostile intent.
        assert not any(t['crit'] >= 4 for t in traits.values()), (name, traits)
        for trait in expected:
            assert traits[trait]['crit'] == 3, (name, trait)
        print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
