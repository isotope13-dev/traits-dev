"""Static controls outside testdata so path-based exclusions cannot hide failures."""
import argparse
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
assert not args.scratch.exists(), 'Use a fresh scratch directory'
args.scratch.mkdir(parents=True)
for source in HERE.iterdir():
    if source.suffix not in {'.md', '.sh', '.js', '.json'} or source.name == 'id-map.json':
        continue
    if source.name == 'keyword-package.json':
        target = args.scratch / 'keyword-package' / 'package.json'
        target.parent.mkdir()
    else:
        target = args.scratch / source.name
    shutil.copyfile(source, target)

# A declared hook and unrelated application identity/config operations must
# not be presented as install-time identity capture. No archive code is run.
with tarfile.open(args.scratch / 'ordinary-install.tgz', 'w:gz') as archive:
    members = {
        'package/package.json': json.dumps({'name': 'ordinary-development-tool', 'scripts': {'postinstall': 'node postinstall.mjs'}}),
        'package/postinstall.mjs': 'console.log("installed");\n',
        'package/application.js': 'import os from "node:os";\nimport fs from "node:fs";\nexport function identity() { return `${os.userInfo().username}/${os.hostname()}`; }\nexport function save(cfg) { fs.writeFileSync("settings.json", JSON.stringify(cfg)); }\n',
    }
    for name, source in members.items():
        data = source.encode()
        info = tarfile.TarInfo(name)
        info.size = len(data)
        archive.addfile(info, io.BytesIO(data))

command = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'jsonl', str(args.scratch)]
result = subprocess.run(command, text=True, capture_output=True, check=True)
assert not result.stderr.strip(), result.stderr
reports = []
for line in result.stdout.splitlines():
    value = json.loads(line)
    if 'files' in value:
        reports.extend(value['files'])
    elif 'raw' in value:
        reports.extend(value['raw']['files'])
assert reports, result.stdout[:500]
by_name = {Path(report['path']).name: report for report in reports if '!!' not in report['path']}

OVERRIDE = 'objectives/evasion/security-bypass/llm/override::'
QUERY = 'micro-behaviors/communications/http/query::'

def check(name, required=(), forbidden=(), alerts=0):
    report = by_name[name]
    traits = {t['id']: t['crit'] for t in report.get('traits', [])}
    assert set(required) <= traits.keys(), (name, 'missing', set(required) - traits.keys())
    assert not set(forbidden) & traits.keys(), (name, 'forbidden', set(forbidden) & traits.keys())
    assert sum(v >= 4 for v in traits.values()) == alerts, (name, 'alerts', [(k, v) for k, v in traits.items() if v >= 4])
    assert all(v < 5 for v in traits.values()), name
    return report, traits

report, _ = check('refusal-examples.md', required=['metadata/package/documentation/security-testing::test-case-expected-refusal'], forbidden=[OVERRIDE+'llm-ignore-prior-instructions-literal', OVERRIDE+'llm-prior-instruction-override'])
assert report['type'] == 'shell', report['type']
check('refusal-with-live-override.md', required=[OVERRIDE+'llm-prior-instruction-override'], alerts=1)
check('bare-override.sh', required=[OVERRIDE+'llm-prior-instruction-override'], alerts=1)
check('query.js', required=[QUERY+'cookie-session-query-key-reference', QUERY+'cookie-session-query-encoding-cooccurrence'])
check('dependency-names.js', required=['metadata/lang/source/literal::okta-package-specifier', 'metadata/lang/source/literal::stripe-package-specifier'])
check('scanner-vocabulary.js', required=['metadata/lang/source/syntax/key-value::repeated-quoted-severity-fields', 'metadata/lang/source/syntax/call/invocation::scan-source-call'])
check('agent-guidance.js', required=['metadata/package/config::claude-guidance-delegates-agents-md'])
check('reference.js', required=['metadata/package/documentation/security-advisory::owasp-llm-top-10-reference', 'metadata/lang/source/literal::codex-cli-name-literal'], forbidden=['well-known/tool/detection/llm-scanner::llm-scanner-context', 'well-known/tool/development/agent/openai-codex::openai-codex-source-context'])
check('package.json', required=['metadata/package/keywords/capability::package-ai-keyword', 'metadata/package/keywords/capability::package-agent-keyword', 'metadata/package/keywords/identity::package-ai-model-keyword'])
check('ordinary-install.tgz', required=['micro-behaviors/os/sysinfo/profile::node-host-user-query-pair', 'micro-behaviors/fs/write/file/full::node-write-file-sync-call', 'micro-behaviors/os/package-manager/hook-install::npm-postinstall-runs-bundled-script'])
check('override-defense.js', forbidden=[OVERRIDE+'llm-ignore-prior-instructions-literal'])
check('override-live.js', required=[OVERRIDE+'llm-prior-instruction-override'], alerts=1)
theft = {t['id']: t['crit'] for t in by_name['cookie-theft.js'].get('traits', [])}
assert theft.get('objectives/exfiltration/http/query::browser-cookie-query-exfil') == 5, theft
print('Passed 13 static release-drift controls, including live overrides and cookie theft')
