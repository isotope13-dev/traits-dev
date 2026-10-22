#!/usr/bin/env python3
"""Scan inert controls for evaluator and file-write consolidation."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
EVAL = 'micro-behaviors/process/interpreter/eval/direct::'
WRITE = 'micro-behaviors/fs/write/file/full::write-all-bytes'
GEM = 'objectives/supply-chain/install-hook/package/rubygems::gemspec-remote-eval'
STAMP = 'micro-behaviors/fs/write/file/target::dropped-executable-with-timestomp'
FETCH = 'micro-behaviors/process/create/start-process::powershell-http-decode-write-start-profile'
CONTEXT = '''$dest = 'C:\\Windows\\system32\\example.exe'
[IO.File]::SetLastWriteTime($dest, (Get-Date))
$response = Invoke-WebRequest -Uri 'https://example.invalid/content'
$bytes = [Convert]::FromBase64String('AA==')
Start-Process -FilePath $dest
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scratch', required=True, type=Path)
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    cases = {}
    for method in ('class_eval', 'instance_eval'):
        specific = EVAL + 'ruby-' + method.replace('_', '-')
        cases[method + '.gemspec'] = (
            "require 'net/http'\nObject." + method + "(\"puts 'ok'\")\n",
            {EVAL + 'ruby-string-eval-call', specific, GEM}, set())
        cases[method + '-block.gemspec'] = (
            "require 'net/http'\nObject." + method + " { puts 'ok' }\n",
            {specific}, {EVAL + 'ruby-string-eval-call', GEM})
    cases['both.rb'] = (
        'Object.class_eval("puts 1")\nObject.instance_eval("puts 2")\n',
        {EVAL + 'ruby-string-eval-call', EVAL + 'ruby-class-eval',
         EVAL + 'ruby-instance-eval'}, set())
    cases['module.gemspec'] = (
        "require 'net/http'\nObject.module_eval(\"puts 'ok'\")\n",
        {EVAL + 'ruby-module-eval'}, {EVAL + 'ruby-string-eval-call', GEM})
    for name, call in (
        ('original', '[IO.File]::WriteAllBytes($dest, $bytes)'),
        ('qualified', '[System.IO.File]::WriteAllBytes($dest, $bytes)'),
        ('spacing-case', '[io.file]::  writeallbytes($dest, $bytes)'),
    ):
        cases[name + '.ps1'] = (CONTEXT + call + '\n', {WRITE, STAMP, FETCH}, set())
    cases['no-write.ps1'] = (CONTEXT, set(), {WRITE, STAMP, FETCH})
    cases['other-type.ps1'] = (
        CONTEXT + '[Other.File]::WriteAllBytes($dest, $bytes)\n',
        set(), {WRITE, STAMP, FETCH})

    with tempfile.TemporaryDirectory(prefix='eval-write-controls-', dir=args.scratch) as temp:
        paths = []
        for name, (source, _, _) in cases.items():
            path = Path(temp) / name
            path.write_text(source)
            paths.append(str(path))
        # One file per scan: multi-path JSON output is a document stream.
        observed = {}
        for path in paths:
            result = subprocess.run(
                [args.cleave, '--traits-dir', str(ROOT), '--format', 'json', path],
                text=True, capture_output=True, check=False)
            assert result.returncode == 0, result.stderr
            for f in json.loads(result.stdout)['files']:
                observed[Path(path).name] = (
                    observed.get(Path(path).name, set())
                    | {t['id'] for t in f.get('traits', [])})
        for name, (_, required, absent) in cases.items():
            traits = observed[name]
            assert required <= traits, (name, 'missing', required - traits)
            assert not absent & traits, (name, 'unexpected', absent & traits)
            print('PASS', name)


if __name__ == '__main__':
    main()
