#!/usr/bin/env python3
"""Statically verify endpoint-review exploit bindings and ordinary controls."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
IDS = {
    'loader': {
        'objectives/execution/payload/file-exec/detached::ruby-detached-unverified-temp-stage',
        'objectives/evasion/process/hidden/execution::ruby-remote-stage-null-stdio-detachment',
    },
    'portal': {
        'objectives/execution/exploit/command-injection::ruby-portalname-command-injection-module',
        'objectives/evasion/masquerade/image::ruby-exploit-shell-upload-as-jpeg',
    },
    'couch': {
        'objectives/execution/exploit/service-command-injection::ruby-couchdb-query-server-shell-exploit-module',
        'objectives/execution/exploit/sonicwall-sma::ruby-sma-negative-bookmark-couchdb-exploit',
    },
    'setwan': {
        'objectives/execution/exploit/http-command-injection::ruby-setwan-shell-substitution-exploit',
        'objectives/discovery/system/fingerprint/user::ruby-exploit-remote-id-marker-probe',
    },
}


def objects(text):
    decoder = json.JSONDecoder()
    offset = 0
    while offset < len(text):
        while offset < len(text) and text[offset].isspace():
            offset += 1
        if offset == len(text):
            return
        value, offset = decoder.raw_decode(text, offset)
        yield value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default=os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave')))
    args = parser.parse_args()
    base = ROOT / 'testdata/hostile/generated/ruby-endpoint-review'
    loader = (base / 'detached-loader.rb').read_text()
    portal = (base / 'portalname-exploit.rb').read_text()
    couch = (base / 'couchdb-exploit.rb').read_text()
    wan = (ROOT / 'testdata/hostile/generated/wan-credential-injection/setwan-substitution.rb').read_text()
    injection = {'objectives/execution/exploit/command-injection::ruby-portalname-command-injection-module'}
    image = IDS['portal'] - injection
    cases = {
        'loader.rb': (loader, IDS['loader'], set()),
        'portal.rb': (portal, IDS['portal'], set()),
        'couch.rb': (couch, IDS['couch'], set()),
        'wan.rb': (wan, IDS['setwan'], set()),
        'verified-download.rb': (loader.replace('--insecure --silent', '--fail --silent'), set(), IDS['loader']),
        'uncalled-helper.rb': ('def launch\n' + loader + 'end\n', set(), IDS['loader']),
        'ordinary-portal-field.rb': (portal.replace('[ "portalname", cmd ]', '[ "portalname", "VirtualOffice" ]'), set(), injection),
        'unrelated-portal-helper.rb': (portal.replace('run_command(swap_cookie, "#{prefix}', 'other_command(swap_cookie, "#{prefix}'), set(), injection),
        'actual-jpeg-content.rb': (portal.replace('#!/bin/bash', 'JPEG image data'), set(), image),
        'renamed-portal-helpers.rb': (re.sub(r'\bupload_payload\b', 'transmit_logo', re.sub(r'\brun_command\b', 'set_portal', portal)), IDS['portal'], set()),
        'read-only-couchdb.rb': (couch.replace("'method' => 'PUT'", "'method' => 'GET'"), set(), IDS['couch']),
        'javascript-couchdb.rb': (couch.replace('/bin/sh -c #{payload.encoded}', '/usr/bin/node'), set(), IDS['couch']),
        'ordinary-wan-user.rb': (wan.replace('$(id > /tmp/marker_sub)', 'example-user'), set(), IDS['setwan']),
        'unsent-wan-object.rb': (wan.replace('http.request(request)', 'http.request(other_request)'), set(), IDS['setwan']),
        'quoted-portal-example.rb': ("puts <<'EXAMPLE'\n" + portal + '\nEXAMPLE\n', set(), IDS['portal']),
    }
    with tempfile.TemporaryDirectory(prefix='ruby-endpoint-review-') as work:
        paths = []
        for name, (source, *_rest) in cases.items():
            path = Path(work) / name
            path.write_text(source)
            paths.append(str(path))
        result = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--format=json', *paths], capture_output=True, text=True, check=True)
        observed = {}
        for report in objects(result.stdout):
            for item in report['files']:
                observed[Path(item['path']).name] = item.get('traits', [])
        for name, (_source, required, forbidden) in cases.items():
            traits = observed[name]
            hostile = {item['id'] for item in traits if item['crit'] == 5}
            assert required <= hostile, (name, 'missing hostile', required - hostile)
            assert not forbidden & {item['id'] for item in traits}, (name, 'unexpected', forbidden & {item['id'] for item in traits})
            if required:
                assert len({item.split('::')[0] for item in hostile}) >= 2, (name, 'needs two hostile directories')
    print(f'Ruby endpoint review regressions passed: {len(cases)} cases')


if __name__ == '__main__':
    main()
