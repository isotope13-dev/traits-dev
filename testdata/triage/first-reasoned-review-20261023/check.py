"""Focused source/format boundaries; no sample code is executed."""
import argparse
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--scratch', type=Path, required=True)
p.add_argument('--atomscan', default='atomscan')
a = p.parse_args()
a.scratch.mkdir(parents=True, exist_ok=True)
inputs = a.scratch / 'inputs'
inputs.mkdir(exist_ok=True)
checks = {}

def case(name, content, required=(), forbidden=()):
    if name.endswith('.html'):
        content = '<!doctype html><html><body>' + content + '</body></html>'
    (inputs / name).write_text(content)
    checks[name] = (required, forbidden)

manifest = 'metadata/build/manifest::'
otp = 'micro-behaviors/ui/window/otp-field::html-otp-input-field'
cache = 'micro-behaviors/fs/path/cache::browser-cache-directory-name'
event = 'micro-behaviors/ui/window/event::dataavailable-event-handler'
token = 'objectives/privilege-escalation/token-manipulation::rust-system-process-token-impersonation'
compare = 'metadata/lang/source/syntax/operator::rust-system-process-name-comparison'
case('eclipse.xml', '<?xml version="1.0"?>\n<?eclipse version="3.5"?>\n<plugin><extension point="org.eclipse.equinox.p2.engine.actions"/></plugin>', [manifest+'eclipse-plugin-descriptor'], [manifest+'jetbrains-plugin-descriptor'])
case('idea.xml', '<idea-plugin xmlns:xi="http://www.w3.org/2001/XInclude"><id>example</id></idea-plugin>', [manifest+'jetbrains-plugin-descriptor'], [manifest+'eclipse-plugin-descriptor'])
case('plugin.xml', '<plugin><name>Generic plugin</name></plugin>', [], [manifest+'jetbrains-plugin-descriptor'])
case('otp.html', '<input name="otp_code">', [otp])
case('mfa.html', '<input id="mfaCode">', [otp])
case('forgot.html', '<input type="submit" value="Log In"><a onclick="showForgotPassword()">Forgot Password</a>', [], [otp])
case('after-tag.html', '<input type="text">MFA', [], [otp])
case('chromium.ps1', "$p = 'C:\\Users\\person\\Chrome\\Cache_Data'", [cache])
case('firefox.ps1', "$p = 'C:\\Users\\person\\Firefox\\cache2'", [cache])
case('cache-name.ps1', "$p = Join-Path $profile 'Cache_Data'", [cache])
case('yui.js', "var CACHE_DATA = 'cacheData';", [], [cache])
case('prototype.js', "element.addEventListener('dataavailable', responder, false);", [event], ['micro-behaviors/data/stream/record::media-stream-recorder'])
case('recorder.js', "var r = new MediaRecorder(stream); r.ondataavailable = save;", [event, 'micro-behaviors/data/stream/record::media-stream-recorder'])
body = 'OpenProcessToken(p,r,o); DuplicateToken(t,l,c); ImpersonateLoggedOnUser(c);'
case('selector.rs', 'fn run() { EnumProcesses(a,b,c); if n == "lsass.exe" { unsafe {'+body+'} } }', [compare, token])
case('names-only.rs', 'fn run() { let names = ["lsass.exe", "winlogon.exe"]; unsafe {'+body+'} }', [], [compare, token])
case('no-enumeration.rs', 'fn run() { if n == "lsass.exe" { unsafe {'+body+'} } }', [compare], [token])
case('comment.rs', '/* fn run() { EnumProcesses(a,b,c); if n == "lsass.exe" {'+body+'} } */', [], [compare, token])

r = subprocess.run([a.atomscan, '--no-update', '--analyze', 'local', '--mode', 'slow', '--follow=none', '-f', 'json', str(inputs)], capture_output=True, text=True)
(a.scratch/'scan.jsonl').write_text(r.stdout)
(a.scratch/'scan.log').write_text(r.stderr)
reports = {}
for line in r.stdout.splitlines():
    x=json.loads(line)
    f=x['raw']['files'][0]
    reports[Path(f['path']).name] = {t['id'] for f in x['raw']['files'] for t in f.get('traits', [])}
results=[]
for name, (required, forbidden) in checks.items():
    ids=reports.get(name,set())
    results.append({'case':name, 'missing':sorted(set(required)-ids), 'unexpected':sorted(set(forbidden)&ids), 'scanned':name in reports})
(a.scratch/'results.json').write_text(json.dumps(results,indent=2)+'\n')
fail=[x for x in results if x['missing'] or x['unexpected'] or not x['scanned']]
assert not fail, fail
print(f'{len(results)} focused boundaries passed')
