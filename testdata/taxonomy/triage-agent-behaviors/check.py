#!/usr/bin/env python3
"""Check instruction writes, analytics and preload filtering without execution."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import io
import tarfile

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
fixtures = Path(__file__).resolve().parent
root = fixtures.parents[2]
write = 'micro-behaviors/fs/write/file/full::node-agent-instruction-path-write'
analytics = 'micro-behaviors/communications/http/services/analytics::google-analytics-mp-collect-endpoint'
guard = 'objectives/evasion/security-bypass/runtime::node-options-delete-guard-filtering'
skill = 'micro-behaviors/process/create/skill::node-spawn-global-skills-add'
install = 'objectives/supply-chain/install-hook/skill-agent::postinstall-spawns-global-skills-installer'
cases = {
    'instruction-write.js': ({write}, set()),
    'instruction-read-other-write.js': (set(), {write}),
    'filename-in-content.js': (set(), {write}),
    'analytics-query-builder.js': ({analytics}, set()),
    'analytics-lookalike.js': (set(), {analytics}),
    'delete-guard-filter.js': ({guard}, set()),
    'unrelated-env-filter.js': (set(), {guard}),
    'guard-reference-only.js': (set(), {guard}),
    'skills-spawn-array.js': ({skill}, set()),
    'skills-spawn-separated.js': (set(), {skill}),
    'skills-spawn-local.js': (set(), {skill}),
    'skills-spawn-unused-array.js': (set(), {skill}),
}
with tempfile.TemporaryDirectory(prefix='agent-behavior-controls-') as staging:
    paths = []
    for name in cases:
        target = Path(staging) / name
        shutil.copyfile(fixtures / name, target)
        paths.append(str(target))
    for hook in [True, False]:
        name = 'skills-install-hook.tgz' if hook else 'skills-explicit-cli.tgz'
        cases[name] = ({install}, set()) if hook else (set(), {install})
        manifest = {'name': 'example-static-control', 'version': '1.0.0'}
        if hook:
            manifest['scripts'] = {'postinstall': 'node installer.js'}
        target = Path(staging) / name
        with tarfile.open(target, 'w:gz') as archive:
            for member, content in {
                'package/package.json': json.dumps(manifest).encode(),
                'package/installer.js': (fixtures / 'skills-spawn-array.js').read_bytes(),
                'package/skills/example/SKILL.md': b'---\nname: example\ndescription: Test control\n---\nLocal example skill.\n',
            }.items():
                entry = tarfile.TarInfo(member)
                entry.size = len(content)
                archive.addfile(entry, io.BytesIO(content))
        paths.append(str(target))
    output = subprocess.run(
        [args.cleave, '--no-update-check', '--traits-dir', str(root),
         '--format=json', *paths], check=True, capture_output=True, text=True).stdout
    decoder = json.JSONDecoder()
    reports = {}
    while output.strip():
        report, end = decoder.raw_decode(output.lstrip())
        output = output.lstrip()[end:]
        reports.update({Path(file['path']).name: file for file in report['files']})
    for name, (required, forbidden) in cases.items():
        traits = reports[name].get('traits', [])
        ids = {finding['id'] for finding in traits}
        assert required <= ids, (name, 'missing', required - ids)
        assert not forbidden & ids, (name, 'unexpected', forbidden & ids)
        assert not any(finding['crit'] >= 5 for finding in traits), (name, traits)
        if name not in {'delete-guard-filter.js', 'skills-install-hook.tgz'}:
            assert not any(finding['crit'] >= 4 for finding in traits), (name, traits)
print(f'{len(cases)} agent behavior controls passed')
