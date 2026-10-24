#!/usr/bin/env python3
"""Static regression checks; never execute specimens or contact their endpoints."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--scratch', type=Path, required=True)
parser.add_argument('--attack', type=Path)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
args.scratch.mkdir(parents=True, exist_ok=True)
password = 'micro-behaviors/data/format/credentials::password-labelled-value-concatenation'
encoder = 'micro-behaviors/data/encode/base64::base64-shifted-character-encoder'
lookup = 'micro-behaviors/data/string/access::char-at-right-shift-two'
security = 'micro-behaviors/communications/http/ws-security::ws-security-username-password-fields'
exfil = 'objectives/exfiltration/messaging/telegram::browser-password-report-telegram-post'
lure = 'objectives/credential-access/phishing/lure::email-password-telegram-false-retry'
concealed = 'objectives/anti-static/obfuscation/eval/browser::base64-document-writer-conceals-password-harvest'
retired = {
    'objectives/exfiltration/messaging/telegram::browser-plaintext-password-report-field',
    'micro-behaviors/communications/http/ws-trust::ws-trust-username-field',
    'micro-behaviors/communications/http/ws-trust::ws-trust-password-field',
    'micro-behaviors/communications/http/ws-trust::ws-trust-username-password-fields',
    'micro-behaviors/communications/http/ws-trust::ws-security-username-token-element',
    'micro-behaviors/communications/http/request/params::browser-device-profile-request-fields--identity',
}
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
token = '<o:UsernameToken><o:Username>alice</o:Username><o:Password>value</o:Password></o:UsernameToken>'
cases = {}

def add(name, source, required=None, absent=(), maximum=3):
    path = args.scratch / name
    path.write_text(source)
    cases[str(path)] = (required or {}, set(absent) | retired, maximum)

add('dom-id.js', 'const p = this.shadowRoot.getElementById("new-password-" + suffix);', absent=[password, exfil])
add('report.js', 'const message = "Password: " + typedValue;', {password: 3}, [exfil])
add('report-renamed.js', "const report = 'PASSWORD: ' + otherInput;", {password: 3}, [exfil])
add('encoded-query.js', 'const request = "password=" + encodeURIComponent(this._base64(this._password));', {password: 3}, [exfil])
add('label-only.js', 'const label = "Password:";', absent=[password, exfil])
add('unrelated-value.js', 'const report = "Status: " + value;', absent=[password, exfil])
add('soap.js', 'const envelope = ' + json.dumps(token) + ';', {security: 3}, [exfil])
add('generic-account-xml.js', 'const record = "<Username>alice</Username><Password>value</Password>";', absent=[security])
add('token-only.js', 'const record = "<o:UsernameToken/>";', absent=[security])
add('ws-trust.js', 'const envelope = ' + json.dumps(token + '<RequestSecurityToken/>') + ';\nconst options={method:"POST"};\nconst endpoint="https://autologon.microsoftazuread-sso.com/test/winauth/trust/2005/usernamemixed";', {
    security: 3,
    'objectives/lateral-movement/brute-force/password/web::ws-trust-credential-submission': 4,
}, maximum=4)
add('encoder.js', 'function encode(bytes) { const table="' + alphabet + '"; return table.charAt(bytes[0] >> 2); }', {encoder: 3, lookup: 3})
add('encoder-renamed.js', 'function convert(octets) { const symbols="' + alphabet + '"; return symbols.charAt(octets[0] >> 2); }', {encoder: 3, lookup: 3})
add('alphabet-only.js', 'const table="' + alphabet + '";', absent=[encoder, lookup])
add('lookup-only.js', 'const result = table.charAt(bytes[0] >> 2);', {lookup: 3}, [encoder])
add('ordinary-lookup.js', 'const table="' + alphabet + '"; const result=table.charAt(index);', absent=[encoder, lookup])
add('quoted-lookup.js', 'const table="' + alphabet + '"; const example="table.charAt(bytes[0] >> 2)";', absent=[encoder, lookup])
add('distant-lookup.js', 'const table="' + alphabet + '";\n' + ' ' * 2000 + 'const result=other.charAt(bytes[0] >> 2);', {lookup: 3}, [encoder])
for name, field, atom in [
    ('query-resource', 'uri=', 'resource-state-query-field'),
    ('query-display', 'screen=', 'location-rendering-query-field'),
    ('query-network', 'wifi=', 'power-connectivity-query-field'),
]:
    add(name + '.js', 'const field=' + json.dumps(field) + ';', {
        'micro-behaviors/communications/http/request/params::' + atom: 3,
    })
add('query-mention.js', 'const label="uri";', absent=['micro-behaviors/communications/http/request/params::client-query-field-prefix'])

if args.attack:
    original = args.attack.read_bytes()
    assert hashlib.sha256(original).hexdigest() == 'cef802016a70b757c624b1b1838ebd1887a341a7fd16c076c75096efc68e17d3'
    outer = original.decode()
    decoded = base64.b64decode(re.search(r'atob\("([A-Za-z0-9+/=]+)"', outer).group(1)).decode()
    add('original-encoded.js', outer, {exfil: 5, lure: 5, concealed: 5}, maximum=5)
    add('original-decoded.html', decoded, {exfil: 5, lure: 5, password: 3}, maximum=5)
    renamed = re.sub(r'\b(passwordInput|messageText|telegramApiUrl|TELEGRAM_CHAT_ID)\b', lambda m: 'changed_' + m.group(), decoded)
    add('original-renamed.html', renamed, {exfil: 5, lure: 5}, maximum=5)
    mutations = {
        'no-label': ("Password: ' + password", "Status: ' + password"),
        'no-bot': ('api.telegram.org/bot', 'example.invalid/bot'),
        'no-password-input': ('type="password"', 'type="text"'),
        'no-post': ("method: 'POST'", "method: 'GET'"),
        'no-chat-id': ('chat_id: TELEGRAM_CHAT_ID', 'destination: TELEGRAM_CHAT_ID'),
    }
    for name, (old, new) in mutations.items():
        assert old in decoded, name
        add(name + '.html', decoded.replace(old, new), absent=[exfil, lure, concealed], maximum=5)

cmd = [args.cleave, '--traits-dir', str(root), '--json', 'analyze', *cases]
result = subprocess.run(cmd, text=True, capture_output=True, env=os.environ.copy())
(args.scratch / 'analysis.jsonl').write_text(result.stdout)
(args.scratch / 'analysis.log').write_text(result.stderr)
assert result.returncode == 0, result.stderr
reports = {f['path']: f for line in result.stdout.splitlines() for f in json.loads(line)['files']}
for path, (required, absent, maximum) in cases.items():
    traits = {t['id']: t['crit'] for t in reports[path].get('traits', [])}
    for ident, crit in required.items():
        assert traits.get(ident) == crit, (path, ident, crit, traits.get(ident))
    assert not absent & traits.keys(), (path, absent & traits.keys())
    assert max(traits.values(), default=0) <= maximum, (path, traits)
    print('PASS', Path(path).name)
print(len(cases), 'boundary controls passed')
