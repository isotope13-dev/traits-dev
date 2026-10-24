#!/usr/bin/env python3
"""Scan inert source variants; never import or execute the specimens."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
PEAR = 'objectives/execution/exploit/include-gadget::'
BUILDER = PEAR + 'python-constructed-pear-command-query'
INJECT = PEAR + 'python-pear-request-command-injection'
TRAVERSE = PEAR + 'python-pear-traversal-command-injection'
MOVE = 'micro-behaviors/process/deploy/file-exec::python-response-move-win32-launch'
FLAGS = 'micro-behaviors/process/create/flags::python-win32-hidden-startup-launch'
HIDDEN = 'objectives/evasion/process/hidden/execution::python-moved-response-hidden-launch'


def main():
    pear = (HERE / 'pear-builder.py').read_text()
    moved = (HERE / 'moved-response.py').read_text()
    cases = []

    def add(name, source, required=(), forbidden=()):
        cases.append((name, source, set(required), set(forbidden)))

    add('pear-original', pear, [BUILDER, INJECT, TRAVERSE])
    add('pear-renamed', pear.replace('payload', 'page_code').replace('drop', 'output_file')
        .replace('writer_query', 'query_arg').replace('.session-cache', 'page-result'),
        [BUILDER, INJECT, TRAVERSE])
    add('pear-get', pear.replace('$_REQUEST', '$_GET'), [BUILDER, INJECT, TRAVERSE])
    add('pear-post', pear.replace('$_REQUEST', '$_POST'), [BUILDER, INJECT, TRAVERSE])
    for name, before, after in [
        ('different-payload', '+ payload +', '+ other_code +'),
        ('different-output', '+ drop\n', '+ other_output\n'),
        ('different-query', 'request(base, writer_query, writer_body)',
         'request(base, another_query, writer_body)'),
        ('local-command', "system($_REQUEST['c'])", "system('id')"),
        ('non-php-output', '.session-cache.php', '.session-cache.txt'),
    ]:
        assert before in pear
        add('pear-' + name, pear.replace(before, after), (), [BUILDER, INJECT, TRAVERSE])
    add('pear-no-transport', pear.replace('"POST",', '"HEAD",'), [BUILDER], [INJECT, TRAVERSE])
    add('pear-comment', '\n'.join('# ' + line for line in pear.splitlines()), (),
        [BUILDER, INJECT, TRAVERSE])
    add('response-original', moved, [MOVE, FLAGS, HIDDEN])
    add('response-renamed', moved.replace('staged_path', 'downloaded_file')
        .replace('mpozzjjdz', 'installed_file').replace('fetch_result', 'result')
        .replace('MicrosoftEngine', 'Tools'), [MOVE, FLAGS, HIDDEN])
    for name, before, after in [
        ('wrong-body', 'write_bytes(fetch_result.body)', 'write_bytes(other.body)'),
        ('wrong-move-source', 'shutil.move(str(staged_path)', 'shutil.move(str(other_file)'),
        ('wrong-move-target', 'str(mpozzjjdz))', 'str(other_file))'),
        ('wrong-command-path', "cmd = f'\"{mpozzjjdz}\"'", "cmd = f'\"{other_file}\"'"),
        ('wrong-command-arg', 'None,\n                    cmd,', 'None,\n                    other_cmd,'),
    ]:
        assert before in moved, name
        add('response-' + name, moved.replace(before, after), [FLAGS], [MOVE, HIDDEN])
    for name, before, after in [
        ('visible-window', 'startup.wShowWindow = 0', 'startup.wShowWindow = 1'),
        ('no-startup-flag', 'startup.dwFlags = 0x00000001', 'startup.dwFlags = 0'),
        ('wrong-startup-pointer', 'ctypes.byref(startup)', 'ctypes.byref(other_startup)'),
        ('console-enabled', '0x08000000,', '0,'),
    ]:
        assert before in moved
        add('response-' + name, moved.replace(before, after), [MOVE], [FLAGS, HIDDEN])
    add('response-decimal-flags', moved.replace('0x08000000,', '134217728,'), [MOVE, FLAGS, HIDDEN])
    add('response-comment', '\n'.join('# ' + line for line in moved.splitlines()), (),
        [MOVE, FLAGS, HIDDEN])
    with tempfile.TemporaryDirectory(prefix='pear-response-controls-') as temporary:
        paths = []
        for name, source, _, _ in cases:
            path = Path(temporary) / (name + '.py')
            path.write_text(source)
            paths.append(str(path))
        run = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'jsonl', *paths],
                             capture_output=True, text=True, check=True)
        decoder = json.JSONDecoder()
        remaining = run.stdout.lstrip()
        findings = {}
        while remaining:
            report, end = decoder.raw_decode(remaining)
            remaining = remaining[end:].lstrip()
            for file in report.get('files', []):
                findings[Path(file['path']).stem] = {t['id'] for t in file.get('traits', [])}
        for name, _, required, forbidden in cases:
            actual = findings[name]
            assert required <= actual, (name, 'missing', sorted(required - actual))
            assert not forbidden & actual, (name, 'unexpected', sorted(forbidden & actual))
    print(json.dumps({'passed': len(cases), 'cases': [name for name, *_ in cases]}, indent=2))


if __name__ == '__main__':
    main()
