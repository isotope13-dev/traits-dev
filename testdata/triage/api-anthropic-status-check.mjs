// Run with node --experimental-vm-modules and an extracted package directory.
// All sample filesystem, subprocess, and network APIs are mocked.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root = process.argv[2];
const expectLeak = process.argv[3] !== '--expect-guarded';
assert(root, 'Pass the extracted package directory');
const settingsFile = '/virtual/.claude/settings.json';
const originalKey = 'SENTINEL_EXISTING_PROVIDER_KEY';
const original = JSON.stringify({ env: {
  ANTHROPIC_BASE_URL: 'https://api.anthropic.com',
  ANTHROPIC_API_KEY: originalKey,
}, permissions: { allow: [] } });
const files = new Map([[settingsFile, original]]);
const requests = [];
const mockFs = {
  existsSync: p => files.has(p),
  readFileSync: p => { assert(files.has(p)); return files.get(p); },
  writeFileSync: (p, value) => files.set(p, value),
  copyFileSync: (src, dst) => { assert(files.has(src)); files.set(dst, files.get(src)); },
  renameSync: (src, dst) => { assert(files.has(src)); files.set(dst, files.get(src)); files.delete(src); },
  rmSync: p => files.delete(p),
  mkdirSync: () => {},
};
const builtins = {
  'node:fs': mockFs,
  'node:os': { homedir: () => '/virtual' },
  'node:path': { dirname: path.posix.dirname, join: path.posix.join },
  'node:child_process': { execFileSync: () => 'mock-claude-version' },
};
const context = vm.createContext({
  process: { env: {}, platform: 'linux', pid: 42 },
  fetch: async (url, options) => {
    requests.push({ url, options });
    return { status: 200, ok: true, json: async () => ({ data: [] }) };
  },
});
const modules = new Map();
function load(name) {
  if (modules.has(name)) return modules.get(name);
  let mod;
  if (Object.hasOwn(builtins, name)) {
    const values = builtins[name];
    mod = new vm.SyntheticModule(Object.keys(values), function () {
      for (const [key, value] of Object.entries(values)) this.setExport(key, value);
    }, { context, identifier: name });
  } else {
    assert(/^(configure|claude|platform|constants|sugarball)\.js$/.test(name));
    mod = new vm.SourceTextModule(readFileSync(path.join(root, 'dist', name), 'utf8'), {
      context, identifier: name,
    });
  }
  modules.set(name, mod);
  return mod;
}
const main = load('configure.js');
await main.link(name => load(name.startsWith('./') ? name.slice(2) : name));
await main.evaluate({ timeout: 1000 });

const status = await main.namespace.status();
assert.equal(status.baseUrlConfigured, false);
assert.equal(files.get(settingsFile), original);
const leaked = requests.find(r => r.options?.headers?.['x-api-key'] === originalKey);
assert.equal(Boolean(leaked), expectLeak, 'Unexpected existing-key transmission');
if (leaked) assert.equal(leaked.url, 'https://api-anthropic.help/v1/models');

requests.length = 0;
await main.namespace.install('SENTINEL_NEW_GATEWAY_KEY');
assert.equal(requests[0].options.headers['x-api-key'], 'SENTINEL_NEW_GATEWAY_KEY');
const installed = JSON.parse(files.get(settingsFile));
assert.equal(installed.env.ANTHROPIC_BASE_URL, 'https://api-anthropic.help');
assert.equal(installed.env.ANTHROPIC_API_KEY, 'SENTINEL_NEW_GATEWAY_KEY');
const state = JSON.parse(files.get('/virtual/.claude/.api-anthropic-state.json'));
assert.equal(state.previous.env.ANTHROPIC_API_KEY.value, originalKey);
main.namespace.uninstall();
assert.deepEqual(JSON.parse(files.get(settingsFile)), JSON.parse(original));
console.log(JSON.stringify({
  statusSendsExistingKeyToDifferentOrigin: Boolean(leaked),
  destination: leaked?.url ?? null,
  statusReportsGatewayConfigured: status.baseUrlConfigured,
  installUsesExplicitNewKey: true,
  stateCopiesPreviousKey: true,
  uninstallRestoresOriginalSettings: true,
  allSampleIOWasMocked: true,
}, null, 2));
