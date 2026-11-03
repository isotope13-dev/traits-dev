#!/usr/bin/env python3
"""Check the conditional WASI SDK context on positive and missing-gate input."""
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = ROOT.parent / 'cleave/target/release/cleave'
RULE = 'metadata/build/wasi::conditional-wasi-sdk-bootstrap'

with tempfile.TemporaryDirectory(prefix='wasi-context-') as temp:
    root = Path(temp)
    dest = root / 'rules/metadata/build/wasi/sdk-context.yaml'
    dest.parent.mkdir(parents=True)
    shutil.copy2(ROOT / 'metadata/build/wasi/sdk-context.yaml', dest)
    common = '''fn download_wasi_sdk() {}
const SDK: &str = "https://github.com/WebAssembly/wasi-sdk/releases/download/v1/sdk.tar.gz";
'''
    cases = (
        ('conditional', common + 'fn f(target_os: &str) { if target_os == "wasi" { get_wasi_sdk_path(); } }\n', True),
        ('cargo-gate', common + 'fn f() { CARGO_CFG_TARGET_OS.wasi.get_wasi_sdk_path(); }\n', True),
        ('no-target-gate', common + 'fn f() { get_wasi_sdk_path(); }\n', False),
        ('no-helper', 'const SDK: &str = "WebAssembly/wasi-sdk/releases/download";\n'
         'fn f(target_os: &str) { if target_os == "wasi" { get_wasi_sdk_path(); } }\n', False),
    )
    for name, content, expected in cases:
        sample = root / (name + '.rs')
        sample.write_text(content)
        result = subprocess.run([str(CLEAVE), '--traits-dir', str(root / 'rules'),
                                 'test-rules', '--rules', RULE, str(sample)],
                                check=True, capture_output=True, text=True)
        status = 'MATCHED ' if expected else 'NOT MATCHED '
        if '\n' + status + RULE + ' ' not in result.stdout:
            raise SystemExit(f'{name}: unexpected result\n{result.stdout}\n{result.stderr}')
        print(f'{name}: ok', flush=True)
