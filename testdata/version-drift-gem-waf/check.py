"""Exercise package-version and PHP startup boundaries without executing specimens."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
DEST = Path(sys.argv[1])
DEST.mkdir(parents=True, exist_ok=True)
SOURCE = 'metadata/lang/source/syntax/assignment::ruby-all-nine-version-assignment'
VERSION = 'metadata/package/versioning/sentinel::gem-version-placeholder'
PREPEND = 'micro-behaviors/process/lifecycle/auto-exec::htaccess-auto-prepend-setting'
OLD = 'objectives/command-and-control/backdoor/webshell/config::htaccess-auto-prepend-directive'
PERSIST = 'objectives/command-and-control/backdoor/webshell/config::userini-prepend-persistence'
COMMAND = 'objectives/command-and-control/backdoor/webshell/request/command::php-request-shell-execution'
CASES = {
    'release_test.rb': ('require "minitest/autorun"\nclass ReleaseTest < Minitest::Test\n'
        'def build_fixture\nGem::Specification.new do |s|\ns.version = "9.9.9"\nend\nend\nend\n',
        {SOURCE}, {VERSION}),
    'package.gemspec': ('Gem::Specification.new do |spec|\nspec.version = "9.9.9"\nend\n',
        {SOURCE, VERSION}, set()),
    'ordinary.gemspec': ('Gem::Specification.new do |spec|\nspec.version = "0.12.6"\nend\n',
        set(), {SOURCE, VERSION}),
    'firewall.php': ('<?php\n$directive = \'php_value auto_prepend_file "/srv/waf/bootstrap.php"\';\n'
        'file_put_contents(".htaccess", $directive);\n', {PREPEND}, {OLD}),
    'prepend.conf': ('php_value auto_prepend_file /srv/app/start.php\n', {PREPEND}, {OLD}),
    'no-prepend.php': ('<?php\n$directive = "php_value memory_limit 256M";\n', set(), {PREPEND, OLD}),
    'command.php': ('<?php\nfile_put_contents(".htaccess", \'php_value auto_prepend_file "/srv/app/start.php"\');\n'
        'system($_POST["job"]);\n', {PREPEND, COMMAND}, {OLD}),
    '.user.ini': ('auto_prepend_file=shell.png\n', {PERSIST}, {PREPEND}),
}
for name, (body, required, excluded) in CASES.items():
    (DEST / name).write_text(body)
result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                         '--format', 'json', '--all-files', str(DEST)],
                        text=True, capture_output=True, check=True)
assert not result.stderr.strip(), result.stderr
reports = []
remaining = result.stdout.strip()
while remaining:
    report, end = json.JSONDecoder().raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:].lstrip()
entries = [entry for report in reports for entry in report.get('files', [report])]
rows = []
for entry in entries:
    name = Path(entry['path']).name
    if name not in CASES:
        continue
    traits = {t['id']: t['crit'] for t in entry.get('traits', [])}
    _, required, excluded = CASES[name]
    assert required <= traits.keys(), (name, 'missing', required - traits.keys())
    assert not excluded & traits.keys(), (name, 'unexpected', excluded & traits.keys())
    if PREPEND in traits:
        assert traits[PREPEND] in (3, 'notable'), (name, traits[PREPEND])
    rows.append({'path': name, 'required': sorted(required), 'excluded': sorted(excluded)})
assert len(rows) == len(CASES), rows
print(json.dumps(rows, indent=2))
