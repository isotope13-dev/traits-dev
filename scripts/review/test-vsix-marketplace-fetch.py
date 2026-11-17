#!/usr/bin/env python3
"""Exercise VSIX dependency outcomes with synthetic Marketplace responses.

Requires a trusted Fletch cache directory and zstd. A cache miss can reach the
network: run under network restriction when that must be prevented.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import time
import zipfile

ROOT = Path(__file__).resolve().parents[2]
QUERY = 'https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery'
MISSING = 'objectives/supply-chain/hidden-payload/extensions/vscode::vscode-requires-unavailable-extension'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--atomscan', required=True)
    parser.add_argument('--work-dir', type=Path, required=True)
    args = parser.parse_args()
    work = args.work_dir.resolve()
    work.mkdir(parents=True, exist_ok=True)
    module_path = ROOT / 'scripts/review/test-vsix-withdrawal.py'
    spec = importlib.util.spec_from_file_location('withdrawal_json_full', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    env = os.environ.copy()
    env.pop('SCAN_LLM', None)
    env.pop('SCAN_HOPPER', None)
    env.update(CLEAVE_TRAITS_DIR=str(ROOT), XDG_CACHE_HOME=str(work / 'xdg'),
               CLEAVE_CACHE_DIR=str(work / 'cleave-cache'), SCAN_REGISTRY_TTL='never',
               CLEAVE_RAYON_THREADS='2', RAYON_NUM_THREADS='2')
    cases = [('absent', {'results': [{'extensions': []}]}, True),
             ('invalid', {'message': 'temporary upstream error'}, False)]
    paths, mtimes = {}, {}
    for label, answer, _ in cases:
        extension_id = 'fixture.' + label
        body = json.dumps({'filters': [{'criteria': [{'filterType': 7, 'value': extension_id}]}],
                           'flags': 257}, separators=(',', ':')).encode()
        headers = [('Content-Type', 'application/json'),
                   ('Accept', 'application/json;api-version=3.0-preview.1')]
        cache_key = f'post:{len(QUERY)}:{QUERY}'
        for key, value in headers:
            cache_key += f'|{len(key)}:{key}{len(value)}:{value}'
        cache_key += '|body:' + hashlib.sha256(body).hexdigest()
        digest = hashlib.sha256(cache_key.encode()).hexdigest()
        directory = work / 'xdg/fletch/refs' / digest[:2]
        directory.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(answer).encode()
        blob = directory / (digest + '.zst')
        blob.write_bytes(subprocess.run(['zstd', '-q', '-c'], input=payload,
                                        stdout=subprocess.PIPE, check=True).stdout)
        sidecar = directory / (digest + '.json')
        sidecar.write_text(json.dumps({'fetched_at': int(time.time()), 'status': 200,
                                      'final_url': QUERY, 'redirects': [],
                                      'headers': [['content-type', 'application/json']],
                                      'size': len(payload)}))
        old = time.time() - 2 * 86400
        os.utime(blob, (old, old))
        os.utime(sidecar, (old, old))
        mtimes[label] = (blob, old)
        path = work / (label + '.vsix')
        manifest = {'name': label, 'publisher': 'regression', 'version': '1.0.0',
                    'engines': {'vscode': '^1.90.0'}, 'main': './extension.js',
                    'extensionDependencies': [extension_id]}
        with zipfile.ZipFile(path, 'w') as archive:
            archive.writestr('extension/package.json', json.dumps(manifest))
            archive.writestr('extension/extension.js', 'exports.activate = () => {};\n')
        paths[label] = path
    command = [args.atomscan, '--no-update', '--analyze', 'local', '--mode', 'slow',
               '--format=json-full', '--all-members', '--follow=dependencies', '--follow-depth=1']
    command.extend(str(path) for path in paths.values())
    result = subprocess.run(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            timeout=180, check=False)
    (work / 'results.jsonl').write_bytes(result.stdout)
    (work / 'stderr.log').write_bytes(result.stderr)
    assert result.returncode in (0, 1, 2) and result.stdout.strip(), result.stderr.decode(errors='replace')
    reports = {r['sha']: r for r in module.json_full_documents(result.stdout)}
    for label, _, expected in cases:
        blob, old = mtimes[label]
        assert blob.stat().st_mtime > old + 86400, f'{label}: synthetic cache entry was not read'
        sha = hashlib.sha256(paths[label].read_bytes()).hexdigest()
        report = reports[sha]
        manifest = [f for f in report['files'] if f['path'].endswith('!!extension/package.json')]
        assert len(manifest) == 1 and manifest[0]['analyzed'], f'{label}: manifest was not analyzed'
        ids = {trait['id'] for trait in manifest[0]['traits']}
        assert (MISSING in ids) == expected, f'{label}: missing-dependency finding = {MISSING in ids}'
        verdict = (report.get('verdict') or {}).get('class', 'unknown')
        print(label, 'missing-dependency finding:', MISSING in ids,
              'overall verdict:', verdict, flush=True)
    print('PASS synthetic Marketplace outcomes', flush=True)


if __name__ == '__main__':
    main()
