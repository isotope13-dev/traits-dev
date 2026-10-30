#!/usr/bin/env python3
"""Static endpoint-review checks for C2 UI, execution probes and an install loader."""
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
    parser.add_argument('--node-sample', type=Path)
    parser.add_argument('--node-reference', type=Path)
    args = parser.parse_args()
    assert bool(args.node_sample) == bool(args.node_reference), 'Supply both Node paths or neither'
    root = Path(__file__).resolve().parents[2]
    cleave = str(Path(args.cleave).resolve())
    fixtures = root / 'testdata/hostile/generated/javascript-endpoint-review'
    callback = (fixtures / 'mythic-callback-config.js').read_text()
    builder = (fixtures / 'mythic-payload-builder.js').read_text()
    dns = (fixtures / 'dns-execution-probe.js').read_text()
    loader = (root / 'testdata/suspicious/generated/javascript-edge-review/profile-exchange.js').read_text()
    cases = {
        'callback.js': callback,
        'builder.js': builder,
        'renamed-callback.js': callback.replace('ImportCallbackConfigDialog', 'RenderImportedSession'),
        'renamed-builder.js': builder.replace('ImportTagtypesDialog', 'RenderBuilder'),
        'quoted-callback.js': 'const source = ' + json.dumps(callback) + ';\n',
        'generic-builder.js': builder.replace('Submitted payload to build pipeline', 'Saved object'),
        'schema-only.js': 'const schema = `mutation { createPayload(payloadDefinition: $payload) { uuid } }`;\n',
        'dns-probe.js': dns,
        'renamed-dns.js': re.sub(r'(?<!\.)\b(domain|pcName|currentDir|networkInterfaces|callbackData)\b', lambda m: 'value_' + m[0], dns).replace('poc.collector.invalid', 'observer.example.invalid'),
        'ordinary-dns.js': 'const dns=require("dns"); dns.resolve("example.invalid", console.log);\n',
        'quiet-inventory.js': dns.replace("console.log('Callback sent to', addresses);", "console.log('Resolved addresses', addresses);"),
        'deferred-dns.js': dns.replace('dns.resolve(domain,', 'function check() { dns.resolve(domain,').replace('// Export a module', '}\n// Export a module'),
        'fake-dns.js': dns.replace("require('dns')", '({ resolve() {} })'),
        'quoted-dns.js': 'const source = ' + json.dumps(dns) + ';\n',
        'loader.js': loader,
        'aliased-loader.js': loader.replace('var exec =', 'var launchStage =').replace('exec(', 'launchStage('),
        'no-replacement.js': loader.replace('exec(pkg_install);', 'console.log(pkg_install);'),
        'reassigned-replacement.js': loader.replace('exec(pkg_install);', 'pkg_install = "echo complete"; exec(pkg_install);'),
    }
    with tempfile.TemporaryDirectory(prefix='javascript-endpoint-') as work:
        stage = Path(work)
        for name, text in cases.items():
            (stage / name).write_text(text)
        def package(name, source, hook=True):
            manifest = {'name': 'identity-helper', 'version': '1.0.0', 'main': 'index.js'}
            if hook:
                manifest['scripts'] = {'preinstall': 'node index.js'}
            with tarfile.open(stage / name, 'w:gz') as archive:
                for member, text in {'index.js': source, 'package.json': json.dumps(manifest)}.items():
                    data = text.encode()
                    entry = tarfile.TarInfo('package/' + member)
                    entry.size = len(data)
                    archive.addfile(entry, io.BytesIO(data))
        package('loader.tgz', loader)
        package('aliased-loader.tgz', cases['aliased-loader.js'])
        package('no-hook.tgz', loader, False)
        package('no-replacement.tgz', cases['no-replacement.js'])
        paths = list(map(str, sorted(stage.iterdir())))
        groups = [paths]
        if args.node_sample:
            # Keep the large binary comparisons in individual reports.
            groups.extend([[str(args.node_sample.resolve())], [str(args.node_reference.resolve())]])
        reports = []
        for group in groups:
            result = subprocess.run([cleave, '--traits-dir', str(root), '--format', 'jsonl', *group], capture_output=True, text=True, check=True)
            assert 'skipped' not in result.stderr.lower(), result.stderr
            # JSON string values can contain Unicode line separators.
            reports.extend(json.loads(line) for line in result.stdout.split('\n') if line)
        files = {Path(r['files'][0]['path']).name: r['files'][0] for r in reports}
        def ids(name, level=None):
            return {t['id'] for t in files[name].get('traits', []) if level is None or t['crit'] == level}
        mythic = 'well-known/tool/offensive/mythic::'
        for name in ['callback.js', 'renamed-callback.js']:
            assert mythic + 'operator-cross-server-callback-importer' in ids(name, 5), (name, ids(name, 5))
        for name in ['builder.js', 'renamed-builder.js']:
            assert mythic + 'operator-payload-build-interface' in ids(name, 5), (name, ids(name, 5))
        probe = 'objectives/exfiltration/oob/callback::node-load-time-host-inventory-dns-probe'
        for name in ['dns-probe.js', 'renamed-dns.js']:
            assert probe in ids(name, 5), (name, ids(name, 5))
        for name in ['ordinary-dns.js', 'quiet-inventory.js', 'deferred-dns.js', 'fake-dns.js', 'quoted-dns.js']:
            assert probe not in ids(name), (name, ids(name))
        launch = 'objectives/execution/payload/interpreter-stdin::npm-preinstall-probed-profile-shell-loader'
        replace = 'objectives/supply-chain/trojanized/app/package::preinstall-profile-loader-scoped-replacement'
        for name in ['loader.tgz', 'aliased-loader.tgz']:
            assert {launch, replace} <= ids(name, 5), (name, ids(name, 5))
        assert launch in ids('no-replacement.tgz', 5)
        assert replace not in ids('no-replacement.tgz')
        assert launch not in ids('no-hook.tgz')
        scoped = 'micro-behaviors/process/create/shell/command-string::node-exec-scoped-registry-install'
        assert scoped not in ids('reassigned-replacement.js')
        for name in ['quoted-callback.js', 'generic-builder.js', 'schema-only.js', 'ordinary-dns.js', 'quiet-inventory.js', 'deferred-dns.js', 'fake-dns.js', 'quoted-dns.js']:
            assert not ids(name, 5), (name, ids(name, 5))
        if args.node_sample:
            signature = 'metadata/signed/certificate/signature::pe-signature-digest-mismatch'
            gui = 'well-known/lib/runtime/scripted/node-runtime::gui-runtime-signed-image-mismatch'
            assert {signature, gui} <= ids(args.node_sample.name, 4)
            assert not {signature, gui} & ids(args.node_reference.name)
    print(f'Endpoint review regressions passed: {len(cases) + 4 + (2 if args.node_sample else 0)} controls; no sample code executed')


if __name__ == '__main__':
    main()
