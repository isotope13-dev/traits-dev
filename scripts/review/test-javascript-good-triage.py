#!/usr/bin/env python3
"""Check raw permutation-loader evidence without relying on a payload decoder."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='../cleave/target/release/cleave')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    cleave = str(Path(args.cleave).resolve())
    source = (root / 'testdata/hostile/generated/javascript-good-triage/permutation-loader.js').read_text()
    protected = re.compile(r'''"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_$][\w$]*\b|\s+''')
    names = {'pHg', 'Rjb', 'Abp', 'QbC', 'duZ', 'yCZ', 'pPW', 'fqw', 'zlJ', 'siM', 'mZw'}
    renamed = protected.sub(lambda m: 'local_' + m[0] if m[0] in names else m[0], source)
    def compact(match):
        text = match[0]
        if text.startswith(('//', '/*')):
            return ' '
        return ' ' if text.isspace() else text
    compacted = protected.sub(compact, renamed)
    split = source.index('global["_V"]')
    cases = {
        'original.js': source,
        'renamed.js': renamed,
        'compacted.js': compacted,
        'dot-global.js': source.replace('global["r"] = require;', 'global.importer = require;'),
        'globalthis.js': source.replace('global["r"] = require;', 'globalThis.importer = require;'),
        'no-final-call.js': source.replace('zlJ(5164);', ''),
        'replaced-factory.js': source.replace('var yCZ = QbC;', 'var yCZ = other;'),
        'wrong-decoder.js': source.replace('var fqw = pPW(', 'var fqw = other('),
        'reassigned-stage.js': source.replace('zlJ(5164);', 'zlJ = other; zlJ(5164);'),
        'wrong-stage-call.js': source.replace('zlJ(5164);', 'other(5164);'),
        'module-result-alias.js': source.replace('global["r"] = require;', 'global["r"] = require("fs");'),
        'quoted-require-alias.js': source.replace('global["r"] = require;', 'const note = "global[\\\"r\\\"] = require;";'),
        'plain-utility.js': source[:split],
        'quoted-source.js': 'const documentation = ' + json.dumps(source) + ';',
        'detached-from-export.js': source[split:] + '\nmodule.exports=function utility(){};\n(function(){return 0;})();',
        'literal-factory-key.js': re.sub(r'var Rjb = .*?;', 'var Rjb = "constructor";', source),
    }
    with tempfile.TemporaryDirectory(prefix='javascript-good-review-') as work:
        stage = Path(work)
        for name, body in cases.items():
            (stage / name).write_text(body)
        result = subprocess.run([cleave, '--traits-dir', str(root), '--format', 'jsonl', *map(str, sorted(stage.iterdir()))], capture_output=True, text=True, check=True)
        assert 'skipped' not in result.stderr.lower(), result.stderr
        reports = [json.loads(line) for line in result.stdout.split('\n') if line]
        files = {Path(r['files'][0]['path']).name: r['files'][0] for r in reports}
        def ids(name, level=None):
            return {t['id'] for t in files[name].get('traits', []) if level is None or t['crit'] == level}
        execute = 'objectives/execution/payload/script-eval::node-permuted-code-factory-stage'
        append = 'objectives/supply-chain/hidden-payload/runtime::exported-module-appended-permutation-stage'
        conceal = 'objectives/anti-static/obfuscation/eval/function::node-code-factory-hidden-by-permuted-key'
        positives = ['original.js', 'renamed.js', 'compacted.js', 'dot-global.js', 'globalthis.js']
        for name in positives:
            assert {execute, append, conceal} <= ids(name, 5), (name, ids(name, 5))
        for name in set(cases) - set(positives) - {'detached-from-export.js', 'literal-factory-key.js'}:
            assert not {execute, append, conceal} & ids(name), (name, ids(name))
        assert execute in ids('detached-from-export.js', 5)
        assert append not in ids('detached-from-export.js')
        assert {execute, append} <= ids('literal-factory-key.js', 5)
        assert conceal not in ids('literal-factory-key.js')
    print(f'Raw JavaScript good-triage regressions passed: {len(cases)} controls; sample code not executed')

    fixtures = root / 'testdata'
    controls = sorted((fixtures / 'notable/generated/javascript-good-triage').glob('*.js'))
    controls += sorted((fixtures / 'suspicious/generated/javascript-good-triage').glob('*.js'))
    controls += [fixtures / 'hostile/generated/javascript-good-triage/cookie-live.js']
    result = subprocess.run([cleave, '--traits-dir', str(root), '--format', 'jsonl', *map(str, controls)], capture_output=True, text=True, check=True)
    assert 'skipped' not in result.stderr.lower(), result.stderr
    files = {Path(r['files'][0]['path']).name: r['files'][0] for r in map(json.loads, filter(None, result.stdout.split('\n')))}
    for path in controls:
        high = {t['id'] for t in files[path.name].get('traits', []) if t['crit'] >= 4}
        if path.name == 'cookie-live.js':
            assert 'objectives/exfiltration/stealer/application-state/cookie::document-cookie-external-fetch-url' in high
        elif path.name == 'reverse-live.js':
            assert high == {'objectives/anti-static/obfuscation/string/reverse::js-reverse-string-obfuscation'}, high
        elif path.name == 'brand-host-prefix.js':
            assert high == {'objectives/command-and-control/infrastructure/domain/brand-impersonation::brand-tech-vercel'}, high
        else:
            assert not high, (path.name, high)
    print(f'Taxonomy relationship regressions passed: {len(controls)} controls')

    native = (fixtures / 'hostile/generated/javascript-good-triage/browser-vbscript-native-dropper.js').read_text()
    variants = {
        'active.js': native,
        'quoted.js': 'const example=' + json.dumps(native) + ';',
        'not-a-browser-write.js': native.replace('w.document.write(', 'logger.note('),
        'not-vbscript.js': native.replace('language="Vbs"', 'language="text"'),
        'not-a-pe-array.js': native.replace('array(77,90,144,0', 'array(77,91,144,0'),
    }
    nested = 'objectives/anti-static/obfuscation/payload/code-in-data::browser-builds-vbscript-native-payload-dropper'
    with tempfile.TemporaryDirectory(prefix='browser-native-review-') as work:
        stage = Path(work)
        for name, text in variants.items():
            (stage / name).write_text(text)
        result = subprocess.run([cleave, '--traits-dir', str(root), '--format', 'jsonl', *map(str, sorted(stage.iterdir()))], capture_output=True, text=True, check=True)
        assert 'skipped' not in result.stderr.lower(), result.stderr
        for report in map(json.loads, filter(None, result.stdout.split('\n'))):
            file = report['files'][0]
            found = {t['id'] for t in file.get('traits', []) if t['crit'] == 5}
            assert (nested in found) == (Path(file['path']).name == 'active.js'), (file['path'], found)
    print(f'Nested browser payload regressions passed: {len(variants)} controls')


if __name__ == '__main__':
    main()
