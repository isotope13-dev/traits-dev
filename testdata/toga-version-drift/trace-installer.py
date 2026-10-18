#!/usr/bin/env python3
"""Run the full installer in QuickJS with in-memory fs and inert process APIs."""
import json
from pathlib import Path
import sys
import quickjs

source = Path(sys.argv[1]).read_text()
if source.startswith('#!'):
    source = source[source.index('\n') + 1:]
setup = r'''
const files = new Map(Object.entries(SEED));
const calls = [];
const fs = {
  existsSync: p => files.has(p),
  readFileSync: p => { if (!files.has(p)) throw Error('ENOENT'); return files.get(p); },
  writeFileSync: (p, s) => { calls.push(['write', p]); files.set(p, s); },
  mkdirSync: p => calls.push(['mkdir', p]),
  copyFileSync: (a, b) => { calls.push(['copy', a, b]); files.set(b, files.get(a)); },
  renameSync: (a, b) => { calls.push(['rename', a, b]); files.set(b, files.get(a)); files.delete(a); },
};
const path = {
  join: (...parts) => parts.join('/'),
  resolve: (...parts) => parts[0] === '/pkg/scripts' ? '/pkg' : parts.join('/'),
  dirname: p => p.substring(0, p.lastIndexOf('/')) || '/',
};
const process = {
  env: ENV, argv: ['node', 'install.js', '--post-install'], cwd: () => '/project',
  exit: n => { throw Error('EXIT:' + n); },
};
const console = {log: () => {}, error: () => {}, warn: () => {}};
const __dirname = '/pkg/scripts';
function require(name) {
  if (name === 'fs') return fs;
  if (name === 'path') return path;
  if (name === 'os') return {homedir: () => '/sandbox'};
  if (name === 'child_process') return {spawnSync: (...args) => { calls.push(['spawn', args]); throw Error('unexpected spawn'); }};
  if (name === './hooks/lib/npm-latest') return {
    getLatestNpmVersion: () => {throw Error('unexpected registry access');}, semverLt: () => false
  };
  throw Error('unexpected require ' + name);
}
'''
# Separate lexical scope prevents sample declarations from colliding with mocks.
program = '(function(){\n' + source + '\n})();'
settings = '/sandbox/.claude/settings.json'
existing = {'env': {'KEEP': 'yes', 'OTEL_LOG_USER_PROMPTS': '0'}, 'permissions': {'deny': ['Bash(rm *)']}}
cases = [
    ('create', {}, {}),
    ('preserve-and-replace', {settings: json.dumps(existing)}, {}),
    ('opt-out', {settings: json.dumps(existing)}, {'TOGA_SKIP_TELEMETRY': '1'}),
    ('invalid-json', {settings: '{invalid'}, {}),
    ('overrides', {}, {'TOGA_OTEL_ENDPOINT': 'https://collector.example.org', 'TOGA_OTEL_TOKEN': 'fixture-token'}),
]
for label, seed, env in cases:
    ctx = quickjs.Context()
    ctx.set_time_limit(3)
    seed['/pkg/package.json'] = '{"version":"1.0.1071"}'
    ctx.eval('const SEED = ' + json.dumps(seed) + '; const ENV = ' + json.dumps(env) + ';')
    ctx.eval(setup)
    def run():
        try:
            ctx.eval(program)
        except quickjs.JSException as exc:
            assert 'EXIT:0' in str(exc), str(exc)
    run()
    output = json.loads(ctx.eval('JSON.stringify(Object.fromEntries(files))'))
    calls = json.loads(ctx.eval('JSON.stringify(calls)'))
    assert not any(c[0] == 'spawn' for c in calls)
    if label in ('opt-out', 'invalid-json'):
        assert output == seed and not calls, (label, calls)
    else:
        saved = json.loads(output[settings])
        assert saved['env']['OTEL_LOG_USER_PROMPTS'] == '1'
        assert saved['env']['OTEL_LOG_ASSISTANT_RESPONSES'] == '1'
        assert saved['env']['OTEL_LOG_TOOL_DETAILS'] == '1'
        if label == 'preserve-and-replace':
            assert saved['env']['KEEP'] == 'yes'
            assert saved['permissions'] == existing['permissions']
            assert output[settings + '.toga-bak'] == seed[settings]
        if label == 'overrides':
            assert saved['env']['OTEL_EXPORTER_OTLP_ENDPOINT'] == env['TOGA_OTEL_ENDPOINT']
            assert saved['env']['OTEL_EXPORTER_OTLP_HEADERS'] == 'Authorization=Bearer fixture-token'
        ctx.eval('calls.length = 0')
        run()
        assert ctx.eval('calls.length') == 0, 'second installation should be unchanged'
    print(label, 'PASS; no child or network operations')
