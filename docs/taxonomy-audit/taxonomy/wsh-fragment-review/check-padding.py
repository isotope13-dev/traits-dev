"""Check that padding does not suppress the WSH token profile."""
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
RULES = (
    'metadata/lang/source/literal/fragment/single::quoted-powersh-fragment',
    'metadata/file/profile/encoding/composition::tokenized-wsh-powershell-ps1-profile',
)
source = (HERE / 'cases/tokenized.js').read_text()
with tempfile.TemporaryDirectory() as temp:
    target = Path(temp) / 'bundle.js'
    target.write_text(source + '\n' + '// harmless padding for bundle context\n' * 2000)
    assert target.stat().st_size > 50000
    result = subprocess.run(
        [str(ROOT.parent / 'cleave/target/release/cleave'), '--traits-dir', str(ROOT),
         'test-rules', '--rules', ','.join(RULES), str(target), '--json'],
        cwd=ROOT, text=True, capture_output=True, check=True,
    )
    for rule in RULES:
        assert '\nMATCHED ' + rule in '\n' + result.stdout, (rule, result.stdout)
print('Both WSH fragment and composite match in a padded bundle')
