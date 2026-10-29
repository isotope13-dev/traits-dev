#!/usr/bin/env python3
"""Check generic archive evidence and PR-input shell interpolation risk."""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='../cleave/target/release/cleave')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    cleave = str(Path(args.cleave).resolve())

    def fixture(level, name):
        return (root / 'testdata' / level / 'go-archive-semantics' / name).read_text()

    base_workflow = '''name: Check metadata
on: pull_request
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - run: echo "${{ github.event.pull_request.title }}"
'''
    safe_workflow = '''name: Check metadata
on: pull_request
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - env:
          TITLE: ${{ github.event.pull_request.title }}
        run: ./validate-title.sh "$TITLE"
'''
    uuid = '0123456789abcdef0123456789abcdef'
    cases = {
        'invoice.java': fixture('notable', 'InvoiceService.java'),
        'header-name.java': 'class Labels { String name = "setHeaders"; }\n',
        'uuid.json': fixture('notable', 'compact-uuid.json'),
        'uuid-upper.json': json.dumps({'uuid': uuid.upper()}) + '\n',
        'uuid-short.json': json.dumps({'uuid': uuid[:-1]}) + '\n',
        'runtime-share.nix': fixture('notable', 'runtime-share.nix'),
        'route.js': 'const route = {"endpoint": "/run/task"};\n',
        'random.js': fixture('notable', 'random-choice.js'),
        'random.ts': 'const selected: boolean = Math.random()>0.5;\n',
        'random-comment.js': '// Math.random() > 0.5\n',
        'random-string.js': 'const docs = "Math.random() > 0.5";\n',
        'dash-single.js': fixture('baseline', 'dash-array.js'),
        'dash-double.js': 'const labels = ["-"];\n',
        'dash-comment.js': 'const labels = [/* label */ "-"];\n',
        'dash-extra.js': 'const labels = ["-", "next"];\n',
        'dash-string.js': 'const docs = "labels = [\'-\']";\n',
        'config-env.go': 'package schema\nconst name = "Config.Env"\n',
        'collection-name.go': 'package schema\nconst name = "TargetCollectionID"\n',
        'query.py': 'def search(data):\n    return data.get("query")\n',
        'q.py': "def search(data):\n    return data.get(\n        'q', None\n    )\n",
        'query-string.py': "guide = '.get(\"query\")'\n",
        'query-comment.py': '# data.get("query")\n',
        'config.sh': '#!/bin/sh\ncurl -fsS https://example.invalid/config\n',
        'repository.go': 'package docs\nconst source = "https://github.com/example/project/poc/demo"\n',
        'postgres.sh': '#!/bin/sh\nservice postgresql stop\n',
        'sshd.sh': '#!/bin/sh\necho "Review PermitRootLogin before deployment"\n',
        'advisory.md': '# CVE-2023-4911 reference\n',
        'rnd.js': 'const address = "https://example.invalid/service?rnd=" + counter;\n',
        'tr-fragment.js': 'const fragment = \'tr+"\';\n',
        'node-options.js': 'const options = { windowsHide: true };\n',
        'usage.c': 'const char *usage = "GET <http address> <save as>";\n',
        'PKG-INFO': 'Metadata-Version: 2.1\nName: audited-helper\nVersion: 1.2.3\nSummary: Protect application data\nAuthor: Example Maintainers\nAuthor-email: maintainers@example.invalid\nHome-page: https://example.invalid/project\nLicense: MIT\n\nA documented utility.\n',
        'pr-scalar.yml': base_workflow,
        'pr-map.yml': base_workflow.replace('on: pull_request', 'on:\n  pull_request: {}'),
        'pr-array.yml': base_workflow.replace('on: pull_request', 'on: [pull_request]'),
        'pr-target.yml': base_workflow.replace('on: pull_request', 'on:\n  pull_request_target: {}'),
        'pr-target-scalar.yml': base_workflow.replace('on: pull_request', 'on: pull_request_target'),
        'pr-target-array.yml': base_workflow.replace('on: pull_request', 'on: [pull_request_target]'),
        'pr-body.yml': base_workflow.replace('pull_request.title', 'pull_request.body'),
        'pr-safe-env.yml': safe_workflow,
        'push-only.yml': base_workflow.replace('on: pull_request', 'on: push'),
        'pr-real.yml': fixture('suspicious', 'workflow-reference.yml'),
    }
    with tempfile.TemporaryDirectory(prefix='archive-semantics-') as work:
        stage = Path(work) / 'source'
        stage.mkdir()
        for name, source in cases.items():
            (stage / name).write_text(source)
        proc = subprocess.run([cleave, '--traits-dir', str(root), '--format', 'jsonl', *[str(stage / name) for name in cases]],
                              capture_output=True, text=True, check=True)
        assert 'skipped' not in proc.stderr.lower(), proc.stderr
        reports = [json.loads(line) for line in proc.stdout.split('\n') if line]
        files = {Path(f['path']).name: f for r in reports for f in r['files']
                 if f['path'] in {str(stage / name) for name in cases}}
        assert files.keys() == cases.keys(), (files.keys(), cases.keys())

        def ids(name):
            return {t['id'] for t in files[name].get('traits', [])}

        def require(name, *wanted):
            assert set(wanted) <= ids(name), (name, set(wanted) - ids(name))

        def reject(name, *unwanted):
            assert not set(unwanted) & ids(name), (name, set(unwanted) & ids(name))

        require('invoice.java', 'micro-behaviors/data/property/assign::java-set-headers-helper-call')
        reject('header-name.java', 'micro-behaviors/data/property/assign::java-set-headers-helper-call')
        compact = 'micro-behaviors/data/format/uuid::compact-uuid-field'
        require('uuid.json', compact)
        require('uuid-upper.json', compact)
        reject('uuid-short.json', compact)
        path = 'metadata/lang/source/syntax/key-value::run-prefix-path-field'
        require('runtime-share.nix', path)
        require('route.js', path)
        random = 'micro-behaviors/os/random/prng/stdlib::math-random-half-comparison'
        require('random.js', random)
        require('random.ts', random)
        reject('random-comment.js', random)
        reject('random-string.js', random)
        dash = 'metadata/lang/source/syntax/array::single-dash-array-literal'
        for name in ['dash-single.js', 'dash-double.js', 'dash-comment.js']:
            require(name, dash)
        for name in ['dash-extra.js', 'dash-string.js']:
            reject(name, dash)
        require('config-env.go', 'micro-behaviors/os/env/config::config-env-field-reference')
        require('collection-name.go', 'metadata/lang/source/naming/setting::target-collection-id-name')
        query = 'micro-behaviors/data/collection/map::python-get-query-key'
        require('query.py', query)
        require('q.py', query)
        reject('query-string.py', query)
        reject('query-comment.py', query)
        require('config.sh', 'micro-behaviors/communications/http/client/exchange::cli-config-url-reference')
        require('repository.go', 'micro-behaviors/communications/url/path::forge-security-term-url')
        require('postgres.sh', 'micro-behaviors/os/service/stop::postgresql-stop-command')
        require('sshd.sh', 'micro-behaviors/communications/ssh/server::permit-root-login-reference')
        require('advisory.md', 'metadata/package/documentation/security-advisory::glibc-tunables-cve-reference')
        rnd = 'micro-behaviors/communications/http/query::rnd-query-parameter'
        require('rnd.js', rnd)
        reject('tr-fragment.js', rnd)
        require('node-options.js', 'micro-behaviors/process/create/hidden::node-windowshide-true-option')
        require('usage.c', 'micro-behaviors/ui/help::get-saveas-usage')
        require('PKG-INFO', 'metadata/package/documentation/claims::pkginfo-protection-wording')
        risk = 'micro-behaviors/process/create/shell/injection::github-pr-command-interpolation'
        risky = {'pr-scalar.yml', 'pr-map.yml', 'pr-array.yml', 'pr-target.yml', 'pr-target-scalar.yml',
                 'pr-target-array.yml', 'pr-body.yml', 'pr-real.yml'}
        for name in risky:
            require(name, risk)
        reject('pr-safe-env.yml', risk)
        reject('push-only.yml', risk)
        for name, report in files.items():
            high = {t['id'] for t in report.get('traits', []) if t['crit'] >= 4}
            expected = {risk} if name in risky else set()
            if name == 'pr-target.yml':
                expected.add('objectives/supply-chain/trojanized/ci-pipeline::gha-pr-target-shell-injection')
            assert high == expected, (name, high)
        old_prefixes = ('well-known/malware/rat/sparkrat::spark-config-uuid-field',
                        'objectives/command-and-control/backdoor/webshell/client::java-webshell-header-editor',
                        'objectives/lateral-movement/delivery/update-service/software-update::sccm-target-collection-field',
                        'objectives/impact/spam::whatsapp-random-synonym-selection')
        for name in cases:
            reject(name, *old_prefixes)
    print(f'Go archive semantic regressions passed: {len(cases)} controls; no sample code executed')


if __name__ == '__main__':
    main()
