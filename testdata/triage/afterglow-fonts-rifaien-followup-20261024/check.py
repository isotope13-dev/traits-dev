"""Scan controls without executing them. Requires a clean baseline rule tree."""
import argparse, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DECODER = 'micro-behaviors/data/decode/custom::js-variable-length-alphabet-integer-decoder'
GEN = 'micro-behaviors/metaprogramming/generation::js-function-constructor'
INDIRECT = 'micro-behaviors/process/interpreter/eval/indirect::js-indirect-eval'
RUN = 'micro-behaviors/process/interpreter/eval/constructed::indirect-function-result-invocation'
JSON_OLD = 'objectives/anti-static/obfuscation/eval/loader::json-fetch-indirect-eval-xor-storage'
JSON_NEW = 'objectives/anti-static/obfuscation/eval/loader::json-fetch-runtime-eval-xor-storage'
MUTANT = 'objectives/anti-static/obfuscation/payload/polymorphic/generator::self-mutating-image-submission-loop'
SLOT = 'objectives/anti-static/obfuscation/payload/polymorphic/generator::native-mutated-self-image-loop'
OLD_FORMAT = 'micro-behaviors/fs/write/file/target::generated-numbered-exe-format'
FORMAT = 'micro-behaviors/data/format/string::numbered-executable-printf-template'


def scan(traits, paths, dest):
    result = subprocess.run(['cleave', '--traits-dir', str(traits), 'analyze',
                             '--format', 'jsonl', *map(str, paths)],
                            text=True, capture_output=True, check=True)
    dest.write_text(result.stdout)
    files = {}
    for line in result.stdout.split('\n'):
        if not line.strip():
            continue
        for file in json.loads(line).get('files', []):
            files[file['path']] = {t['id']: t['crit'] for t in file.get('traits', [])}
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--baseline', type=Path, required=True)
    args = ap.parse_args()
    work = args.work
    controls = work / 'controls'
    controls.mkdir(exist_ok=True)
    decoder = ('var decode=function(data,alphabet,base){'
               'for(var size=alphabet.length,radix=size-base,out=[],pos=0;pos<data.length;)'
               'for(var value=0,weight=1,digit;;){digit=alphabet.indexOf(data[pos++]);'
               'if(value+=weight*(digit%base),digit<base){out.push(value|0);break}'
               'value+=base*weight,weight*=radix}return out}')
    prefix = ('const words=[1,2,3];for(let i=0;i<words.length;i++)words[i]^=37;'
              'localStorage.setItem("preferred",origin);localStorage.getItem("preferred");'
              'fetch(origin).then(r=>r.json()).then(record=>{')
    cases = {
        'decoder.js': decoder,
        'decoder-spaced.js': decoder.replace(';', ';\n').replace(',', ', '),
        'wrong-digit.js': decoder.replace('digit%base', 'unrelated%base'),
        'wrong-base.js': decoder.replace('digit<base', 'digit<other'),
        'wrong-emit.js': decoder.replace('out.push', 'out.pop'),
        'quoted-decoder.js': 'function example(){return ' + json.dumps(decoder) + '}',
        'comment-decoder.js': 'function example(){/*' + decoder + '*/}',
        'construct-only.js': '(0,Function)(source);',
        'construct-run.js': '(0,Function)(source)();',
        'eval.js': '(0,eval)(source);',
        'quoted-eval.js': 'console.log("(0,eval)(source)");',
        'quoted-run.js': 'console.log("(0,Function)(source)()");',
        'nested-run.js': '(0,Function)(decode(source))();',
        'ordinary.js': 'Function(source);',
        'other-callee.js': '(0,Function,other)(source);',
        'function-argument.js': 'other(0,Function)(source);',
        'json-construct-only.js': prefix + '(0,Function)(record[0]);});',
        'json-run.js': prefix + '(0,Function)(record[0])();});',
        'json-eval.js': prefix + '(0,eval)(record[0]);});',
    }
    paths = []
    for name, body in cases.items():
        p = controls / name
        p.write_text(body)
        paths.append(p)
    # Use a real, outside-batch positive rather than a fabricated PE profile.
    native = work / 'outside/hopper/2026-10-17_1f94875f931645ee227d1583e762d247_elex_rhadamanthys_smoke-loader_stealc_stop'
    import pefile
    pe = pefile.PE(str(native))
    data = native.read_bytes()
    paths.append(native)
    for name, rva, old, new in [
        ('native-no-random.exe', 0x1551, bytes.fromhex('e84ac50100'), bytes.fromhex('31c0909090')),
        ('native-other-buffer.exe', 0x158d, bytes.fromhex('20304200'), bytes.fromhex('24304200')),
    ]:
        offset = pe.get_offset_from_rva(rva)
        assert data[offset:offset+len(old)] == old, (name, data[offset:offset+len(old)].hex())
        p = controls / name
        p.write_bytes(data[:offset] + new + data[offset+len(old):])
        paths.append(p)
    outside = [ROOT/'testdata/hostile/ghappier-buried-fetch-eval.js',
               ROOT/'testdata/triage-compromised-page-regression/atob-eval-loader.html',
               ROOT/'testdata/triage/afterglow-rifaien-clr-20261024/school-cloak.html']
    assert all(p.exists() for p in outside)
    paths += outside
    before = scan(args.baseline, paths, work/'controls.before.jsonl')
    after = scan(ROOT, paths, work/'controls.after.jsonl')
    for name in cases:
        ts = after[str(controls/name)]
        assert (DECODER in ts) == (name in ('decoder.js', 'decoder-spaced.js')), name
    for name in ('construct-only.js', 'json-construct-only.js'):
        ts = after[str(controls/name)]
        assert GEN in ts and INDIRECT not in ts and RUN not in ts and JSON_NEW not in ts, name
    for name in ('construct-run.js', 'json-run.js', 'nested-run.js'):
        ts = after[str(controls/name)]
        assert GEN in ts and RUN in ts and INDIRECT not in ts, name
    assert JSON_NEW in after[str(controls/'json-run.js')]
    assert JSON_NEW in after[str(controls/'json-eval.js')]
    for name in ('eval.js', 'json-eval.js'):
        assert INDIRECT in after[str(controls/name)], name
    for name in ('other-callee.js', 'function-argument.js', 'quoted-decoder.js', 'comment-decoder.js', 'quoted-eval.js', 'quoted-run.js'):
        assert not ({GEN, INDIRECT, RUN} & after[str(controls/name)].keys()), name
    assert before[str(native)][MUTANT] == 5
    assert after[str(native)][MUTANT] == 4
    assert after[str(native)][SLOT] == 4
    assert before[str(native)][OLD_FORMAT] == after[str(native)][FORMAT] == 3
    for name in ('native-no-random.exe', 'native-other-buffer.exe'):
        assert MUTANT not in after[str(controls/name)], name
    for p in outside:
        b = {k:v for k,v in before[str(p)].items() if v>=4}
        a = {k:v for k,v in after[str(p)].items() if v>=4}
        assert b == a and any(v==5 for v in a.values()), (p,b,a)
    print(f'Passed {len(paths)} controls; outside attack findings retained')


if __name__ == '__main__':
    main()
