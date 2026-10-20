"""Static positive and near-miss controls; never execute the fixture code."""
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[3]
FIXTURES = pathlib.Path(__file__).resolve().parent
result = subprocess.run(
    ['cleave', '--traits-dir', str(ROOT), '--format', 'json', str(FIXTURES)],
    capture_output=True, text=True, check=False,
)
if result.returncode not in (0, 1) or not result.stdout.strip():
    raise RuntimeError(result.stderr or result.stdout)
decoder = json.JSONDecoder()
remaining = result.stdout
files = {}
while remaining.strip():
    report, consumed = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[consumed:]
    for file in report['files']:
        files[pathlib.Path(file['path']).name] = file

cases = {
    'query-path.ps1': (
        ['micro-behaviors/fs/path/account-db::windows-ntds-database-path-text',
         'micro-behaviors/os/wmi/query::get-wmiobject-remote-process'], []),
    'socket-relay.ps1': (
        ['objectives/command-and-control/reverse-shell/stream-bridge::powershell-tcpclient-shell-stream-bridge'], []),
    'socket-process.ps1': ([],
        ['objectives/command-and-control/reverse-shell/stream-bridge::powershell-tcpclient-shell-stream-bridge']),
    'actions.py': ([], ['well-known/app/infrastructure/harbor::source-tree',
                        'well-known/app/infrastructure/harbor::package-identity']),
    'names.py': (
        ['metadata/lang/source/naming::downloadurl-identifier-text',
         'micro-behaviors/data/string/compare::python-printable-ascii-range-test',
         'micro-behaviors/data/format/credentials::admin-admin-pair',
         'micro-behaviors/data/format/credentials::guest-guest-pair'], []),
    'capabilities.ps1': (
        ['micro-behaviors/data/parse/xml::powershell-downloaded-xml-cast',
         'micro-behaviors/data/string/split::powershell-pipe-field-selector',
         'metadata/lang/natural/vocabulary::bind-shell-term',
         'micro-behaviors/metaprogramming/reflection::powershell-currentdomain-member-text'], []),
}
for name, (required, forbidden) in cases.items():
    traits = {t['id']: t for t in files[name].get('traits', [])}
    for trait in required:
        assert trait in traits, (name, 'missing', trait)
    for trait in forbidden:
        assert trait not in traits, (name, 'unexpected', trait)
    if name != 'socket-relay.ps1':
        assert not any(t['crit'] >= 4 for t in traits.values()), (name, 'unexpected elevated trait')
print(f'{len(cases)} static positive/near-miss controls passed')
