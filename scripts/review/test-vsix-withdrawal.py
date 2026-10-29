#!/usr/bin/env python3
"""Offline withdrawal regressions: provider facts, archive boundaries and follow.

Run with Python 3 and zstd installed. No sample code is executed. The follow
cases feed synthetic npm responses through an isolated Fletch cache, exercising
the real registry normalizer, age gate, missing-artifact path and manifest
attribution. Unresolved names have no invented removal or security facts.
"""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PREFIX = 'objectives/supply-chain/security-hold::'
REMOVED = PREFIX + 'registry-security-withdrawn-package-coordinate'
REASON = PREFIX + 'registry-security-withdrawn-deprecation'
MANIFEST = PREFIX + 'npm-security-holder-manifest'
DEPENDENCY = PREFIX + 'declared-dependency-security-held'
HOLDER = {'name': 'withdrawal-holder', 'version': '0.0.1-security',
          'repository': 'npm/security-holder'}


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--atomscan', default=str(ROOT.parent / 'scan/target/release/atomscan'))
    parser.add_argument('--work-dir', type=Path, required=True)
    args = parser.parse_args()
    work = args.work_dir.resolve()
    work.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(CLEAVE_TRAITS_DIR=str(ROOT), CLEAVE_SKIP_MAPPER_CACHE='1',
               CLEAVE_CACHE_DIR=str(work / 'cleave-cache'),
               XDG_CACHE_HOME=str(work / 'xdg'), CLEAVE_RAYON_THREADS='4',
               RAYON_NUM_THREADS='4', SCAN_FOLLOW='none', SCAN_REGISTRY_TTL='never',
               HTTP_PROXY='http://127.0.0.1:9', HTTPS_PROXY='http://127.0.0.1:9',
               ALL_PROXY='http://127.0.0.1:9', NO_PROXY='')
    registry = {'ecosystem': 'npm', 'name': 'withdrawal-fixture', 'version': '1.0.0'}
    cases = []

    def add(name, data, expected, required=(), forbidden=(), manifest=False):
        path = work / 'inputs' / name / ('package.json' if manifest else name + '.registry.json')
        dump(path, data)
        cases.append(dict(name=name, path=path, hostile=expected,
                          required=set(required), forbidden=set(forbidden)))

    add('security-held-removed-release', registry | {'security_hold': True,
        'version_removed': True, 'description': 'security holding package'}, True, [REMOVED])
    add('security-hold-flag-only', registry | {'security_hold': True}, True,
        [PREFIX + 'registry-security-held-package'])
    add('golang-security-withheld-coordinate', registry | {'ecosystem': 'golang',
        'security_hold': True}, True, [PREFIX + 'registry-security-held-package'])
    add('security-holder-description-only', registry | {'description': 'security holding package'},
        True, [PREFIX + 'registry-security-held-package'])
    # Policy includes the inert stub; assert its status, without inventing
    # historical removal or implying execution of a malicious payload.
    add('inert-holder-still-listed', registry | {'version': '0.0.1-security',
        'security_hold': True, 'version_removed': False, 'description': 'security holding package'},
        True, forbidden=[REMOVED])
    for name, ecosystem, reason in [
        ('npm-security-before-removal', 'npm', 'security withdrawal: malicious code'),
        ('npm-security-after-removal', 'npm', 'removed for security reasons'),
        ('pypi-security-yank', 'pypi', 'Yanked for security reasons'),
        ('crates-security-yank', 'crates', 'Security issue; yanked'),
        ('pypi-verbatim-malware-yank', 'pypi', 'malware'),
        ('npm-explicit-malicious-deprecation', 'npm', 'This package contained malicious code.'),
        ('removed-for-malicious-code', 'npm', 'Removed due to malicious code'),
        ('unpublished-for-security', 'npm', 'Unpublished for security reasons'),
        ('malware-before-unpublish', 'npm', 'Malware found; unpublished'),
    ]:
        add(name, registry | {'ecosystem': ecosystem, 'deprecated': reason}, True, [REASON])
    for name, extra in [
        ('unspecified-unpublish', {'version_removed': True}),
        ('ordinary-deprecation', {'deprecated': 'Use the maintained v2 instead'}),
        ('vulnerability-warning-without-withdrawal', {'deprecated': 'Known security vulnerability; upgrade'}),
        ('unspecified-yank', {'deprecated': 'Yanked: packaging error'}),
        ('security-hold-false', {'security_hold': False, 'version_removed': False}),
        ('unknown-status', {}),
        ('security-holder-mention', {'description': 'Documentation about security holding package status'}),
        ('negated-malware-warning', {'deprecated': 'Not malware; use the maintained version'}),
    ]:
        add(name, registry | extra, False)
    add('holder-manifest-string-repository', HOLDER, True, [MANIFEST], manifest=True)
    add('holder-manifest-object-repository', HOLDER | {'repository': {
        'type': 'git', 'url': 'git+https://github.com/npm/security-holder.git'}},
        True, [MANIFEST], manifest=True)
    add('holder-version-alone', {'name': 'ordinary', 'version': '0.0.1-security'}, False, manifest=True)
    add('holder-repository-alone', {'name': 'ordinary', 'version': '1.0.0',
        'repository': 'npm/security-holder'}, False, manifest=True)
    add('holder-description-alone-in-manifest', {'name': 'ordinary', 'version': '1.0.0',
        'description': 'security holding package'}, False, manifest=True)

    def archive(name, members, expected, required=(), forbidden=()):
        path = work / 'inputs' / (name + '.zip')
        path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(path, 'w') as archive_file:
            for member, value in members.items():
                archive_file.writestr(member, json.dumps(value))
        cases.append(dict(name=name, path=path, hostile=expected,
                          required=set(required), forbidden=set(forbidden)))

    archive('vendored-holder', {'vendor/held/package.json': HOLDER}, True, [MANIFEST])
    archive('holder-legs-in-different-members', {
        'a/package.json': {'name': 'a', 'version': '0.0.1-security'},
        'b/package.json': {'name': 'b', 'version': '1.0.0', 'repository': 'npm/security-holder'}},
        False, forbidden=[MANIFEST])
    archive('registry-removal-and-hold-on-different-dependencies', {
        'a.registry.json': registry | {'security_hold': True, 'description': 'security holding package'},
        'b.registry.json': registry | {'name': 'other', 'version_removed': True}},
        True, forbidden=[REMOVED])

    results = []

    def run(batch, follow):
        phase = 'follow' if follow else 'static'
        command = [args.atomscan, '--no-update', '--analyze', 'local', '--mode', 'slow',
                   '--format=json', '--follow=' + ('dependencies' if follow else 'none'),
                   '--follow-depth=1', '--fetch-timeout=15s', '--fetch-max-age=7']
        command.extend(str(case['path']) for case in batch)
        started = time.monotonic()
        with (work / (phase + '.stderr')).open('wb') as err:
            proc = subprocess.run(command, env=env, stdout=subprocess.PIPE, stderr=err, timeout=300)
        with gzip.open(work / (phase + '.jsonl.gz'), 'wb') as f:
            f.write(proc.stdout)
        assert proc.returncode in (0, 1, 2), (phase, proc.returncode)
        reports = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
        by_sha = {r['raw']['files'][0]['sha']: r for r in reports}
        for case in batch:
            sha = hashlib.sha256(case['path'].read_bytes()).hexdigest()
            report = by_sha[sha]
            files = report['raw']['files']
            traits = {t['id']: t for f in files for t in f.get('traits', [])}
            hostile = {name for name, trait in traits.items() if trait.get('crit') == 5}
            actual = bool(hostile)
            missing = case['required'] - set(traits)
            forbidden = case['forbidden'] & set(traits)
            ok = actual == case['hostile'] and not missing and not forbidden
            if follow and case['hostile']:
                # No fetched payload is needed for a removed dependency:
                # the exact declaring manifest must carry the hostile fact.
                declaring = [f for f in files if f['path'].endswith(case.get('declarer', 'package.json'))]
                declaring_ids = {t['id'] for f in declaring for t in f.get('traits', [])
                                 if t.get('crit') == 5}
                ok = ok and DEPENDENCY in declaring_ids
            row = dict(name=case['name'], phase=phase, passed=ok,
                       expected_hostile=case['hostile'], hostile=sorted(hostile),
                       missing=sorted(missing), forbidden=sorted(forbidden),
                       ml=report.get('ml'), files=len(files))
            results.append(row)
            print(json.dumps({k: v for k, v in row.items() if k != 'ml'}), flush=True)
        print(phase, 'seconds', round(time.monotonic() - started, 1), flush=True)

    run(cases, False)

    def cache_metadata(url, value, status=200):
        # Fletch's public on-disk cache format, isolated from all user caches.
        key = hashlib.sha256(('meta:' + url).encode()).hexdigest()
        directory = work / 'xdg/fletch/refs' / key[:2]
        directory.mkdir(parents=True, exist_ok=True)
        body = json.dumps(value).encode()
        compressed = subprocess.run(['zstd', '-q', '-c'], input=body,
                                    stdout=subprocess.PIPE, check=True).stdout
        (directory / (key + '.zst')).write_bytes(compressed)
        dump(directory / (key + '.json'), dict(fetched_at=int(time.time()), status=status,
             final_url=url, redirects=[], headers=[['content-type', 'application/json']], size=len(body)))

    follow_cases = []
    for name, security, removed, known in [
        ('removed-security-held-dependency', True, True, True),
        ('removed-without-security-reason', False, True, True),
        ('still-listed-ordinary-dependency', False, False, True),
        ('never-published-version', False, True, False),
        ('private-or-unknown-package', False, None, False),
    ]:
        package = 'withdrawal-regression-' + name
        path = dump(work / 'follow-inputs' / name / 'package.json',
                    {'name': 'consumer-' + name, 'version': '1.0.0',
                     'dependencies': {package: '1.0.0'}})
        document = {'name': package, 'maintainers': [{'name': 'fixture-maintainer'}],
                    'dist-tags': {'latest': '0.0.1-security' if security else '2.0.0'},
                    'description': 'security holding package' if security else 'Ordinary library',
                    'versions': {}, 'time': {'created': '2020-01-01T00:00:00.000Z'}}
        if known:
            document['time']['1.0.0'] = '2020-01-01T00:00:00.000Z'
        if removed is False:
            document['versions']['1.0.0'] = {'name': package, 'version': '1.0.0'}
        if removed is None:
            document = {'error': 'Not found'}
        cache_metadata('https://registry.npmjs.org/' + package, document)
        cache_metadata('https://api.npmjs.org/downloads/point/last-month/' + package, {'downloads': 10})
        follow_cases.append(dict(name=name, path=path, hostile=security,
                                 required={DEPENDENCY, REMOVED} if security else set(), forbidden=set()))
        if security:
            vsix_path = path.parent / 'consumer.vsix'
            manifest = json.loads(path.read_text()) | {'publisher': 'regression',
                        'engines': {'vscode': '^1.90.0'}, 'main': './extension.js'}
            with zipfile.ZipFile(vsix_path, 'w') as archive_file:
                archive_file.writestr('extension/package.json', json.dumps(manifest))
                archive_file.writestr('extension/extension.js', 'exports.activate = () => {};\n')
            follow_cases.append(dict(name='vsix-declares-removed-security-held-dependency',
                path=vsix_path, hostile=True, required={DEPENDENCY, REMOVED}, forbidden=set(),
                declarer='!!extension/package.json'))
    # Recorded refusal/failure responses and a cold-cache transport failure
    # must not acquire registry.security_hold or version_removed. A 404 never
    # proves previous publication; 403/429/5xx never prove a security takedown.
    for name, status in [('private-package-404', 404), ('unknown-package-410', 410),
                         ('npm-permission-denied-403', 403), ('registry-rate-limit-429', 429),
                         ('registry-unavailable-503', 503), ('transport-failure', None)]:
        package = 'withdrawal-regression-' + name
        path = dump(work / 'follow-inputs' / name / 'package.json',
                    {'name': 'consumer-' + name, 'version': '1.0.0',
                     'dependencies': {package: '1.0.0'}})
        if status is not None:
            cache_metadata('https://registry.npmjs.org/' + package,
                           {'error': name}, status=status)
        follow_cases.append(dict(name=name, path=path, hostile=False,
                                 required=set(), forbidden={DEPENDENCY, REMOVED}))
    run(follow_cases, True)
    summary = dict(scenarios=len(results), passed=sum(r['passed'] for r in results),
                   atomscan=args.atomscan, traits=str(ROOT), results=results)
    dump(work / 'results.json', summary)
    assert summary['passed'] == summary['scenarios'], 'Withdrawal regression failed; see results.json'
    print('PASS', summary['passed'], 'withdrawal scenarios', flush=True)


if __name__ == '__main__':
    main()
