"""Check appliance-path exclusions without suppressing developer paths."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
fixtures = Path(__file__).resolve().parent
root = fixtures.parents[2]
home_trait = 'micro-behaviors/fs/path/location::hardcoded-home-dir-path'
exploit_traits = {
    'objectives/evasion/security-bypass/auth::ivanti-protected-cgi-fetch-axios-client',
    'objectives/execution/exploit/network-service/command-execution::ivanti-temporary-cgi-fetch-axios-client',
}

for name in ('ivanti-fetch.js', 'ivanti-axios.ts', 'home-path-control.js'):
    path = fixtures / name
    result = subprocess.run(
        [args.cleave, '--traits-dir', str(root), '--format', 'json', str(path)],
        check=True, capture_output=True, text=True,
    )
    report = json.loads(result.stdout)
    traits = {trait['id']: trait for trait in report['files'][0]['traits']}
    if name == 'home-path-control.js':
        source = path.read_text()
        evidence = {
            source[start:start + length].lstrip("'\" \n")
            for start, length in traits[home_trait]['spans']
        }
        assert evidence == {
            '/home/alice/project/',
            '/home/runtime/project/',
            '/home/webserver/project/',
        }, evidence
        assert not exploit_traits.intersection(traits), traits
    else:
        assert home_trait not in traits, name
        assert exploit_traits.issubset(traits), name
        assert all(traits[trait]['crit'] == 5 for trait in exploit_traits), name
    print(f'PASS {name}')
