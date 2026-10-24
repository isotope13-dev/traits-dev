"""Regression controls for Lua masks, metadata moves and retained attack roles."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
ARITH = 'micro-behaviors/data/arithmetic::'
LINE = 'metadata/file/line::source-line-over-1mb'
DLL = 'metadata/lang/runtime::lua-runtime-dll-name'
HEX = 'metadata/lang/source/syntax/call/arguments::hex-number-and-falsy-arguments'
PAD = 'metadata/lang/natural/phrasing::padding-alignment-wording'
OLD_LINE = 'objectives/anti-static/obfuscation/code-metrics/line-length::'

cases = {
    'lua-mask.lua': ({ARITH + 'lua-low-bit-mask-expression'}, {ARITH + 'lsb-bit-mask-source'}),
    'lua-band.lua': ({ARITH + 'lua-low-bit-mask-expression'}, set()),
    'lua-mask-string.lua': (set(), {ARITH + 'lua-low-bit-mask-expression', ARITH + 'lsb-bit-mask-source'}),
    'lua-other-mask.lua': (set(), {ARITH + 'lua-low-bit-mask-expression', ARITH + 'lsb-bit-mask-source'}),
    'lua-runtime.lua': ({DLL}, {'micro-behaviors/process/interpreter/lua::lua-runtime-dll-name'}),
    'lua-runtime-near.lua': (set(), {DLL}),
    'hex-arguments.js': ({HEX}, set()),
    'hex-arguments-near.js': (set(), {HEX}),
    'padding.rb': ({PAD}, set()),
    'padding-near.rb': (set(), {PAD}),
    'overflow-padding.rb': ({PAD, 'objectives/privilege-escalation/exploit/shell::overflow-padding-retaddr-align'}, set()),
}

with tempfile.TemporaryDirectory(prefix='.line-controls-', dir=HERE) as tmp:
    temp = Path(tmp)
    # A huge ordinary literal has a long line; length alone proves no evasion.
    (temp / 'large.lua').write_text('local text = "' + 'a' * 1_000_001 + '"\n')
    (temp / 'short.lua').write_text('local text = "short"\n')
    paths = [HERE / name for name in cases] + [temp / 'large.lua', temp / 'short.lua']
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                             '--format', 'json', *map(str, paths)],
                            capture_output=True, text=True, check=True)
    decoder = json.JSONDecoder()
    reports = []
    rest = result.stdout
    while rest.strip():
        report, end = decoder.raw_decode(rest.lstrip())
        reports.extend(report['files'])
        rest = rest.lstrip()[end:]
    by_path = {file['path']: file for file in reports}
    for name, (required, forbidden) in cases.items():
        file = by_path[str(HERE / name)]
        ids = {trait['id'] for trait in file.get('traits', [])}
        assert required <= ids, (name, required - ids)
        assert not forbidden & ids, (name, forbidden & ids)
    large = by_path[str(temp / 'large.lua')]
    assert LINE in {t['id'] for t in large['traits']}
    assert not any(t['id'].startswith(OLD_LINE) for t in large['traits'])
    assert not any(t['crit'] >= 4 for t in large['traits'])
    assert LINE not in {t['id'] for t in by_path[str(temp / 'short.lua')]['traits']}
print(f'{len(cases) + 2} focused controls passed')
