#!/usr/bin/env python3
"""Check capabilities, real identity controls, and retained loader coverage."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--scratch-dir', required=True)
args = parser.parse_args()
CAPS = {
    'micro-behaviors/data/control-flow/error-handling::javascript-error-stack-capture',
    'micro-behaviors/data/decompress/gzip::node-create-gunzip-call',
    'micro-behaviors/data/decompress/zlib::node-create-inflate-call',
    'micro-behaviors/data/format/string::ejs-render-call',
}
EXT = 'well-known/lib/web/client-side/browser-libraries::extjs-library'
LICENSE = 'metadata/package/license::sencha-copyright-attribution'
TERMINAL = 'well-known/app/utility/tabby-terminal::'
AI = 'well-known/app/ai/coding-agent/tabby::'
URL = 'micro-behaviors/communications/url/scheme::'
LOADER = 'objectives/command-and-control/dropper/script-eval/remote-code::'
cases = {
    'capabilities.js': (CAPS, set()),
    'references-only.js': (set(), CAPS),
    'connect-header.d.ts': ({LICENSE}, {EXT}),
    'extjs-version.js': ({EXT, LICENSE}, set()),
    'builtin-plugins/tabby-plugin-manager/package.json': (
        {TERMINAL + 'tabby-builtin-plugin-keyword'}, {AI + 'tabby-builtin-plugin'}),
    'builtin-plugins/tabby-plugin-manager/dist/index.js': (
        {TERMINAL + 'tabby-builtin-plugin-path',
         TERMINAL + 'tabby-builtin-plugin-dist-path'}, {AI + 'tabby-builtin-plugin'}),
    'dist/builtin-plugin/APIPlugin.d.ts': (
        set(), {AI + 'tabby-builtin-plugin', AI + 'tabby-ai-assistant',
                TERMINAL + 'tabby-builtin-plugin-path'}),
    'data-urls.js': (
        {URL + 'javascript-base64-data-url-text', URL + 'javascript-data-url-text'},
        {LOADER + 'browser-inline-script-xhr-eval-loader'}),
    'data-url-xhr-eval.js': (
        {URL + 'javascript-base64-data-url-text',
         LOADER + 'browser-xhr-response-eval-loader',
         LOADER + 'browser-inline-script-xhr-eval-loader'}, set()),
    'corpus-cookie.js': (
        {'objectives/exfiltration/stealer/browser::browser-cookie-remote-xhr-exfil'},
        set()),
}
with tempfile.TemporaryDirectory(prefix='npm-library-controls-', dir=args.scratch_dir) as tmp:
    paths = []
    for name in cases:
        scan_name = 'inline-remote-loader.js' if name == 'data-url-xhr-eval.js' else name
        destination = Path(tmp) / scan_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        source = (ROOT / 'testdata/hostile/triage-cookie-exfil.js'
                  if name == 'corpus-cookie.js' else HERE / name)
        shutil.copyfile(source, destination)
        paths.append(str(destination))
    # Neutral paths matter: the shared URL rules deliberately exclude testdata.
    # Keep hostile controls in independent reports: benign test/declaration
    # evidence from another requested target must not become their context.
    outputs = []
    for group in (paths[:8], paths[8:9], paths[9:]):
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             '--format', 'json', *group], check=True, capture_output=True, text=True,
            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        outputs.append(result.stdout)
    decoder = json.JSONDecoder()
    remaining = '\n'.join(outputs).lstrip()
    found = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:].lstrip()
        for item in report['files']:
            name = str(Path(item['path']).relative_to(tmp))
            if name == 'inline-remote-loader.js':
                name = 'data-url-xhr-eval.js'
            found.setdefault(name, set()).update(t['id'] for t in item.get('traits', []))
    for name, (required, forbidden) in cases.items():
        actual = found[name]
        assert required <= actual, (name, 'missing', sorted(required - actual))
        assert not forbidden & actual, (name, 'unexpected', sorted(forbidden & actual))
print(f'{len(cases)} focused controls passed')
