"""Static CIL regression controls. No specimen is executed."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / 'testdata/hostile/xworm-damaged-task-client.exe'
ATOM = 'objectives/command-and-control/remote-command/shell::cil-decoded-task-shell-field'
SHELL = 'objectives/command-and-control/remote-command/shell::cil-encrypted-task-shell-dispatch'
LOAD = 'micro-behaviors/process/deploy/module-load::cil-byte-array-instance-invocation'
PAYLOAD = 'objectives/execution/payload/module-load::cil-task-managed-payload-activation'
SCREEN = 'micro-behaviors/hardware/display/screenshot::cil-jpeg-base64-response-construction'
REPLY = 'objectives/collection/screenshot::shell-task-backdoor-jpeg-screen-response'
ALL = {ATOM, SHELL, LOAD, PAYLOAD, SCREEN, REPLY}


def patch(data, offset, old, new):
    assert data[offset:offset + len(old)] == old and len(old) == len(new)
    return data[:offset] + new + data[offset + len(old):]


def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        doc, end = decoder.raw_decode(text.lstrip())
        yield from doc['files']
        text = text.lstrip()[end:]


def main():
    data = FIXTURE.read_bytes()
    no_shell = ALL - {ATOM, SHELL, PAYLOAD, REPLY}
    cases = [
        ('renamed.exe', data, ALL),
        ('renamed-task.exe', data.replace('RunShell'.encode('utf-16le'), 'ExecTask'.encode('utf-16le')), ALL),
        # The strings remain present, but the task ldstr leaves the #US heap.
        ('invalid-task-ldstr.exe', patch(data, 0x1ba6, b'\x00', b'\xff'), no_shell),
        ('wrong-task-local.exe', patch(data, 0x1ba2, b'\x13', b'\x12'), no_shell),
        ('wrong-shell-call.exe', patch(data, 0x1bb8, b'\xa9', b'\xa8'), no_shell),
        ('no-receive.exe', data.replace(b'BeginReceive', b'AwaitReceive'), ALL - {SHELL, PAYLOAD, REPLY}),
        ('no-load.exe', patch(data, 0x2b0a, b'\x6f', b'\x00'), ALL - {LOAD, PAYLOAD}),
        ('no-invoke.exe', patch(data, 0x2b48, b'\x6f', b'\x00'), ALL - {LOAD, PAYLOAD}),
        ('wrong-copy-operation.exe', patch(data, 0x1fb3, b'\xcc', b'\xaa'), ALL - {SCREEN, REPLY}),
        ('different-image-stream.exe', patch(data, 0x2016, b'\x0f', b'\x0e'), ALL - {SCREEN, REPLY}),
        ('different-response-array.exe', patch(data, 0x2063, b'\x14', b'\x13'), ALL - {SCREEN, REPLY}),
        ('wrong-code-section.exe', data.replace(b'.text\0', b'.data\0'), set()),
    ]
    with tempfile.TemporaryDirectory(prefix='damaged-managed-task-') as tmp:
        expected = {}
        for name, content, wanted in cases:
            path = Path(tmp) / name
            path.write_bytes(content)
            expected[str(path)] = wanted
        controls = [
            'testdata/benign/managed-native-interop-only.exe',
            'testdata/benign/managed-status-stubs-only.exe',
            'testdata/hostile/xworm-v3-obfuscated-client.exe',
            'testdata/hostile/xworm-v71-task-client.exe',
        ]
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json',
             *expected, *(str(ROOT / p) for p in controls)],
            capture_output=True, text=True, check=True, timeout=360,
        )
        seen = set()
        for report in documents(result.stdout):
            path = report['path']
            actual = {t['id'] for t in report.get('traits', [])}
            if path in expected:
                assert actual & ALL == expected[path], (Path(path).name, (actual & ALL) ^ expected[path])
                seen.add(path)
            elif '/benign/' in path:
                assert not actual & ALL, (path, actual & ALL)
            elif path.endswith('xworm-v71-task-client.exe'):
                # Retain the existing named-API JPEG/Base64 construction path.
                assert SCREEN in actual, path
            elif path.endswith('xworm-v3-obfuscated-client.exe'):
                assert 'micro-behaviors/hardware/display/screenshot::cil-jpeg-string-response-construction' in actual
        assert seen == set(expected), set(expected) - seen
    print('Passed 12 CIL mutations and 4 outside-batch controls')


if __name__ == '__main__':
    main()
