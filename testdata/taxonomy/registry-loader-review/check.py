"""Focused flow controls. Samples are parsed; only mocked Python I/O runs."""
import argparse
import asyncio
import builtins
import json
from pathlib import Path
import subprocess
import sys
import types
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[3]
FIXTURES = Path(__file__).with_name('fixtures')
p = argparse.ArgumentParser()
p.add_argument('--scratch', type=Path, required=True)
a = p.parse_args()
a.scratch.mkdir(parents=True, exist_ok=True)
cases = {}

HOST = 'micro-behaviors/communications/http/url/build::js-fetch-response-host-indirection'
EVAL = 'objectives/execution/payload/script-eval::js-indirected-http-response-eval'
STAGER = 'objectives/execution/payload/script-eval::js-deaddrop-http-eval-stager'
BEACON = 'objectives/command-and-control/beacon/network/periodic::js-interval-deaddrop-response-eval'
ROUTE = 'objectives/command-and-control/channel/deaddrop/url::python-response-host-threadpool-poll'
CONTROL = 'objectives/command-and-control/channel/deaddrop/url::python-detached-response-host-tasking'
POLL = 'objectives/command-and-control/remote-command/http-poll::python-threadpool-http-exec-poll'
DAEMON = 'objectives/command-and-control/remote-command/http-poll::python-threadpool-http-exec-daemon'
STARTUP = 'objectives/persistence/system/python-startup::startup-hook-threadpool-code-daemon'
WALLET = 'objectives/exfiltration/stealer/wallet::wallet-input-telemetry-http-exfiltration'
DOM = 'micro-behaviors/data/property/access::dom-value-report-channel'
TIMER = 'micro-behaviors/data/property/access::value-alias-timer-reporting-call'
OBF = 'objectives/anti-static/obfuscation/string/charcode-url::js-numeric-endpoint-json-post'


def case(name, data, required=(), forbidden=()):
    path = a.scratch / name
    path.write_bytes(data if isinstance(data, bytes) else data.encode())
    cases[name] = (set(required), set(forbidden))

js = (FIXTURES / 'hostname_loader.js').read_text()
for suffix in ('js', 'ts'):
    case('loader.' + suffix, js, {HOST, EVAL, STAGER, BEACON})
    renamed = js.replace('gateway', 'authority').replace('source', 'script').replace('/stage', '/payload')
    case('renamed.' + suffix, renamed, {HOST, EVAL, STAGER, BEACON})
    case('configuration.' + suffix, js.replace('eval(source)', 'console.log(source)'), {HOST}, {EVAL, STAGER, BEACON})
    case('other-body.' + suffix, js.replace('eval(source)', 'eval(localCode)'), {HOST}, {EVAL, STAGER, BEACON})
    case('overwritten-host.' + suffix, js.replace('  const source', '  gateway = "local.invalid";\n  const source'), forbidden={HOST, EVAL, STAGER, BEACON})
    case('overwritten-code.' + suffix, js.replace('  eval(source)', '  source = "pass";\n  eval(source)'), {HOST}, {EVAL, STAGER, BEACON})
    case('path-only.' + suffix, js.replace('`http://${gateway}/stage`', '`http://fixed.invalid/${gateway}`'), forbidden={HOST, EVAL, STAGER, BEACON})
    case('different-timer.' + suffix, js.replace('setInterval(check,', 'setInterval(other,'), {HOST, EVAL, STAGER}, {BEACON})
    case('quoted.' + suffix, 'const example = ' + json.dumps(js), forbidden={HOST, EVAL, STAGER, BEACON})

py = (FIXTURES / 'renamed_daemon.py').read_text()
case('daemon.py', py, {ROUTE, CONTROL, POLL, DAEMON, STARTUP})
renamed = py
for before, after in (('_retrieve', 'get_text'), ('read_stage', 'load_text'), ('activate', 'execute_text'),
                      ('domain', 'authority'), ('text =', 'routing ='), ('text.splitlines()', 'routing.splitlines()'),
                      ('ROUTING_SOURCE', 'LOCATOR'), ('RESOURCE', 'ROUTE_PATH'), ('httpx', 'requests')):
    renamed = renamed.replace(before, after)
case('other-names.py', renamed, {ROUTE, CONTROL, POLL, DAEMON, STARTUP})
case('foreground.py', py.replace('os.fork()', '0'), {ROUTE, POLL}, {CONTROL, DAEMON, STARTUP})
for name, before, after in (
    ('wrong-host', '.format(domain, RESOURCE)', '.format(local_host, RESOURCE)'),
    ('wrong-text', 'text.splitlines()', 'local_text.splitlines()'),
    ('fixed-authority', '"http://{}{}"', '"http://fixed.invalid/{}{}"'),
    ('host-overwrite', '    await lookup(domain)', '    domain = "local.invalid"'),
    ('guard-overwrite', 'if not domain:\n        return', 'if not domain:\n        domain = "local.invalid"'),
    ('text-overwrite', '    domain = next(', '    text = "local.invalid"\n    domain = next('),
):
    assert before in py
    case(name + '.py', py.replace(before, after), {POLL, DAEMON}, {ROUTE, CONTROL})
for name, before, after in (
    ('body-overwrite', '    await activate(code)', '    code = "pass"\n    await activate(code)'),
    ('other-body', '    await activate(code)', '    await activate(local_code)'),
    ('other-poll', 'asyncio.run(run())', 'asyncio.run(local_step())'),
    ('other-http', 'httpx.get(', 'storage.get('),
    ('compile-only', 'exec(compile(code, "<remote>", "exec"), {"__name__": "__main__"})', 'compile(code, "<remote>", "exec")'),
):
    assert before in py
    case(name + '.py', py.replace(before, after), forbidden={ROUTE, CONTROL, POLL, DAEMON, STARTUP})
case('quoted.py', 'example = ' + repr(py), forbidden={ROUTE, CONTROL, POLL, DAEMON, STARTUP})
case('comments.py', '\n'.join('# ' + line for line in py.splitlines()), forbidden={ROUTE, CONTROL, POLL, DAEMON, STARTUP})

case('inert-wallet.xpi', (FIXTURES / 'inert-wallet.xpi').read_bytes(), {OBF, TIMER}, {WALLET, DOM})
with ZipFile(FIXTURES / 'inert-wallet.xpi') as z:
    case('generic-value-timer.js', z.read('entry.js'), {TIMER}, {DOM})
    case('generic-value-trim-timer.js', z.read('entry.js').replace(b'field.value;', b'field.value.trim();'), forbidden={DOM})
    manifest = json.loads(z.read('manifest.json'))
    assert not any(k in manifest for k in ('background', 'content_scripts', 'browser_action', 'action', 'options_ui'))
    html = z.read('form.html').decode()
    assert '<script' not in html and 'oninput' not in html and 'onsubmit' not in html
for name in ('wallet-seed-clipboard-extension.xpi', 'wallet-seed-clipboard-extension-evasive.xpi'):
    case(name, (ROOT / 'testdata/hostile' / name).read_bytes(), {WALLET, DOM})

report_path = a.scratch.parent / 'focused-scan.json'
subprocess.run(['cleave', '--traits-dir', str(ROOT), '--format', 'json',
                'analyze', str(a.scratch), '-o', str(report_path)],
               text=True, capture_output=True, check=True)
reports = {}
text = report_path.read_text()
while text.strip():
    report, end = json.JSONDecoder().raw_decode(text.lstrip())
    text = text.lstrip()[end:]
    for f in report['files']:
        # Aggregate archive findings for each fixture.
        name = Path(f['path'].split('!!')[0]).name
        reports.setdefault(name, set()).update(t['id'] for t in f.get('traits', []))
for name, (required, forbidden) in cases.items():
    matched = reports[name]
    assert required <= matched, (name, 'missing', sorted(required - matched))
    assert not forbidden & matched, (name, 'unexpected', sorted(forbidden & matched))
(a.scratch.parent / 'focused-results.json').write_text(json.dumps({'passed': len(cases), 'cases': list(cases)}, indent=2) + '\n')
print(f'PASS {len(cases)} flow/near-miss controls, including two pre-existing attack archives')

# Exercise the Python helpers with all remote I/O replaced. The original main
# guard is false, so no real daemon, file creation, fork, or socket lookup runs.
requests = []
executions = []
mock = types.ModuleType('httpx')
def get(url, **options):
    requests.append(url)
    body = 'routing.invalid\n' if url.endswith('host.txt') else 'stage_marker = 42'
    return types.SimpleNamespace(text=body, raise_for_status=lambda: None)
mock.get = get
mock.RequestException = RuntimeError
prior = sys.modules.get('httpx')
sys.modules['httpx'] = mock
scope = {'__name__': 'review_only'}
try:
    builtins.exec(compile(py, 'reviewed_sample.py', 'exec'), scope)
    scope['socket'] = types.SimpleNamespace(getaddrinfo=lambda *a: [('mock',)], gaierror=RuntimeError)
    def execute(code, namespace):
        builtins.exec(code, namespace)
        executions.append(namespace['stage_marker'])
    scope['exec'] = execute
    asyncio.run(scope['run']())
    scope['_executor'].shutdown(wait=True)
finally:
    if prior is None:
        del sys.modules['httpx']
    else:
        sys.modules['httpx'] = prior
assert requests == ['https://raw.githubusercontent.com/example/routing/main/host.txt', 'http://routing.invalid/stage']
assert executions == [42]
print('PASS mocked Python response -> selected hostname -> fetched source -> compile/exec')
