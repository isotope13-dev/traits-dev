"""Check moved behavior, registry near misses, and rebase conflict controls."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

root = Path(__file__).resolve().parents[3]
here = Path(__file__).resolve().parent
manifests = [here / 'cases.json',
             root / 'testdata/triage/threats2-controls/cases.json',
             root / 'testdata/toga-release-triage/cases.json']
cases = [case for manifest in manifests
         for case in json.loads(manifest.read_text())['fixtures']]


def selects(selector, trait):
    if selector.endswith('/'):
        return (trait.split('::')[0] + '/').startswith(selector)
    return selector == trait


with tempfile.TemporaryDirectory(prefix='run-key-check-', dir='/tmp') as work:
    work = Path(work)
    paths = []
    env = dict(os.environ, CLEAVE_SKIP_CACHE='1')
    for index, case in enumerate(cases):
        source = root / case['path']
        directory = work / str(index)
        directory.mkdir()
        target = directory / source.name
        if case.get('compile'):
            target = target.with_suffix('.elf')
            build_env = dict(env, GOOS='linux', GOARCH='amd64',
                             CGO_ENABLED='0', GOWORK='off',
                             GOCACHE=str(work / 'go-cache'))
            subprocess.run(['go', 'build', '-o', str(target), str(source)],
                           env=build_env, check=True)
        elif case.get('replace_class_bytes'):
            old, new = case['replace_class_bytes']
            assert len(old.encode()) == len(new.encode())
            count = 0
            with zipfile.ZipFile(source) as archive, zipfile.ZipFile(target, 'w') as changed:
                for entry in archive.infolist():
                    data = archive.read(entry)
                    if entry.filename.endswith('.class'):
                        count += data.count(old.encode())
                        data = data.replace(old.encode(), new.encode())
                    changed.writestr(entry, data)
            assert count, 'Counterfactual must change a class string'
        else:
            shutil.copyfile(source, target)
        paths.append(str(target))
    result = subprocess.run(
        [os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave')),
         '--traits-dir', str(root), '--format', 'json', *paths],
        env=env, capture_output=True, text=True, check=True)
    decoder = json.JSONDecoder()
    pos = 0
    actual = {}
    while pos < len(result.stdout):
        while pos < len(result.stdout) and result.stdout[pos].isspace():
            pos += 1
        if pos == len(result.stdout):
            break
        report, pos = decoder.raw_decode(result.stdout, pos)
        for file in report['files']:
            actual[file['path']] = {t['id'] for t in file.get('traits', [])}
    observations = []
    for case, path in zip(cases, paths):
        found = actual.get(path, set())
        missing = [s for s in case['matched'] if not any(selects(s, t) for t in found)]
        unexpected = sorted(t for t in found
                            if any(selects(s, t) for s in case['not_matched']))
        failed = bool(missing or unexpected or path not in actual)
        name = case.get('case_id', Path(case['path']).name)
        print(name, 'FAIL' if failed else 'PASS', flush=True)
        observations.append({'case': name, 'passed': not failed,
                             'missing': missing, 'unexpected': unexpected})
    (here / 'observed.json').write_text(json.dumps(observations, indent=2) + '\n')
    if any(not item['passed'] for item in observations):
        raise SystemExit(json.dumps([i for i in observations if not i['passed']], indent=2))
