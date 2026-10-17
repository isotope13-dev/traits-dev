import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[3]
here = Path(__file__).resolve().parent
engine = os.environ.get('CLEAVE', 'cleave')
neutral_eval = 'micro-behaviors/process/interpreter/eval/indirect::js-global-eval-near-response-text'
nav = 'micro-behaviors/communications/http/url/navigation::xhr-response-href-assignment'
decoder = 'objectives/anti-static/obfuscation/string/reconstruct::js-string-deobfuscation'
constants = 'micro-behaviors/crypto/hash/digest::javascript-sha256-round-constants'
hash_call = 'micro-behaviors/crypto/hash/digest::node-createhash-sha256-call'
click = 'micro-behaviors/ui/window/click::browser-computed-click-listener'
shape = 'metadata/file/profile/text-shape::near-zero-whitespace-source'
cases = [
    (here/'compact-source.js', {shape: 3}, []),
    (here/'spaced-source.js', {}, [shape]),
    (here/'events.js', {}, [click]),
    (here/'click.js', {click: 3}, []),
    (root/'testdata/taxonomy/map-iterator-mutation-window/tight-trigger-loop.js', {}, ['objectives/execution/exploit/browser-uaf::map-iterator-mutation-trigger']),
    (root/'testdata/taxonomy/map-iterator-mutation-window/framework-cache-class.js', {}, ['objectives/execution/exploit/browser-uaf::map-iterator-mutation-trigger']),
    (here/'digest-format.js', {constants: 3}, [decoder]),
    (here/'indexed-decoder.js', {decoder: 4}, []),
    (here/'other-href.js', {}, [nav]),
    (here/'hash-call.js', {hash_call: 3}, []),
    (here/'separate-text-eval.js', {neutral_eval: 3}, []),
    (root/'testdata/taxonomy/js-eval-fetched-response/fetch-eval-loader.js', {neutral_eval: 3}, []),
    (root/'testdata/taxonomy/js-eval-fetched-response/separate-eval-fetch.js', {}, [neutral_eval]),
    (root/'testdata/taxonomy/xhr-response-navigation/plain-redirect.js', {nav: 3}, []),
    (root/'testdata/taxonomy/xhr-response-navigation/static-redirect.js', {}, [nav]),
]
with tempfile.TemporaryDirectory(prefix='capability-controls-') as tmp:
    for index, (source, expected, absent) in enumerate(cases):
        target = Path(tmp)/('control%d.js' % index)
        shutil.copyfile(source, target)
        result = subprocess.run([engine, '--traits-dir', str(root), '--format', 'json', str(target)], capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        traits = {t['id']: t['crit'] for f in report['files'] for t in f.get('traits', [])}
        for tid, severity in expected.items():
            assert traits.get(tid) == severity, (source.name, tid, traits.get(tid))
        for tid in absent:
            assert tid not in traits, (source.name, tid)
        assert not any(v == 5 for v in traits.values()), (source.name, 'unexpected hostile')
        print('PASS', source.name)
print('%d controls passed' % len(cases))
