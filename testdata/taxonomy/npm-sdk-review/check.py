#!/usr/bin/env python3
"""Check corrected descriptions, relocated observations, and retained attacks."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent
CASES = [
    (BASE / 'schema-and-errors.js', [], [
        'metadata/package/testing/harness/unit::selftest-verdict-vector-table',
        'metadata/package/testing/corpus::expected-string-case-table',
        'micro-behaviors/process/interpreter/reflection/runtime::jvm-process-class-name',
        'micro-behaviors/data/property/assign::output-amount-field-assignment',
        'micro-behaviors/data/llm/agent::affirmative-tool-approval-required',
    ]),
    (BASE / 'expected-cases.js', ['metadata/package/testing/corpus::expected-string-case-table'], []),
    (BASE / 'transaction-drainer.js', [
        'micro-behaviors/data/property/assign::output-amount-field-assignment',
        'micro-behaviors/data/property/assign::output-destination-field-assignment',
        'objectives/impact/crypto-manipulation/transfer::percentage-output-amount-drainer',
    ], []),
    (BASE / 'jvm-process.js', [
        'micro-behaviors/process/interpreter/reflection/runtime::jvm-process-class-name',
        'micro-behaviors/process/interpreter/reflection/runtime::polyglot-jvm-reflective-process-exec',
    ], []),
    (BASE / 'browser-capabilities.js', [
        'micro-behaviors/process/create/flags::chromium-automation-launch-flags',
        'micro-behaviors/os/clipboard/read::browser-clipboard-read-source-string',
        'micro-behaviors/hardware/display/screenshot::cdp-page-capture-screenshot',
        'micro-behaviors/communications/http/header/custom::tus-upload-offset-header',
        'micro-behaviors/data/llm/wire-marker::mcp-tool-use-field-reference',
        'micro-behaviors/data/llm/wire-marker::google-safety-threshold-api-reference',
        'micro-behaviors/data/llm/agent::affirmative-tool-approval-required',
    ], []),
    (BASE / 'setup-prettier/generator.js', [], ['well-known/tool/development/lint/prettier::package-bundle']),
    (BASE / 'prettier/index.js', ['well-known/tool/development/lint/prettier::package-bundle'], []),
    (BASE / 'missing-manifest.tgz', ['metadata/package/entrypoint::runtime-shipped-without-publish-manifest'], []),
    (BASE / 'nested-extension.tgz', [], ['metadata/package/entrypoint::runtime-shipped-without-publish-manifest']),
    (ROOT / 'testdata/taxonomy/selftest-verdict-vector/vss-selftest-vectors.mjs', [
        'metadata/package/testing/harness/unit::selftest-verdict-vector-table',
    ], ['objectives/impact/degrade/system/recovery::vssadmin-delete']),
    (ROOT / 'testdata/taxonomy/selftest-verdict-vector/vss-exec-call.mjs', [
        'objectives/impact/degrade/system/recovery::vssadmin-delete',
    ], ['metadata/package/testing/harness/unit::selftest-verdict-vector-table']),
]

def check(case):
    path, required, forbidden = case
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--format', 'json', str(path)],
        cwd=ROOT, env=dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), CLEAVE_SKIP_CACHE='1'),
        capture_output=True, text=True, check=True)
    report = json.loads(result.stdout)
    ids = {t['id'] for f in report['files'] for t in f.get('traits', [])}
    errors = [f'missing {r}' for r in required if r not in ids]
    errors += [f'unexpected {r}' for r in forbidden if r in ids]
    return str(path.relative_to(ROOT)), errors

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(check, CASES))
    for name, errors in results:
        print(('FAIL' if errors else 'PASS'), name, '; '.join(errors))
    raise SystemExit(any(errors for _, errors in results))
