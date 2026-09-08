// Static scanner regression: generated PHP is data and is never executed.
// Usage: node scripts/check-php-native-replacements.cjs [cleave binary]
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const cp = require('node:child_process');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..');
const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'php-native-replacements-'));
const loader = 'objectives/anti-static/obfuscation/eval/loader::';
const metrics = 'metadata/file/encoded::';
const cases = [];
function add(name, source, yes = [], no = []) {
  const file = path.join(dir, name + '.php');
  fs.writeFileSync(file, source);
  cases.push({file, yes, no});
}
for (const [name, expression] of Object.entries({
  base64: 'base64_decode("ZWNobyAxOw==")',
  inflate: 'gzinflate(base64_decode("abcd"))',
  uncompress: 'gzuncompress(gzuncompress($data))',
  gzip: 'gzdecode(base64_decode("abcd"))',
  pack: 'pack("H*", "6563686f20313b")',
  prefix: '"?>" . base64_decode("abcd")',
  mixedcase: "'?>' . PaCk ('H*', '6563')",
})) add(name, `<?php EvAl (${expression});`, [loader + ({base64: 'php-eval-string-decoder', inflate: 'php-eval-inflate-decoder', uncompress: 'php-eval-inflate-decoder', gzip: 'php-eval-gzip-or-reverse-decoder', pack: 'php-eval-pack-decoder', prefix: 'php-eval-string-decoder', mixedcase: 'php-eval-pack-decoder'}[name])]);
add('quoted', '<?php $documentation = \'eval(base64_decode("abcd"))\';', [], [loader + 'php-eval-decoder-chain']);
add('data-only', '<?php echo gzinflate(base64_decode("abcd"));', [], [loader + 'php-eval-decoder-chain']);
add('request', '<?php eval(base64_decode($_POST["code"]));', [
  loader + 'php-eval-string-decoder',
  'objectives/command-and-control/backdoor/webshell/decoder::php-decoder-eval-webshell',
]);
const bytes = Buffer.concat(Array.from({length: 512}, (_, i) => crypto.createHash('sha256').update(String(i)).digest()));
const wrapper = (call) => Buffer.from(('<?php ' + call + '\n__halt_compiler();').padEnd(500, ' '));
for (const [name, tail, atom] of [
  ['encoded', Buffer.from(bytes.toString('base64')), 'php-high-entropy-region'],
  ['binary', bytes, 'php-binary-dense-source'],
]) {
  add(name, Buffer.concat([wrapper('eval($payload);'), tail]), [metrics + atom, loader + 'php-encoded-content-execution']);
  add(name + '-data', Buffer.concat([wrapper('echo "data";'), tail]), [metrics + atom], [loader + 'php-encoded-content-execution']);
  add(name + '-quoted', Buffer.concat([wrapper('$doc = \'eval($payload);\';'), tail]), [metrics + atom], [loader + 'php-encoded-content-execution']);
}
for (const [name, call, id] of [
  ['create', 'create_function("", "return 1;");', 'micro-behaviors/process/interpreter/eval/direct::php-create-function-call'],
  ['preg', 'preg_replace("/x/e", "$code", $data);', 'micro-behaviors/data/string/replace::php-preg-eval-modifier'],
  ['filter', 'preg_filter("|.*|e", "$code", $data);', 'micro-behaviors/data/string/replace::php-preg-eval-modifier'],
  ['mb', 'mb_ereg_replace("x", $code, $data, "e");', 'micro-behaviors/data/string/replace::php-mb-regex-eval-option'],
  ['reflection', 'new ReflectionFunction("foo");', 'micro-behaviors/process/interpreter/reflection/function::php-reflection-function'],
  ['pdo', '$stmt->fetchAll(PDO::FETCH_FUNC, "foo");', 'micro-behaviors/process/interpreter/reflection/function::php-pdo-fetch-callback'],
]) add(name, '<?php ' + call, [id]);
for (const [name, call] of [
  ['assertion', 'assert($ok);'],
  ['reflection-encoded', 'new ReflectionFunction("foo");'],
  ['pdo-encoded', '$stmt->fetchAll(PDO::FETCH_FUNC, "foo");'],
]) add(name, Buffer.concat([wrapper(call), Buffer.from(bytes.toString('base64'))]),
  [loader + 'php-encoded-content-dynamic-apis'], [loader + 'php-encoded-content-execution']);
add('unicode-prose', '<?php $message = "' + '日本語の説明文です。'.repeat(300) + '"; echo $message;', [], [metrics + 'php-binary-dense-source']);
add('ordinary-regex', '<?php preg_replace("/x/i", "e", $data); mb_ereg_replace("x", "e", $data, "i");', [], [
  'micro-behaviors/data/string/replace::php-preg-eval-modifier',
  'micro-behaviors/data/string/replace::php-mb-regex-eval-option',
]);
const titleCall = 'micro-behaviors/process/control/signal::cli-set-process-title';
const titleDisguise = 'objectives/evasion/masquerade/process/title::php-kernel-worker-title';
add('worker-title', '<?php cli_set_process_title("queue-worker");', [titleCall], [titleDisguise]);
add('kernel-title', '<?php cli_set_process_title("[kworker/0:1]");', [titleCall, titleDisguise]);
add('pecl-kernel-title', '<?php setproctitle("[kworker/1:2]");', [titleDisguise]);
add('quoted-title', '<?php $help = \'cli_set_process_title("[kworker/0:1]")\';', [], [titleCall, titleDisguise]);
const networkDisguise = 'objectives/evasion/masquerade/process/title::php-networked-kernel-worker-disguise';
add('network-worker-title', '<?php cli_set_process_title("queue-worker"); posix_setsid(); stream_socket_client("tcp://127.0.0.1:9000");', [titleCall], [networkDisguise]);
add('network-kernel-title', '<?php cli_set_process_title("[kworker/0:1]"); posix_setsid(); stream_socket_client("tcp://192.0.2.1:9000");', [networkDisguise]);
const callbackPrefix = 'micro-behaviors/os/callback/dispatch::';
const dispatchPrefix = 'objectives/command-and-control/backdoor/webshell/obf-dispatch::';
for (const [id, functions] of Object.entries({
  'php-array-transform-api': ['array_map', 'array_filter', 'array_reduce', 'array_walk', 'array_walk_recursive'],
  'php-array-callback-difference-api': ['array_diff_uassoc', 'array_diff_ukey', 'array_udiff', 'array_udiff_assoc', 'array_udiff_uassoc'],
  'php-array-callback-intersection-api': ['array_intersect_uassoc', 'array_intersect_ukey', 'array_uintersect', 'array_uintersect_assoc', 'array_uintersect_uassoc'],
  'php-array-callback-sort-api': ['usort', 'uasort', 'uksort'],
  'php-regex-callback-api': ['preg_replace_callback', 'mb_ereg_replace_callback'],
  'php-lifecycle-callback-api': ['register_shutdown_function', 'register_tick_function', 'spl_autoload_register'],
  'php-handler-registration-api': ['set_error_handler', 'set_exception_handler', 'session_set_save_handler'],
  'php-iterator-callback-api': ['iterator_apply'],
  'php-sqlite-callback-api': ['sqlite_create_function', 'sqlite_create_aggregate'],
  'php-assert-options-api': ['assert_options'],
})) for (const fn of functions) add('api-' + fn, '<?php ' + fn + '($input, $callback);', [callbackPrefix + id]);
add('filter-callback', '<?php filter_var($input, FILTER_CALLBACK, $options);', [callbackPrefix + 'php-filter-callback-mode']);
add('quoted-callback', '<?php /* call_user_func($_GET["callback"], $data); */ $doc = \'array_map($callback, $data)\';', [], [dispatchPrefix + 'php-direct-request-callback', callbackPrefix + 'php-array-transform-api']);
add('direct-callback', '<?php call_user_func($_GET["callback"], $_POST["data"]);', [dispatchPrefix + 'php-direct-request-callback']);
add('ordinary-difference', '<?php array_diff($a, $b); array_intersect($a, $b);', [], [callbackPrefix + 'php-array-callback-difference-api', callbackPrefix + 'php-array-callback-intersection-api']);
add('request-function', '<?php $_POST["call"] ( $_GET["arg"] );', [dispatchPrefix + 'dynamic-user-input-call-1']);
add('header-function', '<?php $_SERVER["HTTP_CALL"] ( $_SERVER["HTTP_ARG"] );', [dispatchPrefix + 'dynamic-user-input-call-2']);
add('quoted-request-function', '<?php /* $_POST["call"]($_GET["arg"]); */', [], [dispatchPrefix + 'dynamic-user-input-call-1']);
add('request-map-callback', '<?php array_map($_GET["fn"], $items);', [dispatchPrefix + 'php-request-selected-first-callback']);
add('request-shutdown-callback', '<?php register_shutdown_function($_GET["fn"], $_POST["arg"]);', [dispatchPrefix + 'php-request-selected-first-callback']);
add('safe-map-request-data', '<?php array_map("trim", $_GET["items"]); register_shutdown_function(function () { cleanup(); });', [], [dispatchPrefix + 'php-request-selected-first-callback']);
const result = cp.spawnSync(process.argv[2] || '../cleave/target/release/cleave', ['--traits-dir', root, '--format', 'jsonl', 'analyze', dir], {cwd: root, encoding: 'utf8', maxBuffer: 64 * 1024 * 1024});
fs.writeFileSync(path.join(dir, 'scan.json'), result.stdout || '');
if (result.status !== 0) throw new Error(result.stderr);
// Some cleave builds concatenate per-file JSON objects even in jsonl mode.
const files = [];
let start = 0, depth = 0, quoted = false, escaped = false;
for (let i = 0; i < result.stdout.length; i++) {
  const ch = result.stdout[i];
  if (quoted) {
    if (escaped) escaped = false;
    else if (ch === '\\') escaped = true;
    else if (ch === '"') quoted = false;
    continue;
  }
  if (ch === '"') quoted = true;
  else if (ch === '{') { if (depth++ === 0) start = i; }
  else if (ch === '}' && --depth === 0) {
    const report = JSON.parse(result.stdout.slice(start, i + 1));
    files.push(...(report.files || report.raw?.files || [report]));
  }
}
let failures = 0;
for (const c of cases) {
  const file = files.find(f => f.path === c.file);
  if (!file) { console.error('MISSING FILE', c.file); failures++; continue; }
  const ids = new Set((file.traits || file.findings || []).map(t => t.id));
  for (const id of c.yes) if (!ids.has(id)) { console.error('MISSING', path.basename(c.file), id); failures++; }
  for (const id of c.no) if (ids.has(id) || (id.endsWith('php-eval-decoder-chain') && [...ids].some(i => /::php-eval-(string|inflate|gzip-or-reverse|pack)-decoder$/.test(i)))) { console.error('UNEXPECTED', path.basename(c.file), id); failures++; }
}
console.log(`${cases.length} cases, ${failures} failures; artifacts: ${dir}`);
process.exitCode = failures ? 1 : 0;
