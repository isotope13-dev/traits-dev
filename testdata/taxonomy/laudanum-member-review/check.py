"""Run focused controls outside naming-based test-directory suppressors."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', required=True, type=Path)
args = parser.parse_args()
fixtures = Path(__file__).resolve().parent
traits = fixtures.parents[2]
php404 = 'objectives/evasion/decoy/http-error::php-ip-aware-command-shell-404'
asp404 = 'objectives/evasion/decoy/http-error::asp-ip-aware-command-shell-404'
aspx404 = 'objectives/evasion/decoy/http-error::aspnet-command-webshell-404'
status404 = 'micro-behaviors/communications/http/response::server-response-statuscode-not-found'
aspxshell = 'objectives/command-and-control/backdoor/webshell/request/command::aspnet-request-command-webshell'
fork = 'micro-behaviors/process/create/fork::pcntl-fork'
wait = 'micro-behaviors/process/sync/join::pcntl-waitpid'
with tempfile.TemporaryDirectory(prefix='controls-', dir=args.scratch) as temp:
    for path in fixtures.glob('*'):
        if path.suffix in ('.php', '.asp', '.aspx', '.cs', '.js'):
            shutil.copyfile(path, Path(temp) / path.name)
    # Preserve attack coverage when the error-response leg is absent.
    shell = (fixtures / 'command-form-404.aspx').read_text()
    (Path(temp) / 'command-form-without-404.aspx').write_text(
        shell.replace('StatusCode = 404', 'StatusCode = 200'))
    result = subprocess.run(
        ['cleave', '--traits-dir', str(traits), '--min-crit', 'component', '--json', temp],
        text=True, capture_output=True, check=True)
    files = [f for line in result.stdout.splitlines()
             for f in json.loads(line)['files']]
    observed = {Path(f['path']).name: f['traits'] for f in files}
    for name, expected in [('command-form-404.php', php404),
                           ('command-form-404.asp', asp404),
                           ('command-form-404.aspx', aspx404)]:
        assert expected in {t['id'] for t in observed[name]}, name
    for name in ['ordinary-ip-404.php', 'ordinary-ip-404.asp',
                 'fork-and-wait.php', 'fork-mentions.php',
                 'ordinary-ip-404.aspx', 'status-assignment.cs',
                 'status-comparison.cs', 'status-assignment.js']:
        assert not any(t['crit'] >= 4 for t in observed[name]), name
    for name in ['ordinary-ip-404.aspx', 'status-assignment.cs',
                 'status-assignment.js', 'command-form-404.aspx']:
        assert status404 in {t['id'] for t in observed[name]}, name
    for name in ['status-comparison.cs', 'command-form-without-404.aspx']:
        assert status404 not in {t['id'] for t in observed[name]}, name
        assert aspx404 not in {t['id'] for t in observed[name]}, name
    assert aspxshell in {t['id'] for t in observed['command-form-without-404.aspx']}
    assert fork in {t['id'] for t in observed['fork-and-wait.php']}
    # Unconsumed baseline traits are stripped from rendered scan findings.
    # Trace the preserved wait matcher directly, including the comment control.
    for name, should_match in [('fork-and-wait.php', True),
                               ('fork-mentions.php', False)]:
        trace = subprocess.run(
            ['cleave', '--traits-dir', str(traits), 'test-rules',
             str(Path(temp) / name), '--rules', wait],
            text=True, capture_output=True, check=True)
        assert ('\nMATCHED ' + wait in trace.stdout) == should_match, name
    assert not {fork, wait} & {t['id'] for t in observed['fork-mentions.php']}
    for matches in observed.values():
        assert not any(t['id'] in {
            'micro-behaviors/process/fork/clone::pcntl-fork',
            'micro-behaviors/process/fork/clone::pcntl-waitpid'} for t in matches)
    print(json.dumps({'controls': len(observed), 'status': 'passed',
                      'findings': observed}, indent=2))
