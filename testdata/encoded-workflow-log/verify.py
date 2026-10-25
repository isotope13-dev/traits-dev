#!/usr/bin/env python3
"""Check encoded CI log verdicts and benign controls with one Cleave invocation.

Usage: python3 testdata/encoded-workflow-log/verify.py SAMPLE_DIR CLEAVE_FIXTURES
The article samples live in threat-feed scratch; controls belong in Cleave.
"""
import json
import pathlib
import subprocess
import sys

samples = pathlib.Path(sys.argv[1])
controls = pathlib.Path(sys.argv[2]) / 'threat-feed-4278-gheist-controls'
controls.mkdir(parents=True, exist_ok=True)

def workflow(code, shell='bash'):
    return ('name: diagnostics\non: [workflow_dispatch]\njobs:\n  check:\n'
            '    runs-on: ubuntu-latest\n    steps:\n      - shell: ' + shell +
            '\n        run: |\n' + ''.join('          ' + line + '\n'
                                          for line in code.splitlines()))

original = (samples / 'sync-check.yml').read_text()
cases = {
    'redirected-shell.yml': original.replace('base32 -w 120', 'base32 -w 120 > private.dat'),
    'commented-shell.yml': original.replace('env |', '# env |').replace('echo -n', '# echo -n'),
    'decode-shell.yml': original.replace('base32 -w 120', 'base32 -d'),
    'plain-environment.yml': workflow('env'),
    'encoded-constant.yml': workflow("echo -n 'diagnostics' | base32 -w 120"),
    'secrets-deployment.yml': workflow("export SECRETS='${{ toJSON(secrets) }}'\n./deploy\necho health | base64"),
    'encoded-before-secrets.yml': workflow("echo health | base32\nexport SECRETS='${{ toJSON(secrets) }}'"),
    'python-file.yml': workflow("import base64, os\nprint(base64.b32encode(str(dict(os.environ)).encode()).decode(), file=open('private.txt','w'))\nprint(base64.b32encode(b'${{ toJSON(secrets) }}').decode(), file=open('private.txt','w'))", 'python'),
    'node-length.yml': workflow("console.log(Buffer.from(JSON.stringify(process.env)).toString('base64').length);\nconsole.log(Buffer.from('${{ toJSON(secrets) }}').toString('base64').length);", 'node'),
    'powershell-file.yml': workflow("Write-Output ([Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes((Get-ChildItem Env: | Out-String)))) > private.txt\nWrite-Output ([Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('${{ toJSON(secrets) }}'))) > private.txt", 'pwsh'),
    'code-comments.yml': workflow("# print(base64.b32encode(b'${{ toJSON(secrets) }}').decode())\n# console.log(Buffer.from('${{ toJSON(secrets) }}').toString('base64'));\n# Write-Output ([Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes('${{ toJSON(secrets) }}')))\necho ready"),
}
for name, body in cases.items():
    (controls / name).write_text(body)

root = pathlib.Path(__file__).resolve().parents[2]
result = subprocess.run(['cleave', '--traits-dir', str(root), '--json',
                         str(samples), str(controls)], text=True, capture_output=True)
if result.stderr:
    print(result.stderr, file=sys.stderr)
assert result.returncode == 0, result.returncode
reports = [json.loads(line) for line in result.stdout.splitlines() if line.startswith('{')]
expected = {
    'sync-check.yml': 'shell', 'matrix-macos.yml': 'shell', 'python.yml': 'python',
    'node.yml': 'node', 'powershell.yml': 'powershell',
}
checked = set()
for report in reports:
    for file in report.get('files', []):
        path = pathlib.Path(file['path'])
        if '!!' in str(path):
            continue
        traits = {t['id'] for t in file.get('traits', [])}
        verdicts = {t for t in traits if t.startswith('objectives/exfiltration/stealer/')
                    and ('encoded-secrets-log' in t or 'encoded-environment-log' in t)}
        if path.parent == samples:
            lang = expected[path.name]
            required = {
                f'objectives/exfiltration/stealer/dev-secret::gha-{lang}-encoded-secrets-log',
                'objectives/exfiltration/stealer/env::gha-encoded-environment-log',
            }
            assert required <= verdicts, (path.name, required - verdicts)
            checked.add(path.name)
            print(path.name, 'PASS: secret log + environment log')
        elif path.parent == controls:
            assert not verdicts, (path.name, verdicts)
            checked.add(path.name)
assert checked == set(expected) | set(cases), ('missing reports', checked)
print(f'{len(expected)} positive variants and {len(cases)} benign controls passed')
