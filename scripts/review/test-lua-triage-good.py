#!/usr/bin/env python3
"""Check Lua triage boundaries without executing any sample code."""
import argparse
import json
import re
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='../cleave/target/release/cleave')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    fixture = 'generated/taxonomy/lua-triage-good-20261102'
    hostile = repo / 'testdata/hostile' / fixture
    benign = repo / 'testdata/notable' / fixture
    originals = {p.name: p.read_bytes() for folder in (hostile, benign) for p in folder.iterdir()}
    bits = originals['bits-stage.lua'].decode()
    html = originals['html-package.lua'].decode()
    router = originals['exploit-router.sample'].decode(errors='replace')
    cases = dict(originals)
    # The basename supplies no verdict. The PHP short tag and dispatch body do.
    cases['renamed-router.bin'] = originals['exploit-router.sample']
    cases['renamed-bits.lua'] = originals['bits-stage.lua']
    cases['renamed-html.lua'] = originals['html-package.lua']
    cases['ordinary-data-download.lua'] = html.replace('sessions/reverseshell', 'reports/summary.csv').encode()
    cases['ordinary-download-with-comment.lua'] = (
        '-- reverse shell payload documentation\n' +
        html.replace('sessions/reverseshell', 'reports/summary.csv')
    ).encode()
    cases['no-browser-click.lua'] = html.replace('    l.click();', '').encode()
    cases['transfer-only.lua'] = bits.replace(' && %s && del %s', '').encode()
    cases['no-encoding.lua'] = bits.replace('encodewinbase64 ', 'show-command ').encode()
    cases['documentation.php'] = b'<?php\n// MPack main script\necho "browser exploit documentation";\n'
    cases['browser-only.php'] = b'<?php\nif ($browser[os] == "Windows NT 5.0") { echo "old browser"; }\n'
    cases['stringified-ffi.lua'] = b'local log = "ffi.cdef"\nreturn log\n'
    # Future variants: preserve semantics while changing names and syntax.
    cases['quoted-uppercase-bits.lua'] = bits.replace(
        'bitsadmin /transfer', 'BITSADMIN.EXE  /TRANSFER').replace(
        '&& %s && del %s', '&& "%s"  &&  DEL "%s"').encode()
    cases['renamed-dispatch.lua'] = bits.replace('app.one_cmd', 'tool.submit').encode()
    cases['no-unused-port.lua'] = bits.replace(
        '    local lport = app.params["lport"]\n', '').replace(
        'not lhost or not lport', 'not lhost').encode()
    cases['comment-only-encoder.lua'] = (
        re.sub(r'(?m)^\s*app\.one_cmd[^\n]*\n', '', bits) +
        '\n-- app.one_cmd("encodewinbase64 " .. cmd)\n').encode()
    cases['logged-server.lua'] = bits.replace('os.execute(', 'print(').encode()
    cases['printed-encoder.lua'] = bits.replace('app.one_cmd(', 'print(').encode()
    cases['logged-encoder.lua'] = bits.replace('app.one_cmd(', 'logger.info(').encode()
    renamed_html = html
    for before, after in [('key_bytes', 'material'), ('i', 'position'),
                          ('xor_encrypt', 'scramble')]:
        renamed_html = re.sub(r'\b' + before + r'\b', after, renamed_html)
    cases['renamed-xor.lua'] = renamed_html.encode()
    cases['compact-xor.lua'] = html.replace(
        'string.byte(data, i) ~ key_bytes[(i - 1) % #key_bytes + 1]',
        'string.byte(data,i)~key_bytes[(i-1)%#key_bytes+1]').encode()
    cases['different-index-divisor.lua'] = html.replace(
        '% #key_bytes + 1', '% #other_table + 1').encode()
    cases['xor-name-only.lua'] = b'function xor_encrypt(data) return data end\n'
    cases['quoted-xor.lua'] = (
        'local example = [[string.byte(data,i)~key_bytes[(i-1)%#key_bytes+1]]\n'
        'return example\n').encode()
    cases['parenthesized-router.php'] = re.sub(
        r"include '([^']+)'", r'require_once ("\1")', router).replace(
        '$browser[os]', '$client["os"]').encode()
    body = router.removeprefix('<?').removesuffix('?>')
    cases['quoted-router.php'] = (
        "<?php\n$guide = <<<'EXAMPLE'\n" + body + '\nEXAMPLE;\necho $guide;\n').encode()
    cases['fingerprint.php'] = b'<?php $id = md5(getenv("REMOTE_ADDR").getenv("HTTP_USER_AGENT"));'
    cases['reversed-fingerprint.php'] = b'<?php $id = md5(getenv("HTTP_USER_AGENT").getenv("REMOTE_ADDR"));'
    cases['repeated-ip.php'] = b'<?php $id = md5(getenv("REMOTE_ADDR").getenv("REMOTE_ADDR"));'
    cases['separate-hashes.php'] = b'<?php $a=md5(getenv("REMOTE_ADDR")); $b=md5(getenv("HTTP_USER_AGENT"));'
    cases['append-modes.php'] = b'<?php $mode="a+b"; $f=fopen("visits.log", $mode);'
    cases['qualified-append.php'] = b'<?php $mode="ab+"; $f=\\fopen("visits.log", $mode);'
    cases['append-comment.php'] = b'<?php // fopen("visits.log", "a")\necho "log rotation";'
    cases['get-log.lua'] = b'function rec(...) end\nrec("GET", "name")\n'
    expected_hostile = {'bits-stage.lua', 'html-package.lua', 'exploit-router.sample',
                        'renamed-router.bin', 'renamed-bits.lua', 'renamed-html.lua',
                        'quoted-uppercase-bits.lua', 'renamed-dispatch.lua',
                        'no-unused-port.lua', 'renamed-xor.lua', 'compact-xor.lua',
                        'parenthesized-router.php', 'no-browser-click.lua'}
    with tempfile.TemporaryDirectory(prefix='lua-triage-controls-') as directory:
        work = Path(directory)
        for name, data in cases.items():
            (work / name).write_bytes(data)
        result = subprocess.run([str((repo / args.cleave).resolve()), '--traits-dir', str(repo),
                                 '--all-files', '--format', 'json', str(work)],
                                check=True, capture_output=True, text=True)
        # splitlines also splits U+0085/U+2028 embedded in JSON strings.
        reports = [json.loads(line) for line in result.stdout.split('\n') if line.strip()]
        files = {Path(f['path']).name: f for report in reports for f in report['files']}
        assert set(cases) <= files.keys(), set(cases) - files.keys()
        for name in cases:
            traits = files[name].get('traits', [])
            elevated = [t['id'] for t in traits if t['crit'] >= 4]
            if name in expected_hostile:
                directories = {t['id'].split('::')[0] for t in traits if t['crit'] >= 5}
                assert len(directories) >= 2, (name, directories)
            elif name in {'no-encoding.lua', 'comment-only-encoder.lua', 'logged-server.lua',
                          'printed-encoder.lua', 'logged-encoder.lua'}:
                assert elevated == ['objectives/execution/payload/file-exec/command/fetch::lua-bitsadmin-execute-delete-template'], elevated
                assert all(t['crit'] < 5 for t in traits)
            elif name == 'different-index-divisor.lua':
                assert elevated == ['objectives/anti-static/obfuscation/payload/embedded::lua-reverse-shell-html-smuggling-generator'], elevated
            else:
                assert not elevated, (name, elevated)
            if name in ('exploit-router.sample', 'renamed-router.bin'):
                assert files[name]['type'] == 'php', files[name]['type']
            print('PASS', name)
        font_ids = {t['id'] for t in files['font-tasks.lua'].get('traits', [])}
        assert 'metadata/lang/source/literal/array::lua-letter-index-entries' in font_ids
        assert 'metadata/lang/source/syntax/assignment/name::lua-batch-tasks-field' in font_ids
        assert not any(t.startswith('objectives/') for t in font_ids), font_ids
        decoder_ids = {t['id'] for t in files['decoder-harness.lua'].get('traits', [])}
        assert 'metadata/lang/natural/vocabulary/security::lua-shellcode-term' in decoder_ids
        assert not any(t.startswith('objectives/') for t in decoder_ids), decoder_ids
        assert 'micro-behaviors/metaprogramming/reflection/modify/environment::lua-setfenv-reference' in decoder_ids
        assert 'micro-behaviors/communications/http/client/exchange::http-request-markers-or-response-stream' not in decoder_ids
        required = {
            'exploit-router.sample': {'micro-behaviors/communications/http/fingerprint::php-ip-user-agent-md5'},
            'fingerprint.php': {'micro-behaviors/communications/http/fingerprint::php-ip-user-agent-md5'},
            'reversed-fingerprint.php': {'micro-behaviors/communications/http/fingerprint::php-ip-user-agent-md5'},
            'append-modes.php': {'micro-behaviors/fs/file/io-mode::php-append-file-mode'},
            'qualified-append.php': {'micro-behaviors/fs/file/io-mode::php-append-file-mode'},
            'html-package.lua': {'micro-behaviors/data/decode/base64/unspecified::lua-ngx-decode-base64-call'},
            'renamed-xor.lua': {'micro-behaviors/data/bitwise/xor::lua-xor-byte-key-loop'},
            'compact-xor.lua': {'micro-behaviors/data/bitwise/xor::lua-xor-byte-key-loop'},
        }
        forbidden = {
            **{name: {'micro-behaviors/communications/http/fingerprint::php-ip-user-agent-md5'}
               for name in ['repeated-ip.php', 'separate-hashes.php']},
            **{name: {'micro-behaviors/data/bitwise/xor::lua-xor-byte-key-loop'}
               for name in ['different-index-divisor.lua', 'xor-name-only.lua', 'quoted-xor.lua']},
            'append-comment.php': {'micro-behaviors/fs/file/io-mode::php-append-file-mode'},
            'get-log.lua': {'micro-behaviors/communications/http/client/exchange::http-request-markers-or-response-stream'},
            'quoted-router.php': {'objectives/execution/exploit/watering-hole::php-browser-exploit-include-routing'},
        }
        for name in cases:
            ids = {t['id'] for t in files[name].get('traits', [])}
            assert required.get(name, set()) <= ids, (name, required.get(name, set()) - ids)
            assert not forbidden.get(name, set()) & ids, (name, forbidden.get(name, set()) & ids)
    print(f'{len(cases)} Lua triage controls passed')


if __name__ == '__main__':
    main()
