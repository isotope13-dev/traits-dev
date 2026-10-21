"""Generate benign controls outside repository test-path exclusions."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
hex_id = 'micro-behaviors/data/decode/hex::lua-aliased-radix16-conversion'
table_id = 'metadata/lang/source/literal::lua-table-padded-radix64-strings'
argument_id = 'micro-behaviors/process/argument/file::lua-interpreter-text-file-argument'
retired = {
    'objectives/anti-static/obfuscation/code-metrics/structure::lua-long-base64-table',
    'objectives/evasion/masquerade/file/extension-mismatch::lua-interpreter-runs-text-named-script',
    'objectives/evasion/masquerade/file/extension-mismatch::batch-starts-text-named-lua-script',
    'objectives/command-and-control/infrastructure/blockchain/polygon::lua-polygon-contract-memory-loader',
    'objectives/supply-chain/hidden-payload/exec/archive::readme-image-zip-with-defender-bypass-lua',
    'objectives/supply-chain/impersonation/readme-clone::release-page-lure-launches-packed-data',
}
hex_source = '''do
radix = (16)
other = methods[name]
selector = "tonumber"
spare = "string"
convert = environment[selector]
result = convert(input, radix)
end
'''
cases = {
    'direct.lua': ('do convert=environment["tonumber"]; result=convert(input,(16)) end', {hex_id}, set()),
    'direct-decimal.lua': ('do convert=environment["tonumber"]; result=convert(input,(10)) end', set(), {hex_id}),
    'direct-overwritten.lua': ('do convert=environment["tonumber"]; convert=other; result=convert(input,(16)) end', set(), {hex_id}),
    'docs.md': ('# Tool\n![Download](https://raw.githubusercontent.com/acme/tool/main/tool.zip)\n[Releases Page](https://raw.githubusercontent.com/acme/tool/main/tool.zip)\n', {'objectives/execution/lure/document::raw-zip-disguised-as-image-and-page'}, {'objectives/execution/lure/document::zip-page-image-lure-with-defender-bypass'}),
    'hex.lua': (hex_source, {hex_id}, set()),
    'decimal.lua': (hex_source.replace('(16)', '(10)'), set(), {hex_id}),
    'overwritten-radix.lua': (hex_source.replace('other =', 'radix ='), set(), {hex_id}),
    'overwritten-selector.lua': (hex_source.replace('spare =', 'selector ='), set(), {hex_id}),
    'wrong-member.lua': (hex_source.replace('environment[selector]', 'environment[another]'), set(), {hex_id}),
    'wrong-function.lua': (hex_source.replace('result = convert(', 'result = unrelated('), set(), {hex_id}),
    'wrong-radix.lua': (hex_source.replace('input, radix', 'input, unknown'), set(), {hex_id}),
    'padded.lua': ('local payload={"QUJDREVGR0hJSktMTU4=","T1BRUlNUVVZXWFlaMDE="}', {table_id}, set()),
    'prose.lua': ('local payload={"this is ordinary prose=","this is also ordinary prose="}', set(), {table_id}),
    'short.lua': ('local payload={"QUJDRA==","RUZHSA=="}', set(), {table_id}),
    'launch.cmd': ('start luajit.exe fixture.txt\n', {argument_id}, set()),
    'script-extension.cmd': ('start tool.lua fixture.txt\n', set(), {argument_id}),
}
with tempfile.TemporaryDirectory(prefix='yahoo-controls-', dir=args.scratch) as directory:
    directory = Path(directory)
    for name, (source, _, _) in cases.items():
        (directory / name).write_text(source)
    result = subprocess.run([args.cleave, '--traits-dir', str(Path.cwd()), '--format', 'json', '--all-files', str(directory)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    reports, output = [], result.stdout
    decoder = json.JSONDecoder()
    while output.strip():
        report, length = decoder.raw_decode(output.lstrip())
        reports.append(report)
        output = output.lstrip()[length:]
    files = {Path(f['path']).name: f for report in reports for f in report['files'] if f.get('pid') is None}
    for name, (_, required, forbidden) in cases.items():
        traits = files[name].get('traits', [])
        ids = {t['id'] for t in traits}
        assert required <= ids and not (forbidden | retired) & ids, (name, required - ids, forbidden & ids)
        assert all(t['crit'] < (5 if name == 'docs.md' else 4) for t in traits), (name, [(t['id'], t['crit']) for t in traits if t['crit'] >= 4])
        print('PASS', name)
print(f'{len(cases)} controls passed')
