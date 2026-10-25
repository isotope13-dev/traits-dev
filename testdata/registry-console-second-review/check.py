"""Static controls and before/after coverage; never execute sample code."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PARSER = argparse.ArgumentParser()
PARSER.add_argument('--scratch', type=Path, required=True)
PARSER.add_argument('--baseline', type=Path)
ARGS = PARSER.parse_args()
ARGS.scratch.mkdir(parents=True, exist_ok=True)
COPY = 'micro-behaviors/mem/copy::dotnet-buffer-block-copy'
MODE = 'micro-behaviors/data/decompress/stream::csharp-decompression-mode'
GZIP = 'micro-behaviors/data/decompress/gzip::dotnet-gzip-decompression-constructor'
DECRYPT = 'micro-behaviors/crypto/decrypt::csharp-create-decryptor-symbol'
CONFIG = 'micro-behaviors/communications/proxy/config::devtunnels-rdp-endpoint-context'
UPLOAD = 'micro-behaviors/communications/http/server/request::php-host-profile-upload-handler'
FORGE = 'objectives/evasion/security-bypass/policy/browser::claude-body-onboarding-prompt-forgery'
EXTFORGE = 'objectives/evasion/security-bypass/policy/browser::extension-claude-onboarding-prompt-forgery'
WILDCARD = 'micro-behaviors/communications/ipc/message::postmessage-wildcard-target'
TASK = 'micro-behaviors/communications/ipc/message::sidebar-message-request-type'
CASES = {
 'telemetry-patch.cs': ({'objectives/evasion/anti-av/amsi::csharp-amsi-memory-patch', 'objectives/evasion/anti-av/blinding::csharp-etw-helper-memory-patch'}, set()),
 'diagnostic-upload.php': ({UPLOAD}, set()),
 'buffer-copy.cs': ({COPY}, {'micro-behaviors/data/embedded/payload/resource::dotnet-source-resource-data-extraction'}),
 'gzip-compress.cs': (set(), {GZIP, MODE}),
 'gzip-decompress.cs': ({GZIP, MODE}, set()),
 'decryptor.cs': ({DECRYPT}, set()),
 'endpoint-config.cs': ({CONFIG}, set()),
 'claude-prompt.js': ({FORGE}, {EXTFORGE}),
 'claude-no-click.js': (set(), {FORGE, EXTFORGE}),
 'claude-other-attribute.js': (set(), {FORGE, EXTFORGE}),
 'wildcard-message.js': ({WILDCARD, TASK}, set()),
 'origin-message.js': (set(), {WILDCARD, TASK}),
}
paths = [HERE / p for p in CASES]
for name, declaration in [('extension-positive.zip', True), ('extension-no-content-script.zip', False)]:
 manifest = {'manifest_version': 3, 'name': 'Fixture', 'version': '1'}
 if declaration:
  manifest['content_scripts'] = [{'matches': ['https://example.org/*'], 'js': ['bridge.js']}]
 target = ARGS.scratch / name
 with zipfile.ZipFile(target, 'w') as archive:
  archive.writestr('manifest.json', json.dumps(manifest))
  archive.writestr('bridge.js', (HERE / 'claude-prompt.js').read_bytes())
 CASES[name] = ({EXTFORGE}, set()) if declaration else (set(), {EXTFORGE})
 paths.append(target)
# Original corpus positives and benign controls outside this batch.
for directory in ['webshell-collection-review', 'wordpress-theme-upload-boundary']:
 cases = json.loads((ROOT/'testdata/taxonomy'/directory/'cases.json').read_text())
 for case in cases['fixtures']:
  paths.append(ROOT/case['path'] if case['path'].startswith('testdata/') else ROOT/'testdata/taxonomy'/directory/case['path'])
paths = [p for p in paths if p.exists()]
paths += [ROOT/'testdata/taxonomy/decompression'/p for p in ['decompress.cs','codec-only.cs']]
paths += [ROOT/'testdata/benign'/p for p in ['managed-status-stubs-only.cs','managed-native-interop-only.cs']]
env = {**os.environ, 'CLEAVE_VALIDATE': '0'}

def scan(traits, output):
 result = subprocess.run(['cleave', '--traits-dir', str(traits), '--disable', 'yara,radare2,third-party', '--json', *map(str, paths)],
   cwd=ROOT, env=env, text=True, capture_output=True)
 assert result.returncode == 0, result.stderr
 output.write_text(result.stdout)
 assert not result.stderr.strip(), result.stderr
 return {Path(f['path']).name: f for line in result.stdout.splitlines() for f in json.loads(line)['files']}

current = scan(ROOT, ARGS.scratch/'controls-current.jsonl')
for name, (required, forbidden) in CASES.items():
 traits = {t['id'] for t in current[name].get('traits', [])}
 assert required <= traits, (name, 'missing', required-traits)
 assert not forbidden & traits, (name, 'unexpected', forbidden & traits)
 if name in {'diagnostic-upload.php','buffer-copy.cs','endpoint-config.cs','gzip-compress.cs'}:
  assert not [t for t in current[name].get('traits',[]) if t['crit'] >= 4], (name, 'overstated intent')
# Controls outside the batch must retain their existing technique findings.
if ARGS.baseline:
 baseline = scan(ARGS.baseline, ARGS.scratch/'controls-baseline.jsonl')
 mapping = json.loads((ARGS.scratch/'id-map.json').read_text())
 for name, file in baseline.items():
  if name in CASES: continue
  before = {mapping.get(t['id'], t['id']) for t in file.get('traits',[])}
  after = {t['id'] for t in current[name].get('traits',[])}
  assert before <= after, (name, 'lost corpus coverage', before-after)
print(f'Passed {len(CASES)} focused controls and {len(paths)-len(CASES)} corpus regressions')
