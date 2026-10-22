"""Scan recovered material and controls. Never executes sample code.

python3 verify.py RECOVERY_DIRECTORY [--report OUTPUT.json]
Run recover.py first. CLEAVE optionally selects the scanner binary.
"""
import argparse
import json
import os
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))


def scan(paths):
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'json',
                             *map(str, paths)], capture_output=True, text=True, check=True)
    decoder, remaining, files = json.JSONDecoder(), result.stdout, []
    while remaining.strip():
        remaining = remaining.lstrip()
        report, end = decoder.raw_decode(remaining)
        files.extend(report.get('files', []))
        remaining = remaining[end:]
    return files


def findings(files):
    return {trait['id'] for file in files for trait in file.get('traits', [])}


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('recovery', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    coverage = json.loads((HERE / 'coverage.json').read_text())
    files = scan([args.recovery / 'recovered.tar'])
    ids = findings(files)
    failures, results = [], []
    for row in coverage['items']:
        missing = sorted(set(row['expect']) - ids)
        results.append({**row, 'passed': not missing, 'missing': missing})
        failures.extend(missing)
        print(('FAIL' if missing else 'PASS'), row['item'], flush=True)

    # Passing each path explicitly includes the hidden .github directory.
    controls = scan(sorted(path for path in (HERE / 'controls').rglob('*') if path.is_file()))
    high = [(f['path'], t['id']) for f in controls for t in f.get('traits', []) if t['crit'] >= 4]
    failures.extend(high)
    print('PASS' if not high else 'FAIL', 'benign/near-miss controls:', len(controls), flush=True)

    # Counterexamples above and equivalent spellings below check structural
    # constraints, rather than just matching the pinned sample's bytes.
    variants = args.recovery / 'variants'
    variants.mkdir(exist_ok=True)
    manifest = json.loads((HERE / 'functions.json').read_text())
    sources = {row['name']: (args.recovery / 'recovered/functions' / row['file']).read_text()
               for row in manifest['functions']}
    def renamed(text):
        names = {name: 'v' + str(i) for i, name in enumerate(sorted(set(re.findall(r'\b_0x[\da-f]+\b', text))))}
        return re.sub(r'\b_0x[\da-f]+\b', lambda m: names[m[0]], text)
    cases = {
        'locale.js': (renamed(sources['Ci'] + '\n' + sources['tl']),
                      'objectives/anti-analysis/geofencing/locale::javascript-cis-locale-prefix-cluster'),
        'ssh.js': (renamed(sources['Wa']).replace('"infectHost"', '"dispatch"'),
                   'objectives/lateral-movement/ssh/propagation::bun-self-read-ssh-payload-spread'),
        'gem.js': (renamed(sources['Mu'] + '\n' + sources['_u']),
                   'objectives/supply-chain/trojanized/build-pipeline::rubygems-extension-republisher'),
        'wheel.js': (renamed(sources['$r'] + '\n' + sources['Lr']),
                     'objectives/supply-chain/trojanized/build-pipeline::pypi-sitecustomize-republisher'),
        'cache.js': (renamed(sources['Sy'] + '\n' + sources['Dr']),
                     'objectives/supply-chain/trojanized/build-pipeline::artifactory-cache-replacement-repack'),
        'hosts.js': ('run("echo 127.0.0.1 telemetry.stepsecurity.io >> /etc/hosts");\n',
                     'objectives/evasion/hosts-file/block-security::stepsecurity-hosts-block-write'),
        'dot-ssh.js': (renamed(sources['Wa'])
                       .replace('Bun["file"]', 'Bun.file').replace('Bun["main"]', 'Bun.main')
                       .replace('Bun["spawnSync"]', 'Bun.spawnSync')
                       .replace('Bun["spawn"]', 'Bun.spawn').replace('["text"]()', '.text()'),
                       'objectives/lateral-movement/ssh/propagation::bun-self-read-ssh-payload-spread'),
        'dot-gem.js': (renamed(sources['Mu'] + '\n' + sources['_u']).replace('["replace"]', '.replace'),
                       'objectives/supply-chain/trojanized/build-pipeline::rubygems-extension-republisher'),
        'dot-version.js': (renamed(sources['Dr']).replace('["version"]', '.version'),
                           'objectives/supply-chain/trojanized/build-pipeline::gyp-hook-package-version-rewrite'),
        'dot-sandbox.js': ('const suspect = exec("hostname").toString().includes("sandbox");\n',
                           'objectives/anti-analysis/sandbox-detect/script::javascript-hostname-sandbox-comparison'),
        'dot-hosts.js': ('const domains=["api.stepsecurity.io"];const entry="127.0.0.1 "+domains.join(" ");run("echo "+entry+" >> /etc/hosts");\n',
                         'objectives/evasion/hosts-file/block-security::stepsecurity-domain-list-hosts-rewrite'),
        'sudoers.js': (renamed(sources['Nv']),
                       'objectives/privilege-escalation/elevation-control/sudo::privileged-sudoers-bind-passwordless-grant'),
        'sudoers-reordered.js': ('const grant="operator ALL=(ALL) NOPASSWD:ALL"; const spec={HostConfig:{Binds:["/etc/sudoers.d:/host-policy:rw"],Privileged:true}};\n',
                                 'objectives/privilege-escalation/elevation-control/sudo::privileged-sudoers-bind-passwordless-grant'),
        'auth-explicit.sh': ('#!/bin/bash\nif [[ "$STATUS" == 401 || "$STATUS" == 403 ]]; then eval "$ACTION"; fi\n',
                             'micro-behaviors/communications/http/token-auth::shell-http-rejection-eval-handler'),
        'package-tarball.js': ('const archive="package/addon.tgz";\n',
                               'micro-behaviors/fs/path/archive::node-package-tgz-path-reference'),
        'setup-import.py': ('setup(name="ordinary-package"); import os\n',
                            'metadata/lang/source/syntax/call::post-setup-import-os-sys'),
        'discord-path.py': ('path="discord/Local Storage/leveldb"\n',
                            'micro-behaviors/fs/path/app-data::discord-local-storage-path'),
        'release-api.js': ((HERE / 'controls/release-maintainer.js').read_text(),
                           'micro-behaviors/communications/http/services/registry::npm-search-with-github-commit-api'),
    }
    for name, (source, _) in cases.items():
        (variants / name).write_text(source)
    variant_files = scan([variants / name for name in cases])
    for name, (_, expected) in cases.items():
        matched = findings([f for f in variant_files if f['path'].endswith('/' + name)])
        if expected not in matched:
            failures.append((name, expected))
        print('PASS' if expected in matched else 'FAIL', 'renamed/structural variant:', name, flush=True)
    result = {'sample_sha256': coverage['sample_sha256'], 'scope': coverage['scope'],
              'items': results, 'control_files': len(controls), 'control_high_findings': high,
              'control_inputs': sum(1 for p in (HERE / 'controls').rglob('*') if p.is_file()),
              'variant_cases': len(cases), 'failures': failures,
              'findings': [{'path': f['path'], 'traits': f.get('traits', [])} for f in files]}
    if args.report:
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    if failures:
        raise SystemExit(json.dumps(failures, indent=2))
    print('PASS all coverage assertions and controls', flush=True)


if __name__ == '__main__':
    main()
