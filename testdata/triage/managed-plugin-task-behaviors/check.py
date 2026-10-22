"""Static controls: mutate verified CIL; never execute the client."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
ORIGINAL = ROOT / 'testdata/hostile/xworm-v71-task-client.exe'
PATH = 'micro-behaviors/fs/path/autostart::cil-startup-shortcut-path-construction'
COM = 'micro-behaviors/os/com/shortcut::managed-shortcut-target-and-save-references'
JPEG = 'micro-behaviors/hardware/display/screenshot::cil-jpeg-base64-response-construction'
STARTUP = 'objectives/persistence/login/startup/shortcut::managed-plugin-backdoor-startup-shortcut'
COMMAND = 'objectives/command-and-control/remote-command/dispatch::managed-plugin-task-command-launch'
EXFIL = 'objectives/exfiltration/stealer/screen::managed-plugin-backdoor-jpeg-response'
DISPATCH = 'micro-behaviors/data/control-flow/dispatch::cil-vb-string-task-dispatch'
ALL = {PATH, COM, JPEG, STARTUP, COMMAND, EXFIL, DISPATCH}


def patch(data, offset, old, new):
    assert len(old) == len(new) and data[offset:offset+len(old)] == old
    result = bytearray(data)
    result[offset:offset+len(new)] = new
    return bytes(result)


def rename(data, old, new, encoding='utf-16le'):
    a, b = old.encode(encoding), new.encode(encoding)
    assert len(a) == len(b) and a in data
    return data.replace(a, b)


def reports(text):
    decoder = json.JSONDecoder()
    while text.strip():
        obj, end = decoder.raw_decode(text.lstrip())
        yield from obj['files']
        text = text.lstrip()[end:]


def main():
    data = ORIGINAL.read_bytes()
    assert hashlib.sha256(data).hexdigest() == "a0418a951d0060a4293c795d3375fe7955cabc7765cdafd16af922d797597710"
    cases = [
        ('original', data, ALL),
        # No task label or collector filename is required.
        ('renamed', rename(data, 'RunShell', 'ExecTask'), ALL),
        ('other-special-folder', patch(data, 0x5d4, b'\x1d', b'\x1e'), ALL - {PATH, STARTUP}),
        ('no-shortcut-extension', rename(data, '.lnk', '.dat'), ALL - {PATH, STARTUP}),
        ('no-shortcut-save', rename(data, 'Save', 'Keep'), ALL - {COM, STARTUP}),
        ('no-shortcut-target', rename(data, 'TargetPath', 'OutputPath'), ALL - {COM, STARTUP}),
        ('no-command-launch-call', patch(data, 0x177f, b'\x28', b'\x00'), ALL - {COMMAND, DISPATCH}),
        ('no-task-argument-read', patch(data, 0x177b, b'\x9a', b'\x00'), ALL - {COMMAND, DISPATCH}),
        # Independent streams and response arrays must not form a send chain.
        ('different-jpeg-stream', patch(data, 0x1c19, b'\x0f', b'\x0e'), ALL - {JPEG, EXFIL}),
        ('different-response-array', patch(data, 0x1c2b, b'\x14', b'\x15'), ALL - {JPEG, EXFIL}),
        ('no-base64-encode', rename(data, 'ToBase64String', 'NoBase64String', 'ascii'), ALL - {JPEG, EXFIL}),
        ('no-receive-profile', rename(data, 'BeginReceive', 'AwaitReceive', 'ascii'), ALL - {STARTUP, COMMAND, EXFIL}),
        ('wrong-section', rename(data, '.text', '.data', 'ascii'), set()),
    ]
    with tempfile.TemporaryDirectory(prefix='managed-plugin-') as tmp:
        paths = []
        expected = {}
        for name, content, wanted in cases:
            path = Path(tmp) / (name + '.exe')
            path.write_bytes(content)
            paths.append(path)
            expected[str(path)] = wanted
        # Ordinary managed programs and isolated native interop are controls,
        # rather than assuming that a byte-mutated malware client is benign.
        for name in ['managed-native-interop-only.exe', 'managed-status-stubs-only.exe']:
            path = ROOT / 'testdata/benign' / name
            paths.append(path)
            expected[str(path)] = set()
        result = subprocess.run([
            os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
            '--format', 'json', *(str(p) for p in paths)
        ], text=True, capture_output=True, check=True, timeout=240,
           env={**os.environ, 'CLEAVE_VALIDATE': '0'})
        seen = set()
        for f in reports(result.stdout):
            path = f['path']
            if path not in expected:
                continue
            seen.add(path)
            got = {t['id'] for t in f.get('traits', [])} & ALL
            assert got == expected[path], (path, got ^ expected[path], result.stderr)
        assert seen == expected.keys(), seen ^ expected.keys()
    print(f'{len(paths)} managed task, Startup and screenshot controls passed')


if __name__ == '__main__':
    main()
