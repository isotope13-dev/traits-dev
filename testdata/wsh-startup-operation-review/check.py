#!/usr/bin/env python3
"""Run inert source controls outside test-directory naming exclusions."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
fixtures = Path(__file__).resolve().parent
cases = json.loads((fixtures / 'cases.json').read_text())
args.scratch.mkdir(parents=True, exist_ok=True)
for case in cases:
    shutil.copyfile(fixtures / case['name'], args.scratch / case['name'])
spec = importlib.util.spec_from_file_location(
    'pe_controls', root / 'testdata/managed-records-review/verify.py')
pe_controls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pe_controls)
flag = 'micro-behaviors/mem/protect/constant::page-execute-readwrite'
execute = 'micro-behaviors/mem/protect/constant::page-execute-constant'
old_flags = ['micro-behaviors/mem/alloc/executable::page-execute-readwrite',
             'micro-behaviors/mem/protect/modify::page-execute-constant']
for name, markers, matched, absent in [
    ('rwx-flag.exe', ['PAGE_EXECUTE_READWRITE'], [flag], [execute]),
    ('execute-flag.exe', ['PAGE_EXECUTE'], [execute], [flag]),
    ('unrelated-flag.exe', ['XPAGE_EXECUTE'], [], [flag, execute]),
    ('command-labels.exe', ['StartDDos', 'StopDDos', 'sendPlugin'],
     ['micro-behaviors/data/format/string::start-ddos-command-token',
      'micro-behaviors/data/format/string::stop-ddos-command-token',
      'micro-behaviors/data/format/string::send-plugin-command-token',
      'micro-behaviors/data/format/string::plugin-transfer-command-token'], []),
    ('autoit-command.exe', ['AutoIt3.exe stage.a3x'],
     ['metadata/lang/source/syntax/command::autoit-a3x-command'], []),
]:
    (args.scratch / name).write_bytes(pe_controls.build_pe(markers))
    cases.append({'name': name, 'matched': matched,
                  'not_matched': absent + old_flags})
for name, source, matched in [
    ('command-enum.c', 'enum command { CMD_SHELL, CMD_EXEC };',
     ['metadata/lang/source/naming/action::cmd-shell-exec-identifier']),
    ('command-handler.rs', 'fn command_handler() {}',
     ['metadata/lang/source/naming/function::rust-command-handler-reference']),
    ('unrelated-names.c', 'void cmd_exec(void) {}', []),
    ('unrelated-binding.rs', 'let command_handler = "ordinary binding";', []),
]:
    (args.scratch / name).write_text(source)
    cases.append({'name': name, 'matched': matched, 'not_matched':
        [] if matched else ['metadata/lang/source/naming/action::cmd-shell-exec-identifier',
                            'metadata/lang/source/naming/function::rust-command-handler-reference']})
result = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json',
                         str(args.scratch)], capture_output=True, text=True,
                        env={**os.environ, 'CLEAVE_VALIDATE': '0'})
assert result.returncode == 0, result.stderr
(args.scratch.parent / 'wsh-controls.json').write_text(result.stdout)
decoder = json.JSONDecoder()
remaining = result.stdout.lstrip()
reports = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    for entry in report['files']:
        reports[Path(entry['path']).name] = {t['id'] for t in entry.get('traits', [])}
    remaining = remaining[end:].lstrip()
failures = []
for case in cases:
    actual = reports[case['name']]
    missing = set(case['matched']) - actual
    unexpected = set(case['not_matched']) & actual
    if missing or unexpected:
        failures.append((case['name'], sorted(missing), sorted(unexpected)))
    else:
        print('PASS', case['name'])
assert not failures, failures
