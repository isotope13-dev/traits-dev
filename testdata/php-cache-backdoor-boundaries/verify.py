"""Scan PHP controls as data; never execute the generated programs."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
COPY = 'micro-behaviors/fs/file/copy::php-write-own-source-copy'
WRITE = 'micro-behaviors/fs/write/file/full::php-htaccess-write'
READ = 'micro-behaviors/fs/read/file/full::php-file-get-variable-source'
XOR = 'micro-behaviors/data/encoding/xor::'
LOOPS = {XOR + 'php-repeating-key-index-xor', XOR + 'php-byte-xor-transform-loop'}
CONFIG = 'objectives/command-and-control/backdoor/webshell/config::htaccess-command-webshell-handler'
TRANSFORM = '$out .= chr(ord($bytes[$n]) ^ ord($mask[$n % strlen($mask)]));'
CONSOLE = """
$child = proc_open($_REQUEST['task'], [1 => ['pipe', 'w']], $handles);
echo stream_get_contents($handles[1]);
"""


def main():
    dest = Path(sys.argv[1]).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    cases = {
        'self-copy.php': ("file_put_contents($target, file_get_contents(__FILE__));", {COPY}, {READ}),
        'ordinary-copy.php': ("file_put_contents($target, file_get_contents($source));", {READ}, {COPY}),
        'self-read-only.php': ("echo file_get_contents(__FILE__);", set(), {COPY, READ}),
        'unrelated-write.php': ("$own = file_get_contents(__FILE__); file_put_contents($target, 'report');", set(), {COPY}),
        'htaccess-write.php': ("file_put_contents(__DIR__ . '/.htaccess', 'RewriteEngine On');", {WRITE}, set()),
        'htaccess-content.php': ("file_put_contents('report.txt', '.htaccess');", set(), {WRITE}),
        'htaccess-read.php': ("file_get_contents('.htaccess'); file_put_contents('report.txt', 'report');", set(), {WRITE}),
        'htaccess-backup.php': ("file_put_contents('.htaccess.bak', 'backup');", set(), {WRITE}),
        'loop.php': ('for ($n=0; $n<strlen($bytes); $n++) { ' + TRANSFORM + ' }', LOOPS, set()),
        'single-transform.php': (TRANSFORM, set(), LOOPS),
        'quoted-loop.php': ('// for ($n=0; $n<strlen($bytes); $n++) { ' + TRANSFORM + ' }', set(), LOOPS),
        'false-config.php': ("file_put_contents('report', '.htaccess');\n" +
            "$directive = 'AddHandler application/x-httpd-php .dat';\n" + CONSOLE, set(), {CONFIG, WRITE}),
        'data-handler.php': ("file_put_contents(__DIR__ . '/.htaccess', " +
            "'AddHandler application/x-httpd-php .log');\n" + CONSOLE, {CONFIG, WRITE}, set()),
    }
    paths = []
    for name, (source, _, _) in cases.items():
        path = dest / name
        path.write_text('<?php\n' + source + '\n')
        paths.append(str(path))
    if len(sys.argv) > 2:
        sample = Path(sys.argv[2]).resolve()
        cases[sample.name] = ('', LOOPS | {COPY, WRITE, CONFIG}, {READ})
        paths.append(str(sample))
    run = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                          '--format', 'json', *paths], text=True, capture_output=True, check=True)
    decoder = json.JSONDecoder()
    documents = []
    pending = run.stdout.strip()
    while pending:
        doc, end = decoder.raw_decode(pending)
        documents.append(doc)
        pending = pending[end:].lstrip()
    reports = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
               for doc in documents for f in doc['files']}
    for name, (_, required, excluded) in cases.items():
        actual = reports[name]
        assert required <= actual, (name, 'missing', required - actual)
        assert not excluded & actual, (name, 'unexpected', excluded & actual)
        print('PASS', name)


if __name__ == '__main__':
    main()
