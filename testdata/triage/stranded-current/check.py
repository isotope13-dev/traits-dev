"""Check CGI value relationships and packaged implant detection, statically."""
from pathlib import Path
import json, os, subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUTPUT = 'micro-behaviors/process/io/stream::perl-captured-command-line-output'
QUERY = 'objectives/command-and-control/backdoor/webshell/request/command::perl-cgi-variable-backtick-webshell'
REPLY = 'objectives/command-and-control/backdoor/webshell/relay::perl-cgi-command-output-response'
C2 = 'well-known/tool/offensive/mettle::c2-implant-session'
CASES = {
    'cgi-results.pl': ([OUTPUT, QUERY, REPLY], []),
    'cgi-fixed-command.pl': ([OUTPUT], [QUERY, REPLY]),
    'cgi-unrelated-array.pl': ([QUERY], [OUTPUT, REPLY]),
    'cgi-reassigned-array.pl': ([QUERY], [OUTPUT, REPLY]),
    'console-results.pl': ([OUTPUT], [QUERY, REPLY]),
    'bin/mettle.exe': ([C2], []),
}
env = os.environ.copy()
env.pop('SCAN_HOPPER', None)
env['CLEAVE_TRAITS_DIR'] = str(ROOT)
result = subprocess.run(
    ['atomscan', '--no-update', '--follow=none', '--mode', 'slow', '-f', 'json',
     *[str(HERE / name) for name in CASES]],
    env=env, text=True, capture_output=True,
)
assert result.returncode in (0, 1), result.stderr
assert result.stdout.strip(), result.stderr
reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
by_path = {Path(r['raw']['files'][0]['path']).resolve(): r for r in reports}
for name, (present, absent) in CASES.items():
    report = by_path[(HERE / name).resolve()]
    traits = {t['id']: t['crit'] for f in report['raw']['files'] for t in f.get('traits', [])}
    assert set(present) <= traits.keys(), (name, 'missing', set(present) - traits.keys())
    assert not set(absent) & traits.keys(), (name, 'unexpected', set(absent) & traits.keys())
    if name == 'bin/mettle.exe':
        assert traits[C2] == 5, (name, traits[C2])
    print('PASS', name, flush=True)
print(f'{len(CASES)} focused controls passed')
