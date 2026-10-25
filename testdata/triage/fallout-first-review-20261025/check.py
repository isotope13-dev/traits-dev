"""Check saved scans, relocation preservation, and behavior-specific controls."""
import json
from pathlib import Path
import sys

scratch = Path(sys.argv[1])
mapping = json.loads((scratch / 'mapping.json').read_text())

def reports(path):
    text = path.read_text()
    decoder = json.JSONDecoder()
    while text.strip():
        report, end = decoder.raw_decode(text.lstrip())
        text = text.lstrip()[end:]
        yield report

def files(path):
    result = {}
    for report in reports(path):
        for file in report.get('raw', report).get('files', []):
            result[file['path']] = file
    return result

def ids(file):
    return {trait['id'] for trait in file.get('traits', [])}

for name in ['1', '2', '3', 'positive', 'arcade-dep']:
    ext = '.jsonl' if name.isdigit() else '.json'
    before = files(scratch / (name + '-before' + ext))
    after = files(scratch / (name + '-after' + ext))
    assert before and before.keys() == after.keys(), name
    for path, file in before.items():
        expected = {mapping.get(trait, trait) for trait in ids(file)}
        assert expected <= ids(after[path]), (name, path, expected - ids(after[path]))

network = 'objectives/exfiltration/stealer/system-info/network::managed-infection-network-report-upload'
services = 'objectives/exfiltration/stealer/system-info/software::managed-infection-service-report-upload'
controls = {Path(path).name: file for path, file in files(scratch / 'control-after.json').items() if '!!' not in path}
assert {network, services} <= ids(controls['carve-2ca606.exe'])
assert network not in ids(controls['no-netstat.exe'])
assert services in ids(controls['no-netstat.exe'])
assert services not in ids(controls['no-service.exe'])
assert network in ids(controls['no-service.exe'])
for name in ['no-transport.exe', 'no-infection.exe']:
    assert not {network, services} & ids(controls[name]), name
assert len([t for t in controls['NameConstants.class']['traits'] if 'name-constant' in t['id']]) == 3
assert not [t for t in controls['NameConstants.class']['traits'] if t['crit'] >= 4]

api = {Path(path).name: file for path, file in files(scratch / 'api-controls-after.json').items()}
assert {'metadata/import/jvm::jvm-getaccesstoken-method-reference', 'metadata/import/jvm::jvm-getprofileid-method-reference'} <= ids(api['ProfileCalls.class'])
assert not any('minecraft' in trait for trait in ids(api['ProfileCalls.class']))
assert 'micro-behaviors/process/interpreter/runtime/jvm::classloader-definition-resource-references' in ids(api['ResourceLoader.class'])
for file in api.values():
    assert not [t for t in file['traits'] if t['crit'] >= 4]
print('PASS: five before/after analyses preserve findings; eight focused controls pass')
