"""Static regression checks; no specimen is executed or contacted."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = ROOT / 'testdata/hostile/xworm-v3-obfuscated-client.exe'
SCREEN = 'micro-behaviors/hardware/display/screenshot::cil-jpeg-string-response-construction'
SELF = 'micro-behaviors/fs/delete/file/self::cil-self-image-delete-line-construction'
LAUNCH = 'micro-behaviors/process/create/spawn::cil-vb-shell-literal-command-call'
EXFIL = 'objectives/exfiltration/stealer/screen::managed-plugin-backdoor-string-screen-response'
REMOVE = 'objectives/evasion/self-delete/process::managed-plugin-backdoor-batch-self-removal'
SHUTDOWN = 'objectives/impact/system/shutdown::managed-plugin-backdoor-shutdown-commands'
RISK = 'metadata/build/ci/gate::pr-target-head-local-action-secret-exposure'
OIDC = 'metadata/build/ci/gate::pr-target-head-oidc-credential-exposure'
WRITE = 'metadata/build/ci/gate::pr-target-head-write-secret-exposure'
POLL = 'micro-behaviors/process/lifecycle/supervise::powershell-process-polling-loop'
NEW = {SCREEN, SELF, LAUNCH, EXFIL, REMOVE, SHUTDOWN, RISK, OIDC, WRITE, POLL}


def patch(data, offset, old, new):
    assert len(old) == len(new) and data[offset:offset+len(old)] == old
    return data[:offset] + new + data[offset+len(old):]


def rename(data, old, new, encoding='ascii'):
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
    data = FIXTURE.read_bytes()
    all_rat = {SCREEN, SELF, LAUNCH, EXFIL, REMOVE, SHUTDOWN}
    cases = [
        ('renamed-client.exe', data, all_rat),
        ('renamed-banner.exe', rename(data, 'XWorm V3.0', 'Other V3.0', 'utf-16le'), all_rat),
        ('different-screen-stream.exe', patch(data, 0x1912, b'\x0d', b'\x0c'), all_rat - {SCREEN, EXFIL}),
        ('no-screen-array-call.exe', patch(data, 0x1913, b'\x6f', b'\x00'), all_rat - {SCREEN, EXFIL}),
        ('no-screen-send-call.exe', patch(data, 0x192c, b'\x28', b'\x00'), all_rat - {SCREEN, EXFIL}),
        ('no-capture-reference.exe', rename(data, 'CopyFromScreen', 'CopyFromBuffer'), all_rat - {SCREEN, EXFIL}),
        ('no-self-path-reference.exe', rename(data, 'get_ExecutablePath', 'get_ExecutableInfo'), all_rat - {SELF, REMOVE}),
        ('no-delete-line-call.exe', patch(data, 0x25e1, b'\x6f', b'\x00'), all_rat - {SELF, REMOVE}),
        ('no-shell-reference.exe', rename(data, 'Interaction', 'Transaction'), all_rat - {LAUNCH, SHUTDOWN}),
        ('no-remote-receive.exe', rename(data, 'BeginReceive', 'AwaitReceive'), {SCREEN, SELF, LAUNCH}),
        ('wrong-code-section.exe', rename(data, '.text', '.data'), set()),
    ]
    workflow = (ROOT / 'testdata/benign/gha-unguarded-target-head-secret.yml').read_bytes()
    cases += [
        ('untrusted-head.yml', workflow, {RISK}),
        ('untrusted-head-oidc.yml', workflow.replace(b'jobs:', b'permissions:\n  id-token: write\njobs:'), {RISK, OIDC}),
        ('untrusted-head-write.yml', workflow.replace(b'jobs:', b'permissions:\n  contents: write\njobs:'), {RISK, WRITE}),
        ('trusted-event.yml', workflow.replace(b'pull_request_target:', b'pull_request:'), set()),
        ('no-secret.yml', workflow.replace(b'secrets.INTEGRATION_TOKEN', b'inputs.test_token'), set()),
        ('base-head.yml', workflow.replace(b'pull_request.head.sha', b'pull_request.base.sha'), set()),
        ('ordinary-poll.ps1', b'while ($true) { Get-Process -Name worker; Start-Sleep -Seconds 5 }', {POLL}),
        ('one-query.ps1', b'Get-Process -Name worker; Start-Sleep -Seconds 5', set()),
    ]
    with tempfile.TemporaryDirectory(prefix='rat-ci-review-') as tmp:
        expected = {}
        for name, content, wanted in cases:
            path = Path(tmp) / name
            path.write_bytes(content)
            expected[str(path)] = wanted
        for relative in [
            'testdata/benign/managed-native-interop-only.exe',
            'testdata/benign/managed-status-stubs-only.exe',
            'testdata/benign/gha-ok-to-test-label-gate.yml',
            'testdata/benign/gha-rule-test-fixture-controls.yml',
            'testdata/hostile/github-actions-curl-token-exfil.yml',
        ]:
            expected[str(ROOT / relative)] = set()
        result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                                 '--format', 'json', *expected], text=True, capture_output=True,
                                check=True, timeout=240, env={**os.environ, 'CLEAVE_VALIDATE': '0'})
        seen = set()
        for f in reports(result.stdout):
            path = f['path']
            if path not in expected:
                continue
            seen.add(path)
            got = {t['id'] for t in f.get('traits', [])} & NEW
            assert got == expected[path], (path, got ^ expected[path], result.stderr)
            if path.endswith('.yml'):
                # Exposure properties remain suspicious; real token-exfil
                # code must retain its independently supported hostile rule.
                hostile = [t for t in f.get('traits', []) if t['crit'] == 5]
                if path.endswith('github-actions-curl-token-exfil.yml'):
                    assert hostile, (path, 'lost theft coverage')
                else:
                    assert not hostile, (path, hostile)
        assert seen == expected.keys(), seen ^ expected.keys()
    print(f'{len(expected)} static RAT, CI and process-polling controls passed')


if __name__ == '__main__':
    main()
