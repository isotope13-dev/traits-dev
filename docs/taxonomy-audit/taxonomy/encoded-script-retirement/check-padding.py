"""Verify that ResponseBody fragment evidence survives padding."""
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
RULE = 'micro-behaviors/fs/write/file/stream::js-adodb-stream-write-responsebody'
source = (HERE / 'cases/adodb-fragments.js').read_text()
with tempfile.TemporaryDirectory() as temp:
    target = Path(temp) / 'bundle.js'
    target.write_text(source + '\n' + '// padding\n' * 19000)
    assert target.stat().st_size > 200000
    result = subprocess.run(
        [str(ROOT.parent / 'cleave/target/release/cleave'), '--traits-dir', str(ROOT),
         'test-rules', '--rules', RULE, str(target), '--json'],
        cwd=ROOT, text=True, capture_output=True, check=True,
    )
    assert '\nMATCHED ' + RULE in '\n' + result.stdout, result.stdout
print('ResponseBody fragment cluster matches in a padded bundle')
