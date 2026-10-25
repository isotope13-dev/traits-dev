#!/usr/bin/env python3
"""Static matcher controls; generated fixtures are never executed."""
import argparse
import json
import os
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
parser = argparse.ArgumentParser()
parser.add_argument('--traits', type=Path, default=ROOT)
parser.add_argument('--output', type=Path)
parser.add_argument('--baseline', action='store_true')
parser.add_argument('--scratch', type=Path, default=ROOT)
args = parser.parse_args()
storage = 'micro-behaviors/data/db/web-storage::'
audio = 'micro-behaviors/hardware/input/audio::web-audio-create-oscillator'
cache = 'micro-behaviors/communications/http/header/cache::'
name = 'metadata/package/name/identity::cacheable-request-name'
signature = 'metadata/signed/platform::chrome-webstore-signature-header'
old_signature = 'metadata/permission/manifest::chrome-webstore-verified-contents'
old_identity = {'well-known/lib/network/cacheable-request::package-name',
                'well-known/lib/network/cacheable-request::cacheable-request-library'}
new_calls = {storage + 'dom-storage-removeitem-call',
             storage + 'extension-storage-change-listener', audio,
             cache + 'cache-policy-revalidation-headers',
             cache + 'cache-policy-response-headers'}
cases = {}
with tempfile.TemporaryDirectory(dir=args.scratch) as directory:
    temp = Path(directory)
    def source(label, content, required=(), forbidden=()):
        p = temp / label
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        cases[label] = (p, set(required), set(forbidden))
    source('browser-calls.js', '''
        chrome.storage.onChanged.addListener(changes => render(changes));
        browser.storage.onChanged.addListener(refresh);
        localStorage.removeItem('setting');
        window.sessionStorage.removeItem('temporary');
        const oscillator = context.createOscillator();
    ''', [storage + 'dom-storage-removeitem-call',
          storage + 'extension-storage-change-listener', audio])
    source('cache-calls.js', '''
        const headers = policy.revalidationHeaders(request);
        const cachedHeaders = policy.responseHeaders();
    ''', [cache + 'cache-policy-revalidation-headers',
          cache + 'cache-policy-response-headers'])
    source('uncalled.js', '''
        // chrome.storage.onChanged.addListener(refresh);
        // localStorage.removeItem('setting');
        // context.createOscillator(); policy.responseHeaders();
        // policy.revalidationHeaders(request);
        const messages = ['localStorage.removeItem("setting")',
                          'context.createOscillator()'];
        const api = { responseHeaders() {}, revalidationHeaders() {},
                      createOscillator() {}, removeItem() {} };
        const listener = chrome.storage.onChanged.addListener;
    ''', forbidden=new_calls)
    source('claimed-name/package.json', '{"name":"cacheable-request","version":"9.9.9"}',
           [name], old_identity)
    source('signature-header.json', json.dumps({'root': []}), forbidden=[signature])
    signature_data = [{'signed_content': {'payload': 'e30=', 'signatures': [
        {'header': {'kid': 'webstore'}, 'protected': 'e30=', 'signature': 'unverified'}]}}]
    source('asserted-signature.json', json.dumps(signature_data), [signature])
    manifest = {'manifest_version': 3, 'name': 'Static control', 'version': '1.0',
                'permissions': ['tabCapture', 'webRequest', 'tabs'],
                'host_permissions': ['<all_urls>'],
                'background': {'service_worker': 'worker.js'}}
    capture = 'objectives/supply-chain/hidden-payload/extensions/permission::all-url-capture-request-extension'
    for label, member, content, required, forbidden in [
        ('name-only.zip', '_metadata/verified_contents.json', '{}', [capture], [signature]),
        ('renamed-header.zip', 'integrity.json', json.dumps(signature_data), [signature, capture], []),
    ]:
        p = temp / label
        with zipfile.ZipFile(p, 'w') as z:
            z.writestr('manifest.json', json.dumps(manifest))
            z.writestr(member, content)
            z.writestr('worker.js', '// static fixture\n')
        cases[label] = (p, set(required), set(forbidden))
    existing = {
        'relay.js': ('testdata/hostile/gameograf-signing-review/response-relay.js',
                     'objectives/command-and-control/backdoor/proxy/websocket::channel-controlled-http-response-relay'),
        'breakout.js': ('testdata/gauntlet-missed-controls/remote-feed-breakout.js',
                       'objectives/execution/exploit/remote-feed-xss::json-link-markup-with-breakout-payload'),
    }
    for label, (relative, required) in existing.items():
        source(label, (ROOT / relative).read_text(), [required])
    proc = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(args.traits),
                           '--json', *[str(p) for p, _, _ in cases.values()]],
                          check=True, text=True, capture_output=True)
    decoder = json.JSONDecoder()
    rest = proc.stdout.lstrip()
    reports = []
    while rest:
        obj, end = decoder.raw_decode(rest)
        reports.append(obj)
        rest = rest[end:].lstrip()
    roots = {r['files'][0]['path']: r for r in reports}
    results = {}
    for label, (path, required, forbidden) in cases.items():
        report = roots[str(path)]
        traits = {t['id']: t['crit'] for t in report['files'][0].get('traits', [])}
        results[label] = traits
        if not args.baseline:
            assert required <= traits.keys(), (label, 'missing', required - traits.keys())
            assert not forbidden & traits.keys(), (label, 'unexpected', forbidden & traits.keys())
    if not args.baseline:
        assert results['name-only.zip'][capture] == 4
        assert results['renamed-header.zip'][capture] == 5
    if args.output:
        args.output.write_text(json.dumps(results, indent=2) + '\n')
    print(f'{len(cases)} static controls analyzed' + (' (baseline)' if args.baseline else ' and passed'))
