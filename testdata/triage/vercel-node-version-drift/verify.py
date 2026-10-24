"""Verify saved release scans and controls; pass the research scratch directory."""
import itertools
import json
from pathlib import Path
import re
import sys


OLD = 'objectives/anti-static/obfuscation/string/array::js-array-accumulator-concat'
NEW = 'metadata/lang/source/syntax/assignment::js-repeated-indexed-concat-assignment'
GROUP = 'objectives/anti-static/obfuscation/string/array::js-array-rebuild-loop'
CONCEALMENT = 'objectives/anti-static/obfuscation/string/array::js-cc-array-reconstruction'


def reports(path):
    rest = path.read_text()
    decoder = json.JSONDecoder()
    while rest.strip():
        rest = rest.lstrip()
        report, end = decoder.raw_decode(rest)
        yield report.get('raw', report)
        rest = rest[end:]


def findings(path):
    return {
        file['path']: {t['id']: t['crit'] for t in file.get('traits', [])}
        for report in reports(path) for file in report['files']
    }


def main():
    scratch = Path(sys.argv[1]).resolve()
    before = findings(scratch / 'before.json')
    after = findings(scratch / 'after.json')
    assert before.keys() == after.keys(), 'Archive members changed'
    changes = 0
    for path, traits in before.items():
        expected = dict(traits)
        if OLD in expected:
            assert expected.pop(OLD) == 4
            expected[NEW] = 3
            changes += 1
        assert after[path] == expected, (path, 'Unexpected finding change')
    assert changes == 2, 'Expected one member plus archive rollup'
    assert findings(scratch / 'positive-before.json') == findings(
        scratch / 'positive-after.json'), 'Recovered malware lost coverage'

    controls_before = findings(scratch / 'controls-before.json')
    controls_after = findings(scratch / 'controls-after.json')
    for path, traits in controls_before.items():
        expected = dict(traits)
        if OLD in expected:
            expected.pop(OLD)
            expected[NEW] = 3
        expected.pop(GROUP, None)
        assert controls_after[path] == expected, (path, 'Control coverage changed')
        name = Path(path).name
        assert (CONCEALMENT in controls_after[path]) == (
            name == 'concealed-concat.js'), (name, 'Concealment boundary failed')
        assert (NEW in controls_after[path]) == (name in {
            'ordinary.js', 'concealed-concat.js', 'concat-without-hex.js'
        }), (name, 'Count/assignment boundary failed')

    # Expanding the sole grouping consumer is Boolean-equivalent. The
    # independent length-guard alternative and all suppressors stay intact.
    for bits in itertools.product([False, True], repeat=7):
        hex_map, comments, concat, plus_eval, do_loop, guarded, buried = bits
        old = hex_map and comments and (
            any([concat, plus_eval, do_loop]) or guarded or buried)
        new = hex_map and comments and any([
            concat, plus_eval, do_loop, guarded, buried])
        assert old == new

    modules = []
    for release in ['old', 'current']:
        source = (scratch / release / 'package/dist/index.js').read_text()
        parts = re.split(r'^/\*\*\*/ (\d+):\n', source, flags=re.M)
        modules.append({parts[i]: parts[i + 1] for i in range(1, len(parts), 2)})
    old, current = modules
    normalize = lambda body: re.sub(
        r'__webpack_require__\(\d+\)', '__webpack_require__(ID)', body).strip()
    old_bodies = {normalize(body) for body in old.values()}
    changed = [key for key, body in current.items()
               if normalize(body) not in old_bodies]
    assert len(old) == 666 and len(current) == 1693
    assert changed == ['2855'], changed
    patched_entry = old['2855'].replace(
        'runNpmInstall(entrypointFsDirname, [], spawnOpts, meta);',
        'runNpmInstall(entrypointFsDirname, [], spawnOpts, meta, nodeVersion);'
    ).replace('nodeVersion, spawnOpts, }', 'nodeVersion, spawnOpts }')
    assert patched_entry == current['2855'], 'Unexplained entrypoint change'
    print('PASS: release diff, archive coverage, malware controls, and boundaries')


if __name__ == '__main__':
    main()
