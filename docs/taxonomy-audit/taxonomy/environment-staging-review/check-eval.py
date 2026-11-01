"""Check that an environment-variable name cannot suppress evaluation evidence."""
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
RULES = (
    'micro-behaviors/process/interpreter/eval/direct::powershell-eval-environment-variable',
    'metadata/file/profile/operation-reference::powershell-invoke-expression-environment-text',
)
target = ROOT / 'testdata/notable/generated/taxonomy/environment-eval/vscode-named-variable.ps1'
result = subprocess.run(
    [str(ROOT.parent / 'cleave/target/release/cleave'), '--traits-dir', str(ROOT),
     'test-rules', '--rules', ','.join(RULES), str(target), '--json'],
    cwd=ROOT, text=True, capture_output=True, check=True,
)
for rule in RULES:
    assert '\nMATCHED ' + rule in '\n' + result.stdout, (rule, result.stdout)
print('Both evaluation traits match the VS Code-named environment variable')
