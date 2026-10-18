"""Static mutation controls. Requires the three supplied specimens; executes none.

Usage: python3 check.py --samples <NanoCoreUltimate> <StormAttack> <AsyncRAT>
                       --work-dir <scratch-directory>
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--samples', nargs=3, required=True)
ap.add_argument('--work-dir', type=Path, required=True)
ap.add_argument('--cleave', default='cleave')
ap.add_argument('--traits-dir', default='.')
a = ap.parse_args()
a.work_dir.mkdir(parents=True, exist_ok=True)
hashes = [
    '5fdee438b0ec8fce2e1c1329d403ca66f4ff1432da374a1dc14bf2e4b9344ead',
    '7fe2d4226bf385a971ab451d5181ab30e52cc17529e274b7620e665cb65ad345',
    'ae33e8388bfe7ec272eee2345eede71fde04983ffdb5a8fc1f857527f7c66e45',
]
for path, digest in zip(a.samples, hashes):
    assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest
keylog = 'objectives/collection/keylog/hook::dotnet-hook-keylog-recording'
screen = 'objectives/collection/screenshot::managed-screen-recording'
chrome = 'objectives/evasion/masquerade/version-resource/google-chrome::chrome-branded-managed-plugin-backdoor'
plugin = 'objectives/command-and-control/backdoor/dispatch/module::messagepack-managed-plugin-tasking'
tls = 'micro-behaviors/communications/tls/verify/callback::dotnet-custom-tls-certificate-validation'
active = 'objectives/persistence/login/registry/autostart::active-setup-service-dll-injector'
neutral = 'micro-behaviors/mem/combined::suspended-write-resume-api-profile'
cases = []

def mutated(name, index, replacements, expected):
    data = Path(a.samples[index]).read_bytes()
    for old, new in replacements:
        assert len(old) == len(new)
        count = 0
        for encoding in ['ascii', 'utf-16le']:
            before, after = old.encode(encoding), new.encode(encoding)
            count += data.count(before)
            data = data.replace(before, after)
        assert count, (name, old)
    path = a.work_dir / (name + '.exe')
    path.write_bytes(data)
    cases.append((path, expected))

cases.extend([
    (Path(a.samples[0]), {keylog: True, screen: True, neutral: True}),
    (Path(a.samples[1]), {active: True, keylog: False, chrome: False}),
    (Path(a.samples[2]), {plugin: True, chrome: True, tls: True}),
])
# Removing network support does not remove locally observable collection.
mutated('local-collection-no-upload', 0, [('UploadString', 'XploadString')],
        {keylog: True, screen: True})
mutated('no-keylog-record', 0, [('KEYLOG:', 'RECORD:')],
        {keylog: False, screen: False})
mutated('no-screen-record', 0, [('SCREEN:', 'RECORD:')],
        {keylog: True, screen: False})
# Branding alone and backdoor behavior alone do not prove this impersonation.
mutated('backdoor-without-chrome-claim', 2, [('Google Chrome', 'Sample Client')],
        {plugin: True, chrome: False})
mutated('chrome-claim-without-plugin-tasks', 2,
        [('savePlugin', 'saveRecord'), ('sendPlugin', 'sendRecord')],
        {plugin: False, chrome: False})
mutated('tls-stream-without-validation-callback', 2,
        [('ValidateServerCertificate', 'ValidateRecordCertificate')], {tls: False})
mutated('injector-without-active-setup', 1,
        [('Active Setup', 'Sample Setup')], {active: False})
# The broad mechanics are useful but do not establish a payload-delivery chain.
source = a.work_dir / 'debugger-mechanics.c'
source.write_text('''void Attach(void) {
    CreateProcess(null, CREATE_SUSPENDED);
    WriteProcessMemory(process, address, data, size, written);
    ResumeThread(thread);
}
''')
cases.append((source, {neutral: True}))

def run(case):
    path, expected = case
    command = [a.cleave, '--traits-dir', a.traits_dir, 'test-rules', str(path),
               '--rules', ','.join(expected)]
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout + result.stderr
    assert result.returncode == 0, output
    actual = {rule: any(line.startswith('MATCHED ' + rule + ' ')
                       for line in output.splitlines()) for rule in expected}
    assert actual == expected, (str(path), actual, expected, output)
    (a.work_dir / (path.name + '.trace')).write_text(output)
    return {'case': path.name, 'expected': expected, 'actual': actual}

with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run, cases))
(a.work_dir / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
print(f'{len(results)} controls passed')
