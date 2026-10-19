"""Check saved Cleave reports from the three inert PowerShell controls."""
import json
import sys
from pathlib import Path

pending = Path(sys.argv[1]).read_text().lstrip()
decoder = json.JSONDecoder()
files = {}
while pending:
    report, end = decoder.raw_decode(pending)
    pending = pending[end:].lstrip()
    files.update({Path(f['path']).name: f for f in report['files']})

prefix = 'micro-behaviors/data/encoding/xor::'
for name in ['indexed-input-xor.ps1', 'scalar-flags.ps1', 'reflection-pe-data.ps1']:
    traits = files[name]['traits']
    assert all(t['crit'] < 4 for t in traits), name
    observed = {t['id'] for t in traits}
    if name == 'indexed-input-xor.ps1':
        assert prefix + 'powershell-indexed-xor-assignment' in observed
        assert prefix + 'powershell-indexed-xor-variable' in observed
        assert prefix + 'powershell-xor-modulo-access-references' in observed
    else:
        assert not any(t.startswith(prefix) for t in observed), name
    if name == 'reflection-pe-data.ps1':
        assert {
            'micro-behaviors/process/interpreter/reflection/runtime::powershell-assembly-method-invoke',
            'micro-behaviors/fs/path/system::dotnet-framework-runtime-exe-path',
            'micro-behaviors/data/embedded/payload/array::decimal-mz-dos-header-array',
        } <= observed
print('PASS: three controls; reflection/PE co-occurrence does not imply hollowing')
