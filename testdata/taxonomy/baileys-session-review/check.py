"""Focused trait boundaries for the Baileys socket second review."""
import json
from pathlib import Path
import subprocess
import sys

base=Path(__file__).parent
cases=json.loads((base/'cases.json').read_text())['fixtures']
result=subprocess.run([sys.argv[1] if len(sys.argv)>1 else 'cleave','--no-update-check','--format','jsonl',*[str(base/c['path']) for c in cases]],text=True,capture_output=True)
if result.returncode:
    print(result.stderr, file=sys.stderr)
    result.check_returncode()
reports={}
for line in result.stdout.splitlines():
    report=json.loads(line)
    if 'files' not in report:
        raise AssertionError('unexpected report schema: '+str(report.keys()))
    for file in report['files']:
        reports[Path(file['path']).name]={t['id'] for t in file.get('traits',[])}
for case in cases:
    ids=reports[case['path']]
    missing=set(case.get('matched',[]))-ids
    unexpected=set(case.get('not_matched',[]))&ids
    assert not missing and not unexpected,(case['path'],missing,unexpected)
    direct=case.get('direct_matched',[])+case.get('direct_not_matched',[])
    if direct:
        debug=subprocess.run([sys.argv[1] if len(sys.argv)>1 else 'cleave','test-rules',str(base/case['path']),'--rules',','.join(direct)],text=True,capture_output=True,check=True)
        matched={line.split()[1] for line in debug.stdout.splitlines() if line.startswith('MATCHED ')}
        assert set(case.get('direct_matched',[])) <= matched, (case['path'],debug.stdout)
        assert not set(case.get('direct_not_matched',[])) & matched, (case['path'],debug.stdout)
    print('PASS',case['path'])
print(f'{len(cases)} focused cases passed')
