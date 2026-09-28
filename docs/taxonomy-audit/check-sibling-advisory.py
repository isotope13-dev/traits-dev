"""Exercise spelling advisory, inclusive cap, and leaf-only gates against a CLI.

Usage: python3 check-sibling-advisory.py /absolute/path/to/cleave
The temporary corpus is deliberately empty: this checks validator exit status,
not detection. The production-only file-type allowlist rejects this tiny tree;
assertions distinguish that expected failure from the policies under test.
No validator is disabled. The full repository gate verifies detection separately.
"""
from pathlib import Path
import subprocess
import sys
import tempfile

binary = str(Path(sys.argv[1]).resolve())
with tempfile.TemporaryDirectory(prefix='taxonomy-sibling-advisory-') as tmp:
    root = Path(tmp)
    for name in ('hostile', 'benign'):
        (root / 'testdata' / name).mkdir(parents=True)
    (root / 'testdata/expectations.toml').write_text(
        'hostile = []\nbenign = []\nwalked_hostile = []\n'
        '[does_nothing]\ndefault_cap = 10\n'
    )
    account = root / 'metadata/file/string/account'
    accounting = root / 'metadata/file/string/accounting'
    account.mkdir(parents=True)
    accounting.mkdir()

    def rules(count, stem):
        result = 'defaults:\n  for: [elf]\n  platforms: [unix]\n  crit: baseline\n  conf: 0.8\ntraits:\n'
        for n in range(count):
            result += (f'- id: {stem}-{n}\n  desc: Distinct {stem} token\n'
                       f'  if:\n    type: text\n    exact: taxonomy_{stem}_{n:03d}\n')
        return result

    def run():
        return subprocess.run([binary, '--traits-dir', str(root), 'validate'],
                              capture_output=True, text=True)

    (account / 'traits.yaml').write_text(rules(1, 'identity'))
    (accounting / 'traits.yaml').write_text(rules(1, 'record'))
    result = run()
    assert 'validation failed: 1 issue(s)' in result.stderr, result.stdout + result.stderr
    assert 'file-type allowlist entries match no trait' in result.stderr, result.stderr
    assert 'policy/sibling-restate' not in result.stderr, result.stderr
    assert 'share a name stem' in result.stderr, result.stderr
    print('Spelling advisory emitted; no failure beyond the production allowlist check.')

    (account / 'traits.yaml').write_text(rules(100, 'identity'))
    result = run()
    assert 'validation failed: 1 issue(s)' in result.stderr, result.stdout + result.stderr
    assert 'oversized-dir' not in result.stderr, result.stderr
    print('Inclusive 100-rule cap adds no failure.')

    (account / 'traits.yaml').write_text(rules(101, 'identity'))
    result = run()
    assert result.returncode != 0 and 'oversized-dir' in result.stderr, result.stdout + result.stderr
    print('101 rules still fail strict validation.')

    (account / 'traits.yaml').write_text(rules(1, 'identity'))
    (account / 'profile').mkdir()
    (account / 'profile/traits.yaml').write_text(rules(1, 'profile'))
    result = run()
    assert result.returncode != 0 and ('leaf-yaml' in result.stderr), result.stdout + result.stderr
    print('Mixed parent/child rules still fail strict validation.')
