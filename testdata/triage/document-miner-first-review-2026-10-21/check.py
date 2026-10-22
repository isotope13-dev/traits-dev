#!/usr/bin/env python3
"""Read-only matcher controls; no document, PE or attachment is executed."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
instruction = 'micro-behaviors/ui/help::document-double-click-instruction'
text_instruction = instruction + '-text'
pdf_instruction = 'micro-behaviors/ui/help::pdf-double-click-instruction-bytes'
lure = 'objectives/execution/lure/document::document-double-click-execution-lure'
pool = 'micro-behaviors/data/config/syntax::stratum-pool-array-references'
xmrig = 'well-known/app/finance/xmrig::pe-stratum-pool-config-references'
retired = {
    'objectives/impact/cryptojacking/miner/smart::stratum-method-and-xmrig-pools-binary',
    'objectives/impact/cryptojacking/miner/smart::xmrig-pe-embedded-stratum-pool-config',
}
cases = {
    'editor-tutorial.html': ({text_instruction: 3}, {lure}),
    'executable-instructions.html': ({text_instruction: 3}, {lure}),
    'embedded-executable.pdf': ({pdf_instruction: 3, lure: 4}, set()),
    'embedded-text.pdf': ({pdf_instruction: 3}, {lure}),
    'no-click.pdf': ({}, {instruction, text_instruction, pdf_instruction, lure}),
    'pool-stratum.exe': ({pool: 3}, {xmrig}),
    'xmrig-pool-stratum.exe': ({pool: 3, xmrig: 3}, set()),
    'pool-only.exe': ({}, {pool, xmrig}),
    'stratum-only.exe': ({}, {pool, xmrig}),
}

# Exercise content without the intentional test-directory suppressor. Keeping
# fixtures under testdata must not accidentally make all lure negatives pass.
with tempfile.TemporaryDirectory(prefix='document-miner-',
                                 dir=os.environ.get('REVIEW_SCRATCH')) as tmp:
    for filename in cases:
        shutil.copyfile(HERE / filename, Path(tmp) / filename)
    result = subprocess.run([
        os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
        '--format', 'json', tmp,
    ], text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    # Directory scans may emit concatenated JSON reports without line breaks.
    decoder = json.JSONDecoder()
    rest = result.stdout.lstrip()
    reports = []
    while rest:
        report, end = decoder.raw_decode(rest)
        reports.append(report)
        rest = rest[end:].lstrip()
    observed = {}
    for report in reports:
        for file in report.get('files', []):
            observed[Path(file['path']).name] = {
                trait['id']: trait['crit'] for trait in file.get('traits', [])
            }
    for filename, (required, absent) in cases.items():
        traits = observed[filename]
        assert all(traits.get(key) == value for key, value in required.items()), (
            filename, 'missing or wrong severity', required, traits)
        assert not (absent | retired) & traits.keys(), (filename, traits)
        assert 'well-known/malware/backdoor/crystalx::crystalx-rat' not in traits
    print(f'{len(cases)} document/miner controls passed')
