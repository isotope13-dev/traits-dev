"""htaccess AddHandler persistence drop.

Run: python3 testdata/htaccess-addhandler-persistence/verify.py <scratch-directory>

`htaccess-addhandler-persistence` convicts a PHP file that writes an
.htaccess mapping a data suffix (.cache/.dat/.log) to the PHP handler:
server-config persistence turning an inert data drop into an executable
webshell. The write must sit near the directive so documentation that
merely mentions AddHandler, plain rewrite-rule drops, and far-apart
coincidences do not convict.

Controls: the persistence drop positive must report the hostile; the
rewrite-only, docs-only, and far-apart negatives must not.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ('objectives/command-and-control/backdoor/webshell/config::'
          'htaccess-addhandler-persistence')

POSITIVE = """<?php
$cache = __DIR__ . '/drop.cache';
file_put_contents($cache, $payload);
file_put_contents(__DIR__ . '/.htaccess',
    "AddHandler application/x-httpd-php .cache\\n");
"""

REWRITE_NEGATIVE = """<?php
// Legitimate pretty-URL bootstrap drop: rewrite rules only, no handler.
file_put_contents(__DIR__ . '/.htaccess',
    "RewriteEngine On\\nRewriteRule ^(.*)$ index.php [L]\\n");
"""

DOCS_NEGATIVE = """<?php
// Docs note: some hosts need AddHandler application/x-httpd-php .cache
// in .htaccess for legacy cache files. No write happens here.
echo "see admin guide";
"""

FAR_NEGATIVE = ("<?php\n// Admin pastes a handler docblock at the top.\n"
                "// AddHandler application/x-httpd-php .cache\n"
                + ("// filler line to push the write far away.\n" * 120) +
                "file_put_contents(__DIR__ . '/.htaccess',\n"
                "    \"RewriteEngine On\\n\");\n")


def scan(path):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(path)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'),
        text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    return {t['id'] for entry in report['files'] for t in entry['traits']}


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    cases = {
        'persistence-positive.php': (POSITIVE, True),
        'rewrite-negative.php': (REWRITE_NEGATIVE, False),
        'docs-negative.php': (DOCS_NEGATIVE, False),
        'far-apart-negative.php': (FAR_NEGATIVE, False),
    }
    for name, (body, hostile) in cases.items():
        path = dest / name
        path.write_text(body)
        assert (TARGET in scan(path)) == hostile, name
        print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
